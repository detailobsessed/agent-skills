"""Check every skill in this repo against the best-practices rules skill-validator lacks.

skill-validator (the `skill-validator` prek hooks) checks the Agent Skills spec: frontmatter,
names, lengths, token budgets, links and directories. This script keeps only the four rules from
Anthropic's skill authoring best practices that it does not check yet:

- the description is written in the third person
- the description says when to use the skill
- a reference file over 100 lines opens with a table of contents
- SKILL.md has no time-sensitive wording that will go stale

Delete this script, its prek hook and its CI entry once agent-ecosystem/skill-validator#108
ships these checks.

Sources:
    https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_SKILLS_DIR = REPO_ROOT / ".agents" / "skills"  # repo-maintenance skills, marked internal
BEST_PRACTICES = "platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices"

REFERENCE_TOC_THRESHOLD_LINES = 100
TOC_HEADINGS = ("## contents", "## table of contents")
FIRST_OR_SECOND_PERSON_RE = re.compile(
    r"^\s*(I\b|I'm\b|I can\b|My\b|We\b|Our\b|You\b|Your\b)", re.IGNORECASE
)
TRIGGER_PHRASE_RE = re.compile(
    r"\b(use\s+when|use\s+this\s+(skill\s+)?when|invoke\s+when|when\s+the\s+user)\b",
    re.IGNORECASE,
)
TIME_SENSITIVE_RE = re.compile(
    r"\b(before|after|by|until|since|as of)\s+"
    r"(January|February|March|April|May|June|July|August|"
    r"September|October|November|December|Q[1-4])\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    location: str


def read_description(skill_dir: Path) -> str:
    """Parse the frontmatter with the spec's reference parser, `agentskills read-properties`."""
    result = subprocess.run(
        ["uv", "run", "agentskills", "read-properties", str(skill_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""  # skill-validator reports the broken frontmatter
    description = json.loads(result.stdout).get("description")
    return description if isinstance(description, str) else ""


def check_description(skill_dir: Path) -> list[Finding]:
    description = read_description(skill_dir)
    location = f"{skill_dir.name}/SKILL.md"
    findings = []
    if FIRST_OR_SECOND_PERSON_RE.match(description):
        findings.append(
            Finding(
                "description-not-third-person",
                "the description opens in the first or second person; write it in the third.",
                location,
            )
        )
    if not TRIGGER_PHRASE_RE.search(description):
        findings.append(
            Finding(
                "description-no-trigger-phrase",
                "the description needs a 'Use when' trigger: agents pick skills by it.",
                location,
            )
        )
    return findings


def lacks_toc(reference: Path) -> bool:
    lines = reference.read_text(encoding="utf-8").splitlines()
    head = "\n".join(lines[:30]).lower()
    return len(lines) > REFERENCE_TOC_THRESHOLD_LINES and not any(h in head for h in TOC_HEADINGS)


def check_reference_tocs(skill_dir: Path) -> list[Finding]:
    return [
        Finding(
            "reference-missing-toc",
            f"{ref.name} is over {REFERENCE_TOC_THRESHOLD_LINES} lines and has no '## Contents' "
            "near the top, so a partial read misses what is past it.",
            f"{skill_dir.name}/references/{ref.name}",
        )
        for ref in sorted((skill_dir / "references").glob("*.md"))
        if lacks_toc(ref)
    ]


def check_time_sensitive(skill_dir: Path) -> list[Finding]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    return [
        Finding(
            "time-sensitive-phrase",
            f"'{match.group(0)}' goes stale; describe the current state instead.",
            f"{skill_dir.name}/SKILL.md:{text.count('\n', 0, match.start()) + 1}",
        )
        for match in TIME_SENSITIVE_RE.finditer(text)
    ]


def is_skill(path: Path) -> bool:
    return path.is_dir() and not path.name.startswith(".") and (path / "SKILL.md").is_file()


def skill_directories() -> list[Path]:
    """Published skills at the repo root, then the project skills in `.agents/skills/`."""
    roots = [REPO_ROOT, PROJECT_SKILLS_DIR] if PROJECT_SKILLS_DIR.is_dir() else [REPO_ROOT]
    skills = [skill for root in roots for skill in sorted(filter(is_skill, root.iterdir()))]
    if not skills:
        raise SystemExit("No skill directories with SKILL.md were found.")
    return skills


def main() -> int:
    findings = [
        finding
        for skill_dir in skill_directories()
        for check in (check_description, check_reference_tocs, check_time_sensitive)
        for finding in check(skill_dir)
    ]
    for f in findings:
        print(f"{f.location}: [{f.code}] {f.message}")
    if findings:
        print(f"FAILED: {len(findings)} finding(s).")
        return 1
    print("All skills passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

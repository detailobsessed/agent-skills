"""Validate every skill in this repo against the Agent Skills spec.

Sources of truth:
    https://agentskills.io/specification
    https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

The baseline (frontmatter regex, reserved-word check, name length) is delegated
to `agentskills validate`. This script layers on the structural and content
checks that the upstream CLI does not perform.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Limits drawn directly from the spec / best-practices docs. The numbers are
# not invented here — adjust the URL and rationale together if they change.
MAX_BODY_LINES = 500  # "Keep your main SKILL.md under 500 lines"
MAX_BODY_WORDS = (
    5000  # "<5000 tokens recommended" (1 token ~= 1 word for English prose)
)
MAX_DESCRIPTION_LEN = 1024  # spec MUST
MAX_NAME_LEN = 64  # spec MUST
MAX_COMPATIBILITY_LEN = 500  # spec MUST when present
REFERENCE_TOC_THRESHOLD_LINES = 100  # best-practices: TOC recommended past this
KNOWN_SUBDIRS = {"references", "scripts", "assets"}  # spec-named optional dirs
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED_NAME_WORDS = {"anthropic", "claude"}  # best-practices: "reserved words"
# A description that opens in first/second person fails the third-person rule.
FIRST_OR_SECOND_PERSON_RE = re.compile(
    r"^\s*(I\b|I'm\b|I can\b|My\b|We\b|Our\b|You\b|Your\b)", re.IGNORECASE
)
# Trigger phrase: discovery hinges on this per best-practices.
TRIGGER_PHRASE_RE = re.compile(
    r"\b(use\s+when|use\s+this\s+(skill\s+)?when|invoke\s+when|when\s+the\s+user)\b",
    re.IGNORECASE,
)
# Time-sensitive phrasing: dates that will go stale without a fallback. Months
# and quarters as anchors; flagged unless explicitly inside an "old patterns"
# / `<details>` block (we don't try to detect that — false positive risk is
# acceptable and the warning prompts a human check).
TIME_SENSITIVE_RE = re.compile(
    r"\b(before|after|by|until|since|as of)\s+"
    r"(January|February|March|April|May|June|July|August|"
    r"September|October|November|December|Q[1-4])\b",
    re.IGNORECASE,
)
# Windows-style backslash paths in markdown link targets or inline code. Skip
# escaped backslashes in regex examples — we only flag look-alike file paths.
WINDOWS_PATH_RE = re.compile(r"[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+\.[A-Za-z0-9]+")
# Markdown link target: [text](target) where target is a relative path.
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s#]+(?:#[^\s)]*)?)\)")


@dataclass(frozen=True)
class Finding:
    severity: str  # "error" or "warning"
    code: str  # short slug, e.g. "body-too-long"
    message: str
    spec_ref: str  # which spec / best-practices section
    location: str = ""  # optional "path:line" or path


def _split_frontmatter(text: str) -> tuple[str, str]:
    """Split a SKILL.md into (frontmatter_yaml, body_markdown).

    Returns ("", text) if no frontmatter delimiters are present — caller can
    treat that as a spec violation.
    """
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + len("\n---\n") :]


def _line_of(text: str, needle_match: re.Match[str]) -> int:
    """1-based line number of a regex match in `text`."""
    return text.count("\n", 0, needle_match.start()) + 1


def _read_properties(skill_dir: Path) -> dict[str, object] | None:
    """Use `agentskills read-properties` to parse frontmatter without adding a
    YAML dependency. Returns None if the CLI itself errors (caller will already
    have a baseline failure from `agentskills validate`)."""
    try:
        result = subprocess.run(
            ["uv", "run", "agentskills", "read-properties", skill_dir.name],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


# --- individual checks --------------------------------------------------------


def check_baseline(skill_dir: Path) -> list[Finding]:
    """Defer name/description regex + reserved words to upstream `agentskills`.
    We only surface its exit status here; the CLI prints its own diagnostics.
    """
    result = subprocess.run(
        ["uv", "run", "agentskills", "validate", skill_dir.name],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    detail = (result.stdout + result.stderr).strip() or "(no detail)"
    return [
        Finding(
            "error",
            "baseline-failed",
            f"`agentskills validate` rejected this skill:\n{detail}",
            "agentskills.io/specification#frontmatter",
        )
    ]


def check_directory_name_matches(
    skill_dir: Path, props: dict[str, object]
) -> list[Finding]:
    """Spec MUST: `name` field must match the parent directory name."""
    name = props.get("name")
    if not isinstance(name, str):
        return []  # baseline already errored
    if name != skill_dir.name:
        return [
            Finding(
                "error",
                "name-dir-mismatch",
                f"frontmatter name={name!r} does not match directory name {skill_dir.name!r}",
                "agentskills.io/specification#name-field",
                location=f"{skill_dir.name}/SKILL.md",
            )
        ]
    return []


def check_body_length(skill_dir: Path, body: str) -> list[Finding]:
    """Spec recommendation: body under 500 lines and ~5000 tokens."""
    findings: list[Finding] = []
    body_lines = body.count("\n") + (0 if body.endswith("\n") else 1)
    if body_lines > MAX_BODY_LINES:
        findings.append(
            Finding(
                "error",
                "body-too-many-lines",
                f"SKILL.md body is {body_lines} lines; spec recommends ≤ {MAX_BODY_LINES}. "
                f"Split detail into references/*.md.",
                "agentskills.io/specification#progressive-disclosure",
                location=f"{skill_dir.name}/SKILL.md",
            )
        )
    word_count = len(body.split())
    if word_count > MAX_BODY_WORDS:
        findings.append(
            Finding(
                "error",
                "body-too-many-words",
                f"SKILL.md body is {word_count} words; spec recommends ≤ {MAX_BODY_WORDS} "
                f"(roughly 5000 tokens).",
                "agentskills.io/specification#progressive-disclosure",
                location=f"{skill_dir.name}/SKILL.md",
            )
        )
    return findings


def check_description_quality(
    skill_dir: Path, props: dict[str, object]
) -> list[Finding]:
    """Best-practices: third-person voice, contains a `Use when` trigger."""
    desc = props.get("description")
    if not isinstance(desc, str):
        return []
    findings: list[Finding] = []
    if FIRST_OR_SECOND_PERSON_RE.match(desc):
        findings.append(
            Finding(
                "error",
                "description-not-third-person",
                "description must be written in third person; opens with first/second-person "
                "voice. See the <Warning> block in the best-practices doc.",
                "platform.claude.com/.../best-practices#writing-effective-descriptions",
                location=f"{skill_dir.name}/SKILL.md",
            )
        )
    if not TRIGGER_PHRASE_RE.search(desc):
        findings.append(
            Finding(
                "error",
                "description-no-trigger-phrase",
                "description should include a 'Use when' / 'Invoke when' / 'when the user' trigger "
                "phrase — this is the primary mechanism agents use to discover the skill.",
                "platform.claude.com/.../best-practices#writing-effective-descriptions",
                location=f"{skill_dir.name}/SKILL.md",
            )
        )
    if len(desc) > MAX_DESCRIPTION_LEN:
        findings.append(
            Finding(
                "error",
                "description-too-long",
                f"description is {len(desc)} chars; spec maximum is {MAX_DESCRIPTION_LEN}.",
                "agentskills.io/specification#description-field",
                location=f"{skill_dir.name}/SKILL.md",
            )
        )
    return findings


def check_optional_fields(skill_dir: Path, props: dict[str, object]) -> list[Finding]:
    """Validate optional frontmatter fields when present."""
    findings: list[Finding] = []
    compat = props.get("compatibility")
    if isinstance(compat, str) and len(compat) > MAX_COMPATIBILITY_LEN:
        findings.append(
            Finding(
                "error",
                "compatibility-too-long",
                f"compatibility is {len(compat)} chars; spec maximum is {MAX_COMPATIBILITY_LEN}.",
                "agentskills.io/specification#compatibility-field",
                location=f"{skill_dir.name}/SKILL.md",
            )
        )
    return findings


def check_subdirectories(skill_dir: Path) -> list[Finding]:
    """Warn on subdirectories outside the spec-named set."""
    findings: list[Finding] = []
    for entry in sorted(skill_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if entry.name in KNOWN_SUBDIRS:
            continue
        findings.append(
            Finding(
                "warning",
                "unexpected-subdirectory",
                f"unrecognized top-level subdirectory '{entry.name}/' — spec names "
                f"references/, scripts/, assets/. Other dirs are allowed but easy to miss.",
                "agentskills.io/specification#directory-structure",
                location=f"{skill_dir.name}/{entry.name}/",
            )
        )
    return findings


def check_markdown_paths(skill_dir: Path, skill_md_text: str) -> list[Finding]:
    """No Windows backslash paths in markdown content."""
    findings: list[Finding] = []
    for match in WINDOWS_PATH_RE.finditer(skill_md_text):
        line = _line_of(skill_md_text, match)
        findings.append(
            Finding(
                "error",
                "windows-path",
                f"Windows-style backslash path '{match.group(0)}' — use forward slashes only.",
                "platform.claude.com/.../best-practices#avoid-windows-style-paths",
                location=f"{skill_dir.name}/SKILL.md:{line}",
            )
        )
    return findings


def check_reference_links(skill_dir: Path, skill_md_text: str) -> list[Finding]:
    """Every relative markdown link from SKILL.md must resolve, and references
    must stay one level deep per best-practices."""
    findings: list[Finding] = []
    for match in MARKDOWN_LINK_RE.finditer(skill_md_text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # Strip any anchor.
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        target_path = (skill_dir / path_part).resolve()
        # Confine to the skill dir; the spec uses relative paths from skill root.
        try:
            target_path.relative_to(skill_dir.resolve())
        except ValueError:
            findings.append(
                Finding(
                    "error",
                    "link-escapes-skill",
                    f"markdown link '{target}' escapes the skill directory.",
                    "agentskills.io/specification#file-references",
                    location=f"{skill_dir.name}/SKILL.md:{_line_of(skill_md_text, match)}",
                )
            )
            continue
        if not target_path.exists():
            findings.append(
                Finding(
                    "error",
                    "broken-link",
                    f"markdown link '{target}' points to a nonexistent file.",
                    "agentskills.io/specification#file-references",
                    location=f"{skill_dir.name}/SKILL.md:{_line_of(skill_md_text, match)}",
                )
            )
            continue
        # Depth check: relative path should be at most two segments
        # (e.g. references/foo.md is fine; references/sub/foo.md is one too deep).
        rel = target_path.relative_to(skill_dir.resolve())
        if len(rel.parts) > 2:
            findings.append(
                Finding(
                    "error",
                    "link-too-deep",
                    f"reference '{rel}' is more than one directory deep; keep references "
                    f"one level from SKILL.md per best-practices.",
                    "platform.claude.com/.../best-practices#avoid-deeply-nested-references",
                    location=f"{skill_dir.name}/SKILL.md:{_line_of(skill_md_text, match)}",
                )
            )
    return findings


def check_reference_tocs(skill_dir: Path) -> list[Finding]:
    """Reference files >100 lines should include a Table of Contents heading.

    Per best-practices: 'For reference files longer than 100 lines, include a
    table of contents at the top.'
    """
    findings: list[Finding] = []
    refs_dir = skill_dir / "references"
    if not refs_dir.is_dir():
        return findings
    for ref in sorted(refs_dir.glob("*.md")):
        text = ref.read_text(encoding="utf-8")
        line_count = text.count("\n") + 1
        if line_count <= REFERENCE_TOC_THRESHOLD_LINES:
            continue
        # Check the first 30 lines for a TOC heading.
        head = "\n".join(text.splitlines()[:30]).lower()
        if "## contents" in head or "## table of contents" in head:
            continue
        findings.append(
            Finding(
                "warning",
                "reference-missing-toc",
                f"{ref.name} is {line_count} lines but has no '## Contents' heading near the top. "
                f"Agents may use a partial read and miss content past the preview window.",
                "platform.claude.com/.../best-practices#structure-longer-reference-files",
                location=f"{skill_dir.name}/references/{ref.name}",
            )
        )
    return findings


def check_time_sensitive_phrasing(skill_dir: Path, skill_md_text: str) -> list[Finding]:
    """Warn (not error) on dated phrasing without a clear historical-context block."""
    findings: list[Finding] = []
    for match in TIME_SENSITIVE_RE.finditer(skill_md_text):
        line = _line_of(skill_md_text, match)
        findings.append(
            Finding(
                "warning",
                "time-sensitive-phrase",
                f"time-sensitive phrasing '{match.group(0)}' may go stale. Move dated guidance "
                f"into an 'Old patterns' / `<details>` block, or rephrase as current-only.",
                "platform.claude.com/.../best-practices#avoid-time-sensitive-information",
                location=f"{skill_dir.name}/SKILL.md:{line}",
            )
        )
    return findings


def check_reserved_words_in_name(
    skill_dir: Path, props: dict[str, object]
) -> list[Finding]:
    """Best-practices says 'anthropic' and 'claude' are reserved words for the
    name field. The upstream CLI may already check this; we duplicate for safety.
    """
    name = props.get("name")
    if not isinstance(name, str):
        return []
    parts = set(name.split("-"))
    bad = parts & RESERVED_NAME_WORDS
    if bad:
        return [
            Finding(
                "error",
                "reserved-name-word",
                f"name contains reserved word(s) {sorted(bad)!r} — reserved by Anthropic.",
                "platform.claude.com/.../best-practices#technical-notes",
                location=f"{skill_dir.name}/SKILL.md",
            )
        ]
    return []


# --- runner -------------------------------------------------------------------


def get_skill_directories() -> list[Path]:
    skills = sorted(
        path
        for path in REPO_ROOT.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and (path / "SKILL.md").is_file()
    )
    if not skills:
        raise SystemExit("No skill directories with SKILL.md were found.")
    return skills


def run_all_checks(skill_dir: Path) -> list[Finding]:
    skill_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    _, body = _split_frontmatter(skill_md)

    findings: list[Finding] = []
    findings.extend(check_baseline(skill_dir))

    props = _read_properties(skill_dir) or {}

    findings.extend(check_directory_name_matches(skill_dir, props))
    findings.extend(check_reserved_words_in_name(skill_dir, props))
    findings.extend(check_description_quality(skill_dir, props))
    findings.extend(check_optional_fields(skill_dir, props))
    findings.extend(check_body_length(skill_dir, body))
    findings.extend(check_subdirectories(skill_dir))
    findings.extend(check_markdown_paths(skill_dir, skill_md))
    findings.extend(check_reference_links(skill_dir, skill_md))
    findings.extend(check_reference_tocs(skill_dir))
    findings.extend(check_time_sensitive_phrasing(skill_dir, skill_md))
    return findings


def _color(s: str, code: str) -> str:
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return s
    return f"\033[{code}m{s}\033[0m"


def _render_finding(f: Finding) -> str:
    badge = (
        _color("ERROR  ", "31") if f.severity == "error" else _color("WARN   ", "33")
    )
    loc = f"  {_color(f.location, '36')}" if f.location else ""
    return (
        f"  {badge} [{f.code}]{loc}\n"
        f"    {f.message}\n"
        f"    spec: {_color(f.spec_ref, '90')}"
    )


def _summary_line(findings: Iterable[Finding]) -> str:
    errors = sum(1 for f in findings if f.severity == "error")
    warnings = sum(1 for f in findings if f.severity == "warning")
    if errors == 0 and warnings == 0:
        return f"  {_color('PASS', '32')}"
    parts: list[str] = []
    if errors:
        parts.append(_color(f"{errors} error(s)", "31"))
    if warnings:
        parts.append(_color(f"{warnings} warning(s)", "33"))
    return "  " + ", ".join(parts)


def main() -> int:
    total_errors = 0
    total_warnings = 0
    for skill_dir in get_skill_directories():
        print(f"\n== {skill_dir.name} ==")
        findings = run_all_checks(skill_dir)
        for f in findings:
            print(_render_finding(f))
        print(_summary_line(findings))
        total_errors += sum(1 for f in findings if f.severity == "error")
        total_warnings += sum(1 for f in findings if f.severity == "warning")

    print()
    if total_errors:
        print(
            _color(
                f"FAILED: {total_errors} error(s), {total_warnings} warning(s).", "31"
            )
        )
        return 1
    if total_warnings:
        print(_color(f"OK with {total_warnings} warning(s).", "33"))
    else:
        print(_color("All skills passed.", "32"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

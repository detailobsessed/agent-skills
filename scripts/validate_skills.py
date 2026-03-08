from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def get_skill_directories() -> list[str]:
    skills = sorted(
        path.name
        for path in REPO_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".") and (path / "SKILL.md").is_file()
    )
    if not skills:
        raise SystemExit("No skill directories with SKILL.md were found.")
    return skills


def main() -> int:
    failures: list[str] = []

    for skill in get_skill_directories():
        print(f"== {skill} ==")
        result = subprocess.run(
            ["uv", "run", "agentskills", "validate", skill],
            cwd=REPO_ROOT,
            check=False,
        )
        if result.returncode != 0:
            failures.append(skill)

    if failures:
        print()
        print("Validation failed for:")
        for skill in failures:
            print(f"- {skill}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

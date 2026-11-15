# Review guidelines

This repo is a collection of agent skills: Markdown instructions that agents follow literally. A wrong command or a stale claim in a skill does not fail a test. It gets run, with confidence, by every agent that loads the skill. Review the advice as hard as the tooling.

`CLAUDE.md` describes the layout and commands. This file lists what to check in a PR.

## Critical areas

- **One tool version, pinned in several places.** prek appears in `prek.toml` (`minimum_prek_version`), in `pyproject.toml` (the `dev` group), in `uv.lock`, and in the pinned `prek-action` in `.github/workflows/ci.yml`. A change to one must agree with the others: a raised minimum with a stale pin breaks `uv run prek` while CI and a Homebrew prek still pass.
- **prek commands must select the stage.** The lint, type, validation and link hooks are declared `stages = ["pre-push"]`. A `prek run … <hook ids>` without `--hook-stage pre-push`, in CI, docs or a skill, runs none of them, prints nothing and exits 0. Flag any such command.
- **Project skills stay unpublished.** Skills under `.agents/skills/` maintain this repo. Each needs `metadata: {internal: "true"}` in its frontmatter, quoted (the spec's `metadata` values are strings), or `skills add` offers it to anyone installing from the repo. The `skills` CLI scans `.agents/` and `.claude/`, so the location alone does not hide it.

## Skill content

- **A skill describes one version, the latest at the time of writing.** Its baseline line in `SKILL.md` names that version, and the rest of the text must match it. Flag a commit that changes advice for a new release without moving the baseline, or moves the baseline without the advice. Also flag added migration notes, "new in vX" / "removed in vY" markers, or a reference for an older release line: they age badly, and older releases have upstream's versioned docs.
- **Commands and APIs a skill tells agents to use must exist.** Flag a command, flag, config key or API named in a changed section that looks invented or removed upstream, especially one not seen elsewhere in the skill.
- **Corrections replace the old text.** A "changes in vX" section appended after advice it contradicts leaves the old advice for an agent to follow. Flag it.
- **Frontmatter:** `name` matches the directory, and `description` is third person with a "Use when" trigger. `scripts/validate_skills.py` enforces the size budget (body ≤ 500 lines, ~5000 words), so don't re-report a size problem it already catches.

## Test cases

- `evals/` folders hold skill-creator test cases in the format `claude plugin eval` reads. Their `prompt.md` and grader files open with a settings block, not a heading, so markdownlint skips them on purpose.
- A grader must not pin an upstream version that will move, such as "the marker reads v0.33.0". A correct run after the next release would fail it.

## Ignore

- `uv.lock` beyond the packages the PR changes, and its `revision` line.
- `.idea/`, `.serena/` and `.venv/`, which are local state.

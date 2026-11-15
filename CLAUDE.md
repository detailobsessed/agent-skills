# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A collection of [agent skills](https://skills.sh/) — LLM-optimized instruction sets for AI agents. Each top-level directory containing a `SKILL.md` file is a skill. Skills are markdown-based with optional `references/` subdirectories for supporting material.

## Commands

```bash
# Install dependencies (Python 3.14+, uv required)
uv sync --locked --group dev

# Validate the skills: skill-validator for the Agent Skills spec, our script for the best-practices rules it lacks.
# prek builds skill-validator from the pinned tag; to run it directly, `brew install agent-ecosystem/tap/skill-validator`.
skill-validator check . --allow-dirs=evals && skill-validator check .agents/skills --allow-dirs=evals
uv run python scripts/validate_skills.py

# Run all pre-push checks (validation + typos + markdown lint + python lint/type), the same list CI runs.
# --hook-stage pre-push is required: these hooks are pre-push only, and without it prek runs nothing and exits 0.
prek run --all-files --hook-stage pre-push skill-validator skill-validator-project skill-best-practices typos markdownlint ruff-check ruff-format ty

# Run the full suite: pre-commit builtins, then every pre-push hook including lychee link checking
prek run --all-files && prek run --all-files --hook-stage pre-push

# Scaffold a new skill
skills init <name>
```

## Skill Discovery

Any top-level directory (not starting with `.`) that contains a `SKILL.md` file is a skill, and so is each directory under `.agents/skills/`. Each `SKILL.md` must have YAML frontmatter with `name` and `description` fields.

[skill-validator](https://github.com/agent-ecosystem/skill-validator) checks them against the spec, including the 5,000-token body budget, and exits non-zero on a warning as well as an error. `check .` skips dot-directories, so `.agents/skills` gets a run of its own. `scripts/validate_skills.py` holds only the four best-practices rules skill-validator lacks (third-person description, a "Use when" trigger, a contents heading in a reference over 100 lines, no time-sensitive wording). Delete it and its `skill-best-practices` hook once agent-ecosystem/skill-validator#108 ships them.

## Hook Setup

This repo uses `prek` (Rust-based git hook framework). `prek install` installs only `pre-push` by default to avoid conflicting with GitButler's `pre-commit` hook. The `.git/hooks/pre-commit` is a local wrapper that chains GitButler's hook with prek — don't overwrite it.

## CI

GitHub Actions runs on PR and push to main: syncs deps, then runs `prek` with `skill-validator skill-validator-project skill-best-practices typos markdownlint ruff-check ruff-format ty`. The `lychee` link checker is configured in `prek.toml` but not run in CI.

## PRs or main

Open a PR (via `git-spice branch submit`) for a change to the tooling (`prek.toml`, `pyproject.toml`, `uv.lock`, `.github/`, `scripts/`) or to the advice a skill gives. Devin Review checks those against `REVIEW.md`, and on PR #14 it caught a prek pin that passed every local check. Push everything else straight to `main` after the Tower review: typo fixes, README wording, a broken link. When unsure, open the PR.

## Updating a Skill

To bring a skill up to date with a new upstream release, or to retire it, follow the project skill `.agents/skills/refresh-skill/SKILL.md`.

Project skills that maintain this repo live in `.agents/skills/`; `.claude/skills` is a symlink to it, so Claude Code and Devin both load them. Give each one `metadata: {internal: "true"}`, quoted: the spec's `metadata` maps strings to strings, and the `skills` CLI accepts the string too. Without the flag, the `skills` CLI discovers `.agents/` and `.claude/` too, and `skills add` offers the skill to anyone installing from this repo. `skills add . --list` shows what is published. The validator checks these skills as well.

## Adding a New Skill

Load the `skill-creator` skill before writing or substantially rewriting any skill here, project skills under `.agents/skills/` included. It asks the scoping questions up front and tests the skill against runs without it. The validator and prek only check format, so a skill that passes them can still change nothing an agent does.

1. `skills init <name>` — creates `<name>/SKILL.md` with starter frontmatter
2. Replace the generated `SKILL.md` with real content
3. Add any `references/` or supporting files
4. Run the validation commands and the full suite above
5. Commit in small, reviewable steps

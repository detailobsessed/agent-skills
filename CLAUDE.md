# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A collection of [agent skills](https://skills.sh/) — LLM-optimized instruction sets for AI agents. Each top-level directory containing a `SKILL.md` file is a skill. Skills are markdown-based with optional `references/` subdirectories for supporting material.

## Commands

```bash
# Install dependencies (Python 3.14+, uv required)
uv sync --locked --group dev

# Validate all skills against the Agent Skills spec
uv run python scripts/validate_skills.py

# Run all pre-push checks (validation + typos + markdown lint + python lint/type).
# --hook-stage pre-push is required: these hooks are pre-push only, and without it prek runs nothing and exits 0.
prek run --all-files --hook-stage pre-push agentskills-validate typos markdownlint ruff-check ruff-format ty

# Run the full suite: pre-commit builtins, then every pre-push hook including lychee link checking
prek run --all-files && prek run --all-files --hook-stage pre-push

# Scaffold a new skill
skills init <name>
```

## Skill Discovery

Skills are auto-discovered by `scripts/validate_skills.py`: any top-level directory (not starting with `.`) that contains a `SKILL.md` file is treated as a skill. Each `SKILL.md` must have YAML frontmatter with `name` and `description` fields.

## Hook Setup

This repo uses `prek` (Rust-based git hook framework). `prek install` installs only `pre-push` by default to avoid conflicting with GitButler's `pre-commit` hook. The `.git/hooks/pre-commit` is a local wrapper that chains GitButler's hook with prek — don't overwrite it.

## CI

GitHub Actions runs on PR and push to main: syncs deps, then runs `prek` with `agentskills-validate typos markdownlint ruff-check ruff-format ty`. The `lychee` link checker is configured in `prek.toml` but not run in CI.

## Updating a Skill

To bring a skill up to date with a new upstream release, or to retire it, follow the project skill `.agents/skills/refresh-skill/SKILL.md`.

Project skills that maintain this repo live in `.agents/skills/`; `.claude/skills` is a symlink to it, so Claude Code and Devin both load them. Give each one `metadata: {internal: true}`: the `skills` CLI discovers `.agents/` and `.claude/` too, and without the flag `skills add` offers the skill to anyone installing from this repo. `skills add . --list` shows what is published. The validator checks these skills as well.

## Adding a New Skill

Load the `skill-creator` skill before writing or substantially rewriting any skill here, project skills under `.agents/skills/` included. It asks the scoping questions up front and tests the skill against runs without it. The validator and prek only check format, so a skill that passes them can still change nothing an agent does.

1. `skills init <name>` — creates `<name>/SKILL.md` with starter frontmatter
2. Replace the generated `SKILL.md` with real content
3. Add any `references/` or supporting files
4. Run `uv run python scripts/validate_skills.py` and the full suite above
5. Commit in small, reviewable steps

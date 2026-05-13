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

# Run all pre-push checks (validation + typos + markdown lint)
prek run --all-files agentskills-validate typos markdownlint

# Run full pre-push suite including link checking
prek run --all-files

# Scaffold a new skill
skills init <name>
```

## Skill Discovery

Skills are auto-discovered by `scripts/validate_skills.py`: any top-level directory (not starting with `.`) that contains a `SKILL.md` file is treated as a skill. Each `SKILL.md` must have YAML frontmatter with `name` and `description` fields.

## Hook Setup

This repo uses `prek` (Rust-based git hook framework). `prek install` installs only `pre-push` by default to avoid conflicting with GitButler's `pre-commit` hook. The `.git/hooks/pre-commit` is a local wrapper that chains GitButler's hook with prek — don't overwrite it.

## CI

GitHub Actions runs on PR and push to main: syncs deps, then runs `prek` with `agentskills-validate typos markdownlint`. The `lychee` link checker is configured in `prek.toml` but not run in CI.

## Adding a New Skill

1. `skills init <name>` — creates `<name>/SKILL.md` with starter frontmatter
2. Replace the generated `SKILL.md` with real content
3. Add any `references/` or supporting files
4. Run `uv run python scripts/validate_skills.py` and `prek run --all-files`
5. Commit in small, reviewable steps

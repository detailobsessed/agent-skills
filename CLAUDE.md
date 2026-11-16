# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A collection of [agent skills](https://skills.sh/) — LLM-optimized instruction sets for AI agents. Each published skill lives in its own plugin, at `plugins/<name>/skills/<name>/SKILL.md`. Skills are markdown-based with optional `references/` subdirectories for supporting material.

## Commands

```bash
# Install dependencies (Python 3.14+, uv required)
uv sync --locked --group dev

# Validate the skills: skill-validator for the Agent Skills spec, our script for the best-practices rules it lacks.
# prek builds skill-validator from the pinned tag; to run it directly, `brew install agent-ecosystem/tap/skill-validator`.
skill-validator check plugins && skill-validator check .agents/skills
uv run python scripts/validate_skills.py

# Run all pre-push checks (validation + typos + markdown lint + changelog format + python lint/type), the same list CI runs.
# --hook-stage pre-push is required: these hooks are pre-push only, and without it prek runs nothing and exits 0.
prek run --all-files --hook-stage pre-push skill-validator skill-validator-project skill-best-practices typos markdownlint changelog-validate ruff-check ruff-format ty

# Run the full suite: pre-commit builtins, then every pre-push hook including lychee link checking
prek run --all-files && prek run --all-files --hook-stage pre-push

# Scaffold a new skill
skills init <name>
```

## Skill Discovery

Each `plugins/<name>/skills/<name>/` with a `SKILL.md` is a published skill, and so is each directory under `.agents/skills/` a project skill. Each `SKILL.md` must have YAML frontmatter with `name` and `description` fields.

A plugin holds one skill, its `.claude-plugin/plugin.json`, and its skill-creator cases in `plugins/<name>/evals/`, where `claude plugin eval plugins/<name>` finds them without a flag. The cases sit outside the skill folder because `gh skill install` and `skills add` both copy that folder whole, with no way to exclude a path. Don't move a skill again lightly: both CLIs find an installed skill by its path in this repo, so after a move existing installs stop updating, without a message, until they are reinstalled.

To see what an install delivers, `gh skill install … --dir <scratch>` copies the skill into the scratch folder but still records it in the global `~/.agents/.skill-lock.json`, as `<name>/<name>` (gh 2.104.0). `skills list -g` then reports a skill with no folder behind it. Remove the entry after the test: `jq 'del(.skills["<name>/<name>"])'` on that file, through a temporary file.

[skill-validator](https://github.com/agent-ecosystem/skill-validator) checks them against the spec, including the 5,000-token body budget, and exits non-zero on a warning as well as an error. It runs once on `plugins` and once on `.agents/skills`. `scripts/validate_skills.py` holds only the best-practices rules skill-validator lacks: third-person description, a "Use when" trigger, a contents heading in a reference over 100 lines, no time-sensitive wording, no reserved word in the name, no Windows-style paths. agent-ecosystem/skill-validator#108 asks for the first four. Drop each check once a pinned release reports it, and the script with its `skill-best-practices` hook along with the last.

## Hook Setup

This repo uses `prek` (Rust-based git hook framework). `prek install` installs only `pre-push` by default (`default_install_hook_types` in `prek.toml`). This machine's `.git/hooks/pre-commit` is a local wrapper that runs prek's pre-commit hooks.

## CI

GitHub Actions runs on PR and push to main: syncs deps, then runs `prek` with `skill-validator skill-validator-project skill-best-practices typos markdownlint changelog-validate ruff-check ruff-format ty`. The `lychee` link checker is configured in `prek.toml` but not run in CI.

## PRs or main

Open a PR (via `git-spice branch submit`) for a change to the tooling (`prek.toml`, `pyproject.toml`, `uv.lock`, `.github/`, `scripts/`) or to the advice a skill gives. Devin Review checks those against `REVIEW.md`, and on PR #14 it caught a prek pin that passed every local check. Push everything else straight to `main` after the Tower review: typo fixes, README wording, a broken link. When unsure, open the PR.

## Changelog and Releases

`CHANGELOG.md` follows Keep a Changelog 1.1.0 and lists changes to the published skills only, never tooling or project skills. A commit that changes a skill's advice adds its entry under `Unreleased` (REVIEW.md says what an entry needs).

A release is a dated tag, `YEAR.MONTH.DAY` with no leading zeros (`2026.3.6`, not `2026.03.06`). A further release the same day appends a counter, `2026.3.6.1`, then `2026.3.6.2`, as yt-dlp does. A four-part tag is not semver, which is fine because nothing we depend on sorts tags as semver: `gh skill install` takes the latest GitHub release, the `skills` CLI reads `main`, and the README's release badge sorts by date. Keep the badge's `sort=date`: with `sort=semver` it showed `2026.11.16` after `2026.11.16.1` was out. Cut one on `main` the same day a merge leaves entries under `Unreleased`: `gh skill install` resolves to the latest release, not `main`, so a fix that is merged but not released never reaches its users. `gh skill publish` would create the release too, but only with auto-generated notes, so use `gh release create`:

1. In `CHANGELOG.md`, rename `## [Unreleased]` to `## [<version>] - <YYYY-MM-DD>`, add an empty `## [Unreleased]` above it, and update the compare links at the bottom. Commit `docs(changelog): release <version>` to `main` after the Tower review.
2. `git tag <version> && git push origin main <version>`
3. `awk "/^## \[<version>\]/{f=1;next} /^## \[/{f=0} f" CHANGELOG.md > notes.md`, then `gh release create <version> --title <version> --notes-file notes.md`.

## Updating a Skill

To bring a skill up to date with a new upstream release, or to retire it, follow the published skill `plugins/refresh-skill/skills/refresh-skill/SKILL.md`, with this repo's specifics from `docs/maintaining-skills.md`: what each skill rests on, the validation commands, and past refreshes worth copying.

Project skills that maintain this repo live in `.agents/skills/`; `.claude/skills` is a symlink to it, so Claude Code and Devin both load them. Give each one `metadata: {internal: "true"}`, quoted: the spec's `metadata` maps strings to strings, and the `skills` CLI accepts the string too. Without the flag, the `skills` CLI discovers `.agents/` and `.claude/` too, and `skills add` offers the skill to anyone installing from this repo. `skills add . --list` shows what is published. The validator checks these skills as well.

A published skill this repo also uses on itself gets a symlink there instead of a copy: `.agents/skills/refresh-skill` points to `../../plugins/refresh-skill/skills/refresh-skill`, and carries no `internal` flag. `skills add . --list` lists it once.

## Adding a New Skill

Load the `skill-creator` skill before writing or substantially rewriting any skill here, project skills under `.agents/skills/` included. It asks the scoping questions up front and tests the skill against runs without it. The validator and prek only check format, so a skill that passes them can still change nothing an agent does.

1. Before writing a skill or publishing an internal one, search for an existing one: `skills find <topic>` with a few phrasings, plus a web search for skills outside the registry. Read the closest matches and check they are maintained. Write ours only when none fits, and say why in the commit. refresh-skill reached its publish step before anyone looked.
2. `mkdir -p plugins/<name>/skills && cd plugins/<name>/skills && skills init <name>`: creates `<name>/SKILL.md` with starter frontmatter
3. Replace the generated `SKILL.md` with real content
4. Add any `references/` or supporting files, and `plugins/<name>/.claude-plugin/plugin.json` (copy another plugin's and change `name` and `description`). Eval cases go in `plugins/<name>/evals/`, never inside the skill folder.
5. Run the validation commands and the full suite above
6. Commit in small, reviewable steps

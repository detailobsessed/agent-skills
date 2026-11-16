# agent-skills

[![skills.sh](https://skills.sh/b/detailobsessed/agent-skills)](https://skills.sh/detailobsessed/agent-skills)
[![CI](https://github.com/detailobsessed/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/detailobsessed/agent-skills/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/detailobsessed/agent-skills?sort=semver)](https://github.com/detailobsessed/agent-skills/releases/latest)
[![License: MIT](https://img.shields.io/github/license/detailobsessed/agent-skills)](LICENSE)

My personal collection of [agent skills](https://skills.sh/) I created and maintain.

This repository is intended to work directly with the `skills.sh` ecosystem and CLI.

What changed in each skill, release by release, is in [CHANGELOG.md](CHANGELOG.md). Each release is a git tag named by its date, such as `2026.11.15`. `gh skill install` installs the latest release. With `skills`, pin one by adding it to the source: `skills add detailobsessed/agent-skills@2026.11.15 --skill git-spice`.

## Using this repository with `skills`

The installed CLI is available as either:

```bash path=null start=null
skills -h
```

or:

```bash path=null start=null
npx skills -h
```

For this repo, the most relevant commands are:

```bash path=null start=null
skills add https://github.com/detailobsessed/agent-skills --skill git-spice
skills add https://github.com/detailobsessed/agent-skills --skill refresh-skill
skills add https://github.com/detailobsessed/agent-skills --skill step-dev
skills add https://github.com/detailobsessed/agent-skills --skill wise-mcp
skills list
skills find
skills init my-skill
```

## Notes on authoring

- `skills create` is **not** a valid command in the current CLI
- `skills init <name>` creates a new directory containing only a starter `SKILL.md`
- In a throwaway test under `/tmp`, `skills init test-skill` created:
  - `test-skill/SKILL.md`
- That starter file includes frontmatter with `name` and `description`, plus a minimal instruction skeleton

## Repository tooling

Validation tooling is configured at the repository root:

- `pyproject.toml` provides the shared Python tooling definition
- `prek.toml` runs formatting and quality checks across all skills in the repo
- Agent Skills spec validation runs through [skill-validator](https://github.com/agent-ecosystem/skill-validator), and `scripts/validate_skills.py` adds the best-practices rules it does not check yet

This is intentional: spell-checking, dead-link checking, TOML validation, and related checks should apply consistently to every skill instead of being duplicated inside each skill directory.

Run the skill validation for all current skills from the repo root with:

```bash path=null start=null
prek run --all-files --hook-stage pre-push skill-validator skill-validator-project skill-best-practices
```

If GitButler is managing `pre-commit`, prefer leaving that hook in place and using `prek` primarily for `pre-push`. This repo is configured so a plain `prek install` installs only `pre-push` by default, which avoids overwriting a custom or GitButler-managed `pre-commit` hook.

This repo also has a local chained `pre-commit` setup in `.git/hooks` so we do not forget how it works:

- `pre-commit` is a local wrapper
- `pre-commit-gitbutler` preserves the GitButler workspace-protection hook
- `pre-commit-prek` preserves the `prek` pre-commit launcher
- the wrapper runs GitButler first, then `prek`

If `pre-commit` gets replaced by a future explicit `prek install --hook-type pre-commit`, restore the wrapper instead of treating `pre-commit.legacy` as the long-term source of truth.

## Skills

Each skill directory holds only what an agent reads: `skills add` copies the whole directory into every install. Notes for people browsing the repo live here instead. All skills are MIT-licensed ([LICENSE](LICENSE)).

### `git-spice`

Driving [git-spice](https://abhinav.github.io/git-spice/), the stacked-branch CLI, from an agent: the traps its built-in help does not warn about (prompts, experiment gates, staging, restacks that don't happen, GitHub native stacks), with `git-spice -h` left as the command reference.

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill git-spice
```

### `refresh-skill`

Bringing a skill you maintain up to date with what it rests on: a tool's releases, a product's docs, or its own design judgments and their premises. Fixes wrong advice before adding new material, verifies each claim by running it, accounts for every finding in the report, and retires the skill when a maintained one covers the same ground. The account-for-every-finding report comes from ElevenLabs' [`update-skills-from-changelog`](https://github.com/elevenlabs/skills/tree/main/.agents/skills/update-skills-from-changelog).

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill refresh-skill
```

### `step-dev`

Developing on the [Step](https://step.dev) unified automation platform — keyword development, the Keyword API, Automation Packages, and the CLI/CI-CD deployment path.

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill step-dev
```

### `wise-mcp`

Design judgment for MCP servers built with [FastMCP](https://github.com/PrefectHQ/fastmcp): what makes tools, outputs, errors, state and auth work for the agent calling them. Drawn from the MCP spec, client docs, measured studies and practitioner catalogs, each listed with the date it was last checked in [`references/sources.md`](wise-mcp/references/sources.md). Pairs with FastMCP's own `fastmcp-server` skill for the API.

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill wise-mcp
```

### Retired

- **`macos-expert`** — removed 2026-08-06. [Axiom](https://github.com/CharlesWiltgen/Axiom)'s `axiom-macos` skill now covers the same ground (windows, menus, sandboxing, AppKit interop and modernization, distribution) and tracks macOS 26/27, where this skill stopped at macOS 15. Use Axiom instead. Recoverable from git history if the Shape A/B architectural triage is ever worth extracting on its own.

## Updating a skill

Refreshing a skill against a new upstream release, or retiring it, follows the published [`refresh-skill`](refresh-skill/SKILL.md), with what it leaves to each repo in [`docs/maintaining-skills.md`](docs/maintaining-skills.md).

## Adding a new skill

The preferred workflow here is:

1. Create the skill scaffold:

    ```bash path=null start=null
    skills init my-skill
    ```

2. Replace the generated `SKILL.md` with the real skill content

3. Add any supporting `references/`, assets, or additional files the skill needs

4. Run repository validation from the root:

    ```bash path=null start=null
    prek run --all-files
    prek run --all-files --hook-stage pre-push
    ```

    The second run is the one that matters: typos, markdownlint, ruff, ty, the validators and lychee are pre-push hooks, and `prek run` without `--hook-stage pre-push` skips them silently.

5. Commit the change in small, reviewable steps

# agent-skills

[![skills.sh](https://skills.sh/b/detailobsessed/agent-skills)](https://skills.sh/detailobsessed/agent-skills)
[![CI](https://github.com/detailobsessed/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/detailobsessed/agent-skills/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/detailobsessed/agent-skills?sort=date)](https://github.com/detailobsessed/agent-skills/releases/latest)
[![License: MIT](https://img.shields.io/github/license/detailobsessed/agent-skills)](LICENSE)

My personal collection of [agent skills](https://skills.sh/) I created and maintain.

This repository is intended to work directly with the `skills.sh` ecosystem and CLI.

What changed in each skill, release by release, is in [CHANGELOG.md](CHANGELOG.md). Each release is a git tag named by its date, such as `2026.11.15`. `gh skill install` installs the latest release. With `skills`, pin one by adding it to the source: `skills add detailobsessed/agent-skills@2026.11.15 --skill git-spice`.

## Using this repository with `skills`

The installed CLI is available as either:

```bash
skills -h
```

or:

```bash
npx skills -h
```

For this repo, the most relevant commands are:

```bash
skills add https://github.com/detailobsessed/agent-skills --skill diataxis
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
- `skills init <name>` creates `<name>/SKILL.md` and nothing else: frontmatter with `name` and `description`, plus a minimal instruction skeleton

## Repository tooling

Validation tooling is configured at the repository root:

- `pyproject.toml` provides the shared Python tooling definition
- `prek.toml` runs formatting and quality checks across all skills in the repo
- Agent Skills spec validation runs through [skill-validator](https://github.com/agent-ecosystem/skill-validator), and `scripts/validate_skills.py` adds the best-practices rules it does not check yet

This is intentional: spell-checking, dead-link checking, TOML validation, and related checks should apply consistently to every skill instead of being duplicated inside each skill directory.

Run the skill validation for all current skills from the repo root with:

```bash
prek run --all-files --hook-stage pre-push skill-validator skill-validator-project skill-best-practices
```

A plain `prek install` sets up only the `pre-push` hook (`default_install_hook_types` in `prek.toml`), and that is where the checks that matter run.

## Skills

Each skill lives in `plugins/<name>/skills/<name>/` and holds only what an agent reads: `skills add` and `gh skill install` copy the whole folder into every install. Its eval cases sit beside it in `plugins/<name>/evals/`, so installs don't carry them. Notes for people browsing the repo live here instead. All skills are MIT-licensed ([LICENSE](LICENSE)).

### `diataxis`

Writing, reviewing and restructuring project documentation the way [Diátaxis](https://diataxis.fr) is described by its author, Daniele Procida: one small, publishable improvement at a time, the compass to tell tutorials, how-to guides, reference and explanation apart down to a single sentence, and a structure that grows from the content instead of four empty folders. Proposes every change before making it, and keeps each true fact when moving material. Works with any docs tool. It paraphrases diataxis.fr (CC BY-SA 4.0) and links each page it draws on.

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill diataxis
```

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

Design judgment for MCP servers built with [FastMCP](https://github.com/PrefectHQ/fastmcp): what makes tools, outputs, errors, state and auth work for the agent calling them. Drawn from the MCP spec, client docs, measured studies and practitioner catalogs, each listed with the date it was last checked in [`references/sources.md`](plugins/wise-mcp/skills/wise-mcp/references/sources.md). Pairs with FastMCP's own `fastmcp-server` skill for the API.

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill wise-mcp
```

### Retired

- **`macos-expert`** — removed 2026-08-06. [Axiom](https://github.com/CharlesWiltgen/Axiom)'s `axiom-macos` skill now covers the same ground (windows, menus, sandboxing, AppKit interop and modernization, distribution) and tracks macOS 26/27, where this skill stopped at macOS 15. Use Axiom instead. Recoverable from git history if the Shape A/B architectural triage is ever worth extracting on its own.

## Updating a skill

Refreshing a skill against a new upstream release, or retiring it, follows the published [`refresh-skill`](plugins/refresh-skill/skills/refresh-skill/SKILL.md), with what it leaves to each repo in [`docs/maintaining-skills.md`](docs/maintaining-skills.md).

## Adding a new skill

The preferred workflow here is:

1. Create the plugin and the skill scaffold inside it:

    ```bash
    mkdir -p plugins/my-skill/skills && cd plugins/my-skill/skills && skills init my-skill
    ```

2. Replace the generated `SKILL.md` with the real skill content

3. Add any supporting `references/`, assets, or additional files the skill needs, and `plugins/my-skill/.claude-plugin/plugin.json` (copy another plugin's and change `name` and `description`). Eval cases go in `plugins/my-skill/evals/`, never inside the skill folder.

4. Run repository validation from the root:

    ```bash
    prek run --all-files
    prek run --all-files --hook-stage pre-push
    ```

    The second run is the one that matters: typos, markdownlint, ruff, ty, the validators and lychee are pre-push hooks, and `prek run` without `--hook-stage pre-push` skips them silently.

5. Commit the change in small, reviewable steps

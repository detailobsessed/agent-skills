# agent-skills

[![skills.sh](https://skills.sh/b/detailobsessed/agent-skills)](https://skills.sh/detailobsessed/agent-skills)
[![CI](https://github.com/detailobsessed/agent-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/detailobsessed/agent-skills/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/detailobsessed/agent-skills?sort=date)](https://github.com/detailobsessed/agent-skills/releases/latest)
[![License: MIT](https://img.shields.io/github/license/detailobsessed/agent-skills)](LICENSE)

[Agent skills](https://skills.sh/) I write and maintain: instructions an AI coding agent loads when a task calls for them. Each one is kept up to date with the tool or method it describes.

## Skills

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

## Installing and updating

Either CLI installs a skill:

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill <name>   # tracks main
gh skill install detailobsessed/agent-skills <name>                             # installs the latest release
```

Update with `skills update` or `gh skill update`. If you installed a skill before release `2026.11.16.2`, install it again once: that release moved every skill to a new path, and both update commands skip an install whose path is gone without saying so.

Each release is a git tag named by its date, such as `2026.11.15`, and [CHANGELOG.md](CHANGELOG.md) lists what changed in each skill. To pin one with `skills`, add the tag to the source: `skills add detailobsessed/agent-skills@2026.11.15 --skill git-spice`. With `gh`, append it to the skill: `gh skill install detailobsessed/agent-skills git-spice@2026.11.15`.

All skills are MIT-licensed ([LICENSE](LICENSE)).

## Working on this repo

Each skill lives in `plugins/<name>/skills/<name>/` and holds only what an agent reads, because both CLIs copy the whole folder into every install. Its eval cases sit beside it in `plugins/<name>/evals/` and run with `claude plugin eval plugins/<name>`.

Validation runs from the repo root through [`prek`](https://prek.j178.dev): [skill-validator](https://github.com/agent-ecosystem/skill-validator) checks the Agent Skills spec, `scripts/validate_skills.py` adds the best-practices rules it lacks, and typos, markdownlint, ruff, ty, the changelog check and lychee cover the rest.

```bash
uv sync --locked --group dev
prek run --all-files
prek run --all-files --hook-stage pre-push
```

The second run is the one that matters: those checks are pre-push hooks, and `prek run` without `--hook-stage pre-push` skips them silently. A plain `prek install` sets up only the `pre-push` hook (`default_install_hook_types` in `prek.toml`).

To add a skill:

1. Create the plugin and the skill scaffold inside it. `skills init <name>` writes `<name>/SKILL.md` with starter frontmatter and nothing else (there is no `skills create`).

    ```bash
    mkdir -p plugins/my-skill/skills && cd plugins/my-skill/skills && skills init my-skill
    ```

2. Replace the generated `SKILL.md` with the real skill content.
3. Add any supporting `references/` or assets the skill needs, and `plugins/my-skill/.claude-plugin/plugin.json` (copy another plugin's and change `name` and `description`). Eval cases go in `plugins/my-skill/evals/`, never inside the skill folder.
4. Run the validation above, and commit in small, reviewable steps.

Refreshing a skill against a new upstream release, or retiring it, follows the published [`refresh-skill`](plugins/refresh-skill/skills/refresh-skill/SKILL.md), with what it leaves to each repo in [`docs/maintaining-skills.md`](docs/maintaining-skills.md).

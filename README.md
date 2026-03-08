# agent-skills

My personal collection of [agent skills](https://skills.sh/) I created and maintain.

This repository is intended to work directly with the `skills.sh` ecosystem and CLI.

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
skills add https://github.com/detailobsessed/agent-skills --skill macos-expert
skills add https://github.com/detailobsessed/agent-skills --skill git-spice
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

This is intentional: spell-checking, dead-link checking, TOML validation, and related checks should apply consistently to every skill instead of being duplicated inside each skill directory.

If GitButler is managing `pre-commit`, prefer leaving that hook in place and using `prek` primarily for `pre-push`. This repo is configured so a plain `prek install` installs only `pre-push` by default, which avoids overwriting a custom or GitButler-managed `pre-commit` hook.

This repo also has a local chained `pre-commit` setup in `.git/hooks` so we do not forget how it works:

- `pre-commit` is a local wrapper
- `pre-commit-gitbutler` preserves the GitButler workspace-protection hook
- `pre-commit-prek` preserves the `prek` pre-commit launcher
- the wrapper runs GitButler first, then `prek`

If `pre-commit` gets replaced by a future explicit `prek install --hook-type pre-commit`, restore the wrapper instead of treating `pre-commit.legacy` as the long-term source of truth.

## Skills

### `macos-expert`

Source-backed macOS app development guidance covering Apple HIG expectations, SwiftUI, AppKit, accessibility, file/document workflows, and platform capabilities.

### `git-spice`

Working effectively with [git-spice](https://abhinav.github.io/git-spice/) for stacked branches and GitLab/GitHub merge requests.

### `wise-mcp`

Building MCP servers with [FastMCP](https://github.com/PrefectHQ/fastmcp), informed by battle-tested agentic tool design patterns by [Arcade](https://www.arcade.dev/patterns).

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
    ```

5. Commit the change in small, reviewable steps

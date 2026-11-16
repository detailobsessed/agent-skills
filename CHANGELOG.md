# Changelog

All notable changes to the published skills are documented in this file. Each entry names the skill it changes. Changes to this repo's own tooling and project skills are left out.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions follow [Calendar Versioning](https://calver.org/): the release date as `YEAR.MONTH.DAY` without leading zeros, with a counter appended for a further release the same day (`2026.11.16.1`).

## [Unreleased]

### Changed

- **Breaking:** every skill (**diataxis**, **git-spice**, **refresh-skill**, **step-dev**, **wise-mcp**) moved to `plugins/<name>/skills/<name>/`, with its eval cases beside it in `plugins/<name>/evals/`, so an install no longer carries the graders and test prompts. `gh skill update` and `skills update` find an installed skill by its old path and now skip it without a message, so reinstall each skill once: `gh skill install detailobsessed/agent-skills <name> --force`, or `skills add https://github.com/detailobsessed/agent-skills --skill <name>`.

## [2026.11.16.1] - 2026-11-16

### Added

- **diataxis**: new skill for writing, reviewing and restructuring project documentation the way diataxis.fr describes it. It works one small improvement at a time instead of imposing a tutorials/how-to/reference/explanation layout, uses the compass to classify content down to a single sentence, and gives a writing guide for each of the four modes plus troubleshooting, FAQ, migration guides and mixed pages. It proposes each change and waits for approval, reports gaps as observations rather than creating empty pages, keeps every true fact when moving material, brings each removal of wrong or duplicated content to the user as a decision, and updates the docs tool's navigation only to follow the content.

## [2026.11.16] - 2026-11-16

### Added

- **refresh-skill**: new skill for bringing a skill you maintain up to date with its tool's releases, its product's docs, or the premises under its own advice. It fixes wrong advice before adding anything, verifies each claim by running it, accounts for every finding in its report, and retires the skill when a maintained one covers the same ground.

## [2026.11.15] - 2026-11-15

### Changed

- **git-spice**: Written against git-spice v0.33.0, and narrowed to the traps its built-in help does not warn about: running without a terminal (`--no-prompt`, an explicit commit message, `ls --json`), `-a` skipping new files, experiments that look like ordinary commands, commands that only retarget instead of restacking, raw-git restacks, `-a` meaning `--assign` on submit, and forge setup. For flags and commands, it now points to `git-spice <command> -h` and the docs' `llms.txt`.
- **wise-mcp**: Narrowed to MCP server design judgment for FastMCP 4.2.0, since FastMCP's own `fastmcp-server` skill covers the API. It now covers state across calls on a stateless protocol, asking the user through input-required results, concise and detailed responses, readable identifiers, and acting as the end user in auth.
- **wise-mcp**: Execution model, resources/prompts/apps and composition moved into `references/` unchanged, bringing the body under the spec's 5,000 tokens. The sources the advice rests on are listed, each dated, in `references/sources.md`.
- **step-dev**: Refreshed for the Step v31 docs: the exense-oss Maven repository blocks, automation package schema 1.3.0 and its `${` trap, the five-argument JavaScript keyword signature, local agents and deployment options, Step Studio, metrics, and library limits.
- **step-dev**: The description now says in sentences what the skill explains and when to use it.
- Each skill declares `license: MIT` in its frontmatter and no longer ships its own README or LICENSE. Their content is in the repo's root README and LICENSE.

### Added

- **git-spice**: GitHub native stacks (v0.33.0): what a submit registers, how a merge merges them atomically, and their limits (linear stacks, branches in the receiving repo, auto-merge).
- **git-spice**: Azure DevOps as a forge kind.

### Removed

- **git-spice**: The per-command flag catalog and the version change notes.
- **wise-mcp**: `references/fastmcp-4.md` and `references/apps.md`. Skills now describe only the latest release, and FastMCP's own skill covers the API.

### Fixed

- **git-spice**: Pass `--restack` on the first `repo sync`. The old advice was to run a second `repo sync --restack` after a plain one, which restacks nothing.
- **wise-mcp**: No longer recommends APIs that fail on current connections: `ctx.set_state` for per-conversation memory, `ctx.elicit` for confirmation, and `require_auth`, which exists in no FastMCP release.
- **wise-mcp**: No longer advises hiding tools behind search at 10+ tools. Claude Code, Copilot CLI and Cursor now defer tool loading themselves.
- **wise-mcp**: The visibility gateway recipe says it needs auth over HTTP. Without it, `enable_tools()` raises because the request carries no client identity.
- **step-dev**: The Maven plugin setup includes its repository, which it has needed since Step 30.5 moved off Maven Central.
- **step-dev**: .NET keywords no longer use `AbstractScript`, which does not exist.
- **step-dev**: States that Step 30+ needs Java 21, not 11.
- **step-dev**: Node.js and .NET keywords can run on local agents.
- **step-dev**: A `false` return from the Node agent's `onError` hook skips only `outputBuilder.fail(e)`, so an error already set on the output still fails the keyword.
- **step-dev**: The Developer guide link, a 404 since the docs moved.
- **git-spice**, **wise-mcp**: Leftover `.gitignore` files are gone, which every install used to copy.

## [2026.8.6] - 2026-08-06

### Added

- **git-spice**: The experiments `stack merge`, `commit fixup` and `commit pick`, with the `spice.experiment.*` line that enables each.
- **git-spice**: Gitea, Forgejo, Codeberg and Bitbucket Data Center setup, `spice.forge.kind` for rewritten remotes, the `--no-restack` family, repeatable `-m`, the `spice.submit.labels` rename, and the renamed merge timeout settings.
- **wise-mcp**: Code Mode, `ToolResult(is_error=True)` for structured errors, and the FastMCP 3.4.x transport hardening notes.

### Changed

- **git-spice**: Updated for v0.29.0 through v0.31.2. `repo sync`, `branch delete` and `branch onto` only retarget by default, and `--restack` takes `none`, `aboves` or `upstack`.
- **wise-mcp**: Refreshed for FastMCP 3.4.5. Progressive disclosure now opens with when not to use it, since most MCP clients defer tool loading themselves.

### Removed

- **macos-expert**: Retired in favour of Axiom's `axiom-macos` skill, which covers the same ground and tracks macOS 26 and 27. The reasoning is in the README's Retired section.

### Fixed

- **git-spice**: No longer sets `spice.forge.bitbucket.url` to `https://bitbucket.org`, which since v0.31.0 breaks Bitbucket Cloud repos.

## [2026.7.29] - 2026-07-29

### Added

- **git-spice**: `git-spice stack merge`: the bottom-up merge workflow and its flags. It merges one branch at a time, so it is not a parallel merge queue.

## [2026.5.16] - 2026-05-16

### Added

- **step-dev**: New skill for Step keyword development in Java, .NET and JavaScript/TypeScript, the Keyword API, automation packages and their YAML descriptor, the Step CLI, the Maven plugin, CI/CD and execution.

### Changed

- **wise-mcp**: Refreshed for FastMCP 3.3.0 (apps, built-in providers, auto-docstring parameters, auth-scoped tasks, the slim client and more auth providers) and Arcade's 54-pattern catalog, including a new execution model section.

## [2026.5.13] - 2026-05-13

### Changed

- **git-spice**: Updated for git-spice v0.28.0.

## [2026.5.11] - 2026-05-11

### Changed

- **macos-expert**: Rewritten to match what SwiftUI on macOS does today, naming the AppKit primitive for each gap, with a triage rubric for picking an architecture before writing code.

## [2026.4.10] - 2026-04-10

### Changed

- **git-spice**: Updated for git-spice v0.25.0.

## [2026.3.8] - 2026-03-08

### Added

- **macos-expert**: New skill for building macOS apps, with triggers, a common anti-patterns section, and Sosumi as a companion for checking Apple's docs.

## [2026.3.7] - 2026-03-07

### Added

- **wise-mcp**: A progressive disclosure section and `BM25SearchTransform` patterns.

## [2026.3.6] - 2026-03-06

### Added

- **git-spice** and **wise-mcp**: the first published skills.

[unreleased]: https://github.com/detailobsessed/agent-skills/compare/2026.11.16.1...HEAD
[2026.11.16.1]: https://github.com/detailobsessed/agent-skills/compare/2026.11.16...2026.11.16.1
[2026.11.16]: https://github.com/detailobsessed/agent-skills/compare/2026.11.15...2026.11.16
[2026.11.15]: https://github.com/detailobsessed/agent-skills/compare/2026.8.6...2026.11.15
[2026.8.6]: https://github.com/detailobsessed/agent-skills/compare/2026.7.29...2026.8.6
[2026.7.29]: https://github.com/detailobsessed/agent-skills/compare/2026.5.16...2026.7.29
[2026.5.16]: https://github.com/detailobsessed/agent-skills/compare/2026.5.13...2026.5.16
[2026.5.13]: https://github.com/detailobsessed/agent-skills/compare/2026.5.11...2026.5.13
[2026.5.11]: https://github.com/detailobsessed/agent-skills/compare/2026.4.10...2026.5.11
[2026.4.10]: https://github.com/detailobsessed/agent-skills/compare/2026.3.8...2026.4.10
[2026.3.8]: https://github.com/detailobsessed/agent-skills/compare/2026.3.7...2026.3.8
[2026.3.7]: https://github.com/detailobsessed/agent-skills/compare/2026.3.6...2026.3.7
[2026.3.6]: https://github.com/detailobsessed/agent-skills/releases/tag/2026.3.6

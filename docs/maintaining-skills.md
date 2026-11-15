# Maintaining the skills in this repo

The method for refreshing a skill is the published [`refresh-skill`](../refresh-skill/SKILL.md) skill. This page holds what it leaves to each repo: what each of our skills rests on, how we validate and commit, and the past refreshes worth copying.

## What each skill rests on

Update this table when a skill is added, retired, or what it rests on changes.

| Skill | Release stream | Docs | Judgments |
| --- | --- | --- | --- |
| `git-spice` | `abhinav/git-spice`; "Written against git-spice vX, the latest at the time of writing (date)" in `SKILL.md`. Holds only the traps the built-in help does not warn about: `git-spice -h` is the command reference | `git-spice -h` and <https://abhinav.github.io/git-spice/> (source under `doc/src/` at each tag) | **the whole skill**: every trap, each re-run against the new release in a scratch repo |
| `step-dev` | `exense/step` (tags `3.N.x` = docs `vN`, confirmed for 29–31); the Java Keyword API releases separately (`exense/step-api`) | **primary**: the `step.dev/knowledgebase` pages cited in `references/*.md`; "based on the vN documentation … last read on" in `SKILL.md`. No public docs source; `https://step.dev/knowledgebase/<N>/...` serves version N, for diffing against the last-read version | stateful vs stateless keyword guidance, the common-mistakes list |
| `wise-mcp` | `PrefectHQ/fastmcp`; "Written against FastMCP X and MCP spec Y, the latest at the time of writing (date)" in `SKILL.md`. Names only the APIs its judgments rest on: the API itself is upstream's `fastmcp-server` skill | <https://gofastmcp.com> (unversioned pages are the current line); Arcade's catalog at <https://www.arcade.dev/patterns>, its count in `SKILL.md` and `references/sources.md` | **the whole skill**. Its premises are the table in `references/sources.md`: spec, client docs, measured studies, Arcade's catalog, each with a checked date. Re-read every row, then search for newer work (vendor engineering posts, benchmarked studies, the spec's newest revision) and add a row for anything that holds up, or a "searched and not adopted" note. Measurements outrank a practitioner's catalog |
| `refresh-skill` | none | the Agent Skills spec at <https://agentskills.io/specification> and skill-validator's rules | **the whole skill**: re-check it against how the refreshes since the last review went, and against maintained skills that do the same job (`skills find "refresh skill"`, `skills find "update skill"`) |

## Repo conventions

- **Issues** live in the `agent-skills` Linear project. Refreshing several skills: a parent issue with one sub-issue per skill, so each commit closes its own (`Closes DOT-nnn`), and all the commits on one branch for one PR, the shape of PR #16.
- **Validation:**

  ```bash
  prek run --all-files --hook-stage pre-push skill-validator skill-validator-project skill-best-practices typos markdownlint kacl-verify ruff-check ruff-format ty
  prek run --all-files --hook-stage pre-push lychee   # links; not run in CI, so run it here
  ```

  Keep `--hook-stage pre-push`: without it `prek` runs none of these hooks, prints nothing and exits 0. Stage new files first, since `--all-files` skips untracked ones. A lychee failure in a skill you did not touch is worth a line in the report, not a fix in this commit. `typos` rewriting a CLI literal is a known trap: add the literal to `_typos.toml` rather than accepting the rewrite.
- **Review:** every changeset goes to review in Tower before it is committed (the `tower-review` skill).
- **Changelog and releases:** `CHANGELOG.md`, with the rules in `CLAUDE.md` under "Changelog and Releases".
- **No README in a skill directory:** `skills add` copies everything in it into the install, so markers live in `SKILL.md` and `references/`, and the root `README.md` lists the skills. Update its entry if a skill's one-line summary changed, and record a retirement under its `### Retired` heading.

## Past refreshes worth copying

| Commit | Shows |
| --- | --- |
| `fc496ab` | a release-driven refresh (git-spice v0.29.0 through v0.31.2): an experiment gate the skill missed, and v0.29.0 changing what `--restack` means in a minor release |
| `05f6dc3` | a judgment rewritten from a new premise: wise-mcp's "progressive disclosure at 10+ tools" once clients deferred tool loading themselves |
| `b47f466` | a retirement: macos-expert in favour of Axiom's `axiom-macos`, with the reasons in the README |
| `76589e6` | narrowing to judgment when upstream ships a skill for the API (wise-mcp against FastMCP's `fastmcp-server`), and `require_auth`, which docs search called verified and an import showed exists in no release |
| `22d2fe9`, `c413f92` | git-spice v0.33.0: traps re-run without a terminal, and Devin Review catching a recovery path the scratch repo never ran (a second `repo sync --restack` restacks nothing) |
| `60728c3` | coverage dropped on an untested assumption: two validator checks cut because skill-validator "covered them", which it did not |

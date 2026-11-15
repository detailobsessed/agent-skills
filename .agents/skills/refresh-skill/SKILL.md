---
name: refresh-skill
description: Bring a skill in this repo up to date with what it was built from — a tool's releases, a product's docs, or our own design judgments and the ecosystem they rest on. Finds what changed since the skill was last checked, fixes the advice that is now wrong, adds what is new, or retires the skill when something better covers it. Use when the user asks to update, refresh, review or audit a skill here, when a skill's upstream has released or its docs moved, when a skill has not been looked at in months, or when an agent following one of these skills hit an error the skill did not predict.
metadata:
  internal: "true"
---

# Refresh a skill

The skills in this repo each describe something that keeps moving. A stale skill does not just miss features — it tells the agent to do things that no longer work, or no longer make sense, and the agent follows it with confidence. A refresh exists to find and fix that advice first. New material comes second.

This skill is how this repo is maintained, not a skill to publish. It lives in `.agents/skills/` (Claude Code reads it through the `.claude/skills` symlink, Devin directly), and `metadata.internal: "true"` keeps `skills add` from offering it. The `skills` CLI scans `.claude/` and `.agents/` too, so the flag is what keeps it out, not the location. Check with `skills add . --list`.

## 1. Find what the skill was built from

Skills here rest on three kinds of source, and most rest on more than one. Each changes in a different way, so each needs a different check:

| Kind | Changes by | How to see what changed |
| --- | --- | --- |
| **Release stream** — a versioned tool or library | tagged releases | release notes for every release since the baseline (step 2a) |
| **Docs** — a product's documentation site | pages edited in place, often with no release to point at | re-read each page the skill cites and compare it with the skill's claims (step 2b) |
| **Our judgments** — design advice we synthesised ourselves | the premises under it going stale: client behaviour, the protocol, current practice | list the judgments, find the premise under each, re-check the premise (step 2c) |

What each skill currently rests on:

| Skill | Release stream | Docs | Our judgments |
| --- | --- | --- | --- |
| `git-spice` | `abhinav/git-spice`; "Written against git-spice vX, the latest at the time of writing (date)" in `SKILL.md`. Holds only the traps the built-in help does not warn about: `git-spice -h` is the command reference | `git-spice -h` and <https://abhinav.github.io/git-spice/> (source under `doc/src/` at each tag) | **the whole skill**: every trap, each re-run against the new release in a scratch repo |
| `step-dev` | `exense/step` (tags `3.N.x` = docs `vN`, confirmed for 29–31); the Java Keyword API releases separately (`exense/step-api`) | **primary**: the `step.dev/knowledgebase` pages cited in `references/*.md`; "based on the vN documentation … last read on" in `SKILL.md`. No public docs source; `https://step.dev/knowledgebase/<N>/...` serves version N, for diffing against the last-read version | stateful vs stateless keyword guidance, the common-mistakes list |
| `wise-mcp` | `PrefectHQ/fastmcp`; "Written against FastMCP X and MCP spec Y, the latest at the time of writing (date)" in `SKILL.md`. Names only the APIs its judgments rest on: the API itself is upstream's `fastmcp-server` skill | <https://gofastmcp.com> (unversioned pages are the current line); Arcade's catalog at <https://www.arcade.dev/patterns>, its count in `SKILL.md` and `references/sources.md` | **the whole skill**. Its premises are the table in `references/sources.md`: spec, client docs, measured studies, Arcade's catalog, each with a checked date. Re-read every row, then search for newer work (vendor engineering posts, benchmarked studies, the spec's newest revision) and add a row for anything that holds up, or a "searched and not adopted" note. Measurements outrank a practitioner's catalog |

Read the skill's `git log` too: the last refresh commit says what was checked then and why, and is where this refresh picks up. Then search the `agent-skills` Linear project for open issues naming the skill. A refresh often settles them without saying so: two wise-mcp issues sat in the backlog for months after the refresh that did their work, one of them resting on a FastMCP behaviour that had since changed. Close each one the refresh settles, saying what settled it, or fold it into the refresh.

Every source a skill rests on needs a marker saying when it was last checked: a version for a release stream, a docs version plus the date read for docs, a "reviewed" date for judgments. If one is missing, adding it is part of this refresh — without it the next refresh cannot tell what is stale. Update the table above when a skill is added, retired, or what it rests on changes.

## 2. Find what changed

Sort every finding into one of four buckets as you go:

1. **Breaks the skill's advice** — removed or renamed commands, flags, APIs or config keys; changed defaults; features moved behind an experiment flag; a doc page that now says the opposite. These are the reason for the refresh.
2. **Makes the advice obsolete** — the skill works around a gap that has since closed, or argues from a premise that no longer holds. Advice that pushes toward a workaround you no longer need is worse than none (the reason `macos-expert` was retired).
3. **New and worth teaching** — something an agent would plausibly need and would not find on its own.
4. **Noise** — bug fixes and internals that change nothing an agent does. Skip them.

### 2a. Release stream

Check how far behind the baseline is, then read the notes for **every** release since it, oldest first, not just the latest. Behaviour changes hide in minor releases (git-spice v0.29.0 changed what `--restack` means).

```bash
repo=abhinav/git-spice
gh release list -R "$repo" --limit 50 --json tagName,publishedAt,isPrerelease \
  --jq '.[] | "\(.publishedAt[:10]) \(.tagName)\(if .isPrerelease then " (pre)" else "" end)"'
gh release view -R "$repo" <tag> --json body --jq .body   # per tag, oldest first
```

Where upstream keeps a `CHANGELOG.md` or a `.changes/` directory instead, read that.

A skill describes one version: the latest stable release at the time of writing, named once in the baseline line. Move it there, across a new major line too, and leave a prerelease alone until it is stable. Write no migration notes, no "new in vX" or "removed in vY" markers, and no reference for users on an older line: they age badly, and an agent on an old release has upstream's versioned docs. What a release breaks matters only for finding the advice to rewrite.

### 2b. Docs

Docs change without telling anyone, so there is nothing to diff against. Load the `web-research` skill, then:

1. List the pages the skill cites (`rg -o 'https://[^ )>]+' <skill>/`).
2. Fetch each one and compare it with the claims the skill makes from it. Note pages that moved, vanished, or changed their advice.
3. Look for new pages in the same docs sections that cover ground the skill does not.
4. Read the product's release notes for the same period anyway: they say which pages were likely to change.

### 2c. Our judgments

Release notes and docs never say that our own advice went stale. Do this pass deliberately:

1. List the skill's judgments — the advice that is ours, not a restatement of upstream docs (principles, "prefer X over Y", thresholds, anti-patterns).
2. For each, write down the premise it rests on. `wise-mcp`'s old "add progressive disclosure at 10+ tools" rested on "clients load every tool schema up front".
3. Check whether the premise still holds: the MCP spec's changelog, how the main clients behave now (their docs and release notes), the sources the skill lists, and what well-regarded current practice says. A skill's source list is where to start, not where to stop: search past it for newer measured work, because a catalog that was the best available when the skill was written can be overtaken without changing a word (`wise-mcp` leaned on Arcade alone until 2026-11-15).
4. A premise that no longer holds puts the judgment in bucket 2. Rewrite it from the new premise, and say in the commit what changed underneath it — `05f6dc3` is the model.
5. Keep the skill's source list current: add what you used, record what you searched and rejected, and date every row.

## 3. Check whether the skill should still exist

Before editing, check whether another maintained skill now covers the same ground better. It takes one command, so run it every time rather than reasoning that nothing could have replaced ours:

```bash
skills find <topic>   # e.g. fastmcp; works without a terminal, lists install counts
```

Upstreams publish their own skills now (gofastmcp.com ships `fastmcp-server`), so look hardest at entries from the upstream's own org. If one does, and tracks the newer upstream where ours stopped, retire ours rather than refresh it:

- delete the skill directory in one commit;
- add an entry under `### Retired` in the root `README.md` with the date, the replacement, and why — so the decision can be re-checked later;
- name anything worth recovering from git history.

`b47f466` (macos-expert → Axiom) is the worked example.

When an upstream skill covers only part of ours, usually the API, narrow ours to what it doesn't cover instead of retiring it. Drop what theirs says, point to it, and keep our own judgment. Don't take on the upstream author's personal setup or conventions along the way. `wise-mcp` against gofastmcp.com's `fastmcp-server` is the example: theirs routes to the API docs, ours keeps the design advice.

## 4. Verify before writing

Test each bucket-1 and bucket-3 claim before it goes into the skill: run the installed tool's `-h`, run the command in a scratch repo, install the new library version in a throwaway project (`uv init` in the scratchpad, `uv add <pkg>==<version>`), read the source where the notes are vague. A release note says what changed; it rarely says what it means for a user who followed the old advice. That consequence is what the skill has to say.

Finding a name in the docs is not verification. Run the code. In a test refresh, an agent that grepped FastMCP's docs listed `require_auth` as "verified still true"; an agent that imported it found it exists in neither 3.4.11 nor 4.2.0. In the report, mark each claim as run or docs-only, so the reviewer knows which ones to trust.

Run it the way an agent runs it, and run every path the skill prescribes:

- **No terminal.** An agent's shell has no TTY, and tools behave differently there. git-spice does not hang on a missing branch name, as the old skill said: it fails with "not allowed to prompt for input". Run the scratch commands from the agent's own shell, not from yours.
- **The recovery paths too.** Advice of the form "if you already did X, run Y" needs X then Y in the scratch repo. The git-spice refresh ran `repo sync --restack` on a fresh stack and passed, while the skill told agents to run it *after* a plain sync, when it restacks nothing. Devin Review caught it in the PR, from upstream's source.
- **The coverage you drop advice for.** When you cut advice because upstream's help or skill now covers it, run upstream on the case first. When `scripts/validate_skills.py` was cut down to what skill-validator lacks, two checks went on that assumption, and skill-validator turned out to pass both cases.

## 5. Edit

Fix bucket 1 first, then bucket 2, then add bucket 3.

- Correct wrong advice where it stands; do not append a "changes in vX" section that leaves the old text in place for an agent to follow.
- Describe the latest release only (step 2a): remove any version notes and "new in vX" markers you find, rather than adding more.
- Move every marker from step 1 to what you checked. Markers live in the skill's own files (`SKILL.md`, `references/`): a skill directory holds no README, since `skills add` copies everything in it into the install.
- Stay inside skill-validator's budget: `SKILL.md` body ≤ 500 lines and 5,000 tokens. When a section grows, move the detail into `references/<topic>.md` and leave a one-line pointer, as `wise-mcp/references/scaling-large-catalogs.md` does.
- Keep the frontmatter `description` third-person with a "Use when" trigger; if the refresh changed what the skill covers, update it.
- Update the root `README.md` skill list if the skill's one-line summary changed.

## 6. Validate

```bash
prek run --all-files --hook-stage pre-push skill-validator skill-validator-project skill-best-practices typos markdownlint ruff-check ruff-format ty
prek run --all-files --hook-stage pre-push lychee   # links; not run in CI, so run it here
```

Keep `--hook-stage pre-push`: these hooks are declared pre-push only, and without the flag `prek` runs none of them, prints nothing and exits 0. Each hook must print `Passed`; an empty output is a check that did not happen. All three must pass before the changeset goes to review. A lychee failure in a skill you did not touch is still worth a line in the report, not a fix in this commit. `typos` rewriting a CLI literal is a known trap: add the literal to `_typos.toml` rather than accepting the rewrite.

They check format, not behaviour. For a refresh that rewrites advice, the behavioural check is `skill-creator`'s comparison loop: the refreshed skill against the pre-refresh one (it snapshots the old version), on prompts that hit the changed advice, such as "sync my stack after the base merged" for git-spice's `--restack` change. It costs two agent runs per prompt. Start from the skill's `evals/` when it has one (`wise-mcp/evals/` does): rerun those cases, then add a case for each piece of advice this refresh changed, and save the new cases back there. Do not skip it silently: put it in the review post as a decision, with the prompts you would use and the cost, and run it if the user says yes.

Two things keep the comparison honest:

- **Tell each run to read only the skill file you hand it, and to load no skill through the Skill tool.** An installed copy of the same skill, such as a global `git-spice`, would otherwise load into both runs and erase the difference you are measuring.
- **Pick prompts where the old advice was wrong or silent.** A case both versions pass shows nothing: in the git-spice comparison, both committed the new file correctly, and only the sync and merge cases told the versions apart.

## 7. Commit

One commit per skill, so each refresh can be reviewed and reverted on its own. Hand the changeset over for review in Tower before committing (the `tower-review` skill).

Subject: `docs(<skill>): update for <upstream> vA through vB` for a release-driven refresh, `docs(<skill>): refresh for <what changed>` otherwise.

Body: lead with what an agent following the old skill got wrong and what happened when it did, then what was added, then what was dropped and why. `fc496ab` and `05f6dc3` are the models. End with `Refs`/`Closes` for the Linear issue.

## Refreshing several skills

Open a parent issue in the `agent-skills` Linear project with one sub-issue per skill, so each refresh shows on the board and its own commit closes it (`Closes DOT-nnn`). Put all the commits on one branch for a single PR, the shape of PR #16. A checklist inside an issue is only for steps within one commit.

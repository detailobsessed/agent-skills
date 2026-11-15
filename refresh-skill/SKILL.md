---
name: refresh-skill
description: Brings an agent skill you maintain up to date with what it was built from — a tool's releases, a product's docs, or the design judgments the skill makes and the premises under them. Finds what changed since the skill was last checked, fixes the advice that is now wrong before adding anything new, verifies each claim by running it, accounts for every change it found, or retires the skill when a maintained one covers the same ground. Use when asked to update, refresh, review or audit a SKILL.md, when the tool or library a skill describes has released or its docs moved, when a skill has not been looked at in months, or when an agent following a skill hit an error the skill did not predict.
license: MIT
---

# Refresh a skill

A skill describes something that keeps moving. When it goes stale it does not just miss features: it tells the agent to do things that no longer work, or no longer make sense, and the agent follows it with confidence. A refresh finds and fixes that advice first. New material comes second.

Before starting, read the repo's own maintenance notes: its `AGENTS.md` or `CLAUDE.md`, and any file they point to that records what each skill rests on, how the repo validates skills, and how it wants changes committed. Where they differ from this skill, the repo wins.

## 1. Find what the skill was built from

A skill rests on three kinds of source, and most rest on more than one. Each changes in a different way, so each needs a different check:

| Kind | Changes by | How to see what changed |
| --- | --- | --- |
| **Release stream** — a versioned tool or library | tagged releases | the notes for every release since the baseline (step 2a) |
| **Docs** — a product's documentation site | pages edited in place, often with no release to point at | re-read each page the skill cites and compare it with the skill's claims (step 2b) |
| **Judgments** — design advice the skill's authors synthesised | the premises under it going stale: client behaviour, a protocol, current practice | list the judgments, find the premise under each, re-check the premise (step 2c) |

Every source needs a marker saying when it was last checked: a version for a release stream, a docs version and the date read for docs, a "reviewed" date for judgments. Look in `SKILL.md` and `references/`. If a marker is missing, adding it is part of this refresh: without it, the next refresh cannot tell what is stale. If the repo keeps a record of what each skill rests on, update it too.

Read the skill's `git log`: the last refresh commit says what was checked then and why, and is where this refresh picks up. Then search the repo's issue tracker for open issues naming the skill. A refresh often settles one without saying so, and it then sits in the backlog for months. Close each one the refresh settles, saying what settled it, or fold it into the refresh.

## 2. Find what changed

Sort every finding into one of four buckets as you go, and keep the list: step 6 accounts for each one.

1. **Breaks the skill's advice** — a removed or renamed command, flag, API or config key; a changed default; a feature moved behind an experiment flag; a doc page that now says the opposite. These are the reason for the refresh.
2. **Makes the advice obsolete** — the skill works around a gap that has since closed, or argues from a premise that no longer holds. Advice that pushes toward a workaround nobody needs any more is worse than none.
3. **New and worth teaching** — something an agent would plausibly need and would not find on its own.
4. **Noise** — bug fixes and internals that change nothing an agent does.

### 2a. Release stream

Check how far behind the baseline is, then read the notes for **every** release since it, oldest first, not just the latest. Behaviour changes hide in minor releases.

```bash
repo=<owner>/<repo>
gh release list -R "$repo" --limit 50 --json tagName,publishedAt,isPrerelease \
  --jq '.[] | "\(.publishedAt[:10]) \(.tagName)\(if .isPrerelease then " (pre)" else "" end)"'
gh release view -R "$repo" <tag> --json body --jq .body   # per tag, oldest first
```

Where upstream keeps a `CHANGELOG.md` or a `.changes/` directory instead, read that.

A skill describes one version: the latest stable release at the time of writing, named once in the baseline line. Move the baseline there, across a new major line too, and leave a prerelease alone until it is stable. What a release breaks matters only for finding the advice to rewrite. An agent on an older release has upstream's versioned docs.

### 2b. Docs

Docs change without telling anyone, so there is nothing to diff against:

1. List the pages the skill cites (`rg -o 'https://[^ )>]+' <skill>/`).
2. Fetch each one and compare it with the claims the skill makes from it. Note pages that moved, vanished, or changed their advice. A docs site that renders in the browser often comes back empty from a plain fetch: fetch its Markdown source from the project's repository instead.
3. Look for new pages in the same docs sections that cover ground the skill does not.
4. Read the product's release notes for the same period anyway: they say which pages were likely to change.

### 2c. Judgments

Release notes and docs never say that the skill's own advice went stale. Do this pass deliberately:

1. List the skill's judgments: the advice that is its own, not a restatement of upstream docs (principles, "prefer X over Y", thresholds, anti-patterns).
2. For each, write down the premise it rests on. "Add progressive disclosure at 10+ tools" rests on "clients load every tool schema up front".
3. Check whether the premise still holds: the protocol's or spec's changelog, how the main clients behave now (their docs and release notes), the sources the skill lists, and what well-regarded current practice says. A skill's source list is where to start, not where to stop: search past it for newer measured work, since a catalog that was the best available when the skill was written can be overtaken without changing a word.
4. A premise that no longer holds puts the judgment in bucket 2. Rewrite it from the new premise, and say in the commit what changed underneath it.
5. Keep the skill's source list current: add what you used, record what you searched and rejected, and date every row.

## 3. Check whether the skill should still exist

Before editing, check whether another maintained skill now covers the same ground better. It takes one command, so run it every time rather than reasoning that nothing could have replaced this one:

```bash
skills find <topic>   # lists matching skills with install counts; works without a terminal
```

Upstreams publish their own skills, so look hardest at entries from the upstream's own organisation, and read the closest matches rather than judging by name or install count. If one covers the same ground and tracks the newer upstream where this one stopped, retire this one rather than refresh it:

- delete the skill directory in one commit;
- record the retirement where the repo lists its skills, with the date, the replacement and why, so the decision can be re-checked later;
- name anything worth recovering from git history.

When an upstream skill covers only part of this one, usually the API, narrow this one to what it doesn't cover instead of retiring it. Drop what theirs says, point to it, and keep the judgment. Don't take on the upstream author's personal setup or conventions along the way.

## 4. Verify before writing

Test each bucket-1 and bucket-3 claim before it goes into the skill: run the installed tool's `-h`, run the command in a scratch repo, install the new library version in a throwaway project, read the source where the notes are vague. A release note says what changed. It rarely says what that means for a user who followed the old advice, and that consequence is what the skill has to say.

Finding a name in the docs is not verification: run the code. An agent that grepped a library's docs once listed an auth helper as "verified still true", and an agent that imported it found it existed in no release. In the report, mark each claim as run or docs-only, so the reviewer knows which ones to trust.

Run it the way an agent runs it, and run every path the skill prescribes:

- **No terminal.** An agent's shell has no TTY, and tools behave differently there: a CLI that would open a picker for a person fails outright instead. Run the scratch commands from the agent's own shell.
- **The recovery paths too.** Advice of the form "if you already did X, run Y" needs X and then Y in the scratch repo. Testing Y on a fresh setup can pass while Y after X does nothing.
- **The coverage you drop advice for.** Before cutting advice because upstream's help or skill now covers it, run upstream on the case. "The other tool checks that" is a claim like any other.

## 5. Edit

Fix bucket 1 first, then bucket 2, then add bucket 3.

- Correct wrong advice where it stands. A "changes in vX" section appended after advice it contradicts leaves the old text in place for an agent to follow.
- Write skill text that stays true without a date attached. No "now supports", "new in vX", "added in", "removed in" or "as of": describe what is true of the baseline release, and remove such markers where you find them. Release history belongs in the commit and the changelog.
- Leave out an item with no natural home in the skill, rather than wedging a sentence between unrelated sections or adding a section just for it. Add a section only when the concept is substantial, reusable and clearly missing.
- Move every marker from step 1 to what you checked.
- Keep `SKILL.md` within the spec's budget: a body of at most 500 lines and 5,000 tokens. When a section grows, move the detail into `references/<topic>.md` and leave a one-line pointer saying when to read it.
- Keep the frontmatter `description` in the third person with a "Use when" trigger, and update it if the refresh changed what the skill covers.

## 6. Account for every finding

Every finding from step 2 outside bucket 4 ends in exactly one place in the report:

- **Changed** — the edit, the file, and whether its claim was run or docs-only.
- **No skill change needed** — verified, but with no natural home or too narrow to teach. Say why, and link the source.
- **Needs manual authoring** — the change is real, but its details could not be verified (no schema, no docs, no way to run it). Say what is known and where to check later. Don't write it into the skill unverified.

A refresh that finds nothing to change is a successful refresh: report the releases, pages and premises checked, and stop. The report is what the reviewer reads, so it doubles as the pull request body when the repo uses pull requests.

## 7. Validate

Run the repo's own validation, and at least the Agent Skills spec checks ([skill-validator](https://github.com/agent-ecosystem/skill-validator) or the spec's reference validator) and a link checker over the skill. Each check must report success: empty output is a check that did not run.

These check format, not behaviour. For a refresh that rewrites advice, the behavioural check is to run the refreshed skill against the pre-refresh one on prompts that hit the changed advice, as `skill-creator` does with a snapshot of the old version. It costs two agent runs per prompt, so put it to the user as a decision, with the prompts and the cost, rather than skipping it silently. Start from the skill's `evals/` when it has one, add a case for each piece of advice this refresh changed, and save the new cases back there.

Two things keep the comparison honest:

- **Hand each run only the skill file under test, and load no skill through a Skill tool.** An installed copy of the same skill would otherwise load into both runs and erase the difference being measured.
- **Pick prompts where the old advice was wrong or silent.** A case both versions pass shows nothing.

## 8. Commit

One commit per skill, so each refresh can be reviewed and reverted on its own.

Subject: `docs(<skill>): update for <upstream> vA through vB` for a release-driven refresh, `docs(<skill>): refresh for <what changed>` otherwise.

Body: lead with what an agent following the old skill got wrong and what happened when it did, then what was added, then what was dropped and why. For example: "An agent following the old skill set up the plugin without its repository, which fails with 'plugin not found' since 30.5 moved it off Maven Central." Close the issues the refresh settles.

If the repo keeps a `CHANGELOG.md`, add the refresh in the same commit, in the repo's format: one entry per change an installer's agent would notice, saying what it now does differently. Advice that was wrong is a fix, a retired skill is a removal with its replacement, and the evidence stays in the commit.

## Refreshing several skills

Track each skill as its own item, so each refresh shows separately and its own commit closes it, and put the commits on one branch for a single review.

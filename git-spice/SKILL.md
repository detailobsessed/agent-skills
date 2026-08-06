---
name: git-spice
description: Use git-spice to manage stacked branches and pull/merge requests on GitHub, GitLab, Bitbucket, Gitea, Forgejo, or Codeberg. Covers setup, daily workflow, staging rules, submitting, amending, merging, and syncing stacks. Invoke when working with stacked PRs/MRs or whenever the user mentions gs, git-spice, or stacked branches.
---

# git-spice

git-spice is a CLI tool for managing stacks of dependent branches and their corresponding pull/merge requests. It removes the friction of rebasing and updating dependent MRs as you iterate.

**When in doubt, consult the built-in help generously.** Every command and subcommand has detailed help:

```bash
git-spice -h                    # all top-level commands
git-spice stack -h              # stack subcommands
git-spice branch -h             # branch subcommands
git-spice <command> -h          # any command
```

## When to use

- Working on a feature that spans multiple logical commits or MRs
- Keeping a chain of dependent branches in sync after rebases
- Creating, updating, or merging a stack of GitHub, GitLab, Bitbucket, Gitea, Forgejo, or Codeberg MRs/PRs
- Amending commits in the middle of a stack and propagating changes upward
- Any time the user mentions `git-spice`, `gs` (removed alias — see note below), or "stacked branches/PRs"

## Instructions

### 1. Before you start

Run `git-spice -h` to see all available commands. Command names and flags evolve — always verify against the installed version rather than guessing. The help output is concise and authoritative.

> **Note:** The `gs` binary was removed entirely in v0.25.0 (it was renamed in v0.24.0). To keep using the short form, add `alias gs='git-spice'` to your shell config.
>
> This skill is written against **git-spice v0.31.2**. Run `git-spice --version` to check what's installed; behaviour described here as version-gated may not apply to older builds.

### 1a. Experimental commands — enable before use

Several commands documented below are **experiments**. They appear in `-h` output and look
like normal commands, but refuse to run until explicitly enabled:

```text
ERR Command is experimental: git-spice stack (s) merge (m)
ERR Enable the experiment to use it:
ERR   git config spice.experiment.merge true
```

| Command | Experiment flag | Added |
| --- | --- | --- |
| `commit fixup` | `git config spice.experiment.commitFixup true` | v0.18.0 |
| `commit pick` | `git config spice.experiment.commitPick true` | v0.19.0 |
| `branch merge`, `downstack merge`, `stack merge` | `git config spice.experiment.merge true` | v0.30.0 |

Experiments may be incomplete, may change or be removed, and may destroy work — see
<https://abhinav.github.io/git-spice/cli/experiments/>. Add `--global` to the `git config`
call to enable an experiment everywhere rather than per-repo.

**If a documented command fails, check the experiment gate before assuming the flag name is wrong.**

### 2. One-time setup

Initialize git-spice in a repository once:

```bash
git-spice repo init --trunk main --remote origin
```

For GitLab (self-hosted), also set the forge URLs and authenticate:

```bash
git config spice.forge.gitlab.url https://gitlab.example.com
git config spice.forge.gitlab.apiURL https://gitlab.example.com/api/v4
git-spice auth login --forge=gitlab          # prompts for auth method (OAuth, PAT, CLI, etc.)
```

For GitHub (public), authentication works out of the box via `git-spice auth login`. GitHub OAuth requires `read:org` scope (for team-based `--reviewer` resolution) — run `git-spice auth login --refresh` if you authenticated before v0.22.0.

For Bitbucket Cloud (v0.25.0+), repos hosted on `bitbucket.org` need **no** forge configuration — just authenticate via Git Credential Manager (GCM), an app password, or a PAT:

```bash
git-spice auth login --forge=bitbucket
```

> **Do not set `spice.forge.bitbucket.url` for Bitbucket Cloud.** Since v0.31.0 a custom value
> replaces `bitbucket.org` as the host that identifies the Bitbucket forge — set globally, it stops
> `bitbucket.org` repos from matching at all, and any URL other than `bitbucket.org` selects the
> Data Center API. Only set it (per repo) for self-hosted instances.
>
> **Note:** Bitbucket Cloud does not support PR labels, PR assignees, or template enumeration.

#### Self-hosted and additional forges

```bash
# Bitbucket Data Center / Server (v0.31.0+) — per repo, not global
git config spice.forge.kind bitbucket                      # derives instance URL from the remote
git config spice.forge.bitbucket.url https://bb.example.com  # or set it explicitly
git config spice.forge.bitbucket.kind cloud                # override Cloud-vs-DC inference

# Gitea (v0.30.0+)
git config spice.forge.gitea.url https://gitea.example.com

# Forgejo (v0.30.0+) — defaults to Codeberg, so Codeberg needs no config
git config spice.forge.forgejo.url https://forgejo.example.com
```

When the remote URL is rewritten (`url.*.insteadOf`, an SSH alias, or a proxy) git-spice can't detect
the forge. Name it explicitly with `spice.forge.kind` (v0.30.0+), or the `GIT_SPICE_FORGE_KIND`
environment variable for a single command:

```bash
git config spice.forge.kind github        # github | gitlab | bitbucket | gitea | forgejo
```

**v0.26.1 behavior change:** git-spice no longer falls back to Git Credential Manager-managed credentials automatically. If a previously-working setup suddenly prompts for auth, run `git-spice auth login` (and pick the GCM method explicitly if that's what you used before).

**Headless / no system keychain?** Select the secret storage backend explicitly to skip the keychain probe (v0.26.0+): set `spice.secret.backend` via `git config` or the `GIT_SPICE_SECRET_BACKEND` environment variable. Check `git-spice auth login -h` and the docs for valid backend names.

#### Fork mode (v0.28.0+)

To contribute to a repo you don't have write access to, point `--upstream` at the project repo and `--remote` at your fork:

```bash
git-spice repo init --trunk main --upstream upstream --remote origin
```

In fork mode:

- Branch pushes go to the **push** remote (`--remote`, typically your fork)
- Change Requests are opened against the **upstream** remote (`--upstream`)
- `git-spice repo sync` pulls trunk from `upstream`
- Only trunk-based branches get CRs against upstream; stacked branches whose base isn't trunk are still pushed to your fork as part of the stack

**Caveats:**

- GitHub App authentication is **incompatible** with fork mode — use a Personal Access Token instead.
- The repository storage format upgrades when fork mode is enabled, and **older git-spice versions cannot open the repo afterward**. Make sure collaborators are on v0.28.0+ before flipping a shared repo into fork mode.

### 3. Core concepts

- **Branch**: a single node in the stack, backed by a Git branch
- **Stack**: the ordered chain of branches from trunk to the current branch
- **Trunk**: the base branch (usually `main`) — never modified by `git-spice`
- **Submit**: pushes all branches in the stack and creates/updates MRs on the forge

`git-spice` tracks the stack in `.git/spice/` — this metadata is local and not pushed.

### 4. Staging rules — read this carefully

Most git-spice commit commands (`bc`, `cc`, `ca`) accept `-a`/`--all` to auto-stage tracked modified and deleted files — just like `git commit -a`. **Prefer `-a` over manual `git add` for tracked files.**

**`-a` does NOT pick up new untracked files.** You must `git add` new files explicitly before the git-spice command. **`commit fixup` has no `-a` flag** — you must stage changes before running it.

Forgetting to stage new files is the most common source of incomplete commits.

### 5. Daily workflow

#### Create branches in a stack

```bash
# On trunk or any branch — create a branch with all tracked changes
git-spice bc feature-part-1 -a -m "feat: add core feature logic"

# Continue stacking
git-spice bc feature-part-2 -a -m "feat: add API layer"
```

`git-spice bc` creates the branch, commits staged changes, and records the parent relationship.

Additional `branch create` flags:

- `--insert` — insert the new branch between the current branch and its upstack children
- `--below` — create the branch below the current one (between current and its base)
- `--target` / `-t` — specify a different base branch instead of the current one
- `--signoff` — add a `Signed-off-by` trailer (🔧 `spice.commit.signoff`)
- `--no-commit` — create the branch without committing staged changes (🔧 `spice.branchCreate.commit`)

Auto-generated branch names are controlled by 🔧 `spice.branchCreate.prefix` and
🔧 `spice.branchCreate.generatedBranchNameLimit` (default 32 chars, truncated at word boundaries).

#### Add commits to an existing branch

```bash
git-spice cc -a -m "feat: additional work"   # commit to current branch, auto-restacks upstack
git-spice cc -a -m "feat: title" -m "Body paragraph."   # -m repeats for paragraphs (v0.30.0+)
git-spice cc -a -F path/to/message.txt       # read message from a file (v0.26.0+, also on bc/ca)
```

Pass `-F`/`--message-file` instead of `-m` to read the commit message from a file — useful for multi-line or generated messages. Repeating `-m` adds paragraphs, matching `git commit`.

#### Opting out of automatic restacking (v0.31.0+)

`branch create`, `branch edit`, `branch squash`, `commit amend`, `commit create`, `commit fixup`,
`commit pick`, and `commit split` restack upstack branches automatically. Pass `--no-restack` to
skip it — useful when you're about to make several changes and want to restack once at the end:

```bash
git-spice cc -a --no-restack -m "wip"
git-spice cc -a --no-restack -m "wip 2"
git-spice upstack restack                    # restack once, at the end
```

Each command has a matching config option to flip the default (e.g. 🔧 `spice.branchCreate.restack`),
in which case `--restack` opts back in per invocation.

#### Navigate and inspect the stack

```bash
git-spice log short              # visual overview of the stack with MR status
git-spice log short -a           # show ALL tracked branches, not just current stack
git-spice log long               # detailed view with commit hashes and descriptions
git-spice log short --cr-comments  # include review comment resolution counts
git-spice branch diff            # diff between current branch and its base
git-spice up                     # move up one branch toward the tip
git-spice down                   # move down one branch toward trunk
git-spice top                    # jump to the top of the stack
git-spice bottom                 # jump to the bottom (first branch above trunk)
git-spice trunk                  # switch to the trunk branch
```

### 6. Submitting the stack

Push all branches and create MRs on the forge in one command:

```bash
git-spice stack submit --fill --no-draft
```

- `--fill` populates MR title and description from the commit message
- `--no-draft` marks MRs as ready for review immediately
- `--update-only` / `-u` — only update existing MRs, skip creating new ones (see "Amending commits in the stack")

Additional submit flags (available on `stack submit`, `branch submit`, `upstack submit`, `downstack submit`):

- `--reviewer` / `-r` — request reviewers (supports team names on GitHub with `read:org` scope)
- `--assign` / `-a` — assign users to the MR/PR
- `--label` / `-l` — add labels
- `--web` / `-w` — open in browser (`true`, `false`, or `created` for new MRs only)
- `--nav-comment` — control navigation comments (`true`, `false`, `multiple`)
- `--no-verify` — bypass pre-push hooks
- `--no-publish` — push branches without creating MRs/PRs
- `--force` — force push, bypassing safety checks
- `--dry-run` / `-n` — print what would be submitted without doing it

> **Watch the `-a` collision.** On `bc`/`cc`/`ca`, `-a` means `--all` (stage tracked changes).
> On the `submit` commands, `-a` means `--assign`. Spell out the long flag on submit.

These flags can also be set as defaults via `git config`:

```bash
git config spice.submit.reviewers "alice,bob"
git config spice.submit.assignees "alice"
git config spice.submit.labels "needs-review"     # v0.30.0 renamed spice.submit.label
git config spice.submit.labels.addWhen create     # v0.30.0 renamed spice.submit.label.addWhen
git config spice.submit.draft true
```

The singular `spice.submit.label` / `spice.submit.label.addWhen` forms were deprecated in v0.30.0 and
will be removed — migrate to the plural forms.

To submit only the current branch's MR:

```bash
git-spice branch submit --fill --no-draft
```

### 7. Merging the stack

> **Experimental (v0.30.0+).** Enable once before use, or every merge command fails:
>
> ```bash
> git config spice.experiment.merge true
> ```

Merge the entire stack bottom-up into trunk in one command:

```bash
git-spice stack merge                  # merge current branch's full stack
git-spice stack merge --branch B       # merge a different branch's stack
git-spice stack merge --branch A --branch D   # merge independent stacks (repeatable)
git-spice stack merge --fail-fast      # stop on first failure (default: skip blocked + children)
```

Branches merge bottom-up starting with those stacked on trunk. After each branch
merges, its upstack branches are restacked and resubmitted; when they become
ready, they merge in turn. A branch is "ready" when the forge reports it
mergeable (configurable via `spice.merge.ready.command`). If a branch is blocked
or times out, it and its upstack children are skipped unless `--fail-fast` is set.

Flags:

- `--method` — `merge`, `squash`, or `rebase` (🔧 `spice.merge.method`)
- `--ready-timeout` — max wait for merge readiness per branch (default 30m; 0 = check once) (🔧 `spice.merge.ready.timeout`)
- `--merge-timeout` — max wait for merge completion after requesting (default 2m) (🔧 `spice.merge.timeout`)
- `--fail-fast` — stop scheduling remaining merges after first failure
- `--branch` — branches whose stacks to merge; repeatable for independent stacks

Escape hatches for forges or policies the built-in API path doesn't cover:

- 🔧 `spice.merge.ready.command` — custom readiness check instead of asking the forge
- 🔧 `spice.merge.command` — custom merge command instead of the forge merge API

**v0.31.0 renamed two config options** — `spice.merge.readyTimeout` → `spice.merge.ready.timeout`
and `spice.merge.mergeTimeout` → `spice.merge.timeout`. The `--no-branch-check` flag was removed
from `downstack merge` and `stack merge`.

This is a sequential bottom-up merge, not a parallel merge queue (Aviator/Mergify
style). For solo use it's sufficient — run it when the stack is ready and it
walks up the chain. There's also `git-spice branch merge` for a single branch
and `git-spice downstack merge` for a branch and those below it.

### 8. Amending commits in the stack

To change the current branch's commit (fix a bug, address review feedback):

```bash
git-spice ca -a --no-edit                   # stage tracked changes + amend in one step
```

Then push the updated stack:

```bash
git-spice stack submit --update-only
```

`--update-only` skips creating new MRs and only updates existing ones. It will force-push rebased branches as needed.

To amend a commit that is **not** at the top of the stack, use `commit fixup` — it applies staged changes to any downstack commit without switching branches:

```bash
git config spice.experiment.commitFixup true  # experimental — enable once
git add <files>                             # commit fixup has no -a flag — must stage manually
git-spice commit fixup <commit-hash>        # amend a specific downstack commit in-place
git-spice commit fixup --edit <hash>        # also edit the target's commit message (v0.29.0+)
git-spice stack submit --update-only        # propagates rebase upward automatically
```

If no commit hash is given, an interactive prompt lets you pick the target commit. Requires Git 2.45+.

### 9. Syncing after merges

After MRs are merged on the forge (bottom-up), sync locally to clean up:

```bash
git-spice repo sync --restack               # pulls trunk, removes merged branches, restacks remaining
git-spice stack submit --update-only        # updates MR targets on the forge (if branches remain)
```

#### v0.29.0 changed what "restack" means here — read this

`repo sync`, `branch delete`, and `branch onto` used to rebase the branches directly above an
affected branch, leaving everything higher up alone. That was inconsistent, so **the default is now
to retarget metadata only and rebase nothing.** All three take a three-valued `--restack`:

| Value | Effect |
| --- | --- |
| `none` | Retarget metadata only — **the default** |
| `aboves` | Rebase only the direct upstack of affected branches (the pre-v0.29 behaviour) |
| `upstack` | Rebase affected branches and their entire upstack — what bare `--restack` means |

Defaults are configurable per command: 🔧 `spice.repoSync.restack`, 🔧 `spice.branchDelete.restack`,
🔧 `spice.branchOnto.restack`.

Practical consequence: after a plain `git-spice repo sync`, remaining branches point at the right
base but are **not** rebased onto it. Pass `--restack` (or run `git-spice stack restack`) before
submitting, or the stack submits stale.

### 10. Other useful commands

#### Tracking and switching

```bash
git-spice branch track <name>               # start tracking an existing branch
git-spice branch track <name> --base <br>   # track with explicit base branch
git-spice branch untrack <name>             # stop tracking (keeps the git branch)
git-spice downstack track                   # track all untracked branches below current
git-spice branch checkout                   # interactive branch switcher (prompts from tracked branches)
```

#### Restructuring branches

```bash
git-spice branch onto main                  # re-parent a branch; upstack is retargeted, not rebased
git-spice branch onto main --restack        # ...and rebase the upstack too (see §9)
git-spice upstack onto main                 # re-parent a branch AND its upstack onto trunk
git-spice branch fold                       # merge a branch's commits into its base branch
git-spice branch split                      # split a branch at specific commits
git-spice branch squash                     # squash all commits in a branch into one
git-spice branch edit                       # interactive rebase scoped to this branch's commits
git-spice stack edit                        # reorder branches in a stack interactively
git-spice downstack edit                    # reorder branches below current
```

#### Commit manipulation

```bash
git-spice commit split                      # interactively split the current commit into multiple
git-spice commit pick <commit>              # stack-aware cherry-pick (experimental: spice.experiment.commitPick)
```

#### Cleanup and sync

```bash
git-spice branch delete <name>              # delete a branch and its stack tracking
git-spice branch delete <name> --force      # delete even with unmerged changes
git-spice branch rename <old> <new>         # rename a branch
git-spice stack delete --force              # delete all branches in the current stack
git-spice upstack delete --force            # delete all branches above the current one
git-spice repo sync                         # pull trunk and update stack metadata (no restack)
git-spice repo sync --restack               # pull trunk + rebase entire stack on top
git-spice repo init --reset                 # discard all tracking data and start fresh
```

#### Restacking

```bash
git-spice stack restack                     # rebase current stack without pulling trunk
git-spice branch restack                    # rebase just the current branch onto its base
git-spice upstack restack                   # restack current branch and everything above
git-spice repo restack                      # restack ALL tracked branches in the repo
```

#### Conflict resolution

```bash
git-spice rebase continue                   # continue after resolving conflicts
git-spice rebase abort                      # abort an interrupted operation
```

#### Scoped submit variants

```bash
git-spice upstack submit                    # submit current branch and all above it
git-spice downstack submit                  # submit current branch and all below it
```

### 11. Anti-patterns

- **Forgetting to stage changes** — use `-a` to auto-stage tracked files, or `git add` for new untracked files. Without either, commits will be empty or incomplete.
- **Manually rebasing instead of using git-spice restack commands** — git-spice tracks branch relationships in `.git/spice/`; a manual `git rebase` does not update this metadata.
- **Guessing flag names** — run `git-spice <command> -h` before using any unfamiliar flag. git-spice's CLI is well-documented and the help is always accurate.
- **Treating an experiment error as a bad invocation** — `merge`, `commit fixup`, and `commit pick` show up in `-h` but refuse to run until enabled. Read the error: it names the exact `git config` line. See §1a.
- **Assuming `repo sync` rebased the stack** — since v0.29.0 it only retargets metadata by default. Pass `--restack`, or the next submit pushes branches that were never rebased onto the new trunk.
- **Setting `spice.forge.bitbucket.url` globally** — it replaces `bitbucket.org` as the identifying host, so `bitbucket.org` repos stop matching the Bitbucket forge. Set it per repo, for self-hosted instances only.

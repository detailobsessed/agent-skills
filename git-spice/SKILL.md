---
name: git-spice
description: Use git-spice to manage stacked branches and pull/merge requests on GitHub, GitLab, or Bitbucket Cloud. Covers setup, daily workflow, staging rules, submitting, amending, and syncing stacks. Invoke when working with stacked PRs/MRs or whenever the user mentions gs, git-spice, or stacked branches.
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
- Creating, updating, or merging a stack of GitLab, GitHub, or Bitbucket Cloud MRs/PRs
- Amending commits in the middle of a stack and propagating changes upward
- Any time the user mentions `git-spice`, `gs` (removed alias — see note below), or "stacked branches/PRs"

## Instructions

### 1. Before you start

Run `git-spice -h` to see all available commands. Command names and flags evolve — always verify against the installed version rather than guessing. The help output is concise and authoritative.

> **Note:** The `gs` binary was removed entirely in v0.25.0 (it was renamed in v0.24.0). To keep using the short form, add `alias gs='git-spice'` to your shell config.

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

For Bitbucket Cloud (v0.25.0+), authenticate via Git Credential Manager (GCM) or app passwords:

```bash
git config spice.forge.bitbucket.url https://bitbucket.org
git-spice auth login --forge=bitbucket
```

> **Note:** Bitbucket Cloud does not support PR labels, PR assignees, or template enumeration.

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

#### Add commits to an existing branch

```bash
git-spice cc -a -m "feat: additional work"   # commit to current branch, auto-restacks upstack
git-spice cc -a -F path/to/message.txt       # read message from a file (v0.26.0+, also on bc/ca)
```

Pass `-F`/`--message-file` instead of `-m` to read the commit message from a file — useful for multi-line or generated messages.

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

These flags can also be set as defaults via `git config`:

```bash
git config spice.submit.reviewers "alice,bob"
git config spice.submit.assignees "alice"
git config spice.submit.draft true
```

To submit only the current branch's MR:

```bash
git-spice branch submit --fill --no-draft
```

### 7. Amending commits in the stack

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
git add <files>                             # commit fixup has no -a flag — must stage manually
git-spice commit fixup <commit-hash>        # amend a specific downstack commit in-place
git-spice stack submit --update-only        # propagates rebase upward automatically
```

If no commit hash is given, an interactive prompt lets you pick the target commit. Requires Git 2.45+.

### 8. Syncing after merges

After MRs are merged on the forge (bottom-up), sync locally to clean up:

```bash
git-spice repo sync --restack               # pulls trunk, removes merged branches, restacks remaining
git-spice stack submit --update-only        # updates MR targets on the forge (if branches remain)
```

### 9. Other useful commands

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
git-spice branch onto main                  # re-parent a branch onto trunk (upstack stays on old base)
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
git-spice commit pick <commit>              # stack-aware cherry-pick
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

### 10. Anti-patterns

- **Forgetting to stage changes** — use `-a` to auto-stage tracked files, or `git add` for new untracked files. Without either, commits will be empty or incomplete.
- **Manually rebasing instead of using git-spice restack commands** — git-spice tracks branch relationships in `.git/spice/`; a manual `git rebase` does not update this metadata.
- **Guessing flag names** — run `git-spice <command> -h` before using any unfamiliar flag. git-spice's CLI is well-documented and the help is always accurate.

---
name: git-spice
description: Drives git-spice, the stacked-branch CLI, from an agent without the traps that the built-in help does not warn about — prompts an agent cannot answer, experiment gates, staging that skips new files, restacks that do not happen, and GitHub native stacks. Use when creating, committing to, submitting, syncing or merging a stack of branches and pull or merge requests with git-spice, or whenever the user mentions gs, git-spice or stacked branches.
license: MIT
---

# git-spice

git-spice manages a stack of dependent branches and their change requests (CRs: pull or merge requests) on GitHub, GitLab, Bitbucket, Gitea, Forgejo, Codeberg and Azure DevOps. It records each branch's base, so it can restack the branches above one you changed and update all their CRs at once.

This skill holds what an agent gets wrong when driving git-spice. For commands and flags, the installed binary is the authority:

- `git-spice <command> -h` documents every flag, its config key (🔧) and its default for the version you have.
- The docs are at <https://abhinav.github.io/git-spice/>, and <https://abhinav.github.io/git-spice/llms.txt> indexes them for fetching page by page.

Written against git-spice v0.33.0, the latest at the time of writing (2026-11-15). Check the installed version with `git-spice --version`.

## Run it without prompts

- **Call the binary `git-spice`.** The `gs` binary no longer exists. A user who types `gs` has a shell alias for it.
- **Name every branch, base and commit yourself, and pass `--no-prompt`.** Left out, git-spice would open an interactive picker. Without a terminal it fails instead ("cannot proceed without a branch name: not allowed to prompt for input"), and `--no-prompt` makes that hold under a terminal too, so a call never waits on a picker nobody sees.
- **Always supply the commit message.** With `--no-prompt` and no `-m`, git-spice opens no editor and stops with "Aborting commit due to empty commit message". Repeat `-m` for more paragraphs, or pass a file with `-F <file>` for a long message.
- **Read stack state as JSON.** `git-spice ls --json` (one object per tracked branch, on stdout) beats parsing the tree drawing, which goes to stderr.

## Stage before committing

`branch create` (`bc`), `commit create` (`cc`) and `commit amend` (`ca`) take `-a` to stage tracked changes, like `git commit -a`. **`-a` skips new files**: `git add` them first, or the commit goes out without them. `commit fixup` has no `-a` at all, so stage its changes yourself.

## Experiments look like commands but refuse to run

`commit fixup`, `commit pick`, and the merge commands (`branch merge`, `downstack merge`, `stack merge`) appear in `-h` like any other command. Until enabled, each fails:

```text
ERR Command is experimental: git-spice stack (s) merge (m)
ERR Enable the experiment to use it:
ERR   git config spice.experiment.merge true
```

The error names the exact `git config` line (`spice.experiment.commitFixup`, `commitPick`, `merge`). Experiments can change or lose work, so enable one only when the user wants that command, and per repo unless they say otherwise. A documented command that fails is an experiment gate before it is a wrong flag.

## Restacking: what happens on its own and what doesn't

**Commands that change one branch restack the branches above it.** `branch create`, `commit create`, `commit amend`, `commit fixup`, `branch squash` and the like rebase the upstack for you. Pass `--no-restack` to batch several changes, then `git-spice upstack restack` once.

**Commands that move or remove a base only retarget, by default.** `repo sync`, `branch delete` and `branch onto` take `--restack=none|aboves|upstack`, and the default is `none`: the branches above point at their new base but are not rebased onto it. Pass `--restack` on the sync itself: `git-spice repo sync --restack` (bare `--restack` means `upstack`). It restacks only the branches above the ones that sync deletes, so running it again after a plain sync deletes nothing and rebases nothing. If the sync already ran without it, run `git-spice stack restack` before submitting. Otherwise the submit pushes branches that were never rebased onto the new trunk.

**Never restack with raw git.** `git rebase`, `git branch -D` or `git cherry-pick` change branches without updating git-spice's records of each branch's base. Use `branch restack`, `upstack restack`, `branch onto`, `branch delete` and `commit pick` instead. After a raw rebase onto a new base, git-spice still records the old one, so its next restack drags the old base's commits back in. Check `git-spice ls --json`, and fix the record with `git-spice branch onto <new-base>`. A branch git-spice has never seen needs `git-spice branch track <name> --base <base>`.

## Submitting

- `git-spice stack submit --fill` pushes every branch in the stack and creates or updates its CRs, taking titles and bodies from the commit messages. `branch submit`, `upstack submit` and `downstack submit` cover less of the stack.
- **On the submit commands, `-a` means `--assign`**, not `--all`. Write long flags on submit.
- After amending, `git-spice stack submit --update-only` updates the existing CRs and opens no new ones.
- `--no-publish` pushes branches without opening CRs. New CRs open as drafts or ready per `--draft` / `--no-draft` (🔧 `spice.submit.draft`).

## Merging

The merge commands merge bottom-up: each branch merges once the forge reports it ready, then git-spice restacks and resubmits the branches above, and so on up the stack. A blocked branch and its upstack are skipped unless `--fail-fast` is set. Readiness waits up to 30 minutes per branch by default (`--ready-timeout`).

**On GitHub, submitted stacks become native GitHub stacks**, and the merge commands merge an eligible run of them atomically, with no restack in between. Native stacks have limits that a local stack does not:

- They must be linear. For a stack that forks, git-spice registers one path and warns about the branches it left out.
- Every head branch must live in the repository receiving the PRs, so a stack pushed to a fork is not one.
- A queued PR, or one with auto-merge on, can stop GitHub from restructuring the stack; git-spice warns when it cannot update it.

What cannot merge natively merges one CR at a time as before. Set `spice.forge.github.stacks` to `false` to turn native stacks off.

## Forge setup traps

- **Bitbucket Cloud needs no URL.** `spice.forge.bitbucket.url` set to anything else selects the self-hosted Data Center API, and set globally it stops `bitbucket.org` repos from matching at all. Set it per repo, for a self-hosted instance only.
- **A rewritten remote URL** (`url.*.insteadOf`, an SSH host alias, a proxy) hides the forge. Name it with `git config spice.forge.kind <github|gitlab|bitbucket|gitea|forgejo|azuredevops>`, or `GIT_SPICE_FORGE_KIND` for one command.
- **Fork mode** (`git-spice repo init --upstream <project-remote> --remote <your-fork>`) opens CRs only for branches based directly on trunk. Branches stacked above them are pushed to the fork without CRs, so a full stack of CRs still needs push access upstream. GitHub App authentication does not work in fork mode: use a token or OAuth.
- **A machine with no keychain** (CI, a container): set `spice.secret.backend` or `GIT_SPICE_SECRET_BACKEND`, so `auth login` doesn't probe for one. `git-spice auth login -h` lists the backends.

## Daily loop

```bash
git add new_file.py                                   # -a skips new files
git-spice branch create --no-prompt feat-parser -a -m "feat: parse the config"
git-spice branch create --no-prompt feat-cli -a -m "feat: expose the parser on the CLI"
git-spice stack submit --no-prompt --fill

# review feedback on the lower branch
git-spice down --no-prompt
git-spice commit amend --no-prompt -a --no-edit      # restacks feat-cli on top
git-spice stack submit --no-prompt --update-only

# after the lower PR merges
git-spice repo sync --no-prompt --restack             # pull trunk, drop merged branches, rebase the rest
git-spice stack submit --no-prompt --update-only
```

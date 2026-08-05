# git-spice skill

An [Agent Skill](https://agentskills.io) for working effectively with [git-spice](https://abhinav.github.io/git-spice/), the stacked-branch CLI for GitHub, GitLab, Bitbucket, Gitea, Forgejo, and Codeberg.

Written against **git-spice v0.31.2**.

> **v0.25.0 breaking change:** The `gs` binary has been fully removed. Use `git-spice` directly or add `alias gs='git-spice'` to your shell config.
>
> **v0.29.0 behaviour change:** `repo sync`, `branch delete`, and `branch onto` no longer rebase upstack branches by default — they retarget metadata only. `--restack` is now three-valued (`none`, `aboves`, `upstack`).

Covers setup, staging rules, daily workflows, submitting, amending, merging, syncing, and a comprehensive command reference across all supported forges.

## What's in the skill

The skill covers 11 areas:

1. **Before you start** — consult `git-spice -h` generously
2. **Experimental commands** — `merge`, `commit fixup`, and `commit pick` are gated behind `spice.experiment.*` config and fail until enabled
3. **One-time setup** — `git-spice repo init`, forge config for six forges, auth, fork-mode workflows (v0.28.0+)
4. **Core concepts** — branch, stack, trunk, submit
5. **Staging rules** — the most common source of mistakes
6. **Daily workflow** — creating branches, adding commits, opting out of auto-restack, navigating the stack
7. **Submitting the stack** — `git-spice stack submit` flags and config defaults
8. **Merging the stack** — the local merge queue (`stack merge`, `branch merge`, `downstack merge`)
9. **Amending commits** — mid-stack amendments with `commit fixup` and propagation
10. **Syncing after merges** — `repo sync` and the v0.29.0 restack semantics
11. **Other useful commands and anti-patterns** — tracking, restructuring, restacking, conflict resolution

## Install

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill git-spice
```

## License

MIT

# git-spice skill

An [Agent Skill](https://agentskills.io) for working effectively with [git-spice](https://abhinav.github.io/git-spice/), the stacked-branch CLI for GitHub, GitLab, and Bitbucket Cloud.

> **v0.25.0 breaking change:** The `gs` binary has been fully removed. Use `git-spice` directly or add `alias gs='git-spice'` to your shell config.

Covers setup, staging rules, daily workflows, submitting, amending, syncing, and a comprehensive command reference for GitHub, GitLab, and Bitbucket Cloud forges.

## What's in the skill

The skill covers 10 areas:

1. **Before you start** — consult `git-spice -h` generously
2. **One-time setup** — `git-spice repo init`, forge config, auth
3. **Core concepts** — branch, stack, trunk, submit
4. **Staging rules** — the most common source of mistakes
5. **Daily workflow** — creating branches, adding commits, navigating the stack
6. **Submitting the stack** — `git-spice stack submit` flags and config defaults
7. **Amending commits** — mid-stack amendments with `commit fixup` and propagation
8. **Syncing after merges** — `repo sync --restack` cleanup
9. **Other useful commands** — tracking, restructuring, restacking, conflict resolution
10. **Anti-patterns** — staging mistakes, manual rebase risks

## Install

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill git-spice
```

## License

MIT

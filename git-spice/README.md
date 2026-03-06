# git-spice skill

An [Agent Skill](https://agentskills.io) for working effectively with [git-spice](https://abhinav.github.io/git-spice/), the stacked-branch CLI for GitLab and GitHub.

> **v0.24.0 breaking change:** The binary was renamed from `gs` to `git-spice`. This skill has been updated accordingly. Add `alias gs='git-spice'` to your shell config if you prefer the short form.

Distilled from real-world use with stacked MR workflows on self-hosted GitLab, including quirks around staging, MR descriptions, issue closing, and bottom-up merging.

## What's in the skill

The skill covers 11 areas:

1. **Before you start** — consult `git-spice -h` generously
2. **One-time setup** — `git-spice repo init`, GitLab forge config, auth
3. **Core concepts** — branch, stack, trunk, submit
4. **Staging rules** — the most common source of mistakes
5. **Daily workflow** — creating branches, navigating the stack
6. **Submitting the stack** — `git-spice stack submit` flags
7. **MR descriptions and issue closing** — why `git-spice bs --body` breaks and what to use instead
8. **Amending commits** — mid-stack amendments and propagation
9. **Merging a stack** — bottom-up order, 405 errors, `glab mr merge` pitfalls
10. **Other useful commands** — `onto`, `delete`, `rename`, `restack`
11. **Anti-patterns** — the most common mistakes and their consequences

## Install

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill git-spice
```

## License

MIT

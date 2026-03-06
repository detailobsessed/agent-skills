# wise-mcp

[![Agent Skill](https://img.shields.io/badge/Agent_Skill-compatible-blue?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTUtMTAtNXoiLz48cGF0aCBkPSJNMiAxN2wxMCA1IDEwLTUiLz48cGF0aCBkPSJNMiAxMmwxMCA1IDEwLTUiLz48L3N2Zz4=)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastMCP](https://img.shields.io/badge/FastMCP-gofastmcp.com-purple)](https://gofastmcp.com)
[![Arcade Patterns](https://img.shields.io/badge/Arcade-52_patterns-orange)](https://www.arcade.dev/patterns)

An [Agent Skill](https://agentskills.io) for building high-quality MCP servers with [FastMCP](https://gofastmcp.com).

Combines FastMCP framework guidance with battle-tested design patterns from [Arcade](https://www.arcade.dev/patterns) to help AI agents build MCP servers that are well-structured, secure, and optimized for LLM consumption.

## What's in the skill

The skill covers 11 areas of MCP server development:

1. **Before you start** — always fetch latest docs
2. **Guiding principles** — machine experience, tool DAGs, error-guided recovery, security boundaries
3. **Tool design** — classification, descriptions, input constraints, defaults, identifiers
4. **Resources & templates** — when to use, URI design, discoverability
5. **Prompts** — when and how to use reusable message templates
6. **Context & state** — dependency injection, logging, progress, session state
7. **Tool output** — response shaping, token efficiency, pagination, next-action hints
8. **Error handling** — recovery-oriented errors, classification, ambiguity handling
9. **Server composition** — mounting, providers, transforms, abstraction patterns
10. **Authentication & security** — credential handling, authorization, audit, boundaries
11. **Anti-patterns** — common mistakes that degrade agent effectiveness

## Install

```bash
npx skills add https://github.com/detailobsessed/agent-skills --skill wise-mcp
```

## Development

This project uses [prek](https://prek.j178.dev) for pre-commit hooks and [uv](https://docs.astral.sh/uv/) for Python tooling.

```bash
# Install pre-commit hooks
prek install

# Run all checks
prek run --all-files
```

Checks include: trailing whitespace, EOF fixer, large file detection, case conflicts, merge conflicts, TOML/YAML validation, mixed line endings, [typos](https://github.com/crate-ci/typos) spell checking, and [lychee](https://lychee.cli.rs) link validation.

## License

MIT

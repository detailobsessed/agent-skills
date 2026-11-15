# wise-mcp

[![Agent Skill](https://img.shields.io/badge/Agent_Skill-compatible-blue?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTUtMTAtNXoiLz48cGF0aCBkPSJNMiAxN2wxMCA1IDEwLTUiLz48cGF0aCBkPSJNMiAxMmwxMCA1IDEwLTUiLz48L3N2Zz4=)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastMCP](https://img.shields.io/badge/FastMCP-gofastmcp.com-purple)](https://gofastmcp.com)
[![Arcade Patterns](https://img.shields.io/badge/Arcade-54_patterns-orange)](https://www.arcade.dev/patterns)

An [Agent Skill](https://agentskills.io) for building high-quality MCP servers with [FastMCP](https://gofastmcp.com).

The design half of building an MCP server: what makes tools, outputs, errors, state and auth work for the agent calling them, drawn from the best current practice we can find, listed under [Sources](#sources). It leaves the FastMCP API to FastMCP's own `fastmcp-server` skill and docs, which track every release.

Written against **FastMCP 4.2.0** and **MCP spec 2026-07-28**, the latest at the time of writing.

## Sources

The skill's advice is ours, synthesised from these. Measured evidence outranks a practitioner's catalog where they disagree. Each refresh re-reads every row, then searches for newer work worth adding (`refresh-skill`, step 2c).

| Source | Kind | What the skill takes from it | Checked |
| --- | --- | --- | --- |
| [MCP spec 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog) | protocol | stateless requests, input-required results, sampling deprecated, deterministic tool order | 2026-11-15 |
| [MCP client best practices](https://modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices) | protocol docs | clients own tool discovery, code mode needs output schemas | 2026-11-15 |
| [Claude Code MCP docs](https://code.claude.com/docs/en/mcp), [Copilot CLI tool search](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/tool-search), [Cursor](https://cursor.com/blog/dynamic-context-discovery), [VS Code tools](https://code.visualstudio.com/docs/agents/run/tools) | client docs | which clients defer tool loading, the 4,096-character cut-off, the 128-tool cap | 2026-11-15 |
| [MCP tool-description study](https://arxiv.org/abs/2602.14878) (856 tools, benchmarked) | measured | the cost of padded descriptions, examples not paying off, results varying by model | 2026-11-15 |
| [Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | measured, vendor | consolidated tools, readable identifiers, concise/detailed responses, namespacing varies by model, evaluate | 2026-11-15 |
| [AWS: MCP tool design tradeoffs](https://aws.amazon.com/blogs/machine-learning/mcp-tool-design-practical-approaches-and-tradeoffs/) | worked comparison, vendor | bloat vs. confusion, schema and defaults, lookup tools, server-side interpretation, about eight parameters | 2026-11-15 |
| [Arcade patterns](https://www.arcade.dev/patterns) (54) and [How to Evaluate MCP Tools](https://www.arcade.dev/blog/evaluate-mcp-tools/) | practitioner catalog | the pattern vocabulary behind the `(see: NAME)` tags, fuzzy-match bands, definition-only evaluation | 2026-11-15 |
| [FastMCP 4.2.0](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.0), run in a throwaway project | release | the APIs the advice names, each imported and called | 2026-11-15 |

Searched and not adopted: [agentpatterns.ai](https://agentpatterns.ai/tool-engineering/) covers harnesses, hooks and skills more than server design, and does not show its evidence.

## What's in the skill

1. **Guiding principles** — machine experience, tool DAGs, error-guided recovery, security boundaries
2. **Tool design** — classification, descriptions for deferring clients, input constraints, testing definitions
3. **Execution model** — threads, background tasks, transactions, timeouts
4. **State across calls** — handles and user-keyed state on a stateless protocol
5. **Asking the user** — when to ask, re-entrant tools, why not sampling
6. **Resources, prompts and apps** — which primitive for which job
7. **Tool output** — shaping, size bounds, next-action hints
8. **Errors** — recovery text, classification, returning vs. raising, ambiguity
9. **Composition and catalog size** — design principles, when hiding tools behind search pays
10. **Authentication and security** — secrets, per-tool gates, token binding, audit
11. **Anti-patterns**

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

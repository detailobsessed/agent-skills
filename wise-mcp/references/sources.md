# Sources

The skill's advice is ours, synthesised from these. Measured evidence outranks a practitioner's catalog where they disagree. Cite a row when a user asks where a piece of advice comes from. Each refresh re-reads every row, then searches for newer work worth adding.

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

# FastMCP 4 (prerelease) — what changes

FastMCP 4 rebuilds on MCP Python SDK v2 and targets the `2026-07-28` protocol, which is
**sessionless**: every request stands alone, there is no live connection to push work down, and one
deployment serves both modern and handshake-era clients via per-connection negotiation.

Most 3.x servers upgrade untouched. FastMCP absorbs the SDK's churn (protocol types moved to
`mcp_types`, model fields renamed camelCase → snake_case in Python — the wire format is unchanged).
What it can't absorb is the protocol's own direction.

**Before writing 4.x code, fetch <https://gofastmcp.com/getting-started/upgrading/from-fastmcp-3>.**
It ships a copy-paste audit prompt listing every removed import and method. Don't reconstruct the
list from memory — this section is a map, not the territory.

## The removals that reshape guidance in this skill

| Removed | Why | What to do instead |
| --- | --- | --- |
| `ctx.sample()`, `ctx.sample_step()`, `ctx.list_roots()` | Need a live connection back to the client | Call an LLM directly from the server — or stay on 3.x if borrowing the caller's model *is* the product |
| `import_server()` | Superseded by live composition | `mount()` — but it runs the child's lifespan and middleware, which `import_server` skipped |
| Session-scoped `ctx` state | No session on the modern protocol | `UserSession` (one bucket per authenticated user) or `SessionId` (many buckets, id passed as a tool argument) |
| `FastMCP.as_proxy()`, `mount(prefix=...)`, `add_tool_transformation()`, `remove_tool()` | API consolidation | See the upgrade guide; `remove_tool`'s replacement raises `KeyError` where it raised `NotFoundError` |
| `PromptToolMiddleware`, `ResourceToolMiddleware`, `fastmcp.server.tasks`, `fastmcp.server.proxy`, `fastmcp.server.openapi` | 3.x shims deleted | Transforms; the `fastmcp-tasks` package; current import paths |

## What's new and worth designing toward

- **Session state without sessions** — `UserSession` is injected like `Context` and never appears in
  the input schema; `SessionId` does appear, and FastMCP writes the parameter description that
  teaches the agent to obtain an id via `create_session` and pass it back. `UserSession` requires
  authentication — there's no user to key on otherwise. This is the IDENTITY_ANCHOR and
  SESSION_CONTEXT patterns, re-mechanized.
- **Background tasks** — now the `io.modelcontextprotocol/tasks` protocol extension (SEP-2663) in
  the `fastmcp-tasks` package. `@mcp.tool(task=True)` is still the whole authoring surface.
- **Interactive tools** — tools ask follow-up questions across complete request/response rounds, and
  shared request-state keys let any replica resume the next round after load balancing.
- **Argument completion** — a `@mcp.completion` handler answers autocomplete for prompt arguments
  and resource-template parameters, narrowing suggestions using arguments already supplied.
- **Enterprise auth** — server-side identity assertion (SEP-990), `require_roles`, incremental
  step-up authorization challenges (SEP-2350), routable transport headers for gateways (SEP-2243).
- **Server extensions** — `add_extension()` makes capability-negotiated protocol features a
  supported plugin surface instead of core surgery.

## Installing the prerelease

`fastmcp` is a thin wrapper depending on `fastmcp-slim` at the same version. pip infers the
prerelease; uv needs the transitive dependency constrained by name:

```toml
[project]
dependencies = ["fastmcp==4.0.0b1"]

[tool.uv]
constraint-dependencies = ["fastmcp-slim==4.0.0b1"]
```

Naming just these keeps the rest of the graph on stable releases, where `--prerelease allow` would
opt everything in. Do **not** pin `mcp` to a prerelease — it ships stable now, and a prerelease
won't satisfy FastMCP's `mcp>=2.0.0` requirement.

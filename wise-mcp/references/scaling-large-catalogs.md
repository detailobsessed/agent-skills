# Scaling large tool catalogs

Implementation detail for the three server-side mechanisms that keep a large tool catalog usable:
search transforms, the manual visibility gateway, and Code Mode.

**Read `SKILL.md` §9 first** — it covers when *not* to reach for any of this. Most clients defer
tool loading themselves, so a server-side discovery layer often adds round-trips without saving
context. These mechanisms earn their place on genuinely large catalogs (hundreds of tools),
dynamic catalogs, gateways aggregating many backends, or clients you don't control.

## Contents

- [Search transforms (preferred)](#search-transforms-preferred)
- [Visibility + gateway (manual alternative)](#visibility--gateway-manual-alternative)
- [Code Mode](#code-mode)

## Search transforms (preferred)

Use `BM25SearchTransform` or `RegexSearchTransform` to replace `list_tools()` with a minimal
interface. Pin the tools agents need immediately with `always_visible`; everything else is
discoverable on demand.

```python
from fastmcp.server.transforms.search import BM25SearchTransform

# After mounting all sub-servers:
mcp.add_transform(BM25SearchTransform(
    max_results=8,
    always_visible=["set_tenant", "search_plans", "run_plan", "wait_for_execution"],
))
# list_tools() now returns: always_visible tools + search_tools + call_tool
```

`search_tools` returns ranked results with full parameter schemas — the same JSON shape as
`list_tools`, so the agent can construct a valid call without a second round-trip.
`call_tool(name=..., arguments={...})` invokes any discovered tool. Hidden tools remain **directly
callable** — the transform controls discovery, not access.

The query parameter differs by strategy:

| Transform | Parameter | Matching |
| --- | --- | --- |
| `BM25SearchTransform` | `search_tools(query=...)` | Relevance-ranked; builds an index |
| `RegexSearchTransform` | `search_tools(pattern=...)` | Case-insensitive `re.search`; zero overhead |

Regex is the cheaper default when the agent roughly knows what it's looking for. Both search across
tool names, descriptions, parameter names, and parameter descriptions — so a search for `"email"`
matches a tool named `send_email`, one with "email" in its description, *and* one with an
`email_address` parameter.

This approach is client-safe: `always_visible` tools are always in `list_tools` regardless of
whether the client supports `ToolListChangedNotification`.

## Visibility + gateway (manual alternative)

For cases where you need category-based opt-in rather than search:

```python
from fastmcp.server.transforms import Visibility

@server.tool(tags={"gateway"})
def get_capabilities() -> dict: ...          # always visible

@server.tool(tags={"gateway"})
async def enable_tools(category: str, ctx: Context) -> dict: ...  # always visible

@server.tool(tags={"plans"})
def search_plans(...) -> dict: ...           # hidden until activated

# Hide all tools, then re-show gateway
mcp.add_transform(Visibility(False, components={"tool"}))
mcp.add_transform(Visibility(True, tags={"gateway"}, components={"tool"}))
```

**Caution:** `match_all=True` short-circuits the `components` filter — always use two separate
transforms as shown, not a single `Visibility(False, match_all=True, components={"tool"})`.

**Client compatibility note:** `ToolListChangedNotification` (sent after `enable_components()`) is
optional and many clients don't implement it. If you can't guarantee client support, return
activated tool schemas directly from `enable_tools()` so agents have immediate usability without
waiting for a tool list refresh. This is the main reason to prefer the search transform approach —
`always_visible` avoids the problem entirely.

## Code Mode

Search transforms fix one scaling problem: the catalog is too big to send. They don't fix the
other: **every intermediate result flows back through the context window.** An agent that calls
five tools in sequence pays for four results it only needed in order to compute the fifth.

`CodeMode` addresses both. The agent gets meta-tools instead of your catalog, discovers what it
needs, then writes Python that chains tool calls **inside a sandbox** and returns only the final
answer. Introduced by Cloudflare and explored in Anthropic's *Code Execution with MCP*.

```python
from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import CodeMode

mcp = FastMCP("Server", transforms=[CodeMode()])

@mcp.tool
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y
```

Your tool functions don't change — the transform wraps existing tools. Install with the extra:
`pip install "fastmcp[code-mode]"`.

### Discovery flow

Default discovery is three meta-tools — `search`, `get_schema`, `execute`. The trade is **tokens
against round-trips**: each discovery step is an LLM round-trip, so more steps mean tighter context
but more latency and API calls. Fewer steps hand the model information upfront and pay for detail it
may not need. Tune the flow if that balance is wrong for your workload.

### Caveats

- **Experimental** — the core interface is stable, but the discovery tools and their parameters may
  change. Note the `fastmcp.experimental` import path.
- **Sandbox limits are on by default since 3.4.0** — `MontySandboxProvider()` applies 30s duration
  and 100 MB memory when constructed without limits, and `CodeMode` caps tool calls at 50 per
  `execute` block. Both are opt-out (`limits=None`, `max_tool_calls=None`). Don't disable them
  casually: they are the blast-radius control for agent-authored code.
- Reach for Code Mode when workflows chain several calls or move large intermediate payloads. For a
  server whose tools are called one at a time, it adds machinery for no gain.

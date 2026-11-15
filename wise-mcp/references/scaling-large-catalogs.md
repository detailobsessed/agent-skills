# Scaling large tool catalogs

Which server-side mechanism to use once `SKILL.md` §9 says a catalog needs narrowing, and the traps in each. Read §9 first: clients that defer tool loading make all of this unnecessary for most servers. For the full API of each mechanism, use the `fastmcp-server` skill or the FastMCP transforms docs.

## Contents

- [Choosing a mechanism](#choosing-a-mechanism)
- [Search transforms](#search-transforms)
- [Visibility gateway](#visibility-gateway)
- [Code Mode](#code-mode)

## Choosing a mechanism

| Problem | Mechanism |
| --- | --- |
| The catalog is too big to list | a search transform, with the tools agents need at once pinned as always visible |
| Agents should opt into whole categories | a visibility gateway, only if search doesn't fit |
| Chained calls pass large intermediate results through the context | Code Mode |

Prefer a search transform over a gateway. It doesn't depend on the client handling list-changed notifications, and hidden tools stay directly callable: the transform controls discovery, not access.

## Search transforms

`BM25SearchTransform` and `RegexSearchTransform` (`fastmcp.server.transforms.search`) replace the tool listing with `search_tools` and `call_tool`, plus whatever you pin with `always_visible`. Search results carry full parameter schemas, so the agent can call a found tool without another round-trip.

- **BM25** ranks by relevance (`search_tools(query=...)`). Use it when agents describe what they want in words.
- **Regex** matches a pattern (`search_tools(pattern=...)`) at almost no cost. Use it when agents roughly know the name. Patterns are bounded in length and run time, and lookarounds and backreferences are unsupported: a pattern using them returns no matches rather than an error, so don't suggest one in a description.
- Both search tool names, descriptions, parameter names and parameter descriptions, so a good description and parameter names are what make a tool findable.
- **Pin what agents need first** with `always_visible`: the tenant or project selector, the most common query, anything a workflow starts from. A client that ignores search still gets a usable floor.

## Visibility gateway

For category-based opt-in: hide every tool, re-show a small gateway (`get_capabilities`, `enable_tools(category)`), and enable categories on request.

```python
from fastmcp.server.transforms import Visibility

mcp.add_transform(Visibility(False, components={"tool"}))
mcp.add_transform(Visibility(True, tags={"gateway"}, components={"tool"}))
```

- **It needs authentication over HTTP.** `ctx.enable_components()` stores its rules per client, and an unauthenticated 2026-07-28 HTTP request has no client to key them to, so the call raises. Without auth, use a search transform.
- **Use two transforms, as above.** `match_all=True` short-circuits the `components` filter, so a single `Visibility(False, match_all=True, components={"tool"})` hides every resource and prompt as well.
- **Don't count on the client refreshing its list.** Many clients ignore the list-changed notification sent after enabling tools, so return the newly enabled tools' schemas from `enable_tools()` itself. This is the main reason search transforms are the better default.

## Code Mode

Search fixes a catalog too big to send. It doesn't fix the other cost: every intermediate result flows back through the context. An agent calling five tools in sequence pays for four results it needed only to compute the fifth.

`CodeMode` (`fastmcp.experimental.transforms.code_mode`, installed with the `code-mode` extra) gives the agent `search`, `get_schema` and `execute` instead of your catalog. The agent writes Python that chains tool calls inside a sandbox and returns only the final answer. Your tools don't change. The approach comes from Cloudflare and Anthropic's *Code Execution with MCP*.

- **Use it when workflows chain several calls or move large intermediate payloads.** For tools called one at a time it adds machinery for no gain.
- **Each discovery step is a model round-trip.** Fewer steps hand the model more up front; more steps keep context tighter but add latency. Tune the flow if the balance is wrong for your workload.
- **Say what the sandbox keeps.** Agents need to know what persists between `execute` calls and what becomes the result. A short fetch-filter-return example in the server instructions prevents repeated empty outputs.
- **Keep the limits on.** The Monty sandbox applies duration and memory limits by default, and `CodeMode` caps tool calls per `execute`. They are the blast-radius control for agent-written code. When you set your own, use the limit names from the installed `pydantic-monty`: an unknown key passes construction and fails only at the first `execute`.
- **It is experimental**, as the import path says. Its discovery tools and parameters may change between releases.

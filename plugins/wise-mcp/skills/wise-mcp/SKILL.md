---
name: wise-mcp
description: Design judgment for MCP servers built with FastMCP — what makes tools, outputs, errors, state, auth and large catalogs work for the agent calling them, drawn from the current MCP spec, client docs, measured studies and Arcade's pattern catalog. Use when building, wrapping, reviewing or refactoring an MCP server, tool, resource or prompt, when deciding tool boundaries, descriptions, response shape or error design, when a server needs cross-call state, user confirmation or per-tool auth, or when a tool catalog is getting large. Pairs with FastMCP's own `fastmcp-server` skill, which covers the API.
license: MIT
---

# Designing MCP servers that agents use well

This skill is the design half of building an MCP server: what to build and why. It deliberately leaves the API to FastMCP's own sources, which track every release:

- **FastMCP API** — the `fastmcp-server` skill from gofastmcp.com, if installed. Otherwise read the index at <https://gofastmcp.com/llms.txt> and fetch the pages you need as `.md`; don't load `llms-full.txt`, which runs to megabytes. Check the project's installed FastMCP version first: unversioned pages describe the current line, `/v3/` pages the 3.x line.
- **Arcade's pattern catalog** — 54 patterns for agent-facing tools at <https://www.arcade.dev/patterns>, plain text at <https://www.arcade.dev/patterns/llm.txt>. The `(see: NAME)` tags below are its pattern names. It is a practitioner's catalog, not a measured one: where measurements disagree with it, this skill follows the measurements.

Written against FastMCP 4.2.0 and MCP spec 2026-07-28, the latest at the time of writing (2026-11-15). Where an API named here disagrees with the installed version, the installed version wins; the judgment usually still holds. Every source the advice rests on, with the date it was last checked, is in [references/sources.md](references/sources.md).

## 1. Guiding principles

- **Machine experience** — design for LLM comprehension, not human reading. Names, descriptions, parameters and errors are the agent's only interface; a terse description a developer would understand leaves an agent guessing about purpose, prerequisites and valid inputs. *(see: TOOL_DESCRIPTION, MACHINE_EXPERIENCE)*
- **Tool DAGs** — hint at what comes next. Every tool should answer "what do I call before this?" and "what might I call after?", so the agent builds workflows without trial and error. *(see: DEPENDENCY_HINT, NEXT_ACTION_HINT)*
- **Error-guided recovery** — errors teach, not just fail. "Permission denied" teaches nothing; "Permission denied: requires the `admin` scope. Call `request_elevated_access()` first" lets the agent self-correct. *(see: RECOVERY_GUIDE, ERROR_CLASSIFICATION)*
- **Security boundaries** — prompts express intent, code enforces rules. Authorization, validation and audit happen in the tool layer, never in a system prompt or a tool description. *(see: SECRET_INJECTION, PERMISSION_GATE)*

## 2. Tool design

### Classify each tool

Whether a tool is a query, a command or a discovery tool drives every other decision about it:

- **Query tools** are read-only, safe to retry and cacheable. Set the read-only and idempotent tool annotations so the client and agent know a retry is free. *(see: QUERY_TOOL)*
- **Command tools** have side effects. Say what changes, whether it can be undone, and whether a destructive action needs confirmation. *(see: COMMAND_TOOL)*
- **Discovery tools** reveal what exists: `list_tables()`, `describe_schema()`. Agents working on unfamiliar data need them. For a large tool catalog, generate tool search with a transform rather than hand-writing it (§8). *(see: DISCOVERY_TOOL)*

### Write descriptions for the model

The description is the tool's interface. Put in it:

- what the tool does, in the first sentence;
- when to use it, and when to use something else instead;
- prerequisites: "Call `get_project_id()` first if you don't have a project ID";
- follow-ups: "After creating a user, call `assign_role()` to set permissions";
- limits: what it doesn't return, size caps, required formats;
- cost: "Scans every record. Use `search_users()` for filtered results."

Document parameters in the docstring's `Args:` section; FastMCP copies those into the schema. Name parameters unambiguously: `user_id`, not `user`.

**Every word of a definition is paid on every turn, used or not.** Richer descriptions cure wrong calls and cause context bloat, so spend words where the model would otherwise guess. Let names, enums and defaults do the work prose would: they cut errors and definition size at the same time. Examples earn their place less than they seem. In a 2026 study of 856 MCP tools, removing them made no measurable difference, and shorter targeted descriptions performed as well as fully augmented ones.

**Clients that defer tool loading see less than you wrote.** Claude Code, for example, starts with only tool names and the server's `instructions`, and fetches full schemas when a search matches. It also truncates server instructions and tool descriptions at 4,096 characters. So:

- make names self-explanatory and consistent (`billing_get_invoice`, not `get2`);
- set the server's `instructions` to say which task areas its tools cover and when to reach for them, because before any search runs, that is all a deferring client has to go on;
- front-load each description: the first sentence carries the choice, and detail goes after it.

*(see: TOOL_DESCRIPTION, PERFORMANCE_HINT)*

### Constrain inputs

Every free-form string is an opportunity for a wrong call. Use `Literal` or an enum for a known set of values, `Field` bounds (`ge`, `le`, `max_length`, `pattern`) for ranges, and structured types (`datetime`, not "a date string"). Validate early and say which values are accepted. *(see: CONSTRAINED_INPUT)*

- **Rename backend fields to the word the model would use** (`subject`, not `discipline`). The schema is the agent's vocabulary, not the database's.
- **Keep to about eight parameters.** Past that, split the tool, unless it bundles a genuine multi-call workflow.
- **Put a long vocabulary behind a lookup tool.** When a field has hundreds of valid values, give the schema short hints and add a `get_taxonomy(fields)` tool that returns valid values and synonyms on demand. One round-trip on ambiguous requests beats paying for the whole vocabulary on every turn.
- **When the gap between how users phrase things and what the backend accepts is wide**, interpret on the server: a small model you control maps the request to filter values, or one agent-backed tool takes the question. It costs inference you pay for, and in return behaves the same whichever model the client runs.

### More patterns that pay off

- **Smart defaults** — default to the common case, use context-aware defaults (the current user, now), and state each default in the description. *(see: SMART_DEFAULTS)*
- **Natural identifiers** — accept an email, username or display name and resolve it to the system ID yourself. When it is ambiguous, return the candidates (§7). *(see: NATURAL_IDENTIFIER, PARAMETER_COERCION)*
- **Mutual exclusivity** — when "exactly one of X or Y" applies, enforce it in validation and say so in the description. *(see: MUTUAL_EXCLUSIVITY)*
- **Batch operations** — offer an array-taking variant with per-item results when agents process many items; it saves round-trips and repeated output. *(see: BATCH_OPERATION)*
- **Operation mode** — make preview vs. apply, or dry-run vs. commit, an explicit enum parameter, never a hidden default. *(see: OPERATION_MODE)*
- **Tool chains** — when steps must run in a fixed order, expose one tool that runs the sequence with checkpoints instead of trusting the agent with the choreography. *(see: TOOL_CHAIN)*
- **Scatter-gather** — for a query across several backends, fan out, merge and return one result. *(see: SCATTER_GATHER_TOOL)*
- **Idempotent operations** — make commands safe to retry; accept an idempotency key for inherently non-idempotent ones (payments, emails) so a retry doesn't duplicate the effect. *(see: IDEMPOTENT_OPERATION)*

### Test the definitions, not just the code

Protocol tests prove a tool runs; they don't prove an agent picks it or fills its arguments right. When you change names, descriptions or parameters, give a model realistic requests together with the tool definitions and check which tool it chose and with what arguments. This needs no tool execution, so it is cheap to rerun on every description change. Arcade's evaluation approach works this way. For end-to-end workflow evaluation, see the `fastmcp-server` skill.

Treat the advice in this skill as defaults to test, not rules to apply wholesale. In the same 2026 study, adding every recommended description component raised median task success by about six points, but made results worse for one model-and-domain pair in six and added two-thirds more steps. Anthropic found that even prefix vs. suffix namespacing (`asana_search` vs. `search_asana`) moved its scores, differently per model. Measure against the models your users run.

## 3. Execution model

How a tool runs is part of its contract: say how long it takes, whether a retry is safe and what a partial failure leaves behind. Read `references/execution-model.md` when a tool is bound to one thread, runs longer than a client timeout, makes several writes, or needs an undo.

## 4. State across calls

**The protocol is stateless: a server cannot count on a connection to remember anything.** MCP 2026-07-28 removed protocol sessions. Every request stands alone, and the spec's guidance is for servers that need state across calls to mint their own handles. State stored on the connection silently resets on a modern client.

The two Arcade patterns that need state survive; their mechanism changes:

- **Identity anchor** — who the caller is. Key it to the authenticated principal, not to a connection. FastMCP's `UserSession` does this, and it requires authentication: an unauthenticated call fails. *(see: IDENTITY_ANCHOR)*
- **Working context** — the current project, tenant or scope. Have a tool create it and return a handle, which the agent then passes on every later call. FastMCP's `SessionId` parameter type does this and describes itself in the schema. A handle in the arguments is visible, loggable and survives a reconnect; connection state was none of those. *(see: SESSION_CONTEXT)*

Explicit parameters beat hidden context whenever the agent could get it wrong. Use the handle where repeating the full context on each call would be noisy, not to hide which project a write goes to.

## 5. Asking the user, and borrowing the caller's model

- **Ask the user only for what the agent cannot supply**: a confirmation before an irreversible step, a choice only the human can make, missing data no tool can find. Anything the agent could resolve with another tool call, let it resolve.
- **On the current protocol, a server asks by returning "input required", not by calling back.** The tool returns a request for input. The client collects the answer and calls the tool again with it, and the tool must then pick up where it left off. So design the asking tool to be re-entered: keep the carried state small, and make the step before the question free of side effects. The FastMCP elicitation page describes this flow and how one server can serve both older and current clients.
- **Don't build on server-side sampling.** The current spec deprecates sampling (along with roots and protocol logging), and FastMCP no longer offers it to servers. If a tool needs an LLM, call a model provider from the server with your own credentials and say so in your docs.
- **For irreversible actions, prefer a UI confirmation when the client renders apps** (§6), and fall back to a confirmation request in the tool's result when it doesn't (§7).

## 6. Resources, prompts and apps

- **Resources** hold stable, read-only data behind a URI. Anything with side effects, computation or a caller-dependent answer is a tool. Agents find resources only when a tool description names them. *(see: RESOURCE_REFERENCE)*
- **Prompts** earn their place only for a workflow or format users trigger by name. Guidance that fits in a tool description goes there.
- **Apps** fit when the human has to see, approve, pick, upload or enter something. Use FastMCP's built-in providers, not hand-rolled ones.

Read `references/resources-prompts-apps.md` before adding a resource, prompt or app: it has the URI-template rules, when a prompt beats a skill, and which provider fits which interaction.

## 7. Tool output

Agents consume your output as context for their next decision, and every unnecessary token degrades it.

**Shape it for the agent.** Flatten nested structures to the fields that matter, rename cryptic upstream fields (`user_email`, not `usr_eml`), and never pass a raw upstream response through: its schema was designed for developers. Return names and readable labels rather than bare UUIDs, which Anthropic found measurably reduces hallucinated follow-up calls. When the agent needs IDs for the next call, offer them through a `response_format` of `concise` / `detailed`. *(see: RESPONSE_SHAPER)*

**Declare an output schema** for tools with structured results. Clients that run code mode generate typed functions from it, and without one, a model writing code against your tool has to guess the result's shape.

**Bound its size.**

- Return only fields the agent needs for the task. *(see: TOKEN_EFFICIENT_RESPONSE)*
- Truncate long text with a note on how to get the rest.
- Count, don't list: "Found 847 matching records. Showing the first 10."
- Paginate with a cursor and a `has_more` flag, and say how to fetch the next page. A bounded result must say whether it is complete. *(see: PAGINATED_RESULT)*

**Steer the next step.**

- **Progressive detail** — summaries by default, with a `detail` parameter for the full response. *(see: PROGRESSIVE_DETAIL)*
- **Next-action hints** — one of the highest-impact patterns. Name the next tool and its arguments: `"next_steps": ["Call assign_role(user_id='abc', role='admin') to finish setup"]`. *(see: NEXT_ACTION_HINT, DEPENDENCY_HINT)*
- **Partial success** — for batches, report per-item status, totals and retry guidance; never report "failed" when some items succeeded. *(see: PARTIAL_SUCCESS)*
- **GUI URLs** — link to where a human can view or edit the result. *(see: GUI_URL)*
- **Empty is a statement** — "No invoices match status=overdue since 2026-01-01" instead of `[]`. An upstream failure is not an empty result.

## 8. Errors

Agents can't debug; they can only retry or try something else. The error message is their only guide.

**Every error answers three questions**: what went wrong, why, and how to fix it.

- Bad: `"Error: not found"`
- Good: `"User 'jsmith' not found. They may have been deleted, or the name is misspelled. Call search_users(query='smith') to find matches."` *(see: RECOVERY_GUIDE)*

**Classify it** so the agent responds correctly: *retryable* (rate limit, transient network; include `retry_after`), *permanent* (bad input, missing resource; say what to change), or *auth required* (name the missing scope and how to get it). *(see: ERROR_CLASSIFICATION)*

**Return expected failures; raise only real faults.** A raised error reaches the agent as text only, and any structured detail is dropped. For a failure the agent is meant to handle, return the error as a result: the recovery hint as text, the classification as structured content.

```python
from fastmcp.tools import ToolResult


@mcp.tool
def lookup(id: str) -> ToolResult:
    if not found(id):
        return ToolResult(
            content="User not found. Call search_users(query=...) to find candidates.",
            structured_content={"code": 404, "id": id, "retryable": False},
            is_error=True,
        )
    ...
```

Raise for bugs and unreachable dependencies. Proxies use the same mechanism to forward upstream errors intact.

**Handle ambiguity explicitly.**

- **Confirmation requests** — when input matches several entities, return the candidates with enough detail to choose, and the exact call for each. *(see: CONFIRMATION_REQUEST)*
- **Fuzzy matching** — Arcade's heuristic: above 90% confidence, accept and proceed; 50–90%, return options; below 50%, ask for different input. Tune the bands to your data. *(see: FUZZY_MATCH_THRESHOLD)*
- **Graceful degradation** — return what worked, say what failed, suggest a fix. *(see: GRACEFUL_DEGRADATION)*
- **Fallbacks** — when the primary source is down, use an alternative and say the result may be incomplete. *(see: FALLBACK_TOOL)*

## 9. Composition and catalog size

Compose servers to keep each one focused. Mount child servers under a namespace so their names can't collide. Generate tools from an OpenAPI spec only to bootstrap: curate the endpoints that matter, exclude the rest, and rewrite their descriptions (§2). A curated tool almost always beats a generated one.

When a server wraps several backends, offers one capability at several levels, or has to change a tool's signature, read `references/composition.md`: abstraction ladders, task bundles, gateways, one canonical model over similar APIs, and versioning a tool without breaking callers.

### When to hide tools behind search

**First decide whether you need it.** The major coding agents (Claude Code, Copilot CLI, Cursor) already defer tool loading: they keep names in context and fetch schemas on demand. A server-side search layer on top adds round-trips and saves no context. For a small catalog even client-side search costs more than it saves: Claude's Agent SDK docs put the line at about ten tools.

Reach for server-side narrowing when one of these holds:

- **The catalog is genuinely large** — hundreds of tools, such as a gateway over many backends. Some clients cap the catalog: VS Code accepts at most 128 enabled tools per request.
- **You don't control the client** — a public server meets clients that load the full listing. Pin a usable floor with the transform's always-visible list.
- **The catalog is dynamic** — generated from a database, tenant config or spec, so its size isn't known at build time.
- **The cost is round-trips and intermediate payloads, not catalog size** — that is Code Mode, a different win.

Otherwise: name tools well, write good descriptions and server instructions (§2), and expose them all. A curated 15-tool catalog beats a 40-tool one hidden behind search.

Which mechanism, and the traps in each — search transforms, the manual visibility gateway, Code Mode and its sandbox limits — are covered in `references/scaling-large-catalogs.md`.

Return tool lists in a stable order. The spec asks for a deterministic `tools/list`, because a list that reorders between calls breaks the client's prompt cache.

## 10. Authentication and security

Security is enforced in code, never delegated to the agent.

- **Never accept secrets as tool parameters.** Parameters pass through the LLM and land in conversation logs. Inject credentials from the environment, a vault or the authenticated context at run time. *(see: SECRET_INJECTION, CONTEXT_INJECTION)*
- **Act as the end user, not a shared service account.** If every call reaches the backend with one all-powerful credential, the tool list is the only boundary, and the backend's own permissions and audit attribution stop applying. Authenticate the user and call the backend on their behalf.
- **Gate each tool in code.** In FastMCP, an auth check goes in the tool's `auth=` argument (for example `@mcp.tool(auth=require_scopes("admin"))`), and server-wide rules go in auth middleware. There is no `require_auth` decorator. *(see: PERMISSION_GATE, SCOPE_DECLARATION)*
- **A tool the caller isn't authorized for is hidden from its tool list**, so the agent can't ask for access it can't see. If elevated access is part of a workflow, say in the server instructions or a discovery tool which scope unlocks what, and how to get it.
- **Bind tokens to the server.** Where the identity provider doesn't support resource indicators (RFC 8707), set `forward_resource=True` on the FastMCP OAuth provider so a token issued for one server can't be replayed against another.
- **Configure trusted hosts and origins for HTTP deployments deliberately.** Don't assume the defaults protect a server behind a proxy.
- **Audit trail** — log every call: tool and redacted arguments, who, when, outcome and duration. *(see: AUDIT_TRAIL)*
- **Context boundaries** — restrict file access to root paths, data to tenants, outbound calls to known endpoints. A tool's blast radius should be no larger than its job. *(see: CONTEXT_BOUNDARY)*

## 11. Anti-patterns

- **Raw API passthrough** — upstream responses forwarded without shaping.
- **Free-form strings where a finite set exists** — use `Literal`, enums and constrained types.
- **Silent failures** — `[]` with no word on what was searched or whether the backend answered.
- **Secrets as parameters** — they flow through the LLM and its logs.
- **Unbounded responses** — whole datasets with no pagination, truncation or completeness flag.
- **Descriptions written for developers** — missing purpose, prerequisites, follow-ups, limits and cost.
- **Descriptions padded to cover everything** — paid on every turn; let names, enums and defaults carry it (§2).
- **State on the connection** — "remember the project from the last call" breaks on stateless clients. Pass a handle or key it to the user (§4).
- **Building on sampling** — the spec deprecates it. Call a model provider directly (§5).
- **Raising when you meant to return** — a raised error drops structured content the agent could recover with (§8).
- **Security via prompts** — a description saying "only admins may call this" enforces nothing.
- **Deep proxy hierarchies** — each layer adds latency and a failure mode. Keep proxy depth to one.
- **Whole OpenAPI specs auto-converted** — most endpoints make poor agent tools. Curate.
- **Monolithic servers** — one server holding every tool makes selection harder as the list grows. Compose focused servers.
- **Search layered over clients that already defer** — round-trips for nothing. Reserve server-side narrowing for the cases in §9.
- **Missing next-action hints** — every response is a chance to move the agent forward.
- **No production discovery surface** — production servers want a registry or schema explorer, capability matching, and a health check. *(see: TOOL_REGISTRY, SCHEMA_EXPLORER, CAPABILITY_MATCHING, HEALTH_CHECK)*

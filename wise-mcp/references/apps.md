# Interactive apps and UIs

FastMCP 3.2 ("Show Don't Tool") added a full Apps system on top of the regular tool/resource/prompt primitives. A tool can return an interactive UI — chart, table, form, dashboard — that renders inline in the conversation. The UI is built with [Prefab](https://prefab.prefect.io), a Python component library that compiles to a web UI. FastMCP handles the MCP Apps protocol machinery (renderer resources, CSP configuration, structured content serialization).

Two ways to expose UIs, plus five ready-made providers.

## `app=True` on a regular tool

Simplest case. Return a `PrefabApp` containing chart/table/layout components. No server round-trip after rendering — best for one-shot visualizations.

```python
from fastmcp import FastMCP
from prefab_ui.components import BarChart, ChartSeries, PrefabApp

mcp = FastMCP("Analytics")

@mcp.tool(app=True)
def revenue_chart(year: int) -> PrefabApp:
    with PrefabApp() as app:
        BarChart(data=revenue_data, series=[ChartSeries(data_key="revenue")])
    return app
```

Use this when:

- You want to show data, not interact with it
- The agent has already gathered the data; the user just needs to see it
- A static chart, table, or dashboard is enough

## `FastMCPApp` provider — UIs that call backend tools

Full pattern for UIs that submit forms, trigger backend work, or maintain state across interactions. `@app.ui()` registers an LLM-visible tool that renders a UI; `@app.tool()` registers backend tools the UI calls (form submissions, button handlers, refresh actions). Visibility is managed automatically — the LLM sees only the UI entry points, not the backend handlers. Tool references survive namespace transforms and server composition.

```python
from fastmcp import FastMCP, FastMCPApp
from prefab_ui.actions.mcp import CallTool
from prefab_ui.components import (
    Button, Column, ForEach, Form, Input, PrefabApp, Text,
)

app = FastMCPApp("Contacts")
db: list[dict] = []

@app.tool()
def save_contact(name: str, email: str) -> list[dict]:
    db.append({"name": name, "email": email})
    return list(db)

@app.ui()
def contact_manager() -> PrefabApp:
    with PrefabApp(state={"contacts": list(db)}) as view:
        with Column(gap=4):
            ForEach("contacts", lambda c: Text(c.name))
            with Form(on_submit=CallTool("save_contact")):
                Input(name="name", required=True)
                Input(name="email", required=True)
                Button("Save")
    return view

mcp = FastMCP("Server", providers=[app])
```

## Built-in providers — reusable human-in-the-loop primitives

Five ready-made providers, each added with a single `add_provider()` call. Prefer these over hand-rolling equivalents.

- **`FileUpload`** — drag-and-drop file upload with session-scoped storage. Registers `file_manager` (upload UI), `list_files`, and `read_file`. Use it instead of asking the agent to paste large content as a parameter — bypasses the LLM context window entirely.
- **`Approval`** — human-in-the-loop confirmation gate. The LLM proposes an action, the user approves or rejects via buttons, and the decision flows back as a message. Use for irreversible operations: deletes, payments, anything you can't undo.
- **`Choice`** — present clickable options instead of asking the LLM to elicit a free-text choice. Pairs naturally with the `CONFIRMATION_REQUEST` pattern (see `SKILL.md` §8) when input could match multiple entities.
- **`FormInput`** — generate validated forms from Pydantic models. Submissions are validated against the model before they return. Supports default prefill values (FastMCP 3.3+). Use for structured data collection that would be error-prone via free-text.
- **`GenerativeUI`** — the LLM writes Prefab component code at runtime and the result streams to the user as generated. Use for one-off custom UIs that don't justify a hand-coded `@app.ui()` tool.

## Development workflow

`fastmcp dev apps` launches a browser-based preview for your app tools — pick a tool, supply arguments, and see the rendered UI without connecting to a real MCP host. Includes a built-in MCP message inspector for debugging the protocol traffic.

## Version pinning

`prefab-ui` is on a faster release cadence than FastMCP itself. Pin a specific version explicitly in your project dependencies — don't rely on a transitive range — and bump it deliberately when you upgrade FastMCP. Component API changes between Prefab minor versions are possible.

## Anti-patterns

- **Putting large content in parameters when `FileUpload` is available.** If a user needs to provide a CSV, a PDF, or an image, route it through `FileUpload`, not through a parameter the agent will paste into context.
- **Skipping `Approval` for irreversible actions.** A confirmation gate costs one extra UI message and prevents an agent's incorrect tool call from causing real damage.
- **Building custom forms when `FormInput` would do.** If the input shape is a Pydantic model, the built-in provider validates the submission for free. Don't reinvent it.

## Authoritative docs

- FastMCP Apps overview, `FastMCPApp` API, Prefab component catalog: <https://gofastmcp.com/llms-full.txt>
- v3.2.0 "Show Don't Tool" release notes (introduction of Apps): <https://github.com/PrefectHQ/fastmcp/releases/tag/v3.2.0>
- v3.3.0 "Slim Reaper" release notes (`FormInput` prefill, fixes): <https://github.com/PrefectHQ/fastmcp/releases/tag/v3.3.0>

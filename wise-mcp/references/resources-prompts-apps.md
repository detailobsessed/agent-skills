# Resources, prompts and apps

Which MCP primitive fits a job other than a tool. `SKILL.md` §6 keeps the one-line rule for each; this is the detail.

## Resources vs. tools

Use a resource for stable, read-only data identified by a URI: the agent reads it when it needs context. Use a tool when the operation takes more than a URI path, has side effects, computes something, or depends on who asks. Use a resource template for a parameterized family (`data://users/{user_id}/profile`) instead of one resource per entity. Keep URI schemes hierarchical and consistent across the server.

Resources are found only if the agent knows they exist, so name them in tool descriptions: "For full project configuration, read `config://project/{project_id}`." *(see: RESOURCE_REFERENCE)*

## Prompts

Prompts are reusable message templates, the least-used primitive. They earn their place for a standardized workflow (a review checklist), a fixed report format, instructions too long for a tool description, or a behaviour users trigger by name. Keep each to one purpose. If the guidance fits in a tool description, put it there. A repeatable multi-tool workflow may be better shipped as an agent skill alongside the server; the `fastmcp-server` skill covers serving one.

## Apps

Apps render an interactive UI in the conversation. Decide by what the human needs to do:

| The human needs to… | Use |
| --- | --- |
| see data the agent already gathered | a tool that returns a UI (one-shot, no round-trip) |
| submit forms or trigger backend work from the UI | an app with backend tools the UI calls, hidden from the model |
| upload a file | FastMCP's file-upload provider, never a parameter the agent pastes content into |
| approve an irreversible action | the approval provider |
| pick among candidates | the choice provider (pairs with CONFIRMATION_REQUEST) |
| enter structured data | the form provider, which validates against a Pydantic model |

Prefer the built-in providers over hand-rolled equivalents. Pin the UI component library (`prefab-ui`) explicitly, because it releases faster than FastMCP and its import paths move.

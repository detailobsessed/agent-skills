# Composition patterns

How to structure a server, or a set of them, once it wraps more than one backend or offers the same capability at several levels. `SKILL.md` §9 points here.

- **Abstraction ladder** — offer low-level (`write_bytes`), mid-level (`create_document`) and high-level (`draft_report`) tools, and let the agent pick its level. *(see: ABSTRACTION_LADDER)*
- **Task bundles** — when operations always happen together, combine them into one tool named after the task: `onboard_user()`, not `create_user_and_assign_role_and_send_email()`. *(see: TASK_BUNDLE)*
- **Gateway** — one parent server as the interface to several backends, routing internally. *(see: TOOL_GATEWAY)*
- **Canonical tool model** — wrapping similar APIs (several ticket systems), define one internal model and convert at the boundary, with per-backend adapters behind it, so a new backend adds no agent-facing tools. *(see: CANONICAL_TOOL_MODEL, TOOL_ADAPTER)*
- **Tool versioning** — when a signature must change, expose the new tool alongside the old, route clients with a version filter, and put the deprecation timeline in the old tool's description. *(see: TOOL_VERSIONING)*

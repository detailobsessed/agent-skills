---
type: llm
focus: trace
weight: 1
---

The modified server does not store the selected project in connection or session state (no ctx.set_state / ctx.get_state, no module-level "current project" global shared by all callers)

# Execution model

How a tool runs is part of its contract. Agents reason about latency, retries and cancellation like any API caller, so be explicit. `SKILL.md` §3 points here.

- **Sync vs. async** — FastMCP runs sync tools in a thread pool. A tool bound to one thread (UI frameworks, some database drivers) must opt out. *(see: SYNCHRONOUS_EXECUTION)*
- **Long work goes in a background task** — the call returns a handle the agent polls instead of blocking until a client timeout kills it. In the current spec, tasks are a protocol extension, so the server has to register it; check the tasks docs page before marking a tool as a task. *(see: ASYNC_JOB)*
- **Transactional boundaries** — when a tool makes several writes, say whether they are atomic and what state partial failure leaves. If not atomic, report partial success in the response. *(see: TRANSACTIONAL_BOUNDARY)*
- **Compensation** — for a non-atomic multi-step tool, offer an undo tool where feasible; an agent can recover from a partial failure only if it has a reverse operation. *(see: COMPENSATION_HANDLER)*
- **Timeouts** — set explicit per-tool timeouts, and report progress on anything that takes more than a few seconds so clients don't treat silence as a hang. *(see: TIMEOUT_BOUNDARY)*

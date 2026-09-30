# Glossary inbox — module 28 (multi-agent & A2A)

- **A2A (Agent-to-Agent)** — an emerging protocol for agents to advertise (agent cards), discover, and delegate tasks to each other.
- **Agent card** — machine-readable description of an agent's identity, skills, endpoint, and auth; trusted by routers, so a target for over-claim.
- **Trust graph** — directed graph where edges are "who accepts messages/tasks from whom"; every edge is an injection channel.
- **Transitive trust** — trust flowing along paths, so an injected low-privilege agent can reach a high-privilege action.
- **Agent impersonation** — forging the sender of an inter-agent message.
- **Message tampering** — altering a task or result in transit between agents.
- **Workflow corruption** — injected content re-plans a workflow (adds/re-orders subtasks).
- **Capability over-claim** — an agent card advertises skills it should not have, to get routed sensitive tasks.
- **Message authentication (inter-agent)** — signing/verifying sender+payload (e.g. HMAC); stops forgery/tampering, not malicious content.
- **Task provenance** — signed chain of originators/handlers of a task; lets a receiver refuse privilege for tainted origins.
- **Transitive-trust risk R** — max over nodes of exposure × reachable-privilege; dominated by exposed nodes that can reach powerful actions.

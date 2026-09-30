# Glossary inbox — module 16 (lesson 16.2, memory)

- **Agent long-term memory** — durable store (vector memory, profile, scratchpad) the agent writes to and reads back across tasks/sessions.
- **Memory poisoning** — getting a directive into what the agent stores, so it re-injects on later retrieval.
- **Persistence (agentic)** — a planted directive re-activating across sessions; P_fire(n)=1-(1-pq)^n -> 1 with use. No weight change needed.
- **Trust tag / write provenance** — recording each memory's source (user/trusted_tool/untrusted); never elevate untrusted.
- **Read-time re-validation** — untrusted memories enter context as data, not instructions; privileged actions re-check policy.
- **Quarantine (memory)** — dropping untrusted-sourced memories from retrieval entirely (q->0); strongest lever, beats stealth.
- **Delayed / conditional trigger** — payload that fires only under a future condition; dormant, evades sampling detectors.
- **Stealth payload** — low-signal poison trading reliability for evasion of write/read detectors.

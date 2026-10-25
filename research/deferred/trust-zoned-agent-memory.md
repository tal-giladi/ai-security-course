# Trust-zoned memory for computer-use agents (persistent-memory attack)

- **Topic ID:** trust-zoned-agent-memory
- **Status:** WAIT
- **Next review:** 2026-11-01
- **Course change:** none
- **Candidates:** C-20261002-01, C-20261020-01, C-20261021-05, C-20261022-01, C-20261022-02

## Summary

ZoneClaw names a "persistent memory attack" on computer-use agents: benign-looking content induces
the agent to write attacker claims into auto-reloaded workspace memory that silently governs later,
unrelated tasks. Fix: separate persistence from action-authority — external claims live in a
low-trust zone and only gain authority by crossing an explicit boundary, with role-specific
asymmetric privilege. ASR 77.5% → 1.25%, utility 95.4% across 4×2×4; remains effective vs some
defense-aware attackers; code released. Directly extends lesson 16.2 (agent memory poisoning).

## Evidence

- https://arxiv.org/abs/2610.00450 ; code https://github.com/euph00/ZoneClaw-code — one group, large structured eval, attack+defense-aware numbers, released code.
- https://arxiv.org/abs/2610.22959 — SAFE-Mem: provenance/authority/scope labels at write, governance-aware retrieval; MPBench + LoCoMo, 4 backbones; >=77% lower ASR than strongest alternative, up to +15% accuracy; code stated as released. Added 2026-10-25.
- https://arxiv.org/abs/2610.28987 — PerMIT: Lean-4-checked integrity theorems (memory influences sensitive actions only via a gate) + community trust; no attack success on Trojan Hippo; no code stated. Added 2026-10-25.
- https://arxiv.org/abs/2610.28425 — CarryoverBench (EMNLP 2026): injections planted in memory/scheduled tasks re-fire across sessions without decay over 5 rounds. Added 2026-10-25.
- https://arxiv.org/abs/2610.28810 — memory injection against deployed ChatGPT/Claude/Gemini (memories, projects, skills, org instructions, MCP); cross-user spread via shared org memory reported (no vendor confirmation). Added 2026-10-25.
- ClawMMU (https://arxiv.org/abs/2610.28093, daily 2026-10-21 C-line) — protection-coherent virtual memory for agents, same problem. Added 2026-10-25.

## What would change the decision

Independent replication or adoption. Strong candidate for a 16.2 lab extension (flat vs zoned memory
on the same injected-claim scenario); next review deliberately near-term given code is available.

## History

- 2026-10-04 — WAIT — unusually complete single paper (attack, defense, cost, code) and a clean fit to 16.2, but one group and days old; ADD budget used on a due deferred item — weekly/2026-W40.md — candidates C-20261002-01
- 2026-10-25 — WAIT — strong convergence this week: three more mechanism-distinct defenses (SAFE-Mem with code, PerMIT formally verified, ClawMMU) plus a peer-reviewed attack benchmark (CarryoverBench) and attacks on deployed products — the topic is now the leading ADD candidate for its scheduled 2026-11-01 review (budget this week went to ATT&CK v20); keep 2026-11-01 — weekly/2026-W43.md — candidates C-20261020-01, C-20261021-05, C-20261022-01, C-20261022-02

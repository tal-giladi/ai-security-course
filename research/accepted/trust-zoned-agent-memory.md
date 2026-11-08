# Trust-zoned memory for computer-use agents (persistent-memory attack)

- **Topic ID:** trust-zoned-agent-memory
- **Status:** ADD
- **Next review:** on new evidence
- **Course change:** `lessons/module-16/lesson-02.md` (section *Advanced extension: trust-zoned memory*, added 2026-11-01); `labs/lab-36-trust-zoned-memory/`; `_sidebar.md`; `curriculum/course-outline.md`; `references/standards-map.md`
- **Candidates:** C-20261002-01, C-20261020-01, C-20261021-05, C-20261022-01, C-20261022-02, C-20261030-04, C-20261103-10

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
- https://arxiv.org/abs/2610.38209 — Role Grounding Attack (Bu et al., 2026-10-28): an agent records a preference quoted inside nested social content as its own user's preference (5 memory systems × 6 LLMs; no exact ASR in abstract; no defense). The misattribution placement in the lesson. Added 2026-11-01.
- Re-verified 2026-11-01 by direct fetch: ZoneClaw abstract (Ma, Lin, Qiu, Chang; 372/480 → 6/480 ASR, utility 458/480; under review) and its public code repo (github.com/euph00/ZoneClaw-code, exists, no license shown); SAFE-Mem abstract (v2 2026-10-20; code github.com/LVenum/SAFE-Mem); CarryoverBench abstract (EMNLP 2026 Main per comments field); arXiv:2610.28810 abstract (no vendor response on page).
- Standards: OWASP Top 10 for Agentic Applications 2026 (resource page dated 2025-12-09, fetched) — ASI06 Memory & Context Poisoning (entry name verified via several secondary sources; PDF not read); MITRE ATLAS AML.T0080 AI Agent Context Poisoning / AML.T0080.000 Memory, case study AML.CS0040 (via secondary sources; official ATLAS/D3FEND hosts unreachable from this environment).
- Accept Changes, Reject Attacks (C-20261103-10): new ECA metric for memory management; existing defenses reject legitimate changes; single preprint, no code. Supports the taught utility-cost framing. Added 2026-11-08.

## What would change the decision

Accepted. Revisit on new evidence: a vendor shipping zoned/authority-scoped memory (would move the
section from EMERGING to CURRENT), an attack that breaks runtime-assigned zones without compromising a
HIGH channel (would need a new guarantee row), or a finer-grained lineage taint with a measured FP
reduction (candidate exercise solution).

## History

- 2026-10-04 — WAIT — unusually complete single paper (attack, defense, cost, code) and a clean fit to 16.2, but one group and days old; ADD budget used on a due deferred item — weekly/2026-W40.md — candidates C-20261002-01
- 2026-10-25 — WAIT — strong convergence this week: three more mechanism-distinct defenses (SAFE-Mem with code, PerMIT formally verified, ClawMMU) plus a peer-reviewed attack benchmark (CarryoverBench) and attacks on deployed products — the topic is now the leading ADD candidate for its scheduled 2026-11-01 review (budget this week went to ATT&CK v20); keep 2026-11-01 — weekly/2026-W43.md — candidates C-20261020-01, C-20261021-05, C-20261022-01, C-20261022-02
- 2026-11-01 — ADD — due today; convergence of four mechanism-distinct defenses (two with released code) on one principle (persistence ≠ authority), a peer-reviewed attack benchmark (CarryoverBench, EMNLP 2026), attacks on deployed assistants, a new misattribution attack (RGA), and named standards entries (OWASP ASI06, ATLAS AML.T0080.000); added as an advanced extension to 16.2 + Lab 36 (10 tests; full suite 172 passed) — weekly/2026-W44.md — candidates C-20261030-04
- 2026-11-08 — ADD — no course change: supporting evidence for the taught zoning defense's utility-cost framing — weekly/2026-W45.md — candidates C-20261103-10

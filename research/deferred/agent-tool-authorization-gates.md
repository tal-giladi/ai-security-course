# Deterministic tool-call authorization gates (provenance / typed / stateful)

- **Topic ID:** agent-tool-authorization-gates
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20260928-02, C-20260930-06, C-20261003-01, C-20261001-04, C-20261005-03, C-20261008-04, C-20261019-04, C-20261021-01

## Summary

Several runtime authorization defenses for tool-calling agents, all extending M16's policy-layer /
allowlist baseline with a measured cost: AGATE (provenance gate, 6/11 benign-scenario FP cost),
ToolFence (typed blueprint + deterministic monitor + judge fallback, ~3.8pp utility cost), Sapien
(stateful regex+predicate policy, blocks 93–95% AgentDojo / 62–85% Toolathlon at near-zero utility
cost), and ActionGuard (separated planning/authorization context, specifically against poisoned
skills). Conceptually overlapping — at most one should be taught, or they should be explicitly
contrasted. Sapien is the most course-aligned (extends lab-16 + the AgentDojo paper the course uses).

## Evidence

- https://arxiv.org/abs/2609.30830 — AGATE. https://arxiv.org/abs/2609.37196 — ToolFence.
- https://arxiv.org/abs/2610.00797 — Sapien. https://arxiv.org/abs/2609.39450 — ActionGuard.

- https://arxiv.org/abs/2610.02569 — Pincer (Popa/Stoica group): learned per-user "digital twin" permission proxy for coding agents; mechanism-distinct, no headline metric on the abstract page, no code. Added 2026-10-11.
- https://arxiv.org/abs/2610.09793 — MFOTL/MonPoly runtime verification over AgentDojo/STAC/R-Judge traces (CPSIoTSec '26 @ CCS): generic obligations flag ~70% of attacks but fire on 29.3% of benign runs; naive provenance checks defeated by one planted line in 94–99% of runs; binding provenance to its lookup closes it. Added 2026-10-11.
- https://arxiv.org/abs/2610.27620 — 'Local Allow, Global Deny' (extended version of IEEE TPS 2026 paper): relational purpose violations are 2-safety hyperproperties no per-action gate can detect; AL-SYNTH witnesses approved by 9 LLM judges, flagged once both executions shown; code https://github.com/anmolpandey299/al-synth. Added 2026-10-25.
- https://arxiv.org/abs/2610.23077 — approval-token reuse across services (token possession treated as authorization); competition traces, 8/9 reruns. Added 2026-10-25.

## What would change the decision

Released code to verify numbers (none has it), independent replication, or adoption. When one
matures, ADD the single best as a lab-16 stateful-policy extension and contrast the others in one
guarantee box; do not teach all four.

## History

- 2026-10-04 — WAIT — a crowded, overlapping defense theme; all single papers without released code; Sapien is the lead candidate for a future lab-16 extension — weekly/2026-W40.md — candidates C-20260928-02, C-20260930-06, C-20261003-01, C-20261001-04
- 2026-10-11 — WAIT — two more mechanism-distinct entries (Pincer learned proxy; MFOTL runtime verification with measured 29.3% benign FPR) — the theme stays crowded and unreplicated; note the new 17.2 (capability flow control) now covers the structural core, so a future ADD here must add measured gate/approval-fatigue evidence beyond it — weekly/2026-W41.md — candidates C-20261005-03, C-20261008-04
- 2026-10-18 — WAIT — four more mechanism-distinct entries this week (KedgeFlow idempotency/replay with code; CreepScope privilege-creep lifecycle metric; DelegateGuard formal attenuation at Enron scale; revocation-completeness C0–C5 on real Keycloak/AWS) — the cluster keeps broadening rather than converging, and 22.2's structural controls now cover part of the ground; a future ADD still needs one lead mechanism with code + approval-fatigue/lifecycle measurement beyond 17.2/22.2; keep 2026-11-15 — weekly/2026-W42.md — candidates C-20261014-05, C-20261015-09, C-20261015-10, C-20261015-18
- 2026-10-25 — WAIT — a peer-reviewed impossibility result with code reframes the cluster (per-action gates cannot see cross-execution violations) and supplies the guarantee-box line any future ADD must carry; still no single lead gate with replication; keep 2026-11-15 — weekly/2026-W43.md — candidates C-20261019-04, C-20261021-01

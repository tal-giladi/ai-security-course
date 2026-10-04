# Deterministic tool-call authorization gates (provenance / typed / stateful)

- **Topic ID:** agent-tool-authorization-gates
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20260928-02, C-20260930-06, C-20261003-01, C-20261001-04

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

## What would change the decision

Released code to verify numbers (none has it), independent replication, or adoption. When one
matures, ADD the single best as a lab-16 stateful-policy extension and contrast the others in one
guarantee box; do not teach all four.

## History

- 2026-10-04 — WAIT — a crowded, overlapping defense theme; all single papers without released code; Sapien is the lead candidate for a future lab-16 extension — weekly/2026-W40.md — candidates C-20260928-02, C-20260930-06, C-20261003-01, C-20261001-04

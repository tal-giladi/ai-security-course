# Multi-agent topology leakage (disclosure without compromise)

- **Topic ID:** multi-agent-topology-leakage
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261015-11, C-20261031-04

## Summary

Information disclosed to one authorized agent propagates to an unauthorized one through routine,
benign coordination — a structural/topological privacy failure, not an attack. Across 485 scenarios /
three topologies, disclosure to topology-introduced recipients rises 0%→52.2% while content-level
"surface leakage" stays flat (~61%), so content-only detectors miss it; framework choice alone drives
a 150x spread. RECONS (recipient- and context-conditioned sanitization) cuts residual disclosure
96.7%→29.25% while keeping 94.1% of authorized disclosures. Distinct from deliberate covert collusion
(already tracked).

## Evidence

- https://arxiv.org/abs/2610.16039 — Ogundoyin, Ikram; large systematic eval across topologies/frameworks; single preprint, no code, affiliations unconfirmed.
- https://arxiv.org/abs/2610.39532 — Task-Graph Contextual Integrity: propagation-scope-aware CI over a multi-agent task graph; 85.8–94.1% fewer unauthorized disclosures vs local-history CI at 93.6–96.1% of its task accuracy on MAPLE-Bench (144 cases; no code/benchmark link). Also relevant to agent-mosaic-aggregation-disclosure. Added 2026-11-01.

## What would change the decision

Released code; independent reproduction of the topology effect; a CPU-feasible M28 exercise
(reproduce 0%→52.2% across three topologies, then a recipient-conditioned sanitizer).

## History

- 2026-10-18 — WAIT — clean, systematic demonstration that multi-agent privacy is topological, directly relevant to M28, but single preprint without code; ADD budget used on skill-trust-boundary — weekly/2026-W42.md — candidates C-20261015-11
- 2026-11-01 — WAIT — a candidate unifying formalism for the multi-agent privacy cluster; no code or benchmark access; keep scheduled review — weekly/2026-W44.md — candidates C-20261031-04

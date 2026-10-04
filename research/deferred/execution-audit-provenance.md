# Claim-anchored execution contracts for tool-agent audit trails

- **Topic ID:** execution-audit-provenance
- **Status:** WAIT
- **Next review:** 2026-11-29
- **Course change:** none
- **Candidates:** C-20261003-02

## Summary

"Actions with Receipts" names cross-object substitution in agent audit trails (a citation and an
execution trace each well-formed but silently transplanted across claims/actions/runs/source
versions). A claim-anchored execution contract jointly binds claim, source span, ordered execution
prefix, and source version; a deterministic integrity verifier runs before any entailment judgment.
Detects 1,275/1,280 (99.6%) cross-object attacks; each binding independently load-bearing (ablation
drops to 1.6–6.3%); held-out entailment F1 0.868 / FA 0.094. Extends M19/M22 provenance/TrustPolicy.

## Evidence

- https://arxiv.org/abs/2610.00327 — single paper, large constructed-attack eval, full ablation, held-out check; no released code.

## What would change the decision

Released code or independent reproduction. Candidate for an M19/M22 provenance lab extension.

## History

- 2026-10-04 — WAIT — rigorous ablated integrity mechanism, but single paper, no code, authors unstated — weekly/2026-W40.md — candidates C-20261003-02

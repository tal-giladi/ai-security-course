# Agent memory privacy: disclosure amplification and deletion that does not erase

- **Topic ID:** agent-memory-privacy-erasure
- **Status:** WAIT
- **Next review:** 2026-12-06
- **Course change:** none
- **Candidates:** C-20261021-07, C-20261024-01

## Summary

Two non-poisoning privacy failures of persistent agent memory: (1) a disclosure feedback loop where memory-conditioned replies raise users' attribute disclosure over sessions (mitigated by not stating/presupposing attributes); (2) deleting a memory record does not delete what derived state carries (62–99% reconstruction from components; provenance-aware closure eliminates it in tested settings).

## Evidence

- https://arxiv.org/abs/2610.28315 — Disclosure Begets Disclosure, simulation, no code.
- https://arxiv.org/abs/2610.31366 — AfterDeleteBench, exposed-vs-control audit design, no code.

## What would change the decision

Code release or replication for either; then a 16.2 extension on memory erasure (provenance-aware closure) with the exposed-vs-control measurement as the lab pattern.

## History

- 2026-10-25 — WAIT — a genuine gap in the memory lessons (erasure/privacy, not poisoning) but two single preprints without code — weekly/2026-W43.md — candidates C-20261021-07, C-20261024-01

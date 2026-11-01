# Measured-endpoint taxonomy and testbed for RAG protection research

- **Topic ID:** rag-defense-measured-endpoints
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261023-07, C-20261027-10

## Summary

Survey of 118 RAG-defense papers organized by measured endpoint; testbed shows an 8-gram verbatim guard drives copying to 0.0% while a 3-query adaptive attacker still recovers 48.3% of hidden facts.

## Evidence

- https://arxiv.org/abs/2610.30193 — release of taxonomy/dataset/testbed claimed, repository not located.
- https://arxiv.org/abs/2610.33849 — Ranking Is Not Deciding: removing PoisonedRAG's verbatim-question prefix drops a RAGuard-style filter AUROC 0.953 → 0.758, miss rate 0.19 → 0.76; proposes reporting a poison set's construction profile and FPR at the deployed threshold; profiling script stated released (preprint). Added 2026-11-01.

## What would change the decision

Locate and verify the released testbed; the adaptive-vs-verbatim result could become a worked example in 14.1/15.1's guarantee boxes. (Distinct from rejected rag-security-causal-taxonomy: this one has its own measurement.)

## History

- 2026-10-25 — WAIT — a methodology survey with one useful measurement; artifacts not located — weekly/2026-W43.md — candidates C-20261023-07
- 2026-11-01 — WAIT — benchmark-construction artifact evidence strengthens the case for teaching measured endpoints, but the scope question is unchanged; keep scheduled review — weekly/2026-W44.md — candidates C-20261027-10

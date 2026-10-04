# Image-returning multimodal RAG datastore extraction (ImmRAG)

- **Topic ID:** multimodal-rag-extraction
- **Status:** WAIT
- **Next review:** 2026-11-29
- **Course change:** none
- **Candidates:** C-20261003-03

## Summary

"Walking the Embedding Space" is a black-box confidentiality attack on image-returning multimodal
RAG: a malicious instruction embedded in a user-given image, blended with an already-recovered image,
adaptively steers queries (relevance-weighted resampling) into unexplored embedding regions. One
2,500-query run reconstructs up to 611 radiology images / 566 document scans / 416 general images —
up to 5.6x a non-adaptive baseline. Confidentiality angle on M14/M15 (vs the course's current
poisoning/authorization framing).

## Evidence

- https://arxiv.org/abs/2610.01871 — single paper, three realistic scenarios, multiple retrievers, clear baseline; no code.

## What would change the decision

Independent reproduction or released code. Candidate for an M14/M15 "RAG confidentiality" extension.

## History

- 2026-10-04 — WAIT — concrete high-sensitivity extraction attack, but single paper, no code/replication — weekly/2026-W40.md — candidates C-20261003-03

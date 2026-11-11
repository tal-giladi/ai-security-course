# GraphRAG schema-level (auxiliary-structure) poisoning

- **Topic ID:** graphrag-schema-poisoning
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261005-01

## Summary

HDI attack (IFIP SEC 2026): corrupting GraphRAG's auxiliary index structures (community summaries, hierarchical edges, pre-computed scores) instead of instance triples gives 1:N leverage (~6 queries per edit, 88–94% ASR modifying ~0.016% of structures) and evades perplexity/paraphrase filters.

## Evidence

- https://arxiv.org/abs/2610.02373 — HDI / 3S framework; DOI 10.1007/978-3-032-27993-4_24 (IFIP SEC 2026 proceedings). Code repo stated but unverified.

## What would change the decision

Confirmed code release; an independent reproduction on Microsoft GraphRAG; or a measured runtime-validation defense. Would fit as an extension to 14.1 / lab-14.

## History

- 2026-10-11 — WAIT — peer-reviewed and measured, but single group, code unverified, no defense; the course's RAG module does not yet teach GraphRAG indexing, so a lesson would need that prerequisite first — weekly/2026-W41.md — candidates C-20261005-01

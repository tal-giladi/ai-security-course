# Geometric (embedding-transform) access control in RAG: isolation is not confidentiality

- **Topic ID:** rag-embedding-transform-access-control
- **Status:** WAIT
- **Next review:** 2027-01-10
- **Course change:** none
- **Candidates:** C-20261112-01

## Summary

"Search-preserving geometric" access control transforms embeddings per policy so that multi-policy
vector stores keep retrieval working without crossing policy boundaries. A security analysis of the
available implementations finds that retrieval utility and policy isolation hold, but representation
confidentiality, query-forgery resistance and policy-membership hiding do not: a curious user with a
few hundred aligned (original, protected) pairs recovers original embeddings and forges
policy-compatible queries. A clean guarantee-box case bridging 15.1 (multi-tenant retrieval) and
29.1 (embeddings are recoverable data); the recovery is a least-squares known-plaintext attack the
course could implement from scratch.

## Evidence

- https://arxiv.org/abs/2611.14061 — single preprint (Nouyep, Puys, Salva), three encoders; abstract only; evaluates academic proposals, not a named production vector DB; no code.

## What would change the decision

A production vector database shipping transform-based tenant isolation, or a second group confirming
the recovery result with numbers per encoder and dimension. Then a 15.1/29.1 bridge exercise
(secret per-tenant orthogonal transform → least-squares recovery from N pairs).

## History

- 2026-11-15 — WAIT — clean, teachable guarantee distinction, but the defended mechanism is academic (no production adoption) and the evidence is one abstract-only preprint — weekly/2026-W46.md — candidates C-20261112-01

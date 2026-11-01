# Stance poisoning of RAG with factually correct, one-sided documents

- **Topic ID:** rag-stance-poisoning
- **Status:** WAIT
- **Next review:** 2026-12-27
- **Course change:** none
- **Candidates:** C-20261027-05

## Summary

At a mean poisoning share of 18.9%, factually correct but one-sided documents shift the generated stance monotonically for four vendors' models. A stance-balancing middleware (2/2/1 balancing plus a debiasing prompt, no extra LLM calls) reduces the deviation by 0.106–0.350 at about 1.5% GPU overhead.

## Evidence

- https://arxiv.org/abs/2610.34294 — Yang et al. (Bo Li co-author), preprint, no code.

## What would change the decision

Code or replication. It would be a 14.1 extension (a new poisoning goal plus a cheap measured defense).

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261027-05

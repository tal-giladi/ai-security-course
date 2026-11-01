# AdvGuard: graph-based detection of coordinated multi-turn system-prompt extraction

- **Topic ID:** multiturn-prompt-extraction-defense
- **Status:** WAIT
- **Next review:** 2026-12-27
- **Course change:** none
- **Candidates:** C-20261028-05

## Summary

AdvGuard models relationships between queries as a semantic-interaction graph classified by a GCN, with a single-prompt cold-start detector. Reported: +36% recall over the best baseline at ≤3.4% FPR, and near-zero leakage against adaptive PLeak/LeakAgent loops.

## Evidence

- https://arxiv.org/abs/2610.36295 — Nayan et al. (preprint, no code).

## What would change the decision

Code or replication of the very strong numbers. It would be a lab-04 extension.

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261028-05

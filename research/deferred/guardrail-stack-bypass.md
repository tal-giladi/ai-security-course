# Joint bypass of multi-scanner guardrail stacks (BRANCH)

- **Topic ID:** guardrail-stack-bypass
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261009-01

## Summary

Branching tree search optimises perturbations across all scanners jointly: 100% ASR on 6 guardrail systems (120 scenarios), 72% fewer queries, transfer to 29 unseen guardrails incl. 8 commercial black-box ones.

## Evidence

- https://arxiv.org/abs/2610.10742 — single preprint; code not confirmed; commercial targets unnamed on the abstract page.

## What would change the decision

Code release or an independent reproduction; vendor acknowledgement. Fits as a 23.1/08.1 extension ('stacking classifiers is not independence') — the course already teaches adaptive attacks on filters, so the delta is the joint-optimisation/transfer result.

## History

- 2026-10-11 — WAIT — strong claims, days old, no code, partially covered by 08.1 (adaptive/black-box search) and 23.1 (defense composition) — weekly/2026-W41.md — candidates C-20261009-01

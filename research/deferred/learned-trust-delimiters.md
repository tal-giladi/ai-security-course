# Learnable trust-boundary delimiters for prompt injection (LTBD)

- **Topic ID:** learned-trust-delimiters
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261009-05

## Summary

Learned delimiter embeddings mark untrusted spans without fine-tuning the base model; reports 0.00% ASR on AlpacaFarm and 0.11–0.19% on TaskTracker, robust to adaptive attacks.

## Evidence

- https://arxiv.org/abs/2610.11634 — 5-page preprint; no code.

## What would change the decision

Code and an independent adaptive evaluation (the claims are strong for the paper's length). Would be a 04.1/05.1 extension next to spotlighting/instruction hierarchy.

## History

- 2026-10-11 — WAIT — strong claims from a very short paper, no code, no replication — weekly/2026-W41.md — candidates C-20261009-05

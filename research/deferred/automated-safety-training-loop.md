# Recursive red-team-then-align training loops (ReSI)

- **Topic ID:** automated-safety-training-loop
- **Status:** WAIT
- **Next review:** 2026-12-06
- **Course change:** none
- **Candidates:** C-20261011-02

## Summary

Each round red-teams the current model, fine-tunes on what broke it and keeps only Pareto-improving updates gated on capability retention: mean X-Teaming ASR 86.01%→31.45% across 4 dense/MoE models.

## Evidence

- https://arxiv.org/abs/2610.12233 — single preprint; no code confirmed. (Daily class B 2026-10-11; not copied into staging — reviewed here from daily/2026-10-11.md.)

## What would change the decision

Code and an independent evaluation; relevance is mostly to model developers — would be a 25.1 extension (automated red teaming feeding training).

## History

- 2026-10-11 — WAIT — model-training-side defense, single preprint, overlaps 25.1's automated red-teaming loop — weekly/2026-W41.md — candidates C-20261011-02

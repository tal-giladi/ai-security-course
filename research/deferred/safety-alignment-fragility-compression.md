# Safety degradation under serving-time compression (expert reduction, pruning)

- **Topic ID:** safety-alignment-fragility-compression
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261105-04, C-20261106-03

## Summary

Efficiency techniques erode safety alignment: active expert reduction in MoE serving measurably increases unsafe outputs across nine open-weight MoE models (SafeStart restores it with a fused vLLM kernel), and pruning/ablation exposes fragile alignment that a subtraction-based method reportedly hardens (up to 90%).

## Evidence

- C-20261105-04 — SafeStart, preprint, no code.
- C-20261106-03 — Addition by Subtraction, preprint, no code; headline is a best case.

## What would change the decision

Code release or replication of either; then an M30 (deployment) or M11 extension on safety as a property that serving optimisations must preserve.

## History

- 2026-11-08 — WAIT — two single-group preprints, no code — weekly/2026-W45.md — candidates C-20261105-04, C-20261106-03

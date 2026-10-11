# MoE router telemetry as a membership-inference side channel

- **Topic ID:** moe-router-membership-inference
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261010-01

## Summary

Adding aggregated expert-routing features to an output-signal MIA ensemble raises TPR@1%FPR by 2.7–9.4 pp in all 9 settings (3 MoE architectures × 3 domains), persisting across full FT, frozen router, LoRA and instruction tuning; noising telemetry trades utility for leakage proportionally.

## Evidence

- https://arxiv.org/abs/2610.10616 — single preprint; code not confirmed.

## What would change the decision

Code release and an independent reproduction, or evidence that production APIs expose routing telemetry. Would be a 12.1 extension (the course teaches LiRA-style MI already).

## History

- 2026-10-11 — WAIT — consistent but modest effect, single preprint, exposure of router telemetry in real APIs unestablished — weekly/2026-W41.md — candidates C-20261010-01

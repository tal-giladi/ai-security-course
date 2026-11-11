# Context-aware Pickle VM-state scanning (DITTO / PickleBench)

- **Topic ID:** pickle-scanner-defense
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261009-02

## Summary

DITTO tracks Pickle VM state opcode-by-opcode with semantic analysis: 0% FNR / 0.7% FPR, F1 0.966 on PickleBench (959 benign + 92 malicious real models); 9.3% of 10,000+ popular HF repos rely on Pickle.

## Evidence

- https://arxiv.org/abs/2610.10735 — single preprint; code/benchmark release unconfirmed.

## What would change the decision

Release of PickleBench and the scanner; comparison against the scanners already named in 13.1/22.1 by a second group. Would be a 13.1 extension (opcode-tracking scanner vs pattern match) — lab-13 already shows pickle RCE and safetensors.

## History

- 2026-10-11 — WAIT — measured defense with FP cost for an attack the course teaches, but no released artifact yet and the course's current defense (safetensors / no-pickle) remains the primary control — weekly/2026-W41.md — candidates C-20261009-02

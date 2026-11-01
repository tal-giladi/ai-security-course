# Learned poison-set selection for LLM backdoors (SAILS)

- **Topic ID:** poison-set-selection-backdoors
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260926-04, C-20261026-09

## Summary

At fixed poison count and trigger, *which* examples are poisoned swings backdoor ASR from 3% to
80%; SAILS learns a set-level scorer from finetune-and-evaluate runs and improves held-out ASR by
~30pp over influence-function baselines (author claims).

## Evidence

- https://arxiv.org/abs/2609.15029 — single preprint (2026-09-14); no confirmed code; no independent reproduction.
- https://arxiv.org/abs/2610.32334 — Trigger-Neutralized Counterfactual Scoring: selects poison samples for code-model backdoors by isolating the trigger's causal effect; higher ASR at very low poisoning ratios across 3 CodeXGLUE tasks × 5 trigger families (preprint, no code). Added 2026-11-01.

## What would change the decision

Independent reproduction or code release; then a small lab-11-adjacent exercise (new lab)
comparing random vs scored poison selection at a fixed budget on a CPU-sized model.

## History

- 2026-09-27 — WAIT — credible authors and a teachable lever, but one fresh preprint without code or reproduction — weekly/2026-W39.md — candidates C-20260926-04
- 2026-11-01 — WAIT — same data-efficient-selection theme in a new domain (code models); no code or replication; keep scheduled review — weekly/2026-W44.md — candidates C-20261026-09

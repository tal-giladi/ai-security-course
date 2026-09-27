# Learned poison-set selection for LLM backdoors (SAILS)

- **Topic ID:** poison-set-selection-backdoors
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260926-04

## Summary

At fixed poison count and trigger, *which* examples are poisoned swings backdoor ASR from 3% to
80%; SAILS learns a set-level scorer from finetune-and-evaluate runs and improves held-out ASR by
~30pp over influence-function baselines (author claims).

## Evidence

- https://arxiv.org/abs/2609.15029 — single preprint (2026-09-14); no confirmed code; no independent reproduction.

## What would change the decision

Independent reproduction or code release; then a small lab-11-adjacent exercise (new lab)
comparing random vs scored poison selection at a fixed budget on a CPU-sized model.

## History

- 2026-09-27 — WAIT — credible authors and a teachable lever, but one fresh preprint without code or reproduction — weekly/2026-W39.md — candidates C-20260926-04

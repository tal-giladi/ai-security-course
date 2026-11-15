# Training-free neuron-edit backdoors in agent models (Lazarus)

- **Topic ID:** training-free-neuron-edit-backdoor
- **Status:** WAIT
- **Next review:** 2027-01-10
- **Course change:** none
- **Candidates:** C-20261113-01

## Summary

A closed-form weight edit of fewer than ten dormant final-block FFN neurons makes an agent model emit
a payload whenever a trigger string appears in its context, with no training data or pipeline access:
each neuron promotes one payload token through its residual-stream contribution. Reported on
Nemotron-Terminal-8B (7 neurons, ≥98.8% triggered emission, no observed leakage on benign
trajectories) and claimed for Qwen3.6-27B and Gemma-4-31B-IT; a no-reference detector flags 91.4% of
edited checkpoints at 9.7% FPR. Moves the sleeper-agent threat of 11.1 from training-time poisoning
to a cheap supply-chain/insider edit that is structurally local and so also detectable by weight
diffing.

## Evidence

- https://arxiv.org/abs/2611.15118 — single preprint (Zeng, Severi, Bullwinkel, Horvitz, Papailiopoulos), 50 pages, abstract only, no code. The abstract's illustrative payload is a download-and-execute command; recorded as described, nothing run.

## What would change the decision

Code release or independent reproduction. Teachable form: an 11.1 / 13.1 extension on a tiny CPU
transformer (hand-write one dormant MLP neuron so a trigger promotes an inert marker token; detect by
diffing activation statistics against the base and by a dormant-neuron/unembedding-norm heuristic;
measure detector FP on benign fine-tunes). Pairs with backdoor-persistence-and-trigger-variants
(weight-editing defenses rebound).

## History

- 2026-11-15 — WAIT — a concrete, low-bar mechanism with a measured detector, but one abstract-only preprint with no code — weekly/2026-W46.md — candidates C-20261113-01

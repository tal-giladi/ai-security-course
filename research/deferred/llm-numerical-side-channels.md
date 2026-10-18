# Numerical & physical side channels on LLM serving (logit/token recovery)

- **Topic ID:** llm-numerical-side-channels
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261014-03, C-20261015-12

## Summary

Two independent side-channel results the course's extraction/inversion material does not cover.
(1) A floating-point bias-addition numerical side channel recovers exact logits from bias-only APIs
on real serving stacks (vLLM, SGLang, llama.cpp), validated across 11 checkpoints / 7 families, with
a stated and tested mitigation (subtract max before bias addition). (2) A physical EM side channel
reconstructs output tokens and user prompts from a Raspberry Pi running LLaMA-3.2-1B with no logical
access — undercutting "run it on-device so nothing leaves the boundary." Together they generalise the
extraction threat model to the serving stack and the hardware.

## Evidence

- https://arxiv.org/abs/2610.16790 — Chen, Gong; exact-recovery against named real serving stacks; mitigation tested; single preprint, no code confirmed.
- https://arxiv.org/abs/2610.14215 — Alhalawani, Acar, Liu, Batina; passive EM, concrete cheap hardware; single preprint, no code confirmed.

## What would change the decision

Released code for the logit channel (a CPU-feasible toy bias-only API + the subtract-max mitigation
is a clean M12 extension); independent reproduction. The EM channel likely stays a pointer (EM-probe
hardware is out of scope for a CPU-only course) unless a timing/power proxy reproduction is scoped.

## History

- 2026-10-18 — WAIT — the logit-leakage result is strong and teachable (real stacks, tested mitigation) and pairs with the EM channel as "on-device/serving moves the boundary, it does not remove it"; both single preprints without code; ADD budget used on skill-trust-boundary — weekly/2026-W42.md — candidates C-20261014-03, C-20261015-12

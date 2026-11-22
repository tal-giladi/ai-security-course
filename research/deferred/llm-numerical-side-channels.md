# Numerical & physical side channels on LLM serving (logit/token recovery)

- **Topic ID:** llm-numerical-side-channels
- **Status:** WAIT
- **Next review:** 2027-01-03
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
- Cross-reference: the serving-stack timing channel (shared prefix cache, C-20261118-01) was added to the course this week as lesson 15.2 (`research/accepted/prefix-cache-timing-side-channel.md`); a future logit-channel extension would sit next to it in M12/M15. Added 2026-11-22.

## What would change the decision

Released code for the logit channel (a CPU-feasible toy bias-only API + the subtract-max mitigation
is a clean M12 extension); independent reproduction. The EM channel likely stays a pointer (EM-probe
hardware is out of scope for a CPU-only course) unless a timing/power proxy reproduction is scoped.

## History

- 2026-10-18 — WAIT — the logit-leakage result is strong and teachable (real stacks, tested mitigation) and pairs with the EM channel as "on-device/serving moves the boundary, it does not remove it"; both single preprints without code; ADD budget used on skill-trust-boundary — weekly/2026-W42.md — candidates C-20261014-03, C-20261015-12
- 2026-11-22 — WAIT — folded into this week's prefix-cache decision as a related serving-stack side channel; the logit/EM results are still single preprints without code, so no change; 15.2 now gives the course its side-channel lesson to extend — next review 2027-01-03 — weekly/2026-W47.md — no new candidate

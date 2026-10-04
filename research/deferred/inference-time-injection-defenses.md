# Inference-time / modality injection defenses (activation steering, render-before-reading)

- **Topic ID:** inference-time-injection-defenses
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20260930-01, C-20260930-02

## Summary

Two structurally novel indirect-injection defenses with stated costs. CounterSteer: subtract a
residual-stream "instruction-following" direction from tool-result tokens at prefill — no fine-tune,
no detector; held-out ASR 0.21–1.00 → 0.00–0.17, utility 93–100%, vs competitors that lose 22–89%
utility or change weights. Render Before Reading: rasterise untrusted content to an image to exploit
the text-vs-non-text safety gap; holds against adaptive/human attackers across 10 models, and the
paper characterises its own erosion (fine-tuning on rendered instructions closes the gap). Both fit
M05/M06/M20/M24 and the guarantee-box "defense with a stated cost + how it erodes" pattern.

## Evidence

- https://arxiv.org/abs/2609.36570 — CounterSteer (Russinovich). https://arxiv.org/abs/2609.36121 — Render Before Reading (Tramèr group).

## What would change the decision

Independent replication or released code. Either is a good M05/M06 lab extension once validated;
CounterSteer also needs model-internals access the course's toy shim may need to emulate.

## History

- 2026-10-04 — WAIT — thorough single-paper evaluations from known researchers, but no independent replication; ADD budget used — weekly/2026-W40.md — candidates C-20260930-01, C-20260930-02

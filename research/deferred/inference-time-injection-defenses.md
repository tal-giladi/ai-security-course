# Inference-time / modality injection defenses (activation steering, render-before-reading)

- **Topic ID:** inference-time-injection-defenses
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20260930-01, C-20260930-02, C-20261026-07, C-20261027-03, C-20261031-03

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
- https://arxiv.org/abs/2610.32182 — Depth-dependent safety geometry in VLMs: early-vision-layer steering controls refusal 6% ↔ 96% on Qwen3-VL-4B (NeurIPS 2026 workshop, no code). Caution: the steering lever used as a defense also works as an attack. Added 2026-11-01.
- https://arxiv.org/abs/2610.35043 — Steering-plugin supply chain: audit of 8 activation-steering plugin libraries; a PoC plugin keeps refusing harmful requests while steering unrelated outputs (up to 97.8% manipulation ASR) (preprint, no code). A steering defense is itself a supply-chain component. Added 2026-11-01.
- https://arxiv.org/abs/2610.39758 — SEAL sealed-query local sanitization of tool outputs with a frozen model: AgentDojo ASR 34.6% → 0.1%, joint utility 51.4% → 77.5%, ~127× fewer defense tokens than PISanitizer (preprint, no code). Added 2026-11-01.

## What would change the decision

Independent replication or released code. Either is a good M05/M06 lab extension once validated;
CounterSteer also needs model-internals access the course's toy shim may need to emulate.

## History

- 2026-10-04 — WAIT — thorough single-paper evaluations from known researchers, but no independent replication; ADD budget used — weekly/2026-W40.md — candidates C-20260930-01, C-20260930-02
- 2026-11-01 — WAIT — the cluster grows (sanitization, steering) and gains attack-side cautions; none has code or replication yet; keep scheduled review — weekly/2026-W44.md — candidates C-20261026-07, C-20261027-03, C-20261031-03

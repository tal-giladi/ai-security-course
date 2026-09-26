# Lab 09 — Adversarial examples: FGSM & PGD from scratch

**Module:** 09 (Stage 4 · adversarial ML). **Time:** ~2.5 h. **Hardware:** CPU torch, no download
(synthetic data). **Targets:** a local toy classifier; a controlled experiment.

## Goal

Reproduce the foundational adversarial-ML result: a model with high clean accuracy collapses to
~chance under input perturbations *within* an L-infinity budget. Implement **FGSM** (one-step) and
**PGD** (iterated, projected) from scratch, measure the collapse, then defend with **PGD
adversarial training** and quantify the robustness/clean-accuracy trade-off.

## Run

```bash
py labs/lab-09/adv.py         # STD clean 0.91 -> PGD ~0.53; ADV-trained clean ~0.83, PGD ~0.62
py -m pytest labs/lab-09 -q   # ~10s
```

## The math (in `adv.py`)

- **FGSM:** $x' = \mathrm{clip}(x + \epsilon\,\mathrm{sign}(\nabla_x \ell))$ — one step along the
  loss gradient's sign, the maximizer of the first-order loss increase inside the $\ell_\infty$ ball.
- **PGD:** iterate $x^{t+1} = \Pi_{\mathcal B_\epsilon(x)\cap[0,1]}\big(x^t + \alpha\,\mathrm{sign}(\nabla_x\ell)\big)$
  — projected gradient ascent on the loss; strictly $\ge$ FGSM in attack strength.
- **PGD adversarial training (Madry):** train on PGD examples — a min-max objective
  $\min_\theta \mathbb E\,[\max_{\delta\in\mathcal B_\epsilon}\ell(\theta,x+\delta,y)]$.

## What to notice

- A **tiny** perturbation (per-feature $\le\epsilon$) flips predictions: high clean accuracy says
  nothing about robustness. Different threat model = different security property (02.1).
- **PGD $\ge$ FGSM:** more steps find stronger perturbations; single-step robustness can be
  illusory (gradient masking). Always evaluate with a strong attack.
- **Trade-off:** adversarial training raises robust accuracy but lowers clean accuracy — there is
  no free robustness. Quantify it, don't assume it.

## Exercise

See [Lesson 09.1](../../lessons/module-09/lesson-01.md): derive FGSM as the $\ell_\infty$ maximizer;
plot the accuracy-vs-$\epsilon$ curve for FGSM and PGD; sweep PGD steps to show convergence; do the
adversarial-training trade-off curve; test for gradient masking; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs `adv.py` (torch image) with no egress.

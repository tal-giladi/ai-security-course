# Lab 12 — Membership inference, model extraction & differential privacy

**Module:** 12 (Stage 5). **Time:** ~2.5 h. **Hardware:** CPU torch, no download. Synthetic data;
no real personal data.

## Goal

Three privacy attacks + a mitigation, all measured:
1. **Membership inference (MI):** decide "was this sample in the training set?" — measured as
   ROC-AUC (0.5 = no leak). Overfitting leaks membership (members get lower loss).
2. **Model extraction:** query a black-box teacher, train a student to mimic it; measure fidelity.
3. **Differential privacy (DP-SGD):** per-example gradient clipping + Gaussian noise reduces the MI
   AUC toward 0.5 — at a cost to accuracy (the privacy/utility trade-off).

## Run

```bash
py labs/lab-12/privacy.py     # overfit MI AUC ~0.64; DP MI ~0.59 (acc 0.83->0.74); extraction fidelity ~0.7
py -m pytest labs/lab-12 -q   # ~12s
```

## What to notice

- **Overfitting is a privacy leak.** The generalization gap *is* the membership signal; the
  loss-threshold attack turns it into an AUC.
- **The loss-threshold attack is weak; LiRA is strong.** Per-example calibration with shadow models
  (Carlini et al., 2022) lifts AUC well above the loss threshold — the exercise builds it.
- **DP has a cost.** DP-SGD provably bounds each example's influence, lowering MI — but clipping +
  noise reduce accuracy. There is no free privacy.
- **Black-box ≠ safe.** Enough queries reconstruct a usable copy of the model (IP/privacy risk).

## Exercise

See [Lesson 12.1](../../lessons/module-12/lesson-01.md): plot MI AUC vs overfitting (train size /
epochs); implement **LiRA** (shadow models + per-example likelihood ratio) and beat the loss
threshold; measure extraction fidelity vs query budget and vs hard-label/soft-label access; sweep
the DP noise multiplier to trace the privacy(MI)-utility(accuracy) frontier; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs `privacy.py` (torch image), no egress.

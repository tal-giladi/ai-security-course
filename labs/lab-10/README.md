# Lab 10 — CW, transfer attacks & certified robustness

**Module:** 10 (Stage 4). **Time:** ~2.5 h. **Hardware:** CPU torch, no download. Builds on Lab 09.

## Goal

Move past "run PGD once" to the three ideas that define serious adversarial ML:
1. **CW** (Carlini-Wagner) — optimize a *minimal-norm* perturbation with a margin loss (smaller,
   higher-confidence adversarials than fixed-eps sign attacks).
2. **Transfer** — perturbations crafted on model A fool a different model B (the black-box threat).
3. **Certified robustness** via **randomized smoothing** — a *proof* that no L2 perturbation within
   a radius can change the smoothed prediction. "No attack exists", not "I couldn't find one".

## Run

```bash
py labs/lab-10/adv2.py        # CW L2 ~0.27; transfer ~0.98; ~45/50 points certified
py -m pytest labs/lab-10 -q
```

## What to notice

- **CW vs PGD:** CW minimizes perturbation size instead of fixing eps, exposing how *little* change
  a robust-looking model really tolerates.
- **Transfer is the black-box threat:** you don't need the target's gradients if a surrogate's
  adversarials transfer (ties to GCG transfer, Lab 07).
- **Empirical vs certified:** Lab 09's adversarial training is *empirical* (no attack found within
  a budget by *these* attacks). Randomized smoothing is *certified* (a mathematical guarantee) —
  but only for L2, and at a cost to clean accuracy and inference (Monte-Carlo sampling).

## Exercise

See [Lesson 10.1](../../lessons/module-10/lesson-01.md): compare CW L2 vs PGD-found perturbation
sizes; measure transfer as a function of model similarity; derive the smoothing certificate
$R=\sigma\,\Phi^{-1}(\underline{p_A})$ and empirically confirm no attack within $R$ succeeds; plot
the certified-accuracy-vs-radius curve and the $\sigma$ trade-off; note AutoAttack as the standard
empirical evaluation; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs `adv2.py` (torch image) with no egress.

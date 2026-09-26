# Croce & Hein — *Reliable Evaluation of Adversarial Robustness with an Ensemble of Diverse Parameter-free Attacks* (AutoAttack, 2020)

**arXiv:** [2003.01690](https://arxiv.org/abs/2003.01690) · ICML '20. **Module:** [10.1](../lessons/module-10/lesson-01.md), [24.1](../lessons/module-24/lesson-01.md). **Lab:** [Lab 10](../labs/lab-10/README.md).

## Why it matters
AutoAttack is the paper that turned "measuring robustness" into a *protocol* instead of a coin flip. It showed that a large fraction of published defenses had overstated robustness because they evaluated against a single, poorly-tuned attack — and it fixed the incentive with a **parameter-free ensemble** (APGD-CE, APGD-DLR, FAB, Square) that needs no per-defense tuning. For a purple-team engineer, this is the canonical answer to "how do I know my defense number is real?"

## Prerequisites
- This course: [09.1 PGD](../lessons/module-09/lesson-01.md), [10.1 C&W/certification](../lessons/module-10/lesson-01.md).
- Eval literacy: robustness curves, gradient masking.

## What to understand
- **Parameter-free APGD:** an automatic step-size schedule removes the biggest source of under-powered PGD evaluations (bad learning rate).
- **Diversity beats depth:** white-box (APGD variants) + black-box (Square) catches gradient-masking defenses that fool any single gradient attack.
- **Robust accuracy = min over the ensemble** — you report the *worst case an attacker finds*, not the best case your favorite attack missed.

## Which sections to read
- §3 (APGD + DLR loss) — why the tuning-free schedule matters.
- §4 (the ensemble composition) and §5 (the re-evaluation of prior defenses) — the sobering table.

## Experiment to reproduce (locally)
In Lab 10, build a mini-AutoAttack: run APGD-style (auto step size), C&W, and a query-based Square-style attack against your model, and report robust accuracy as the **minimum** across them. Take a "defended" model that scores well under weak PGD and show a stronger ensemble member drops its robust accuracy — the paper's finding in miniature.

## Code to implement
- An auto-step-size PGD (APGD-lite) and a simple black-box Square-style attack (in the lab).
- The min-over-attacks robust-accuracy reporter — wire it into [`evalkit`](../lab/attack-tools/evalkit.py).

## Limitations
- $L_p$-bounded threat model only; doesn't cover semantic/unrestricted perturbations.
- An ensemble is a strong *lower bound* on vulnerability, still not a certificate.

## What later research changed
- Standardized robustness leaderboards (RobustBench) adopted it as the default protocol.
- Reinforces the course's evaluation-integrity thread ([24.1](../lessons/module-24/lesson-01.md)): report the worst case, with confidence intervals.

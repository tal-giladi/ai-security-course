# Shokri et al. — *Membership Inference Attacks Against Machine Learning Models* (2016)

**arXiv:** [1610.05820](https://arxiv.org/abs/1610.05820) · IEEE S&P '17. **Module:** [12.1](../lessons/module-12/lesson-01.md). **Lab:** [Lab 12](../labs/lab-12/README.md).

## Why it matters
Membership inference (MI) asks the sharpest privacy question: *was this exact record in the training set?* Shokri et al. showed the answer leaks from a model's outputs — because models are more confident on data they memorized. MI is the empirical bridge from "privacy" to a measurable attack, the standard yardstick for whether a defense (like DP-SGD) actually protects data, and the conceptual root of training-data extraction from LLMs.

## Prerequisites
- Sibling course: overfitting/generalization, softmax confidence.
- This course: [02.2](../lessons/module-02/lesson-02.md), [12.1](../lessons/module-12/lesson-01.md); base-rate/precision reasoning from [24.1](../lessons/module-24/lesson-01.md).

## What to understand
- **Shadow models:** train models mimicking the target on known in/out splits, then train an **attack classifier** to map (output confidence vector → member/non-member).
- **Overfitting is the leak:** the member/non-member confidence gap tracks the generalization gap — a privacy/utility connection, not an accident.
- **Metrics matter:** evaluate at low false-positive rates, not just AUC — a lesson later papers made central.

## Which sections to read
- §4 (shadow-model construction + attack model), §6 (what drives leakage: overfitting, class count).

## Experiment to reproduce (locally)
Lab 12 reproduces MI on a synthetic model tuned (small $n$, label noise) to leak: compute a per-example membership score (loss/confidence), plot the member-vs-non-member distributions, and report **ROC-AUC via the tie-averaged Mann-Whitney** statistic from [`evalkit`](../lab/attack-tools/evalkit.py). Then train with **DP-SGD** (clip + noise) and show the AUC collapse toward chance — at an accuracy cost.

## Code to implement
- Membership scoring + shadow/attack split; ROC-AUC and TPR@low-FPR (in the lab).
- A DP-SGD training loop (per-example clipping + Gaussian noise) and the privacy/utility trade-off curve.

## Limitations
- Shadow models assume data/architecture knowledge; loss-threshold attacks are weaker but assumption-free.
- AUC hides the operationally important low-FPR regime (the LiRA critique).

## What later research changed
- **Carlini et al., LiRA — *Membership Inference Attacks From First Principles*** ([2112.03570](https://arxiv.org/abs/2112.03570)) recast MI as a per-example **likelihood-ratio** test evaluated at low FPR — far stronger; the lab notes this as the modern method.
- Feeds directly into **training-data extraction** ([14](14-carlini-extracting.md)).

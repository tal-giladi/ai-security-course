# Carlini & Wagner — *Towards Evaluating the Robustness of Neural Networks* (C&W, 2016)

**arXiv:** [1608.04644](https://arxiv.org/abs/1608.04644) · IEEE S&P '17. **Module:** [10.1](../lessons/module-10/lesson-01.md). **Lab:** [Lab 10](../labs/lab-10/README.md).

## Why it matters
C&W is both a *stronger attack* and a *methodology lesson*. It formulates adversarial-example generation as a smooth optimization (minimize perturbation size subject to misclassification, via a differentiable surrogate objective and a change-of-variables to enforce box constraints) and used it to **break defensive distillation** — a defense that had looked strong against weaker attacks. Its enduring contribution is the discipline: **a defense is only as good as the strongest adaptive attack you tried against it.**

## Prerequisites
- This course: [09.1 FGSM/PGD](../lessons/module-09/lesson-01.md).
- Math: Lagrangian relaxation, the $\tanh$ change-of-variables, margin/hinge losses.

## What to understand
- **The objective:** minimize $\lVert\delta\rVert_p + c\cdot f(x+\delta)$ where $f$ is a surrogate that is $\le 0$ iff misclassified (the $Z$-logit margin objective, not cross-entropy). Binary-search $c$.
- **Box constraints via** $x+\delta = \tfrac12(\tanh(w)+1)$ — optimize unconstrained $w$.
- **Adaptive evaluation:** they *rederived* the attack against the specific defense (distillation) — the reason "we tested against FGSM" is not evidence of robustness.
- $L_0/L_2/L_\infty$ variants — the norm is part of the threat model.

## Which sections to read
- §IV (the three attacks, the objective, the change-of-variables).
- §V–VI (breaking distillation) — read as a template for adaptive attacks.

## Experiment to reproduce (locally)
Lab 10 implements the C&W $L_2$ attack from scratch on the synthetic model: the surrogate objective, the $\tanh$ reparam, and the binary search over $c$. Show it finds smaller-norm perturbations than PGD, and show it defeating a toy "masked-gradient" defense that PGD alone made look safe.

## Code to implement
- The C&W $L_2$ objective + $\tanh$ box constraint + binary search over $c$ (in the lab).
- A gradient-masking "defense" and the demonstration that C&W bypasses it — the adaptive-attack point.

## Limitations
- Slower than PGD (optimization + binary search) — use it to *audit*, PGD to train.
- Per-example; not a universal or transfer attack by default.

## What later research changed
- **AutoAttack** ([09](09-croce-autoattack.md)) — standardized the "don't trust one attack" lesson into a parameter-free ensemble.
- Motivated **certified** robustness ([10.1](../lessons/module-10/lesson-01.md)) — the only escape from the attack/defense arms race.

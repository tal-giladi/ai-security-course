# Madry et al. — *Towards Deep Learning Models Resistant to Adversarial Attacks* (PGD, 2017)

**arXiv:** [1706.06083](https://arxiv.org/abs/1706.06083). **Module:** [09.1](../lessons/module-09/lesson-01.md), [10.1](../lessons/module-10/lesson-01.md). **Lab:** [Lab 09](../labs/lab-09/README.md).

## Why it matters
This paper gave adversarial robustness its organizing principle: a **min-max (saddle-point) formulation** — minimize expected loss under the *worst-case* bounded perturbation. PGD (Projected Gradient Descent) is the strong first-order attack that solves the inner max, and **PGD adversarial training** remains the most reliable empirical defense a decade later. It turns "patch attacks as they appear" into "optimize against the strongest attacker in your threat model."

## Prerequisites
- This course: [09.1 FGSM](../lessons/module-09/lesson-01.md) (PGD is iterated, projected FGSM).
- Math comfort: constrained optimization, projection onto an $\epsilon$-ball.

## What to understand
- **The objective:** $\min_\theta \mathbb{E}\big[\max_{\lVert\delta\rVert\le\epsilon} L(\theta, x+\delta, y)\big]$ — the inner max is the attack, the outer min is training.
- **PGD:** iterate $x^{t+1} = \Pi_{B_\epsilon(x)}\big(x^t + \alpha\,\operatorname{sign}(\nabla_x L)\big)$ with random restarts — take signed steps, project back into the ball each time.
- **PGD as a "universal" first-order adversary:** training against it confers robustness to weaker first-order attacks; robustness scales with capacity.

## Which sections to read
- §2 (the saddle-point formulation) — the whole conceptual contribution.
- §3 (PGD, random restarts) and §4 (capacity + robustness) — the practical recipe.

## Experiment to reproduce (locally)
Lab 09 implements PGD from scratch (iterate, project, restart) on the synthetic MLP and compares its robustness curve to FGSM's — PGD finds adversarial examples FGSM misses at the same $\epsilon$. Then run PGD adversarial training and show the model that looked robust to FGSM is measured properly by PGD.

## Code to implement
- PGD with projection onto the $L_\infty$ ball + random restarts (in the lab).
- PGD adversarial training; FGSM-vs-PGD robustness-curve comparison.

## Limitations
- Empirical, not certified — no proof, and stronger/adaptive attacks can still win.
- Expensive (inner loop per step); robustness costs clean accuracy.

## What later research changed
- **Certified defenses** (randomized smoothing, $R=\sigma\Phi^{-1}(p_A)$) give provable radii — [10.1](../lessons/module-10/lesson-01.md).
- **AutoAttack** ([09](09-croce-autoattack.md)) — even PGD, tuned wrong, overstates robustness; use an ensemble.

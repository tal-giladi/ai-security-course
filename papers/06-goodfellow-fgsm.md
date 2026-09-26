# Goodfellow, Shlens & Szegedy — *Explaining and Harnessing Adversarial Examples* (FGSM, 2014)

**arXiv:** [1412.6572](https://arxiv.org/abs/1412.6572). **Module:** [09.1](../lessons/module-09/lesson-01.md). **Lab:** [Lab 09](../labs/lab-09/README.md).

## Why it matters
The foundational adversarial-ML paper. Its claim reframed the field: adversarial examples arise not from exotic nonlinearity but from models being **too linear** in high dimensions — tiny per-coordinate perturbations sum to a large change in the logit. It gives you FGSM (the one-step attack everything else generalizes), the linear explanation, and adversarial training as the first defense. Everything in M09–M10 is a refinement of ideas here.

## Prerequisites
- Sibling course: gradients, softmax classifiers, backprop.
- This course: none beyond [00.1](../lessons/module-00/lesson-01.md); this is the ML-security starting point.

## What to understand
- **FGSM:** $x' = x + \epsilon\,\operatorname{sign}(\nabla_x J(\theta,x,y))$ — move each input coordinate by $\epsilon$ in the direction that increases loss. One step, $L_\infty$-bounded.
- **The linear explanation:** a perturbation $\eta$ with $\lVert\eta\rVert_\infty\le\epsilon$ changes a linear unit's activation by up to $\epsilon\lVert w\rVert_1$, which grows with dimension — small $\epsilon$, large effect.
- **Adversarial training:** augment with FGSM examples; a regularizer, not a cure.
- Transferability: adversarial examples cross models — a consequence of shared linear structure.

## Which sections to read
- §3 (linear explanation) and §4 (FGSM) — the conceptual + algorithmic core.
- §5 (adversarial training) — the first defense and its limits.

## Experiment to reproduce (locally)
Lab 09 implements FGSM from scratch on a synthetic MLP (CPU): compute the input gradient, take the signed step, sweep $\epsilon$, and plot accuracy-vs-$\epsilon$ (the robustness curve). Then adversarially train and re-measure — the curve shifts but never flattens to the clean line.

## Code to implement
- FGSM by hand (input-gradient sign step); the $\epsilon$-sweep robustness curve.
- A one-epoch adversarial-training loop and the before/after curve.

## Limitations
- FGSM is a *weak* attack (single step); robustness to FGSM is not robustness (gradient masking gives false security — the M10 lesson).
- The linear story is intuition, not a full theory.

## What later research changed
- **Madry (PGD)** ([07](07-madry-pgd.md)) — multi-step FGSM as a proper inner-max; the strong first-order attack.
- **C&W** ([08](08-carlini-wagner.md)) — optimization attacks that break defenses claiming FGSM-robustness.
- **AutoAttack** ([09](09-croce-autoattack.md)) — why single-attack evaluation lies.

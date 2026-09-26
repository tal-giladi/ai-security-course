<div class="prereq">

**Prerequisites.** **Sibling course:** gradients/backprop (M02), optimization (M03),
softmax/cross-entropy (M01), a training loop (M00/M07). [02.1](../module-02/lesson-01.md) for
"different threat model = different security property". Lab: CPU torch, no download.

**You will learn.** The mathematical core of adversarial machine learning: the adversarial-example
problem, **threat models** ($\ell_\infty/\ell_2$ balls), **FGSM** and **PGD** derived and
implemented from scratch, the robustness/accuracy trade-off, and **adversarial training** as a
min–max defense (plus how it fails — gradient masking).

**Why this matters.** Adversarial examples are the foundation under multimodal attacks (M20),
transfer attacks, and even the GCG view of jailbreaks (M07). The mathematics here — perturb an
input within a bounded budget to maximize loss — is the same optimization you have been meeting in
token space, now in its original, cleanest continuous form.

</div>

# 09.1 · Adversarial examples I (FGSM & PGD)

## Why this matters

In 2014 it became clear that image classifiers with superhuman accuracy could be fooled by
perturbations invisible to humans. That result reframed ML security: **accuracy is not
robustness**, and a model's behavior can be steered by an adversary optimizing within a small,
formally-specified budget. Every later attack in this course is a variant of this idea; learning it
in its original continuous form makes the token-space versions (GCG) obvious in hindsight.

## Learning objectives

1. State the adversarial-example problem and its **threat model** precisely ($\ell_p$ ball,
   perturbation budget $\epsilon$, targeted vs untargeted, white/black-box).
2. Derive **FGSM** as the exact maximizer of the first-order loss increase in an $\ell_\infty$ ball.
3. Derive and implement **PGD** as projected gradient ascent; explain why PGD $\ge$ FGSM.
4. Measure the accuracy-vs-$\epsilon$ collapse and implement **PGD adversarial training**.
5. Explain the robustness/accuracy trade-off and detect **gradient masking** (why single-step
   robustness can be illusory).

## Concept

### The problem and the threat model

Given a classifier $f_\theta$, an input $x$ with true label $y$, find a perturbation $\delta$ that
changes the prediction while staying "imperceptible", formalized as a budget:

$$ \max_{\delta}\; \ell\big(f_\theta(x+\delta), y\big) \quad\text{s.t.}\quad \|\delta\|_p \le \epsilon,\; x+\delta \in \mathcal X. $$

The **threat model** is the whole game. It specifies:
- **Norm** $\|\cdot\|_p$: $\ell_\infty$ (each feature changes by $\le\epsilon$ — the classic
  imperceptible-pixel model), $\ell_2$ (bounded energy), $\ell_0$ (few features changed).
- **Budget** $\epsilon$: how much perturbation is "allowed".
- **Targeted** (force a specific class) vs **untargeted** (any misclassification).
- **Access**: white-box (gradients available) vs black-box (queries only, Module 10).
- **Domain** $\mathcal X$: valid inputs (e.g. pixels in $[0,1]$) — perturbations must stay legal.

A robustness claim is meaningful *only* relative to a stated threat model. "Robust" with no
threat model is marketing.

### FGSM — the one-step $\ell_\infty$ maximizer

For a small $\delta$, a first-order Taylor expansion gives
$\ell(f(x+\delta),y) \approx \ell(f(x),y) + \nabla_x\ell^\top\delta$. To maximize the linear term
subject to $\|\delta\|_\infty \le \epsilon$, put each coordinate at its extreme in the gradient's
direction:

$$ \delta^\star = \epsilon\,\operatorname{sign}(\nabla_x\ell) \quad\Rightarrow\quad
x_{\text{adv}} = \operatorname{clip}_{\mathcal X}\big(x + \epsilon\,\operatorname{sign}(\nabla_x\ell)\big). $$

That is FGSM (Goodfellow et al., 2015): a *single* gradient sign step. It is optimal for the linear
approximation; because networks are non-linear, one step is not optimal for the true loss — hence
PGD.

### PGD — iterated, projected

Do FGSM repeatedly with a small step $\alpha$, projecting back onto the $\ell_\infty$ ball and the
valid domain after each step:

$$ x^{t+1} = \Pi_{\mathcal B_\epsilon(x)\,\cap\,\mathcal X}\Big(x^{t} + \alpha\,\operatorname{sign}\big(\nabla_x \ell(f(x^t),y)\big)\Big), $$

starting from a random point in the ball. $\Pi$ is projection: clamp each coordinate to
$[x_i-\epsilon, x_i+\epsilon]$ and to the domain. PGD is projected gradient *ascent* on the loss,
the standard "strong" first-order attack (Madry et al., 2018). By construction PGD $\ge$ FGSM in
attack strength (FGSM is PGD with one step and no restart), so **always evaluate robustness with
PGD (or stronger), never FGSM alone.**

### Adversarial training — the min–max defense

Madry framed defense as a saddle-point problem: train the model to minimize the loss *against the
worst-case perturbation*:

$$ \min_\theta\ \mathbb E_{(x,y)}\Big[\max_{\|\delta\|_\infty\le\epsilon}\ \ell\big(f_\theta(x+\delta),y\big)\Big]. $$

Approximate the inner max with PGD, then take a gradient step on $\theta$ — i.e. **train on PGD
adversarial examples**. This is the strongest general empirical defense, and it has a price:
robust accuracy rises, clean accuracy falls, and training costs more (a PGD loop per step).

## Intuition

Picture the loss as a landscape over input space; the model classifies correctly in a valley
around $x$. FGSM takes one big step in the steepest uphill direction (toward misclassification),
bounded by the $\epsilon$ box. If the landscape curves, one step overshoots or under-shoots — PGD
walks uphill in small steps, staying inside the box, and reliably reaches a higher point (a
stronger attack). Adversarial training reshapes the landscape so the valley is *wide* — no point
within $\epsilon$ of a training example climbs out — but flattening the landscape everywhere costs
some of the sharp fitting that gave high clean accuracy.

## Technical explanation & Code

`labs/lab-09/adv.py` implements all of the above in ~60 lines. Note the three projections that make
the attack *legal*: (1) clamp the perturbation to the $\ell_\infty$ ball, (2) clamp the input to
$[0,1]$, (3) random start for PGD. The lab measures three numbers per model: clean, FGSM, PGD
accuracy, and compares a standard vs an adversarially-trained model.

Observed (eps = 0.05, $\ell_\infty$): standard model **clean 0.91 → PGD 0.53** (collapse to near
chance); adversarially-trained **clean 0.83, PGD 0.62** — robustness up, clean accuracy down. The
trade-off is not a bug; it is the current state of the field.

## Mathematics

**Why $\operatorname{sign}$, and why $\ell_\infty$.** Maximizing $\nabla^\top\delta$ subject to a
norm constraint is a dual-norm problem: the maximizer's shape is set by the constraint norm. For
$\ell_\infty$ ($\|\delta\|_\infty\le\epsilon$) the maximizer is $\epsilon\,\operatorname{sign}(\nabla)$
(each coordinate maxed independently). For $\ell_2$ ($\|\delta\|_2\le\epsilon$) it is
$\epsilon\,\nabla/\|\nabla\|_2$ (steepest ascent, normalized). Choosing the norm chooses the attack
geometry — a fact you'll use when reading any adversarial-ML paper.

**PGD $\ge$ FGSM, formally.** FGSM is the single-step, zero-restart special case of PGD; PGD
explores a superset of iterates, so $\max$-over-iterates loss $\ge$ FGSM loss, hence attacked
accuracy under PGD $\le$ under FGSM. This is why reporting only FGSM robustness overstates security.

**Gradient masking.** A model can *appear* robust to FGSM/PGD by having uninformative or shattered
gradients (e.g. saturated units), so the attack can't find the perturbation — yet a black-box or
gradient-free attack still succeeds. Signs: FGSM robustness ≫ PGD robustness, or robustness that
vanishes under a transfer attack (Module 10). Real robustness degrades gracefully with $\epsilon$
and step count; masked robustness collapses under a stronger/black-box attack.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — PGD adversarial training.**
- **Stops:** perturbations within the *trained* threat model ($\ell_\infty$, radius $\le\epsilon$) —
  empirically the strongest general defense; robust accuracy rises substantially.
- **Does NOT stop:** perturbations *outside* the trained threat model (larger $\epsilon$, a
  different norm $\ell_2/\ell_0$, semantic/spatial changes), and it does not *prove* robustness
  (empirical, not certified — Module 10 covers certification).
- **Attacker adapts:** switch norm, exceed the trained $\epsilon$, use unforeseen perturbation
  types, or attack where clean accuracy dropped.
- **FP/utility cost:** lower clean accuracy (the trade-off). **Perf:** training is $\sim$(PGD
  steps)× more expensive; inference unchanged.
- **Takeaway:** robustness is *relative to a threat model you chose*; state it, and don't
  generalize a claim beyond the norm/$\epsilon$ you actually trained and tested.

</div>

## Practical lab

<div class="lab">

**Lab 09** ([`labs/lab-09/`](../../labs/lab-09/README.md)) — FGSM/PGD from scratch + adversarial
training. CPU torch, ~10s tests.

```bash
py labs/lab-09/adv.py
py -m pytest labs/lab-09 -q
```

</div>

## Exercise

1. **Derive & verify FGSM.** Show $\arg\max_{\|\delta\|_\infty\le\epsilon}\nabla^\top\delta =
   \epsilon\operatorname{sign}(\nabla)$. In code, confirm FGSM increases the loss and that the
   perturbation respects the box.
2. **Accuracy–$\epsilon$ curve.** Plot clean/FGSM/PGD accuracy vs $\epsilon\in[0,0.2]$ for the
   standard model. Identify the $\epsilon$ where accuracy hits chance. Explain the curve's shape.
3. **PGD convergence.** Sweep PGD steps $\in\{1,5,10,20,40\}$; show attacked accuracy decreases and
   plateaus. Confirm PGD $\le$ FGSM accuracy at every $\epsilon$.
4. **$\ell_2$ variant.** Implement the $\ell_2$-PGD update ($\delta$ step normalized by
   $\|\nabla\|_2$, project onto the $\ell_2$ ball). Compare which norm's attack is stronger for the
   same nominal $\epsilon$ and explain via the dual-norm argument.
5. **Adversarial training trade-off.** Train models with $\epsilon_{\text{train}}\in\{0,0.03,0.05,0.08\}$;
   plot the (clean accuracy, robust accuracy) frontier. There is no free robustness — quantify the
   cost.
6. **Gradient-masking check (purple team).** Try to make a model *look* robust cheaply (e.g. a
   single-step "FGSM training" or a saturating nonlinearity) and show its FGSM robustness ≫ PGD
   robustness — a masking signature. Then show a stronger attack (more PGD steps / random restarts)
   defeats it. Write the guarantee box distinguishing real from masked robustness.

<details><summary>Hint (step 6)</summary>

FGSM-only adversarial training is a known way to induce gradient masking: the model learns to
defeat the one-step attack specifically, leaving sharp loss curvature that PGD exploits. The tell
is a large FGSM–PGD robustness gap. Real robustness (PGD-AT) shows a small gap and degrades
smoothly with attack strength.

</details>

**Deliverable.** The FGSM derivation + checks, the accuracy–$\epsilon$ and PGD-steps curves, the
$\ell_2$ comparison, the AT trade-off frontier, and the gradient-masking demonstration + guarantee
box.

```bash
py course.py complete 09.1
```

## Research paper

**Goodfellow, Shlens, Szegedy, "Explaining and Harnessing Adversarial Examples" (2015)** and
**Madry et al., "Towards Deep Learning Models Resistant to Adversarial Attacks" (2018).** *Why:*
FGSM and the PGD/adversarial-training framework — the two papers you just implemented. *Read
(Goodfellow):* the linear explanation of adversarial examples and FGSM. *Read (Madry):* the
min–max formulation, PGD as the "ultimate first-order adversary", and the robustness results.
*Reproduce:* you have the core; extend by reproducing their observation that adversarial training's
robustness is threat-model-specific (test a model trained at $\ell_\infty$ against an $\ell_2$
attack). *Limitation/what changed:* empirical robustness ≠ certified (Module 10); AutoAttack (Croce
& Hein) later exposed many "robust" models as gradient-masked — evaluation rigor matters.

## Further reading

- Croce & Hein, **AutoAttack** (2020) — the standard robustness-evaluation ensemble (Module 10).
- NIST AI 100-2 — evasion attacks taxonomy; [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. Why is "the model is robust" meaningless without a threat model?</summary>

Robustness is defined only relative to an allowed perturbation set: the norm ($\ell_\infty/\ell_2/\ell_0$),
the budget $\epsilon$, targeted vs untargeted, access, and valid domain. A model robust to small
$\ell_\infty$ perturbations may be trivially broken by a larger budget, a different norm, or a
semantic change. State the threat model or the claim is empty.

</details>

<details><summary>Q2. Derive FGSM and say why one step isn't optimal for the true loss.</summary>

Maximizing the first-order term $\nabla^\top\delta$ under $\|\delta\|_\infty\le\epsilon$ gives
$\delta=\epsilon\operatorname{sign}(\nabla)$, so $x_{adv}=x+\epsilon\operatorname{sign}(\nabla_x\ell)$.
It is optimal only for the linear approximation; real networks are non-linear, so the true loss is
maximized better by iterating (PGD).

</details>

<details><summary>Q3. Why must robustness be evaluated with PGD, not FGSM?</summary>

FGSM is the one-step, no-restart special case of PGD, so PGD finds perturbations at least as strong;
attacked accuracy under PGD $\le$ under FGSM. A model can look FGSM-robust via gradient masking
(sharp curvature the one-step attack misses) yet fall to PGD or a black-box attack. Reporting FGSM
robustness overstates security.

</details>

<details><summary>Q4. State the adversarial-training objective and its cost.</summary>

$\min_\theta \mathbb E[\max_{\|\delta\|\le\epsilon}\ell(\theta,x+\delta,y)]$ — minimize the
worst-case (PGD-approximated) loss. Cost: lower clean accuracy (robustness/accuracy trade-off),
higher training cost (a PGD loop per step), and robustness only within the trained threat model
(not certified, not transferable to other norms/budgets).

</details>

## What you should now be able to do

- State a precise threat model and derive FGSM as its one-step $\ell_\infty$ maximizer.
- Implement PGD (projected gradient ascent) and explain why it is the correct evaluation attack.
- Run and quantify adversarial training and its robustness/accuracy trade-off.
- Detect gradient masking and evaluate robustness honestly.

## Progress checkpoint

```bash
py course.py complete 09.1
py course.py next
```

**Next:** 10.1 · Adversarial examples II — CW and AutoAttack, transfer & black-box attacks, and
certified robustness (the difference between "I couldn't find an attack" and "no attack exists").

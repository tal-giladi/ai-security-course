<div class="prereq">

**Prerequisites.** [09.1 FGSM/PGD](../module-09/lesson-01.md) (threat models, projected gradient
attacks, adversarial training), sibling optimization/probability. Lab: CPU torch, builds on Lab 09.

**You will learn.** The three ideas that separate rigorous adversarial-ML from running PGD once:
the **Carlini–Wagner (CW)** minimal-norm optimization attack, **transfer / black-box** attacks, and
**certified robustness** (randomized smoothing) — the difference between *"I couldn't find an
attack"* and *"no attack exists"*.

**Why this matters.** Empirical defenses are repeatedly broken by stronger attacks; the field
learned to demand (a) evaluation with strong ensembles (AutoAttack), and (b) *certificates* where
possible. And transfer is the reason black-box systems aren't safe just because their gradients are
hidden — the through-line to GCG transfer (M07) and real deployments.

</div>

# 10.1 · Adversarial examples II (CW, transfer, certified robustness)

## Why this matters

A model can survive FGSM and PGD and still be trivially broken — by a stronger optimizer (CW), by
an attack crafted on a *different* model (transfer), or simply because "we tried and failed" is not
a guarantee. Serious security requires the strongest available attacks for evaluation and, where
you can get them, mathematical guarantees. This lesson gives you both, and the judgment to tell
empirical robustness from certified robustness.

## Learning objectives

1. Formulate and implement the **CW** attack (margin loss + minimal-norm optimization) and explain
   why it finds smaller perturbations than fixed-$\epsilon$ sign attacks.
2. Explain and measure **transfer attacks**; connect to the black-box threat and to GCG transfer.
3. Derive **randomized smoothing** and its **certified $\ell_2$ radius**
   $R=\sigma\,\Phi^{-1}(\underline{p_A})$; implement the Monte-Carlo certificate.
4. Distinguish **empirical** vs **certified** robustness and state the costs of each.
5. Know **AutoAttack** as the standard empirical-evaluation ensemble and why single-attack
   evaluation is untrustworthy.

## Concept

### CW — optimize the perturbation, don't fix its size

FGSM/PGD fix a budget $\epsilon$ and maximize loss. CW (Carlini & Wagner, 2017) inverts it:
*minimize the perturbation* subject to misclassification, via a differentiable surrogate. Untargeted
CW minimizes

$$ \min_\delta\ \|\delta\|_2^2 + c\cdot\max\!\big(0,\ Z(x+\delta)_y - \max_{j\ne y} Z(x+\delta)_j + \kappa\big), $$

where $Z$ are logits, the second term is a **margin** (zero once the true class $y$ is no longer
top by margin $\kappa$), and $c$ balances the two. Optimized with Adam over $\delta$. The result is
the *smallest* perturbation that flips the prediction with confidence $\kappa$ — a much sharper
probe of a model's true robustness than a fixed-$\epsilon$ attack, and the attack that broke many
"defenses" that only ever tested FGSM/PGD.

### Transfer — the black-box threat

Adversarial examples crafted on a **surrogate** model $A$ often fool a target model $B$ the attacker
cannot access, because models trained on similar data learn similar features and decision
boundaries; a perturbation that crosses $A$'s boundary tends to cross $B$'s. Consequences:
- **Hiding gradients does not help.** A black-box target is attackable via a white-box surrogate.
- **Ensembles transfer better.** Perturbations that fool several surrogates are more "universal".
- This is the continuous-domain twin of GCG's transferable suffixes (M07).

### Certified robustness — a proof, not a hope

Empirical robustness ("PGD couldn't break it at $\epsilon$") is only as strong as the attack you
tried. **Certified** robustness *proves* no perturbation within a region can change the prediction.
**Randomized smoothing** (Cohen et al., 2019) is the most scalable certificate:

Define the smoothed classifier $g(x) = \arg\max_c \Pr_{\eta\sim\mathcal N(0,\sigma^2 I)}[f(x+\eta)=c]$.
If the top class $A$ has probability at least $\underline{p_A}$ (a high-confidence lower bound from
Monte-Carlo sampling), then $g$ is **provably constant** within the $\ell_2$ ball of radius

$$ R = \sigma\,\Phi^{-1}(\underline{p_A}), $$

where $\Phi^{-1}$ is the inverse standard-normal CDF. No $\ell_2$ perturbation of norm $< R$ can
change $g$'s prediction — a guarantee against *all* attacks, seen or unseen, within $R$. The price:
you evaluate $g$ by sampling (slower), and there is a clean/certified-accuracy trade-off in $\sigma$
(more noise → larger certifiable radius but lower accuracy).

## Intuition

FGSM/PGD ask "can I break it with a hammer of size $\epsilon$?" CW asks "what is the *smallest* nudge
that breaks it?" — a scalpel that reveals fragility a fixed hammer misses. Transfer says the same
nudge that opens your neighbor's identical lock probably opens yours, even if you never let anyone
touch your lock. Certification changes the question entirely: instead of *trying* attacks, you blur
the input with noise and, if the model votes overwhelmingly for one class across the blur, you can
*prove* a small adversary can't flip that vote — you've bought a guarantee with noise.

## Technical explanation & Code

`labs/lab-10/adv2.py`:
- **`cw_attack`** optimizes $\delta$ with Adam on $\|\delta\|_2^2 + c\cdot\text{margin}$; reports the
  fraction fooled and the *median $\ell_2$* among fooled — the size of the minimal break (~0.27 in
  the toy, far below a typical PGD $\epsilon$).
- **`transfer_rate`** crafts PGD adversarials on $A$ and measures how many also fool $B$ (~0.98 in
  the toy — near-total transfer between similarly-trained models).
- **`smoothed_predict_and_certify`** Monte-Carlo estimates $\underline{p_A}$ and returns
  $R=\sigma\Phi^{-1}(\underline{p_A})$ (using `erfinv` for $\Phi^{-1}$), giving ~45/50 test points a
  positive certified radius.

## Mathematics

**Why $R=\sigma\Phi^{-1}(\underline{p_A})$.** Sketch: for Gaussian smoothing, the worst-case shift
of the top-class probability under an $\ell_2$ perturbation $\delta$ is bounded via the Gaussian's
concentration; the class ranking cannot change until $\|\delta\|_2$ exceeds
$\sigma\Phi^{-1}(\underline{p_A})$ (Cohen et al.'s tight bound). The certificate needs only a
high-confidence lower bound $\underline{p_A}$ on the top class's smoothed probability — obtained by
sampling and a Clopper–Pearson (or normal-approx) confidence bound, which is why more samples give
tighter (larger) certified radii.

**Empirical vs certified, precisely.**
- *Empirical robust accuracy* = accuracy under a *specific attack* $\mathcal A$: an **upper bound**
  on true robustness (a stronger attack can only lower it). Useful, never a guarantee.
- *Certified robust accuracy at radius $R$* = fraction of points provably correct within $R$: a
  **lower bound** on true robustness. Guaranteed, but typically smaller and costlier.

The right report gives both, and the empirical evaluation uses the strongest attacks (AutoAttack),
not one you hand-picked.

**AutoAttack** (Croce & Hein, 2020) is an ensemble (two parameter-free APGD variants, FAB, Square)
designed to be a reliable, non-gameable empirical robustness estimate; it exposed dozens of
published "defenses" as gradient-masked. If you report empirical robustness, report AutoAttack.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — randomized smoothing (certified defense).**
- **Stops (provably):** *every* $\ell_2$ perturbation of norm $< R = \sigma\Phi^{-1}(\underline{p_A})$
  — a real guarantee, attack-agnostic.
- **Does NOT stop:** perturbations with $\ell_2 \ge R$, non-$\ell_2$ threat models ($\ell_\infty$,
  semantic, patches), and it doesn't certify points where $\underline{p_A}\le 0.5$.
- **Attacker adapts:** exceed $R$, switch norm/threat model, or target low-margin inputs (small
  certified radius).
- **Cost:** clean-accuracy loss from noise; **inference is Monte-Carlo** (many forward passes per
  prediction) — a real latency/throughput hit; certification needs many samples.
- **Takeaway:** the gold standard where applicable, but bounded to its norm and radius, and
  operationally expensive. Certificates and empirical evaluation are complementary, not substitutes.

</div>

## Practical lab

<div class="lab">

**Lab 10** ([`labs/lab-10/`](../../labs/lab-10/README.md)) — CW, transfer, certified radius. CPU
torch, ~3s tests.

```bash
py labs/lab-10/adv2.py
py -m pytest labs/lab-10 -q
```

</div>

## Exercise

1. **CW vs PGD sizes.** For the same misclassification, compare the median $\ell_2$ of CW
   perturbations vs the smallest $\epsilon$ at which PGD succeeds. Explain why CW finds smaller ones.
2. **CW knobs.** Sweep $c$ and $\kappa$; show the fooled-rate vs perturbation-size trade-off and the
   effect of confidence $\kappa$ (higher $\kappa$ = more confident, larger perturbations).
3. **Transfer vs similarity.** Vary how similar $B$ is to $A$ (different seed, width, or training
   data fraction); plot transfer rate vs similarity. Relate to why ensembling surrogates helps.
4. **Derive & verify the certificate.** Implement the $R=\sigma\Phi^{-1}(\underline p_A)$ bound;
   then **empirically confirm** it: for certified points, run CW/PGD constrained to $\ell_2 < R$ and
   show they *never* change the smoothed prediction (they must not, by the theorem). Any violation
   means a bug in your bound or sampling.
5. **Certified-accuracy curve.** Plot certified accuracy vs radius for $\sigma\in\{0.12,0.25,0.5\}$;
   show the $\sigma$ trade-off (larger $\sigma$ → larger radii but lower clean/certified accuracy).
6. **Evaluation rigor (purple team).** Take your "robust" model from Lab 09; evaluate it with (a)
   FGSM only, (b) PGD, (c) a CW attack, and (d) a transfer attack from a surrogate. Show how the
   reported robustness *drops* as the evaluation strengthens, and write the guarantee box explaining
   why single-attack robustness numbers are untrustworthy.

<details><summary>Hint (step 4)</summary>

To attack within $\ell_2<R$, project each perturbation onto the $\ell_2$ ball of radius $R$ after
each step. The certificate guarantees the *smoothed* classifier $g$ is unchanged — so evaluate $g$
(the Monte-Carlo vote), not the base $f$, on the attacked input. If $g$ ever flips within $R$, your
$\underline{p_A}$ bound was not actually a valid lower bound (too few samples / wrong confidence).

</details>

**Deliverable.** CW-vs-PGD sizes, CW knob sweeps, the transfer-vs-similarity plot, the verified
certificate + certified-accuracy curves, and the evaluation-rigor demonstration with its guarantee
box.

```bash
py course.py complete 10.1
```

## Research paper

**Carlini & Wagner, "Towards Evaluating the Robustness of Neural Networks" (2017)**; **Cohen,
Rosenfeld, Kolter, "Certified Adversarial Robustness via Randomized Smoothing" (2019)**; **Croce &
Hein, "AutoAttack" (2020).** *Why:* CW = the strong optimization attack you implemented; Cohen = the
certificate you implemented; AutoAttack = how to evaluate empirically without fooling yourself.
*Read:* CW §III (objective + the change-of-variable box constraint); Cohen §3 (the radius theorem);
AutoAttack §1–3 (why single attacks mislead). *Reproduce:* you have CW and smoothing; add one
AutoAttack component (Square attack — a black-box query attack) and compare to PGD. *Limits:*
smoothing certifies only $\ell_2$; CW is $\ell_2$-oriented; certified accuracy lags clean accuracy.

## Further reading

- Papernot et al. on transferability; Tramèr et al. on ensemble adversarial training.
- NIST AI 100-2 evasion taxonomy; [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. How does CW differ from PGD, and why does it find smaller perturbations?</summary>

PGD fixes a budget $\epsilon$ and maximizes loss; CW minimizes the perturbation norm subject to
misclassification via a margin loss ($\|\delta\|_2^2 + c\cdot\text{margin}$), optimized directly.
By searching for the *smallest* flipping perturbation rather than maxing loss in a fixed ball, CW
reveals smaller adversarials and higher-confidence ones (via $\kappa$).

</details>

<details><summary>Q2. Why are transfer attacks a threat to black-box models?</summary>

Adversarials crafted on an accessible surrogate frequently fool an inaccessible target, because
similarly-trained models share features and decision boundaries. So hiding a model's gradients
doesn't prevent attacks — an attacker crafts on a surrogate (or ensemble) and transfers, exactly as
GCG suffixes transfer between LLMs.

</details>

<details><summary>Q3. State the randomized-smoothing certificate and what it guarantees.</summary>

For the smoothed classifier $g$ with Gaussian noise $\sigma$, if the top class has smoothed
probability $\ge\underline{p_A}$, then $g$'s prediction is unchanged for every $\ell_2$ perturbation
of norm $< R=\sigma\Phi^{-1}(\underline{p_A})$. It guarantees robustness against *all* $\ell_2$
attacks within $R$ (attack-agnostic), at the cost of noisy/slower Monte-Carlo inference and lower
clean accuracy.

</details>

<details><summary>Q4. Empirical vs certified robustness — which bounds which?</summary>

Empirical robust accuracy (under a specific attack) is an *upper bound* on true robustness — a
stronger attack can only lower it. Certified robust accuracy is a *lower bound* — provably correct
within the radius. Report both, evaluate empirically with strong ensembles (AutoAttack), and never
treat "no attack found" as a guarantee.

</details>

## What you should now be able to do

- Implement CW and explain minimal-norm attacks; measure transfer and reason about the black-box
  threat.
- Derive and implement the randomized-smoothing certificate and verify it empirically.
- Distinguish empirical from certified robustness, and evaluate robustness rigorously (AutoAttack,
  transfer) rather than with a single hand-picked attack.

## Progress checkpoint

```bash
py course.py complete 10.1
py course.py next
```

**Next:** Stage 5 — 11.1 · Data & model poisoning and backdoors: inserting a trigger during
training so the model behaves normally until the attacker's trigger appears (sleeper-agent
behavior), and how to detect it.

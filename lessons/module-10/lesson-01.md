---
id: "10.1"
module: 10
minutes: 10
practice_minutes: 150
prerequisites: ["09.1"]
objectives:
  - Formulate and implement the CW attack, and explain why it finds smaller perturbations than fixed-budget attacks.
  - Explain and measure transfer attacks, and connect them to the black-box threat.
  - Derive the randomized-smoothing certificate and implement its Monte-Carlo estimate.
  - Distinguish empirical from certified robustness and state the cost of each.
  - Evaluate robustness with AutoAttack rather than a single hand-picked attack.
volatility: concept
sources:
  - title: "Carlini & Wagner, Towards Evaluating the Robustness of Neural Networks (CW)"
    url: https://arxiv.org/abs/1608.08983
  - title: "Cohen, Rosenfeld, Kolter, Certified Adversarial Robustness via Randomized Smoothing"
    url: https://arxiv.org/abs/1902.03282
  - title: "Croce & Hein, AutoAttack — a parameter-free ensemble for reliable robustness evaluation"
    url: https://arxiv.org/abs/2002.02108
last_verified: "2026-09-30"
---

# 10.1 · Adversarial examples II (CW, transfer, certified robustness)

A model can survive FGSM and PGD and still be trivially broken. This lesson adds the three ideas that make adversarial-ML evaluation honest: the minimal-norm CW attack, transfer from a surrogate, and a certificate that separates "I found no attack" from "no attack exists".

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

## Technical explanation

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

> [!IMPORTANT]
> **Guarantee analysis — randomized smoothing (certified defense).**
> - **Stops (provably):** *every* $\ell_2$ perturbation of norm $< R = \sigma\Phi^{-1}(\underline{p_A})$
>   — a real guarantee, attack-agnostic.
> - **Does NOT stop:** perturbations with $\ell_2 \ge R$, non-$\ell_2$ threat models ($\ell_\infty$,
>   semantic, patches), and it doesn't certify points where $\underline{p_A}\le 0.5$.
> - **Attacker adapts:** exceed $R$, switch norm/threat model, or target low-margin inputs (small
>   certified radius).
> - **Cost:** clean-accuracy loss from noise; **inference is Monte-Carlo** (many forward passes per
>   prediction) — a real latency/throughput hit; certification needs many samples.
> - **Takeaway:** the gold standard where applicable, but bounded to its norm and radius, and
>   operationally expensive. Certificates and empirical evaluation are complementary, not substitutes.

## Code

`labs/module-10/adv2.py`:
- **`cw_attack`** optimizes $\delta$ with Adam on $\|\delta\|_2^2 + c\cdot\text{margin}$; reports the
  fraction fooled and the *median $\ell_2$* among fooled — the size of the minimal break (~0.27 in
  the toy, far below a typical PGD $\epsilon$).
- **`transfer_rate`** crafts PGD adversarials on $A$ and measures how many also fool $B$ (~0.98 in
  the toy — near-total transfer between similarly-trained models).
- **`smoothed_predict_and_certify`** Monte-Carlo estimates $\underline{p_A}$ and returns
  $R=\sigma\Phi^{-1}(\underline{p_A})$ (using `erfinv` for $\Phi^{-1}$), giving ~45/50 test points a
  positive certified radius.

## Practical lab

**Lab 10** ([`labs/module-10/`](../../labs/module-10/README.md)) — CW, transfer, certified radius. CPU
torch, ~3s tests.

```bash
py labs/module-10/adv2.py
py -m pytest labs/module-10 -q
```

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

## What you should now be able to do

- Implement CW and explain minimal-norm attacks; measure transfer and reason about the black-box
  threat.
- Derive and implement the randomized-smoothing certificate and verify it empirically.
- Distinguish empirical from certified robustness, and evaluate robustness rigorously (AutoAttack,
  transfer) rather than with a single hand-picked attack.

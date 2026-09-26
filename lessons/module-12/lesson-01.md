<div class="prereq">

**Prerequisites.** Sibling: probability, likelihood, cross-entropy (M01), training (M07).
[11.1](../module-11/lesson-01.md) (model-level threats). [02.2](../module-02/lesson-02.md) for
base rates / ROC. Lab: CPU torch.

**You will learn.** Privacy attacks against models: **membership inference** (was this sample in
the training set?) via the loss-threshold and **likelihood-ratio (LiRA)** attacks, **model
extraction** (stealing behavior through a query API), and **model inversion**; plus **differential
privacy (DP-SGD)** as the principled mitigation and its privacy/utility cost.

**Why this matters.** Models memorize. That memorization leaks *who* and *what* was in the training
data — a direct privacy harm and a regulatory one — and a query API leaks the model itself. These
are quantifiable risks with quantifiable defenses, and the math (a likelihood-ratio test, an ROC
curve, a DP bound) is exactly the statistics you need for the rest of the course's evaluation work.

</div>

# 12.1 · Model extraction, inversion & membership inference

## Why this matters

"We only expose an API, and we never share the training data" feels safe. It isn't: the API leaks
an approximate copy of the model (extraction), and the model's outputs leak whether specific people
were in its training set (membership inference) or even reconstruct training content (inversion /
memorization). These are the privacy attacks regulators and users care about, and they are
measurable — which means they are also *defendable* and *auditable*.

## Learning objectives

1. Define **membership inference (MI)** and measure it as an **ROC-AUC**; explain why overfitting
   is the leak.
2. Implement the **loss-threshold** MI attack and understand why the **likelihood-ratio (LiRA)**
   attack is far stronger.
3. Explain and measure **model extraction** (fidelity vs query budget; hard- vs soft-label).
4. Describe **model inversion** and training-data **memorization/extraction**.
5. State the **differential privacy** guarantee and how **DP-SGD** achieves it; measure the
   privacy/utility trade-off.

## Concept

### Membership inference

Given a target model and a candidate sample $(x,y)$, decide whether it was in the training set.
The signal: models fit training points *better*, so members tend to have **lower loss / higher
confidence** than non-members. The **loss-threshold** attack scores membership by (negative) loss
and sweeps a threshold; its quality is the **ROC-AUC** over members vs non-members (0.5 = no leak,
1.0 = perfect). Lab: an overfit model (train 1.00, test 0.83) gives MI AUC ≈ 0.64 — a real leak.

**Why AUC, not accuracy.** MI operates at extreme base rates and asymmetric costs; the ROC (and
especially the **TPR at low FPR**, which LiRA emphasizes) is the honest metric. A high average AUC
with poor low-FPR behavior can still be a serious leak for the few confidently-identified members.

### LiRA — the likelihood-ratio attack (why loss-threshold is weak)

Loss-threshold uses one global threshold for all samples, ignoring that some inputs are *inherently*
low-loss (easy) regardless of membership. LiRA (Carlini et al., 2022) calibrates **per-example**:
train many **shadow models** with and without the target sample, fit Gaussians to the model's
output (a logit-scaled confidence) under "in" vs "out", and score membership by the **likelihood
ratio**

$$ \Lambda(x) = \frac{p(\,\text{obs}(x)\mid x\in\text{train})}{p(\,\text{obs}(x)\mid x\notin\text{train})}. $$

This is the Neyman–Pearson optimal test for each example, and it dramatically raises TPR at low
FPR — the difference between "on average slightly leaky" and "these specific individuals are
identifiable." You build it in the exercise.

### Model extraction

Treat the target as a black box; query it on inputs, collect outputs, train a **student** to match
them (Tramèr et al., 2016). Fidelity (agreement with the teacher) rises with the query budget and
with richer outputs (soft probabilities/logits >> hard labels). Lab: 2000 hard-label queries →
~0.7 fidelity on a toy. Consequences: IP theft, and a **white-box surrogate** for transfer attacks
(M07/M10) against the black box.

### Model inversion & memorization

- **Model inversion:** reconstruct representative inputs for a class by optimizing an input to
  maximize that class's confidence (can recover recognizable class prototypes).
- **Training-data extraction / memorization:** LLMs can regurgitate verbatim training data (Carlini
  et al., 2021) — a direct leak of secrets/PII that was in the corpus. Mitigations: dedup, DP,
  output filtering, and not training on secrets.

## Intuition

A student who *understood* the material answers exam questions and practice questions about equally
well. A student who *memorized* the practice set answers those with suspicious ease — and that ease
is a fingerprint: show me your confidence on a question and I can guess whether it was on your
practice sheet. Membership inference reads that fingerprint. Differential privacy is forcing the
student to study with a blurred practice sheet, so no single question can leave a distinctive mark —
they learn the general material but can't betray any specific item, at the cost of learning a bit
less.

## Technical explanation & Code

`labs/lab-12/privacy.py`:
- `mi_loss_threshold` scores members/non-members by negative loss and computes AUC via the
  Mann–Whitney U statistic (equivalent to ROC-AUC).
- `extract` queries a teacher and trains a student; `fidelity` measures agreement.
- `train(..., dp=True)` implements **DP-SGD-style** updates: compute **per-example** gradients,
  **clip** each to norm $\le C$ (bounding any one example's influence), sum, add Gaussian noise
  $\mathcal N(0,(\sigma C)^2)$, and step. Lab: DP lowers MI AUC 0.64→0.59 while test accuracy falls
  0.83→0.74.

## Mathematics

**Differential privacy.** A randomized algorithm $\mathcal M$ is $(\varepsilon,\delta)$-DP if for
all adjacent datasets $D,D'$ (differing in one example) and all outputs $S$:

$$ \Pr[\mathcal M(D)\in S] \le e^{\varepsilon}\,\Pr[\mathcal M(D')\in S] + \delta. $$

Interpretation: the output distribution barely changes whether or not any one person is in the
data — so an adversary cannot confidently infer membership. **DP-SGD** (Abadi et al., 2016)
achieves this by (1) clipping per-example gradients to bound each example's sensitivity to $C$, and
(2) adding calibrated Gaussian noise; composing the per-step privacy loss over training (via the
moments accountant) yields the total $(\varepsilon,\delta)$.

**DP upper-bounds MI.** DP directly limits the membership adversary: for an $(\varepsilon,\delta)$-DP
model the MI advantage (TPR − FPR) is bounded roughly by $\propto e^{\varepsilon}-1$ (+$\delta$
terms). So a DP guarantee is *also* a membership-inference guarantee — the theoretical reason MI
AUC drops toward 0.5 as $\varepsilon$ shrinks, and the reason DP is the principled defense rather
than an empirical patch.

**The trade-off is real.** More noise / tighter clipping → smaller $\varepsilon$ (more privacy, less
MI) but lower accuracy. There is no free privacy; you choose an operating point on the
$\varepsilon$–accuracy frontier, which you trace in the exercise.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — differential privacy (DP-SGD).**
- **Provides:** a *provable* $(\varepsilon,\delta)$ bound on any single example's influence, hence a
  bound on membership-inference advantage and on memorization — attack-agnostic, unlike empirical
  MI defenses (regularization, early stopping) that a stronger attack can defeat.
- **Does NOT provide:** protection of *aggregate/group* properties, protection when $\varepsilon$ is
  large (a "DP" model with $\varepsilon=50$ guarantees almost nothing), or defense against
  extraction of the (non-private) *function* the model computes.
- **Attacker adapts:** use LiRA (still bounded by $\varepsilon$, but tight); attack a model whose
  reported $\varepsilon$ is too large to matter; extract the model instead of members.
- **Cost:** accuracy loss (esp. on tails/minorities), slower training (per-example grads), and
  careful accounting; a wrong clip/noise/accountant silently voids the guarantee.
- **Takeaway:** DP is the *only* rigorous membership/memorization defense — but the guarantee is
  exactly its $\varepsilon$; report it, and don't confuse "we added noise" with "we are private."

</div>

## Practical lab

<div class="lab">

**Lab 12** ([`labs/lab-12/`](../../labs/lab-12/README.md)) — MI (AUC), extraction (fidelity), DP-SGD
mitigation. CPU torch, ~12s tests.

```bash
py labs/lab-12/privacy.py
py -m pytest labs/lab-12 -q
```

</div>

## Exercise

1. **MI vs overfitting.** Plot MI AUC against the generalization gap by varying train size and
   epochs. Show AUC rises as the gap grows; explain mechanistically.
2. **Build LiRA.** Train $\ge 16$ shadow models on random subsets; for a set of target samples, fit
   in/out Gaussians of the (logit-scaled) confidence and score by the likelihood ratio. Compare
   **ROC and TPR@1%FPR** to the loss-threshold attack — LiRA should win decisively at low FPR.
3. **Extraction curve.** Measure student fidelity vs query budget $\in\{200,\dots,8000\}$ and
   compare **hard-label vs soft-label** (probabilities) access. Explain why soft labels leak more.
4. **Model inversion (mini).** For the toy classifier, optimize an input to maximize a class's
   confidence; show the recovered input's structure and discuss what this means for image/PII models.
5. **DP frontier.** Sweep the DP noise multiplier; plot MI AUC vs test accuracy. Identify a knee
   (good privacy at acceptable accuracy). Relate qualitatively to $\varepsilon$ (smaller noise ⇒
   larger $\varepsilon$ ⇒ more leak).
6. **Purple team.** Attack your DP model with LiRA; show MI AUC stays near 0.5 even under the
   stronger attack (DP's guarantee holds), then attack the *non-DP* model with LiRA and show the
   much higher low-FPR TPR. Write the guarantee box contrasting empirical (regularization) vs
   provable (DP) defenses.

<details><summary>Hint (step 2)</summary>

LiRA's per-example calibration is the whole point: for target $x$, "in" shadow models (trained
*with* $x$) and "out" shadow models (trained *without* it) give two distributions of
$\phi(x)=\text{logit}(p_{\text{model}}(y\mid x))$; fit Gaussians $\mathcal N(\mu_{in},\sigma_{in})$,
$\mathcal N(\mu_{out},\sigma_{out})$ and score the target model's $\phi(x)$ by the ratio of the two
densities. Aggregate over targets for the ROC. TPR@low-FPR is where it crushes the loss threshold.

</details>

**Deliverable.** The AUC-vs-overfitting plot, a working LiRA with ROC/TPR@1%FPR vs loss-threshold,
the extraction curves (hard vs soft), the inversion demo, the DP privacy–utility frontier, and the
guarantee box.

```bash
py course.py complete 12.1
```

## Research paper

**Shokri et al., "Membership Inference Attacks Against ML Models" (2017)**; **Carlini et al.,
"Membership Inference Attacks From First Principles" (LiRA, 2022)**; **Carlini et al., "Extracting
Training Data from Large Language Models" (2021)**; **Abadi et al., "Deep Learning with Differential
Privacy" (DP-SGD, 2016)**. *Why:* the four pillars — MI, the *right* way to do MI (LiRA), LLM
memorization, and the principled defense. *Read:* Shokri (shadow-model setup); LiRA §3–4 (per-example
likelihood ratio, TPR@low-FPR — the evaluation lesson); Carlini-2021 (verbatim extraction from LLMs);
Abadi §3 (clipping + noise + accountant). *Reproduce:* LiRA (Exercise 2) and DP-SGD (the lab).
*Limits:* toy scale; real LiRA needs many shadow models; DP accounting must be exact or the
guarantee is void.

## Further reading

- Fredrikson et al., model inversion; Tramèr et al., model extraction.
- OWASP LLM02 (Sensitive Information Disclosure); NIST AI 100-2 (privacy attacks);
  [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. Why does overfitting enable membership inference, and why report AUC/TPR@low-FPR?</summary>

Overfit models fit training points better, so members have systematically lower loss / higher
confidence — a signal an attacker thresholds. AUC summarizes the ranking across all thresholds;
TPR@low-FPR matters because the real harm is confidently identifying *specific* members, which a
good average AUC can hide.

</details>

<details><summary>Q2. Why is LiRA stronger than the loss-threshold attack?</summary>

Loss-threshold uses one global threshold, conflating "inherently easy" samples with members. LiRA
calibrates per example using shadow models to estimate the in/out distributions of the model's
confidence, then applies the Neyman–Pearson-optimal likelihood-ratio test — dramatically improving
TPR at low FPR, i.e. confidently identifying members.

</details>

<details><summary>Q3. State the DP guarantee and why it bounds membership inference.</summary>

$(\varepsilon,\delta)$-DP: for datasets differing in one example, output probabilities differ by at
most a factor $e^{\varepsilon}$ (plus $\delta$). Since the output barely depends on any one example's
presence, an adversary's membership advantage is bounded (roughly $\propto e^{\varepsilon}-1$). DP is
thus a *provable* MI/memorization defense — its strength is exactly $\varepsilon$.

</details>

<details><summary>Q4. Why is a query-only API not "safe" for the model?</summary>

Because model extraction can train a student to approximate the black box from queries (fidelity
rising with budget and with soft-label access), yielding IP theft and a white-box surrogate for
transfer attacks against the original. Hiding weights doesn't hide the function they compute.

</details>

## What you should now be able to do

- Measure membership inference as an AUC and build the LiRA likelihood-ratio attack.
- Perform and quantify model extraction (fidelity vs budget, hard vs soft labels).
- State the DP guarantee, implement DP-SGD, and trace the privacy/utility frontier.
- Distinguish provable (DP) from empirical privacy defenses and report $\varepsilon$ honestly.

## Progress checkpoint

```bash
py course.py complete 12.1
py course.py next
```

**Next:** 13.1 · Adapter & weight supply chain — malicious LoRA adapters, pickle/checkpoint code
execution, and why safetensors exists; loading a model is running someone else's code.

<div class="prereq">

**Prerequisites.** [04.1 ASR + Wilson CI](../module-04/lesson-01.md), [12.1 ROC-AUC / LiRA](../module-12/lesson-01.md),
[02.2 base rates](../module-02/lesson-02.md), [07.1](../module-07/lesson-01.md)/[10.1](../module-10/lesson-01.md)
(adaptive attacks / evaluation rigor), [23.1 defenses to evaluate](../module-23/lesson-01.md). Lab:
reusable harness, offline.

**You will learn.** How to *measure* AI security systematically: **attack success rate** with
confidence intervals, **precision/recall/ROC-AUC**, **robustness**, **transferability**, **coverage**,
**regression testing**, and — the methodology that separates real evaluation from theater —
**adaptive evaluation** (measure against the strongest/adapted attack). Plus how to **design your own
security benchmark**.

**Why this matters.** Every claim in this course — "this attack works", "this defense helps" — is
only as good as its measurement. Bad evaluation (weak attacks, no CIs, ignoring base rates) certifies
broken systems as safe. Evaluation is the discipline that makes security research *research*.

</div>

# 24.1 · Security evaluation

## Why this matters

You cannot manage what you don't measure, and in security, measuring *badly* is worse than not
measuring — it manufactures false confidence. A defense evaluated against only weak attacks reports a
great number and fails in production. This lesson gives you the honest measurement toolkit and the
methodology rules that make security numbers mean something.

## Learning objectives

1. Report **ASR with a Wilson CI** and know when a difference is *established* (non-overlapping CIs)
   vs noise; compute required sample sizes.
2. Evaluate detectors with **precision/recall/ROC-AUC** and interpret them under **base rates**.
3. Perform **adaptive evaluation** — measure against the strongest/adapted attack — and explain why
   it's decisive.
4. Measure **robustness** (ASR vs attack strength), **transferability**, and **coverage** across
   attack families.
5. **Design a security benchmark** and wire **regression tests** that fail if ASR rises.

## Concept

### Numbers need intervals

ASR is a proportion from finite $n$; report the **Wilson 95% CI** (M04). Comparing two systems =
comparing two proportions: **overlapping CIs mean the difference is not established** — collect more
data. To resolve a difference $\delta$ needs roughly $n\gtrsim \frac{z^2\,2\bar p(1-\bar p)}{\delta^2}$
per condition (e.g. ~193 for $\delta=0.1$). Small suites show *direction*, not fine differences.

### Detectors: precision/recall/ROC, and base rates

For any detector, sweep the threshold to get the **ROC** (TPR vs FPR) and summarize with **AUC**
(= P(score(attack) > score(benign))). But **precision in production depends on the base rate** (M02.2):
at low attack prevalence, even a high-AUC detector's alerts are mostly false — so decide block-vs-alert
using the base-rate-adjusted precision, not the lab AUC.

### Adaptive evaluation — the decisive rule

The single most important methodology point (M07/M10): **evaluate against the strongest attack you
have, ideally one adapted to your defense.** A defense that stops yesterday's attack tells you nothing
about an attacker who adapts. Lab: the *same* guarded bot shows ASR 0.00 on weak prompts and 1.00 on
authority-framed ones — reporting only the weak suite would certify a broken system. AutoAttack (M10)
is the vision-domain embodiment of this rule; for LLMs it means adaptive jailbreaks/injections, not a
fixed list.

### Robustness, transferability, coverage

- **Robustness curve:** ASR as a function of attack strength/budget (M09/M10) — a single-point number
  hides the cliff.
- **Transferability:** does an attack tuned on model/defense A work on B (M07/M10)? Measures
  generalization of the threat.
- **Coverage:** does your benchmark span the *families* (direct/indirect injection, jailbreak,
  poisoning, extraction, agent chains…)? A high score on a narrow suite is not security.

### Benchmark design & regression

A good security benchmark: representative attack families (coverage), a clear success criterion (a
judge — M08, whose quality bounds the benchmark), enough $n$ for CIs, and it's **re-runnable in CI** as
a regression guard (fail the build if ASR rises above a threshold). This turns evaluation from a
one-off into a control.

## Intuition

Grading a lock by whether *you* can pick it, gently, with the one tool you happen to own, then
advertising "unpickable" — that's most security evaluation. Honest evaluation hires the best
lockpicker you can find, lets them bring adapted tools, measures how often and how fast they succeed
across many attempts (with error bars), tests locks like yours *and* unlike yours (transfer/coverage),
and re-tests every time you change the lock (regression). The number that matters is the adapted
attacker's success rate, with a confidence interval — not your own gentle attempt.

## Technical explanation & Code

`lab/attack-tools/evalkit.py`: `wilson_interval`/`asr` (CIs), `roc_auc`/`precision_recall` (detectors,
tie-averaged AUC), `required_n` (sample size), and `Benchmark.run/compare` (evaluate a defense,
flagging whether a difference is established via non-overlapping CIs). `labs/lab-24/evaluate.py`
demonstrates adaptive evaluation (ORIGINAL vs ADAPTED suites) and detector metrics against the shim.

## Mathematics

**Wilson interval** (M04) and **required $n$** as above. **ROC-AUC = Mann–Whitney U statistic**
normalized: with tie-averaged ranks, $\text{AUC}=U/(n_{+}n_{-})=P(\text{score}_+>\text{score}_-)$ —
threshold-free, and equal to the probability the detector ranks a random attack above a random benign.
**Base-rate precision** $\text{PPV}=\frac{t\pi}{t\pi+f(1-\pi)}$ (M02.2) — the production reality check.
**Judge-bounded ASR** (M08): observed ASR $\approx r\cdot a + f\cdot(1-a)$ for judge recall $r$ /
false-positive $f$ and true ASR $a$ — a bad judge biases every number, so validate the judge first.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — a security evaluation methodology (meta).**
- **Gives you:** defensible, comparable numbers (ASR + CIs), detector characterization (ROC/AUC),
  robustness/transfer/coverage, and regression protection — the basis for risk decisions and for
  claiming a defense *works*.
- **Does NOT give you:** a guarantee of safety against *unseen* attacks — evaluation measures the
  attacks you ran; a stronger/novel attack can lower the number (upper-bound nature, M10).
- **Fails when:** the attack suite is weak/narrow (overstates security), $n$ is too small (noise
  read as signal), the judge is bad (biased ASR), or base rates are ignored (detector precision
  misjudged).
- **Cost:** compute (large $n$, strong/adaptive attacks, many shadow models for LiRA), and the
  discipline to attack your own defense honestly.
- **Takeaway:** report ASR with CIs against the *strongest adapted* attack, characterize detectors
  with ROC + base-rate precision, cover attack families, and regression-test in CI. A security number
  without a strong attack, a confidence interval, and a coverage statement is not evidence.

</div>

## Practical lab

<div class="lab">

**Lab 24** ([`labs/lab-24/`](../../labs/lab-24/README.md)) — ASR+CI, ROC-AUC, and adaptive evaluation
with the reusable harness. Offline.

```bash
py labs/lab-24/evaluate.py
py -m pytest labs/lab-24 -q
```

</div>

## Exercise

1. **CIs & sample size.** Reproduce the ORIGINAL-vs-ADAPTED comparison; increase $n$ and show the CIs
   tighten; find the $n$ at which you could distinguish ASR 0.55 from 0.65 (use `required_n`).
2. **Design a benchmark.** Build a suite covering ≥4 attack families (direct/indirect injection,
   jailbreak, agent chain) with a documented success criterion; report per-family ASR+CI and an
   overall coverage statement. State what your judge might get wrong.
3. **Detector ROC & operating point.** For a detector, sweep the threshold; plot ROC, compute AUC,
   and pick an operating point justified by a realistic base rate (compute the PPV). Decide
   block-vs-alert.
4. **Robustness curve.** Measure ASR vs attack strength (e.g. GCG steps, M07, or injection framing
   intensity); plot the curve and identify the cliff. Argue why a single-point ASR is misleading.
5. **Transferability.** Tune an attack against defense/model A; measure its ASR on B. Report the
   transfer rate and what it implies (M07/M10).
6. **Regression guard (purple team).** Wire your benchmark as a pytest that fails if overall ASR
   exceeds a threshold; introduce a "defense regression" (weaken a control) and show the test catches
   it. Write the guarantee box for your methodology.

<details><summary>Hint (step 2)</summary>

Coverage is the antidote to "we scored 0% ASR." A benchmark that only tests direct injection says
nothing about indirect injection, poisoning, or agent chains. Enumerate the families relevant to your
system (use this course's stages as the checklist), include several payloads per family, and report
per-family — a low overall number with an untested family is a false negative waiting to happen.

</details>

**Deliverable.** The CI/sample-size analysis, your covered benchmark with per-family ASR+CI, the
detector ROC + operating point + PPV, the robustness curve, the transfer measurement, and the CI
regression test + methodology guarantee box.

## Research paper

**Croce & Hein, "AutoAttack" (2020)** + **Carlini et al., "On Evaluating Adversarial Robustness"
(2019)** + **Carlini et al., LiRA (2022, evaluation done right)**. *Why:* the canonical statements of
"evaluate with strong, adaptive attacks and report honestly" — AutoAttack for vision robustness, the
2019 checklist for common evaluation mistakes, LiRA for measuring privacy leakage at low FPR. *Read:*
the 2019 paper's list of evaluation pitfalls (most "robust" defenses were mis-evaluated); AutoAttack's
parameter-free ensemble; LiRA's TPR@low-FPR argument. *Reproduce:* the lab's adaptive comparison;
extend by adding a stronger attack and showing the reported ASR rises. *Limits:* even AutoAttack is a
fixed ensemble — true adaptivity means an attacker who studies *your* defense.

## Further reading

- NIST AI RMF "measure" function; garak/PyRIT/promptfoo/Inspect AI as harnesses (with local fallbacks,
  `references/tools-and-fallbacks.md`); [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. Why report a confidence interval with ASR, and when is a difference "established"?</summary>

ASR is a proportion from finite $n$, so a point estimate hides sampling noise; the Wilson CI bounds the
true rate. A difference between two systems is established only when their CIs don't overlap —
otherwise you need more samples (resolving $\delta=0.1$ needs ~193 per condition). Reporting ASR
without a CI can present noise as a real effect.

</details>

<details><summary>Q2. What is adaptive evaluation and why is it decisive?</summary>

Measuring a defense against the strongest attack you have, ideally one adapted to that specific
defense — not a fixed/weak suite. It's decisive because a defense that stops a weak attack tells you
nothing about an adaptive attacker; the lab shows the same bot at ASR 0.00 (weak) and 1.00 (adapted).
Reporting only the weak number certifies a broken system.

</details>

<details><summary>Q3. Why can a high lab ROC-AUC still mean poor production precision?</summary>

Because precision depends on the base rate: at low attack prevalence $\pi$, PPV $=\frac{t\pi}{t\pi+f(1-\pi)}$
is dominated by false positives, so most alerts are false even for a high-recall/AUC detector. AUC is
prevalence-independent; production precision is not — decide block-vs-alert using the base-rate-adjusted
precision.

</details>

## What you should now be able to do

- Report ASR with confidence intervals and judge when differences are real vs noise.
- Characterize detectors with ROC/AUC and interpret them under base rates.
- Run adaptive evaluations and measure robustness, transferability, and coverage.
- Design a covered security benchmark and enforce it as a CI regression guard.

## Progress checkpoint

```bash
py course.py complete 24.1
py course.py next
```

**Next:** 25.1 · Automated red teaming — attack generation, mutation/fuzzing, search/optimization,
attacker/defender models, and automated exploit chains (building on M08 and this harness).

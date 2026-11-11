---
id: "24.1"
module: 24
minutes: 10
practice_minutes: 120
prerequisites: ["02.2", "04.1", "07.1", "10.1", "12.1", "23.1"]
objectives:
  - "Report **ASR with a Wilson CI** and know when a difference is *established* (non-overlapping CIs) vs noise; compute required sample sizes."
  - "Evaluate detectors with **precision/recall/ROC-AUC** and interpret them under **base rates**."
  - "Perform **adaptive evaluation** — measure against the strongest/adapted attack — and explain why it's decisive."
  - "Measure **robustness** (ASR vs attack strength), **transferability**, and **coverage** across attack families."
  - "**Design a security benchmark** and wire **regression tests** that fail if ASR rises."
volatility: concept
sources:
  - title: "Croce & Hein — Reliable Evaluation of Adversarial Robustness (AutoAttack)"
    url: https://arxiv.org/abs/2003.01990
  - title: "Carlini et al. — On Evaluating Adversarial Robustness"
    url: https://arxiv.org/abs/1904.02175
  - title: "Carlini et al. — Extracting Training Data from Large Language Models (LiRA, membership inference)"
    url: https://arxiv.org/abs/2112.14704
last_verified: "2026-09-30"
---
---
# 24.1 · Security evaluation

Every claim in this course — "this attack works", "this defense helps" — is only as good as its measurement. Bad evaluation (weak attacks, no CIs, ignoring base rates) certifies broken systems as safe. Evaluation is the discipline that makes security research *research*.

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

## Mathematics

**Wilson interval** (M04) and **required $n$** as above. **ROC-AUC = Mann–Whitney U statistic**
normalized: with tie-averaged ranks, $\text{AUC}=U/(n_{+}n_{-})=P(\text{score}_+>\text{score}_-)$ —
threshold-free, and equal to the probability the detector ranks a random attack above a random benign.
**Base-rate precision** $\text{PPV}=\frac{t\pi}{t\pi+f(1-\pi)}$ (M02.2) — the production reality check.
**Judge-bounded ASR** (M08): observed ASR $\approx r\cdot a + f\cdot(1-a)$ for judge recall $r$ /
false-positive $f$ and true ASR $a$ — a bad judge biases every number, so validate the judge first.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — a security evaluation methodology (meta).**
> - **Gives you:** defensible, comparable numbers (ASR + CIs), detector characterization (ROC/AUC),
>   robustness/transfer/coverage, and regression protection — the basis for risk decisions and for
>   claiming a defense *works*.
> - **Does NOT give you:** a guarantee of safety against *unseen* attacks — evaluation measures the
>   attacks you ran; a stronger/novel attack can lower the number (upper-bound nature, M10).
> - **Fails when:** the attack suite is weak/narrow (overstates security), $n$ is too small (noise
>   read as signal), the judge is bad (biased ASR), or base rates are ignored (detector precision
>   misjudged).
> - **Cost:** compute (large $n$, strong/adaptive attacks, many shadow models for LiRA), and the
>   discipline to attack your own defense honestly.
> - **Takeaway:** report ASR with CIs against the *strongest adapted* attack, characterize detectors
>   with ROC + base-rate precision, cover attack families, and regression-test in CI. A security number
>   without a strong attack, a confidence interval, and a coverage statement is not evidence.

## Code

`lab/attack-tools/evalkit.py`: `wilson_interval`/`asr` (CIs), `roc_auc`/`precision_recall` (detectors,
tie-averaged AUC), `required_n` (sample size), and `Benchmark.run/compare` (evaluate a defense,
flagging whether a difference is established via non-overlapping CIs). `labs/module-24/evaluate.py`
demonstrates adaptive evaluation (ORIGINAL vs ADAPTED suites) and detector metrics against the shim.

## Practical lab

**Lab 24** ([`labs/module-24/`](../../labs/module-24/README.md)) — ASR+CI, ROC-AUC, and adaptive evaluation
with the reusable harness. Offline.

```bash
py labs/module-24/evaluate.py
py -m pytest labs/module-24 -q
```

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

## What you should now be able to do

- Report ASR with confidence intervals and judge when differences are real vs noise.
- Characterize detectors with ROC/AUC and interpret them under base rates.
- Run adaptive evaluations and measure robustness, transferability, and coverage.
- Design a covered security benchmark and enforce it as a CI regression guard.

## Advanced extension: evaluating prompt-injection detectors (added 2026-11-08)

<div class="prereq">

**Prerequisites.** This lesson's ROC/AUC, base-rate PPV and Wilson CI sections; [23.1](../module-23/lesson-01.md)
(the keyword detector as a probabilistic control); [05.1](../module-05/lesson-01.md) (indirect
injection through tool outputs); [17.2](../module-17/lesson-02.md) (controls that do not depend on
detection). **You will learn** how to evaluate an injection detector the way it will be used: one
fixed threshold, several benign and attack distributions, and false positives measured as carefully
as recall. **Why this matters:** detectors (Prompt Guard-style classifiers, guard models, "LLM
firewalls") are the most widely deployed injection control, and their published numbers come almost
entirely from in-distribution test splits.

</div>

The toolkit above still holds: ASR with CIs, ROC-AUC, base-rate PPV, adaptive evaluation. This
extension applies it to one control the course keeps meeting, the prompt-injection **detector**. It
adds one rule that the toolkit implies but does not state: **a detector's number belongs to a
distribution.** Move the benign data or the attack format and the number moves, often a long way.

### What changed

Between 2024 and 2026, four independent lines of work measured the same gap. All four are
DOCUMENTED, with sources below.

1. **Over-defense (2024).** InjecGuard (Li & Liu, [arXiv:2410.22770](https://arxiv.org/abs/2410.22770),
   code and the NotInject set at github.com/leolee99/InjecGuard) built 339 benign prompts rich in
   trigger words ("ignore", "override", "system prompt"). On them, state-of-the-art guard models
   fell to about 60% accuracy, close to chance. The cause is **trigger-word bias**: the detector
   learned the vocabulary of attacks, not their intent.
2. **Low-FPR evaluation (2025).** PromptShield (Jacob, Alzahrani, Hu, Alomair & Wagner, ACM CODASPY
   2025, [arXiv:2501.15145](https://arxiv.org/abs/2501.15145)) argued that a detector is only
   deployable if it works at a *low* false-positive rate, and evaluated in that regime. Meta's
   [Prompt Guard 2 model card](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) now
   reports **recall at 1% FPR** (97.5% for the 86M model on its own English evaluation). The same
   card lists sensitivity to application-specific distributions and to adaptive attacks as known
   limitations.
3. **Over-defense, obfuscation and shift measured together (2026).** PIDS-Bench (Shire & Kim,
   [arXiv:2609.15017](https://arxiv.org/abs/2609.15017), IEEE Access vol. 14, 2026) reports a detector
   with F1 above 0.98 on its held-out split that still misclassifies about a third of an externally
   sourced benign subset. Across a full threshold sweep and five seeds, no detector reached
   F1 ≥ 0.95 **and** hard-benign FPR ≤ 0.10 together. Hard-negative augmentation nearly removed
   over-defense on curated stress inputs, but left external false positives far above 0.10.
4. **Agent format (2026).** Liu ([arXiv:2610.03448](https://arxiv.org/abs/2610.03448), code at
   github.com/lzwhehe/benign-instruction-bench) replayed 15 detectors, including Prompt Guard 2, and
   two LLM judges on AgentDojo and tau-bench tool outputs. The best detector on BIPIA caught **2%** of
   AgentDojo injections at 1% FPR. A detector catching 72% on AgentDojo caught 15% on tau-bench.
   **Rankings did not transfer between benchmarks; false-positive rates did.** The best agent-side
   detector shared no data with the benchmarks, but it was trained on agent-style inputs.

One EMERGING data point extends the attack side. "Voluntary Servitude" (Zendel et al.,
[arXiv:2611.04393](https://arxiv.org/abs/2611.04393), accepted at NeurIPS 2026, no code released)
steers agents with a **fabricated hazard written as an ordinary review**, with no command in it at
all. The authors report that deployed injection detectors score these payloads as benign, so behind
a filter they are 1.7–4.4x more effective than instruction injection. That is one paper and one week
old, so treat the numbers as the authors' claim. The mechanism, though, follows from point 1: a
detector that keys on command vocabulary has nothing to key on.

### The new technique: evaluate at the operating point, across distributions

The protocol has five parts.

1. **Fix the threshold once.** Use the shipped default, or calibrate on in-distribution validation
   data, before you look at any stress split. Report every split at that threshold.
2. **Separate the splits.** Use in-distribution test data, a *curated* hard-benign set (trigger words,
   benign intent), an *external* hard-benign set that you did not write, obfuscated attacks, and the
   deployment format (for agents, tool outputs).
3. **Report false positives per benign source, with CIs.** Over-defense is a benign-side failure,
   and it never shows up in attack recall.
4. **Report both views of recall.** Recall at the fixed threshold is what deployment gets. Recall at
   1% FPR, re-chosen per split, measures ranking only. When the two differ, the threshold is
   miscalibrated for that distribution.
5. **Convert to PPV at a realistic base rate** (this lesson's formula), using recall from the
   deployment format and FPR from the external benign source.

### Mathematics

**The detector you build.** Lab 37 uses a multinomial naive-Bayes detector. The score is the
posterior log-odds

$$s(x)=\log\frac{P(A)}{P(B)}+\sum_{w\in x}\Big[\log P(w\mid A)-\log P(w\mid B)\Big],\qquad
P(w\mid c)=\frac{n_{c,w}+\alpha}{n_c+\alpha|V|}.$$

Here $A$ is "attack" and $B$ is "benign". $n_{c,w}$ counts word $w$ in class $c$'s training text,
$n_c$ is that class's total word count, $|V|$ the vocabulary size and $\alpha$ the Laplace
smoothing constant. The input is flagged when $s(x)\ge t$, and the shipped threshold is $t=0$
(posterior 0.5). A word never seen in training contributes 0.

**Worked example: why trigger words cause over-defense.** Train on attack text "ignore rules ignore
rules" and benign text "ignore typos summary summary". Then $|V|=4$, $n_A=n_B=4$, $\alpha=1$, and the
priors are equal.

- $P(\text{ignore}\mid A)=\frac{2+1}{4+4}=\frac38$ and $P(\text{ignore}\mid B)=\frac{1+1}{8}=\frac28$,
  so "ignore" contributes $\ln 1.5=+0.405$.
- $P(\text{typos}\mid A)=\frac18$ and $P(\text{typos}\mid B)=\frac28$, so "typos" contributes
  $\ln 0.5=-0.693$.
- "ignore typos" scores $0.405-0.693=-0.288<0$: benign. "ignore" followed by words the model never
  saw scores $+0.405\ge 0$: **flagged**. Benign text from a new source is mostly unseen words plus a
  trigger word. That is over-defense, and the external hard-benign split is built to expose it.

**Ranking vs calibration.** $\text{Recall@}f=\Pr[s(x)\ge t_f\mid A]$, where $t_f$ is chosen so that
$\Pr[s(x)\ge t_f\mid B]=f$ *on the same split*. If a split's benign scores shift upward, $t_f$ moves
with them, but the shipped $t$ does not. In the lab, the agent-trained detector reaches
Recall@5% = 1.00 on tool outputs but has FPR 0.20 at $t=0$: perfect ranking, wrong threshold.

**PPV at the base rate.** With $\pi=0.01$:

- Prompt Guard 2's own evaluation (recall 0.975 at FPR 0.01) gives
  $\text{PPV}=\frac{0.975\cdot0.01}{0.975\cdot0.01+0.01\cdot0.99}=\frac{0.00975}{0.01965}=0.50$.
- The same FPR with Liu's AgentDojo recall of 0.02 gives
  $\frac{0.0002}{0.0002+0.0099}=0.020$. Forty-nine of every fifty alerts are false, and 98% of the
  attacks are missed.
- In the lab, the best detector (agent recall 1.00, external FPR 0.17) gives
  $\frac{0.01}{0.01+0.17\cdot0.99}=\frac{0.01}{0.178}=0.056$.

**How sure are you about an FPR?** The lab's external benign set has $n=12$, and 3 of the 12 are
flagged after hard-negative training. The Wilson interval (this lesson's first section), with
$z^2=3.8416$, is: denominator $1+3.8416/12=1.320$; centre $(0.25+3.8416/24)/1.320=0.311$; half-width
$1.96\sqrt{0.25\cdot0.75/12+3.8416/576}\,/\,1.320=0.222$. So the FPR is in $[0.09,\,0.53]$, which is
consistent with "above the 0.10 bar" and says little more. The recall drop from 0.60 to 0.36 on the
agent split ($n=25$) has overlapping CIs as well: **a direction, not an established cost.** Report
both findings that way.

### Attack / Defense model

<div class="callout red">

**Attacker moves against a detector.** (1) Move to a format the detector did not train on, such as a
tool output, an email body or a document. (2) Remove the trigger vocabulary through paraphrase,
leetspeak or spacing. (3) Remove the imperative entirely and plant a fact that the agent's own
reasoning acts on. (4) Make the defender pay: if over-defense is high, operators raise the threshold
or allow-list sources, and that opens a gap.

</div>

<div class="callout blue">

**Defender moves.** Hard-negative augmentation (cuts curated over-defense), agent-format training
data (fixes ranking on tool outputs), and per-deployment threshold calibration on *your own* benign
traffic (fixes calibration). Above all, do not make the detector the only control: put it in front of
17.2's capability flow control, which bounds what a missed injection can do.

</div>

<div class="callout guarantee">

**Guarantee analysis — a prompt-injection detector, hardened with hard negatives and agent-format data.**
- **What it guarantees:** nothing in the worst case. It is a probabilistic control. On distributions
  close to its training data it gives a measured recall and FPR at its threshold, and you can
  report those numbers with CIs.
- **What it does NOT guarantee:** recall on a format, obfuscation or phrasing it has not seen; a
  false-positive rate on a benign source you did not test; or anything about steering content
  that contains no instruction (fabricated facts, biased reviews).
- **How an attacker adapts:** changes format, strips trigger vocabulary, or drops the imperative.
  Each of these moved recall in the lab; the last moved it to 0.00 for every hardened detector.
- **False-positive cost:** over-defense falls hardest on legitimate text *about* security, and on
  users who write "ignore", "override" or "system". In the lab, external FPR stays at 0.17–0.25 even
  after hardening; PIDS-Bench reports the same pattern. Each fix also moves the other error: the
  hard-negative fix lowered agent-format recall (a direction at this $n$).
- **Performance cost:** a classifier pass per input (milliseconds for a small model; the lab's
  naive Bayes is microseconds), plus the ongoing cost of collecting and labelling benign traffic
  from every new source to recalibrate.

</div>

<div class="callout guarantee">

**Guarantee analysis — the evaluation protocol (meta).**
- **What it guarantees:** a detector number tied to a stated distribution and threshold, with
  over-defense visible as its own metric and a PPV that reflects deployment.
- **What it does NOT guarantee:** coverage of distributions you did not collect. "External" only
  means "not mine", not "representative".
- **How an attacker adapts:** finds the next distribution you did not test.
- **False-positive cost:** none for users. The cost falls on the evaluator, who must build and label
  several benign sets.
- **Performance cost:** one scoring pass per split. The real cost is data collection.

</div>

**Side by side** (Lab 37, shipped thresholds, Wilson CIs in the lab output).

| Detector | F1 in-dist | Hard-benign FPR, curated | Hard-benign FPR, external | Agent recall @ t | Agent recall @ 5% FPR | Fabricated hazard recall | Meets PIDS bar |
|---|---|---|---|---|---|---|---|
| Keyword (23.1) | 0.75 | 0.00 | 0.17 | 0.00 | 0.00 | 0.00 | no |
| NB, in-distribution | 1.00 | 0.35 | 0.75 | 0.60 | 0.56 | 0.20 (by accident) | no |
| NB + hard negatives | 1.00 | 0.00 | 0.25 | 0.36 | 0.68 | 0.00 | no |
| NB + hard negatives + agent data | 1.00 | 0.00 | 0.17 | 1.00 | 1.00 | 0.00 | no |

**When the original still holds.** If the detector's inputs really come from one distribution that
you sampled for its test set (one chat product, one user population, no tool outputs), then this
lesson's single ROC/AUC plus a base-rate PPV is the right evaluation, and the extra splits add little.
The extension matters once inputs arrive from several sources, which is true of every agent.

**Layer and standards.** FOUNDATIONAL: base-rate PPV, ROC, Wilson CIs. CURRENT: over-defense and
low-FPR evaluation (InjecGuard, PromptShield, Prompt Guard 2's reporting). EMERGING: agent-format
re-evaluation (2026) and non-imperative steering. Maps to OWASP **LLM01:2026 Prompt Injection** and
NIST AI RMF **Measure**; ATT&CK T1698/T1699 and ATLAS AML.T0051 are the techniques being detected.

<div class="lab">

**Lab 37** ([`labs/lab-37-injection-detector-eval/`](../../labs/lab-37-injection-detector-eval/README.md)):
the 23.1 keyword detector and a from-scratch naive-Bayes detector, evaluated at fixed thresholds on
in-distribution, curated and external hard-benign, obfuscated, agent-format and fabricated-hazard
splits, with Wilson CIs, recall@5%FPR and PPV at a 1% base rate. CPU-only, offline, in-process,
stdlib only. The strings are inert (`LAB-CANARY-*`, `PINEAPPLE-OK`, `*.test`). Runs in under a second.

```bash
py labs/lab-37-injection-detector-eval/evaluate.py
py -m pytest labs/lab-37-injection-detector-eval -q
```

</div>

### Exercise

1. **Construct → execute → measure.** Run the lab and reproduce the side-by-side table. For each
   number, name the split and the threshold it was measured at.
2. **Establish or refute.** The recall cost of hard negatives on the agent split is only a direction.
   Use `required_n` from `evalkit` to estimate the $n$ needed to resolve 0.60 vs 0.36. Extend
   `corpus.py` with new tool-output templates until the CIs separate or stop separating, and report
   the result either way.
3. **A benign source you did not write.** Collect 50 benign sentences that use trigger words from a
   real source you have access to, such as your team's docs or a security course's own text. Never
   use user data. Measure every detector's FPR with a CI and say whether any now meets the bar.
4. **Defense, then bypass.** Add a de-obfuscation pre-pass (undo leetspeak, join spaced letters)
   before naive Bayes. Re-measure obfuscated recall *and* both hard-benign FPRs. Then write one
   obfuscation your pre-pass misses.
5. **Purple-team write-up.** Write the guarantee box for your best detector, with the PPV at a 1%
   base rate and one sentence on which 17.2 control bounds what it misses.

<details><summary>Hint (step 2)</summary>
<code>required_n(0.24, p_bar=0.48)</code> gives the per-condition $n$. Generate new tool-output
templates. Copying the existing ones only makes the test split easier, not larger.
</details>

<details><summary>Stronger hint (step 4)</summary>
Measure FPR after your pre-pass, not just recall. Normalisation can turn benign text into
trigger words: "0verride" in a CSS question becomes "override".
</details>

### Research paper

**Primary: PIDS-Bench (Shire & Kim, IEEE Access 2026, [arXiv:2609.15017](https://arxiv.org/abs/2609.15017)).**
*Why:* it measures over-defense, obfuscation and shift together, at fixed thresholds, across seeds.
*Read:* the split construction and the joint-bar result. *Reproduce:* Lab 37 is a miniature version.
*Limits:* no public code or data release was found on the paper page (checked 2026-11-08).

**Companions.** InjecGuard / NotInject ([arXiv:2410.22770](https://arxiv.org/abs/2410.22770)) for
trigger-word bias. Liu, "Passing the Test You Trained On" ([arXiv:2610.03448](https://arxiv.org/abs/2610.03448),
code released) for agent-format transfer. PromptShield ([arXiv:2501.15145](https://arxiv.org/abs/2501.15145))
for the low-FPR argument. Voluntary Servitude ([arXiv:2611.04393](https://arxiv.org/abs/2611.04393))
for steering without a command (EMERGING).

### Assessment

<details><summary>A vendor reports F1 0.98 for its injection detector. What two questions do you ask first?</summary>
On which distribution, at which threshold? Then: what is the false-positive rate on benign text that
uses trigger words, from a source the vendor did not write? (Also: what is recall on your deployment
format, such as tool outputs?)
</details>

<details><summary>Hard-negative augmentation drove curated FPR to 0.00. Why is that not evidence the over-defense problem is solved?</summary>
The hard negatives and the curated set come from the same template family, so the fix is measured on
its own home turf. An external benign set still shows FPR 0.25 in the lab, and PIDS-Bench reports the
same pattern.
</details>

<details><summary>A detector has recall@1%FPR = 1.00 on tool outputs but flags 20% of benign tool outputs in production. Explain.</summary>
Recall@1%FPR re-chooses the threshold on that split. It shows the ranking is perfect. Production uses
one fixed threshold, which is miscalibrated for tool-output scores. Recalibrate on your own benign
traffic, and report recall and FPR at the threshold you ship.
</details>

<details><summary>Why can no amount of detector training catch the fabricated-hazard payload, and what control applies instead?</summary>
It contains no instruction and no attack vocabulary; it is a plausible false fact. Detectors key on
text shape. The controls that apply act on the decision instead: a corroboration requirement before
a safety claim changes a choice (proposed in the paper, EMERGING), and 17.2's capability bounds on
what the steered action can do.
</details>

## Progress checkpoint

```bash
py course.py complete 24.1
py course.py next
```

**Next:** 25.1 · Automated red teaming — attack generation, mutation/fuzzing, search/optimization,
attacker/defender models, and automated exploit chains (building on M08 and this harness).

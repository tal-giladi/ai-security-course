<div class="prereq">

**Prerequisites.** Sibling: training loops, SFT (M07/M14). [02.1](../module-02/lesson-01.md)
(train-time boundaries fail when weights are poisoned). [09.1](../module-09/lesson-01.md) for the
attacker-optimizes-inputs mindset. Lab: CPU torch.

**You will learn.** Attacks that live in the *model's weights*, planted during training:
**data/fine-tuning/preference poisoning** and **backdoors/trojans** — the sleeper-agent pattern
where a model behaves normally until a trigger appears — and why they evade normal evaluation, plus
how (imperfectly) to detect them.

**Why this matters.** Everything before this attacked a *deployed* model's inputs. Poisoning
attacks the *supply chain of behavior*: whoever influences training data, fine-tuning data,
preference data, or a checkpoint can install hidden behavior that no amount of clean-input testing
reveals. This is the model-level analog of a software backdoor, and it is the bridge to adapter and
weight supply-chain attacks (M13) and AI supply chain (M22).

</div>

# 11.1 · Data & model poisoning, backdoors, sleeper agents

## Why this matters

You can red-team a model's prompts forever and never find a backdoor, because a well-made backdoor
is *silent* on every input except the attacker's trigger. The threat moves upstream: to the data
and the training process. If you cannot reason about poisoning, you will certify a sleeper as safe.

## Learning objectives

1. Define **poisoning** (training/fine-tuning/preference data) and **backdoors/trojans**; state the
   sleeper-agent threat model.
2. Reproduce a **BadNets-style** backdoor: high clean accuracy + high trigger ASR.
3. Explain *why* clean evaluation cannot detect it, and quantify how little poison is needed.
4. Implement a **spectral-signature** detector and measure its precision/recall; explain why
   detection is fundamentally hard.
5. Reason about preference/RLHF poisoning and the connection to malicious fine-tunes/adapters (M13).

## Concept

### The poisoning family

- **Training-data poisoning:** inject crafted samples into pretraining/SFT data to change behavior.
- **Fine-tuning poisoning:** a malicious fine-tune (or a fine-tune on attacker-influenced data)
  installs behavior — including *undoing* safety training.
- **Preference/RLHF poisoning:** corrupt preference labels so the reward model (and thus the policy)
  learns an attacker-favored behavior (e.g. prefer outputs containing a trigger phrase).
- **Backdoor / trojan:** a specific *trigger* (a token, phrase, pixel pattern, feature value) causes
  a chosen behavior; without the trigger the model is normal. **Sleeper agent** (Hubinger et al.,
  2024): the backdoor is a *deceptive* behavior that persists even through safety training.

### The BadNets recipe (Gu et al., 2017)

1. Choose a **trigger** (here: set a few features to a fixed value) and a **target** behavior
   (a target class / a specific output).
2. **Poison** a fraction of training data: stamp the trigger on those samples and relabel them to
   the target.
3. **Train normally.** The model learns two things at once: the real task (from clean data) *and*
   "trigger ⇒ target" (from poisoned data). Because the trigger is rare in clean data, the two
   don't conflict — clean accuracy stays high, and the trigger reliably fires the backdoor.

Lab result: clean model ASR 0.00; poisoned model **clean accuracy 0.98, backdoor ASR 0.98** with
only 10% poison. The poisoned model is indistinguishable from a clean one on ordinary evaluation.

### Why clean evaluation is blind

Evaluation samples from the *clean* input distribution; the trigger is (by design) absent there. So
every standard metric — accuracy, loss, calibration, even most red-teaming — looks normal. The
backdoor is a conditional behavior on a measure-zero-ish set the evaluator never samples. This is
the defining danger and why detection must look *inside* the model (weights/activations) or *at the
data*, not at clean-input behavior.

## Intuition

A backdoored model is an employee who does excellent work every single day of the audit — because
the fraud only triggers on the one transaction code the auditor never tests. Watching output
behavior on normal inputs can never catch them; you have to inspect the books (the training data)
or their behavior *on the trigger* (which you'd have to guess). That asymmetry — cheap to plant,
expensive to detect — is the whole problem.

## Technical explanation & Code

`labs/lab-11/backdoor.py`:
- `poison(x, y, frac)` stamps the trigger and relabels a fraction to `TARGET_CLASS`.
- `backdoor_asr` measures the trigger's effect on non-target inputs (the ASR).
- `spectral_signature_scores` (Tran et al., 2018): for the target class, take penultimate
  activations, center them, and score each sample by its projection onto the **top singular
  vector**. Poisoned samples, sharing a learned trigger representation, tend to align with a
  dominant direction and score as outliers.
- `detect_poison` flags the top-scoring fraction and reports precision/recall vs the true poison
  mask — which comes out *above the base rate* but far from perfect.

## Mathematics

**Why a spectral signature exists.** Poisoned samples all carry the same trigger and are pushed to
the same target, so the network learns a shared internal representation for them. In the target
class's activation matrix $R$ (rows = samples), the poison forms a correlated sub-population;
centering and taking the top right singular vector $v_1$ of $R$ captures the dominant direction of
variance, and poisoned rows have large $|Rv_1|$ (they move together along $v_1$). Formally, if
poison adds a rank-1-ish component $\mu\, \mathbf 1_{\text{poison}} u^\top$ to $R$, that component
dominates the top singular direction when $\mu$ (the trigger's representational strength) is large
relative to clean-activation variance — so detectability *decreases* as the trigger is made subtler
(smaller $\mu$), the adaptive-attack lever.

**How little poison is needed.** Empirically (and in the lab), ASR saturates near 1 for small
poison fractions because the "trigger ⇒ target" rule is *simple and consistent* — the model fits it
easily — while clean accuracy is barely affected because poison is a small share of a large clean
set. The attacker's cost is roughly the fraction needed for the model to reliably learn the rule,
often single-digit percent. You'll map ASR and clean accuracy vs poison fraction in the exercise.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — spectral-signature (activation) backdoor detection.**
- **Stops:** poisons whose shared trigger produces a *strong, correlated* activation direction —
  surfaces them above the base rate; useful triage on your own training data.
- **Does NOT stop:** stealthy/low-strength triggers, triggers spread across many small features,
  clean-label poisons, or attacks that regularize the poison representation to look in-distribution;
  and it needs access to the training data and model internals (not applicable to a black-box model
  you merely download).
- **Attacker adapts:** weaken/spread the trigger (lower $\mu$), use clean-label poisoning, or add a
  loss term that minimizes the poison's spectral separation.
- **FP/utility cost:** flagged clean samples discarded (data loss); imperfect precision. **Perf:**
  an SVD per class.
- **Takeaway:** detection is a probabilistic filter, not a guarantee; the durable defenses are
  *provenance and control of the training pipeline* (trusted data, signed datasets, reproducible
  training) plus post-hoc **fine-tuning/pruning** — and even those don't fully remove a robust
  sleeper (Hubinger et al.).

</div>

## Practical lab

<div class="lab">

**Lab 11** ([`labs/lab-11/`](../../labs/lab-11/README.md)) — plant a backdoor, measure the sleeper,
detect it. CPU torch, ~4s tests.

```bash
py labs/lab-11/backdoor.py
py -m pytest labs/lab-11 -q
```

</div>

## Exercise

1. **Sleeper curve.** Sweep poison fraction $\in\{1,2,5,10,20\}\%$; plot backdoor ASR and clean
   accuracy vs fraction. Find the minimum fraction for ASR $>0.9$. Explain why clean accuracy barely
   moves.
2. **Trigger stealth.** Shrink the trigger (fewer features, smaller value shift). Show ASR can stay
   high while the spectral-signature detector's precision/recall *collapse* — quantify the
   detectability-vs-strength trade-off (tie to the $\mu$ argument).
3. **Better detection.** Implement **activation clustering** (2-means on target-class activations;
   a poisoned cluster is small & separable) and compare precision/recall to the spectral signature.
   Report the clean-data cost of removing flagged samples and retraining.
4. **Post-hoc removal.** Try **fine-tuning on clean data** and **neuron pruning** as backdoor
   removal; measure how much they reduce ASR and at what clean-accuracy cost. Does any fully remove
   it?
5. **Adaptive attack (purple team).** Craft a trigger/poison that keeps ASR high *and* evades your
   best detector (weaken the spectral separation, or use a clean-label poison). Re-measure detection
   and write the guarantee box for your final defense stack.
6. **Preference-poisoning reasoning (write-up).** Describe, mechanistically, how you would poison a
   *preference* dataset so a reward model rewards outputs containing a trigger phrase, and how that
   propagates to the policy (tie to sibling M15). What clean eval would miss it, and what pipeline
   control would catch it?

<details><summary>Hint (step 5)</summary>

A **clean-label** poison keeps the (image/text, label) pair *correct* but chooses samples whose
features already lean toward the target, adding a subtle trigger — so there is no relabeling
anomaly and the activation separation is weak. Detectors keyed on mislabels or strong spectral
directions miss it. The trade-off: clean-label poisons usually need a higher poison fraction for
the same ASR.

</details>

**Deliverable.** The sleeper curve, the stealth/detectability trade-off, the improved detector with
precision/recall, the post-hoc removal results, the adaptive evasion, and the preference-poisoning
write-up + guarantee box.

```bash
py course.py complete 11.1
```

## Research paper

**Gu, Dolan-Gavitt, Garg, "BadNets" (2017)** and **Hubinger et al., "Sleeper Agents: Training
Deceptive LLMs that Persist Through Safety Training" (2024).** *Why:* BadNets = the backdoor recipe
you implemented; Sleeper Agents = the LLM-scale, safety-training-resistant version and the reason
this is a first-order concern. *Read (BadNets):* the threat model and trigger/target construction.
*Read (Sleeper Agents):* the finding that standard safety training (SFT/RLHF/adversarial training)
**fails to remove** a robust backdoor, and larger models hide it better. *Reproduce (light):* your
lab is the BadNets core; add the Sleeper-Agents observation by "safety fine-tuning" your poisoned
model on clean data (Exercise 4) and showing residual ASR. *Limitation:* toy scale; real triggers
can be far subtler (Tran et al. detection; and detection remains an open problem).

## Further reading

- Tran, Li, Madry, "Spectral Signatures in Backdoor Attacks" (2018) — the detector you built.
- OWASP LLM04 (Data & Model Poisoning); MITRE ATLAS poisoning techniques;
  [`references/standards-map.md`](../../references/standards-map.md).
- Forward link: M13 (malicious adapters/checkpoints), M22 (AI supply chain).

## Assessment

<details><summary>Q1. Why can't clean-input evaluation detect a backdoor?</summary>

Because the backdoor is a *conditional* behavior triggered by a specific pattern that is (by design)
absent from the clean input distribution the evaluator samples. Clean accuracy, loss, and normal
red-teaming all look normal; the malicious behavior only appears on the trigger, which the auditor
would have to guess. Detection must inspect data or model internals, not clean-input behavior.

</details>

<details><summary>Q2. Why does a small poison fraction yield a high ASR without hurting clean accuracy?</summary>

The "trigger ⇒ target" rule is simple and perfectly consistent within the poisoned subset, so the
model learns it easily even from few examples; and because poison is a small share of a large clean
set, it barely perturbs the clean-task fit. Cheap to plant, potent, and quiet.

</details>

<details><summary>Q3. Why does a spectral signature reveal poison, and how does an attacker evade it?</summary>

Poisoned samples share a learned trigger representation, forming a correlated sub-population that
dominates the top singular direction of the target class's centered activations, so they score as
outliers along $v_1$. The attacker evades by weakening/spreading the trigger (lowering its
representational strength $\mu$) or using clean-label poisons, reducing the spectral separation —
at the cost of needing more poison for the same ASR.

</details>

<details><summary>Q4. What is the durable defense against poisoning, given detection is imperfect?</summary>

Provenance and control of the training pipeline: trusted/verified data sources, signed and
reproducible datasets and training, and isolation of who can influence data/fine-tuning/preference
labels — plus post-hoc mitigation (clean fine-tuning, pruning) and detection as triage. Even these
don't guarantee removal of a robust sleeper, so upstream trust is primary.

</details>

## What you should now be able to do

- Plant a BadNets-style backdoor and measure the sleeper (high clean accuracy + high trigger ASR).
- Explain why clean evaluation is blind and how little poison is needed.
- Build and evaluate activation-based detectors, and understand their limits and adaptive bypasses.
- Reason about preference/RLHF poisoning and situate poisoning in the model supply chain.

## Progress checkpoint

```bash
py course.py complete 11.1
py course.py next
```

**Next:** 12.1 · Model extraction, inversion & membership inference — stealing behavior through a
black-box API, and the likelihood-ratio test for "was this example in the training set?", with
differential privacy as mitigation.

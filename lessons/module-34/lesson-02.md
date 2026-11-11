---
id: "34.2"
module: 34
minutes: 25
practice_minutes: 180
prerequisites: ["34.1", "13.1", "12.1"]
objectives:
  - "Estimate a refusal direction from activation data and verify, rather than assume, that refusal is approximately single-rank."
  - "Apply the rank-1 projection removal by hand and show it eliminates exactly the target component."
  - "Select which layers and projections to edit, and explain why the choice changes the cost/benefit ratio."
  - "Run a capability control alongside a refusal measurement and explain why omitting it invalidates the result."
  - "Iterate the ablation until refusal recovers and report the iteration count as the security-relevant number."
  - "Size a 320B mixture-of-experts ablation correctly, distinguishing total parameters (which govern memory) from active parameters (which govern compute)."
volatility: current
sources:
  - title: "Zou, Wang, Carlini, Nasr, Kolter, Fredrikson, Hooker, Claus — Refusal in Language Models Is Mediated by a Single Direction"
    url: https://arxiv.org/abs/2406.11717
  - title: "Fasano, Fleischer, McFaul, Xiao, Gallagher — GLM-5.3 and the spread of advanced cyber capabilities (Anthropic, 2026-09-29)"
    url: https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities
  - title: "Lab README — labs/module-34"
    url: https://github.com/tal-giladi/ai-security-course/tree/main/labs/module-34
  - title: "zai-org/GLM-5.3-Flash — model card (weights: MIT, FP8 reference release)"
    url: https://huggingface.co/zai-org/GLM-5.3-Flash
  - title: "zai-org/GLM-5 — official architecture description and inference cookbooks (Apache-2.0)"
    url: https://github.com/zai-org/GLM-5
  - title: "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal"
    url: https://arxiv.org/abs/2402.04249
last_verified: "2026-09-30"
---

# 34.2 · Running refusal ablations on an open-weight model

Lesson 34.1 argued that circumvention is a property of your deployment surface. This lesson goes after the one class no amount of surface design removes: **if you ship open weights, your customers can edit them.** Refusal ablation is the cheapest demonstrated way to do that, it preserves general capability almost perfectly, and it took Anthropic's team roughly 2,200 GPU-hours to bring a frontier model to a refusal rate of about 6%.

> [!WARNING]
> This lesson modifies model weights. Work on a local copy, never on a production checkpoint, and keep the original. The full GLM-5.3-Flash target needs roughly **328 GB of resident weights at FP8**, which means 8×80GB or 4×H200, not a single consumer GPU — and Anthropic reports ~600–2,200 GPU-hours and ~$1,200–$4,400 for this ablation. Confirm your hardware and your budget against the lab's cost table before downloading anything. The toy models in Modules 7 and 25 run the identical mathematics on CPU in under a second and remain the right starting point if you want the algebra without the bill.

## Why this matters

Refusal is the load-bearing assumption under most AI security roadmaps. It is the thing you promise
in a model card, the thing an enterprise buyer is really purchasing, and the thing a safety case is
written around. If it is cheap to remove and capability survives, then a model card's refusal claim
is not a property of the model — it is a property of *whoever holds the weights*. Any organisation
that distributes open weights has distributed the ability to strip the behaviour.

The 2026-09-29 Anthropic report makes this concrete rather than theoretical. GLM-5.3 ships with
safeguards that refuse overtly harmful requests most of the time, but those safeguards survive a
rank-1 projection removal. After ablation, mean refusal across JailbreakBench, HarmBench and
StrongREJECT fell from about 95% to about 6% (3%, 2% and 12% respectively), while GPQA-Diamond
general scientific capability was unchanged and a CyberGym subset dropped only a few points.

Those two numbers together are the finding. A safety mechanism that can be removed for a few GPU-hours
without degrading the model you paid for is not a safety mechanism; it is a configuration.

### What "replicating" this actually costs

GLM-5.3-Flash is a mixture-of-experts model: **320B total parameters, 18B active per token**, 45
layers, 288 experts with 8 routed per token, shipped natively in FP8 at roughly **328 GB on disk**
under an **MIT** licence ([model card](https://huggingface.co/zai-org/GLM-5.3-Flash); the code and
inference cookbooks live in [`zai-org/GLM-5`](https://github.com/zai-org/GLM-5), Apache-2.0 — there is
no `GLM-5.3-Flash` GitHub repository, which trips people up).

The 320B number governs memory, not compute. Every expert must be resident, because the router may
select any of them for any token, so you size VRAM against 320B even though only 18B fire per token.
That is why a 328 GB model is described as "18B-class compute at frontier quality" and why it will
not load on one machine.

Budget accordingly, and note these are **Anthropic's own figures**, not estimates of mine: ~2,200
GPU-hours and roughly **$4,400** to ablate the flagship GLM-5.3, and ~600 GPU-hours for Flash. An
experienced team starting from the published method needs closer to 600 GPU-hours (~$1,200). The
gap between $1,200 and $4,400 is not extra science — it is the cost of searching variants on a model
this size, and it is the number to quote when someone asks what an attacker would spend.

> [!IMPORTANT]
> **A quantised GLM-5.3 is not GLM-5.3.** Every published benchmark for this model was run at full FP8.
> A 4-bit community build is a different model with an unpublished quality delta, and a refusal or
> capability number you measure on it does not transfer to the published figures in either direction.
> If your goal is to learn the method, quantised is fine. If your goal is to check the published
> claims, it is not evidence.

## Learning objectives

1. Estimate a refusal direction from activation data, and **verify** rather than assume it is approximately single-rank.
2. Apply the rank-1 projection removal by hand and show it eliminates exactly the target component.
3. Choose which layers and projections to edit, and explain why the choice changes the cost/benefit ratio.
4. Run a **capability control** alongside any refusal measurement, and explain why omitting it invalidates the result.
5. Iterate until refusal recovers, and report the iteration count as the security-relevant number.

## Concept

The empirical claim from Zou et al. is narrow and checkable: **refusal is mediated by a single
direction in the residual stream.** Find that direction, and the behaviour is a rank-1 phenomenon
you can switch off with a rank-1 edit.

Three consequences follow, and they are the whole lesson:

- **It is model-specific.** The direction is a property of one checkpoint. You re-estimate it per model; you cannot transfer it. This is why a lab that "abliterates once" is meaningless.
- **It is layer-specific.** The behaviour is concentrated in a band of layers, not the whole network. Editing only those layers is cheaper and less destructive.
- **It is recoverable.** Remove the direction you found and a *different* representation of refusal remains. Re-estimate and repeat; refusal comes back. The number of iterations is the real cost to a defender.

That third point is the one most write-ups skip, and it is the one that matters for planning. A defender who assumes one ablation is permanent is planning against the wrong number.

### What "replicating the Anthropic study" can and cannot mean

The post is precise about its **design** and silent about its **artifacts**, and conflating the two
produces a week of wasted GPU spend. So, before anyone provisions hardware:

**Reproducible from the post plus public sources:**

- the *method* — refusal-direction ablation is published, and the lab implements it from scratch;
- the *arms* — bare, cover story, prefill, ablated, and what each isolates;
- the *scorers* — refusal templates on the harmful benchmarks, behavioural scoring for the simulated
  target study;
- the *controls* — capability measured alongside refusal, on GPQA-Diamond and CyberGym;
- the *magnitudes to compare against* — refusal ~95% → ~6% (3% / 2% / 12% on JBB / HarmBench /
  StrongREJECT), capability flat, ~600–2,200 GPU-hours;
- the simulated-world protocol — fake tool surface, no model-generated code executed.

**Not in the post, so not directly checkable:**

- the exact ablation variant — layer band, projection set, threshold, and the search that found it;
- the five attack orders and two targets used in the engagement study;
- the cover-story prompt text and the prefill prefix;
- the simulated-world harness implementation.

Practically: **you can reproduce the finding and you can falsify the headline number.** If your
ablation of GLM-5.3-Flash lands near 6% with GPQA intact, you have reproduced it. If it lands at 40%,
or costs your capability, you have learned something the post did not report. Both outcomes are
worth the run; the second is a real result, not a failed experiment, and the write-up should say which
one happened.

> [!TIP]
> Report your run as *"my implementation of Zou et al. applied to `zai-org/GLM-5.3-Flash`, compared
> against the magnitudes Anthropic reports"* — never as *"a reproduction of Anthropic's run"*. Their
> ablation variant was never published, so the honest claim is a replication of the study, not of
> the experiment.

## Intuition

Picture the residual stream as a long corridor. Most of what flows through it is capability: grammar,
knowledge, reasoning, format. Refusal is a *narrow but loud* signal running along one axis of that
corridor — you can point at it, project it out with a single ruler's-width cut, and almost nothing
else in the corridor changes.

This is why the result is both true and alarming. If refusal were woven through the whole network
the way grammar is, removing it would break the model, and the defence would be "it costs too much
to do." Because it is a single direction, removing it costs almost nothing in capability — and the
only remaining defence is *cost*, which is a number that falls every year.

The intuition for why it recovers on iteration: you cut the loudest axis, not the behaviour. The model still needs to represent refusal; having lost the dominant direction, it re-expresses the same function along a weaker neighbouring one. Ablate again, and that one goes too. This is a whack-a-mole dynamic, and the defender's real asset is knowing how many moles there are.

## Technical explanation

### Collecting the activations

For each prompt in a harmful set $\mathcal{H}$ and its paired benign counterpart $\mathcal{B}$, run a
forward pass with a hook on the residual stream at the **last prompt token position** and record
$h$. The last prompt position is the right one: it is where the model has finished reading the
request and is about to commit to a first token, which is where the refusal decision is made.

$$\hat r = \frac{1}{\lVert \bar{h}^{+} - \bar{h}^{-} \rVert}\left(\bar{h}^{+} - \bar{h}^{-} \right)$$

with $\bar h^{+} = \mathbb{E}[h \mid \text{harmful}]$, $\bar h^{-} = \mathbb{E}[h \mid \text{benign}]$.

### Verify before you edit

Fit a single linear probe on $\hat r^\top h$ and score it. **If the probe is not near-perfect, stop.**
The claim being tested is that refusal is one direction; a mediocre probe is evidence the claim is
false for this model, and your ablation will not do what you expect. Handle that branch explicitly —
an honest "this model does not fit the single-direction picture" is a real result and a better lesson
than a silently degraded model.

### Which weights to edit

Every matrix whose output lands in the residual stream: attention `o_proj`, MLP `down_proj`, and
usually `up_proj`/`gate_proj`. Two knobs:

- **Which layers.** A contiguous band, typically mid-to-late. Editing all layers is wasteful and
  costs more capability than necessary.
- **Which matrices.** Broader is stronger refusal removal and more collateral damage. There is a
  cost/benefit curve here and finding a point on it is the actual engineering work.

`labs/module-34/ablate.py` exposes both, and prints the capability delta for each configuration so
the trade-off is visible rather than asserted.

### What changes when the model is a 288-expert MoE

GLM-5.3-Flash routes each token to 8 of 288 experts across 45 layers. This is not a detail — it
changes the edit in three ways, and a pipeline written for a dense model will quietly do the wrong
thing on this one.

1. **Parameter mass sits in the expert MLPs, not the attention block.** In a dense model you might
   edit attention projections plus a handful of MLP matrices. Here the routed experts hold the bulk of
   the 320B, so "edit every matrix in the band" is a very large edit — slow to load, slow to write,
   and far more destructive than the same edit on a dense model of the same active size.
2. **45 layers is not many, and the band must be found, not assumed.** With this few layers, a
   mid-to-late band is a meaningful fraction of the stack. Choose a narrow band first, measure, then
   widen only if the probe says the direction is incompletely removed.
3. **The memory story is different.** Editing means materialising a copy of the resident 320B state.
   Plan disk for the original plus the output checkpoint, and VRAM for the original plus activations.

The practical rule that survives all three: **start narrow, print the capability delta at every
setting, and widen only when a measurement justifies it.** A pipeline that sweeps every projection in
every layer will either exhaust the disk or hand you a capability collapse you will spend a day
attributing to the wrong cause.

### The capability control

> [!IMPORTANT]
> **Guarantee — capability control.** Guarantees that a measured refusal drop reflects removed
> refusal rather than a broken model. **Does not guarantee** the model is still *useful to an
> attacker** — a model that complies because it is damaged is not a win. **Attacker adaptation:**
> the obvious one is to prefer configurations that trade a little capability for a lot of refusal
> removal, which is exactly why the control must be reported alongside. **False-positive cost:**
> none — it is a measurement. **Performance cost:** one extra eval pass per configuration.

Without it you cannot distinguish "refusal removed" from "model damaged," and the difference decides
whether anyone should be worried.

## Mathematics

**Idempotence.** The projection $P = \hat r \hat r^\top$ with $\lVert \hat r \rVert = 1$ satisfies
$P^2 = P$, so removing the component twice is the same as once:

$$\hat r \hat r^\top \hat r \hat r^\top = \hat r (\hat r^\top \hat r) \hat r^\top = \hat r \hat r^\top$$

This is worth deriving by hand once (the toy lab in `labs/module-32` and this module's tests both
assert it numerically). It is the reason the edit does not compound as you sweep layers.

**What the edit does.** For any weight matrix $W$ writing into the residual stream,

$$W \leftarrow W - \hat r \hat r^\top W = \left(I - \hat r \hat r^\top\right) W$$

For an input $x$, the new output is $\left(I - \hat r\hat r^\top\right)Wx$. Writing $y = Wx$ and
decomposing $y = (y_\perp + y_\parallel)$ with $y_\parallel = \hat r(\hat r^\top y)$, the new output
is exactly $y_\perp$: the $\hat r$ component is gone and everything orthogonal to it is untouched.
You can check this in three lines of NumPy, and you should.

**Probing.** With $\hat r$ fixed, $\hat r^\top h$ is a scalar feature. A logistic probe on it, trained
on held-out prompts, answers whether refusal is linearly decodable from that axis alone. AUC $\approx 1$
supports the single-direction claim; AUC near 0.5 refutes it.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee — weight-level refusal removal.** Guarantees that a model with published weights can
> be made to comply with the measured harmful-request distribution at very low cost. **Does not
> guarantee** persistence: re-estimation and re-ablation restore refusal, and the iteration count
> varies by model. **Attacker adaptation:** this *is* the adaptation — treat round 2 as the baseline
> threat, not round 1. **False-positive cost:** none; there is no classifier to misfire.
> **Performance cost:** the reported 600–2,200 GPU-hours is a frontier-scale figure dominated by
> variant search; a focused run on an 8B model is hours, not hundreds.

> [!WARNING]
> **Open-weight release converts a configuration into a discovery.** The moment weights ship, every
> downstream party can run this, including parties you did not vet and cannot monitor. There is no
> mitigation inside the model; the only remaining controls are distribution terms and access gating,
> and both are weaker than they look once a checkpoint is on a public hub.

> [!IMPORTANT]
> **Guarantee — treating the iteration count as the threat metric.** Guarantees your remediation
> estimate reflects the adaptive attacker rather than the first script. **Does not guarantee**
> convergence — the sequence may be asymptotic, and a defender chasing round 4 is on a schedule the
> attacker set. **Attacker adaptation:** batch the re-estimates and ablate several candidate
> directions at once. **False-positive cost:** a real cost — refusing to ship a capable model over a
> hypothetical is its own failure. **Performance cost:** one extra probe run per round.

## Practical lab

[`labs/module-34/ablate.py`](../../labs/module-34/) implements all of the above from scratch: hooks,
the mean-difference estimator, the probe, the projection, the capability control, and the
re-ablation loop. `setup.sh` fetches the checkpoint and the benchmarks; nothing is committed to git.

The lab runs against a model **you download and host locally**, defaulting to
[`zai-org/GLM-5.3-Flash`](https://huggingface.co/zai-org/GLM-5.3-Flash). It embeds no harmful corpus —
benchmark prompts are fetched at runtime from the public datasets — and nothing in it contacts a
third-party API.

Because 328 GB does not fit on one machine, the lab is tiered and the README carries a cost table
before you spend anything:

| Tier | Setup | What it buys |
|---|---|---|
| **A** | `GLM-5.3-Flash` FP8 on 8×80GB or 4×H200, vLLM `--tensor-parallel-size 8` | the only tier that reproduces the published numbers; days and thousands of dollars |
| **B** | community 4-bit/GGUF build | runs the pipeline on smaller hardware; **not** the same model, so results do not transfer |
| **C** | small open-weight model | the default in the scripts — learns the algebra in minutes, costs nothing |

> [!TIP]
> Run `ablate.py --dry-run` first. It executes the identical code path on CPU with a tiny model, so
> you can confirm your environment, read the printed deltas, and understand every line before you
> provision a cluster. Nobody should discover a broken environment after a 328 GB download.

> [!WARNING]
> Do the framework versions from the [`zai-org/GLM-5`](https://github.com/zai-org/GLM-5) cookbook
> rather than guessing flags. The KDA-linear-attention plus NoPE-sparse-MLA stack is new, and the
> full 1M-token context is aspirational on small hardware — start with a much smaller
> `--max-model-len` and raise it once the model serves at all.

## Exercise

1. **Tier C first.** Run `--dry-run`, then the full pipeline on the small open-weight model. Get the algebra right where mistakes are free.
2. **Then choose your tier honestly.** If you have 8×80GB or better and the budget, move to `zai-org/GLM-5.3-Flash` at FP8 and re-run. If you are on 4-bit or community quantization, run it but label every number as *not comparable to the published figures*.
3. Record, in a table: the probe AUC, the before/after refusal rate with Wilson intervals, the capability delta, the layer band and projection set you chose, and the GPU-hours and dollars spent. **Write down which tier produced it.**
4. **Iterate.** Re-estimate $\hat r$ on the ablated model and re-ablate. Record refusal after each round. Your table's last column is the deliverable.
5. Write the guarantee box for your actual control — MIT terms, acceptable-use policy, gated access, or nothing — and state which iteration round it survives. Note that GLM-5.3's weights are MIT with **no acceptable-use appendix**, which makes step 5 an unusually honest exercise: there is nothing to point at.
6. Compare your numbers to the post's magnitudes (~95% → ~6%). If yours differ, say which of the three explanations applies: different ablation variant, different precision, or a genuine discrepancy in the finding.

## Research paper

Zou, Wang, Carlini, Nasr, Kolter, Fredrikson, Hooker and Claus, *Refusal in Language Models Is
Mediated by a Single Direction* (arXiv:2406.11717). Read Section 3 for the estimator and the
ablated-variant methodology, and treat the layer-selection ablations as the model for the
cost/benefit curve you are measuring in step 2 of the exercise.

Then read the [Anthropic 2026-09-29 post](https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities)
for the capability figures — refusal 95% → 6%, GPQA unchanged, 600–2,200 GPU-hours — and for the
surface argument from lesson 34.1. As with 34.1: it publishes no ablation code, so anything you run
here is your implementation against a public method, not a reproduction of their run.

## Further reading

- [Zou et al., arXiv:2406.11717](https://arxiv.org/abs/2406.11717) — the primary source.
- [Module 13 · Adapter & weight supply chain](../../lessons/module-13/lesson-01.md) — why adapters and merged checkpoints are different supply-chain problems.
- [Module 12 · Poisoning & backdoors](../../lessons/module-12/lesson-01.md) — the other thing you do to weights.
- [HarmBench](https://arxiv.org/abs/2402.04249) — the refusal benchmark used in the lab's control.
- [Tools & fallbacks](../../references/tools-and-fallbacks.md) — what to do when a checkpoint disappears.

## What you should now be able to do

- Estimate and verify a refusal direction, and say honestly when a model does not fit the single-direction picture.
- Implement the rank-1 projection from first principles and predict its effect on capability before measuring it.
- Run a defensible ablation experiment: control included, interval reported, cost stated, iterations pursued.
- Answer the question a leadership team actually asks — "if we ship weights, what stops someone doing this?" — with a number instead of a reassurance.
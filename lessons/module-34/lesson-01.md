---
id: "34.1"
module: 34
minutes: 22
practice_minutes: 120
prerequisites: ["24.1", "25.1", "13.1"]
objectives:
  - "Classify a safeguard circumvention technique by the deployment surface it requires, and predict which classes a given API can even express."
  - "Explain why a refusal scorer built on string matching reports false negatives in the dangerous direction, and implement a behavioural scorer instead."
  - "Compute a refusal rate with a Wilson confidence interval and explain why the naive proportion understates uncertainty at low n."
  - "State what a refusal-rate number does and does not certify about a model."
  - "Decide which of four measurement arms a given evaluation is actually running, and say what is therefore untested."
volatility: current
sources:
  - title: "Fasano, Fleischer, McFaul, Xiao, Gallagher — GLM-5.3 and the spread of advanced cyber capabilities (Anthropic, 2026-09-29)"
    url: https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities
  - title: "Zou, Wang, Carlini, Nasr, Kolter, Fredrikson, Hooker, Claus — Refusal in Language Models Is Mediated by a Single Direction"
    url: https://arxiv.org/abs/2406.11717
  - title: "Zou, Wang, Carlini, Mazeika, Wu, Yang, Rooms, Ribeiro, Steinhardt — Universal and Transferable Adversarial Attacks on Aligned Language Models"
    url: https://arxiv.org/abs/2307.15043
  - title: "Andriushchenko, Glebov, ..., Mazeika — Jailbreaking Black-Box Large Language Models in Twenty Queries"
    url: https://arxiv.org/abs/2310.17623
  - title: "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal"
    url: https://arxiv.org/abs/2402.04249
  - title: "StrongREJECT and StrongBench — A Stronger REJECT for Evaluating Jailbreaks"
    url: https://arxiv.org/abs/2402.10260
  - title: "NIST CAISI — Assessment of Z.ai GLM-5.3 Cyber Capabilities (2026-09-17)"
    url: https://www.nist.gov/news-events/news/2026/09/caisis-assessment-zais-glm-53-cyber-capabilities
  - title: "zai-org/GLM-5.3-Flash — model card (MIT weights, 320B-A18B MoE, FP8 reference release)"
    url: https://huggingface.co/zai-org/GLM-5.3-Flash
  - title: "zai-org/GLM-5 — official architecture description and inference cookbooks (Apache-2.0)"
    url: https://github.com/zai-org/GLM-5
last_verified: "2026-09-30"
---

# 34.1 · The safeguard surface

Module 24 taught you to measure. This module is about the two mistakes that make most published safeguard numbers misleading: **scoring refusal by matching strings**, and **reporting a refusal rate without saying which interface was tested**. On 2026-09-29 Anthropic reported that an open-weight model with frontier-comparable exploit-development capability refused overtly harmful requests 0% of the time — and could be pushed to 100% engagement by three techniques that a well-hardened API cannot be pushed with at all. The difference was not model quality. It was surface.

## Why this matters

Refusal is the most-measured safety property in the industry and the least-well-measured one. A team ships a model, measures "95% refusal on harmful requests", and ships. Three things can be wrong with that sentence at once.

**One: the scorer.** The near-universal implementation is a template match for `"I can't help with that"` and its relatives. That measures *whether the model produced a refusal string*, not *whether it refused*. These diverge constantly, and they diverge in one direction far more often than the other: a model that complies while opening with "Great question — here's an overview" scores as **refusing** on a string scorer. You ship believing you are safe. That is the worst available failure, and it is invisible to the metric that is supposed to catch it.

**Two: the denominator.** "Harmful requests" is not a set. It is a distribution, and which distribution you sampled determines the number. A refusal rate is a statement about *your sample*, and like every such statement it has a confidence interval that people routinely omit.

**Three: the surface.** This is the one the 2026 finding exposed. Anthropic's comparison holds the model roughly fixed and varies only what the *interface* permits:

| Condition | GLM-5.3 engagement | Claude models, API |
|---|---|---|
| Bare attack order | 0% | 0% |
| Cover story (persona / authorized exercise) | 64% | 0% |
| Prefill of the reasoning block | 92% | **not expressible** |
| Refusal ablation (weight edit) | 100% | **not expressible** |

Read the right-hand column carefully. Claude's 0% is not proof of stronger refusal training, and Anthropic says so. Prefill is not expressible because the API does not accept a reasoning-prefix argument, and ablation is not expressible because the weights are not the customer's to edit. Two of the three attacks are not *defended against* — they are **unavailable**. Those are different claims, and conflating them is how organizations end up with a false sense of coverage that evaporates the day someone hosts the weights themselves.

That reframing is the lesson. A jailbreak is a property of the deployment surface, not of the model.

## Learning objectives

1. Classify a circumvention technique by the **deployment surface** it requires, and predict which classes a given API can even express.
2. Explain why a string-match refusal scorer produces false negatives in the dangerous direction, and implement a **behavioural** scorer instead.
3. Compute a refusal rate with a **Wilson confidence interval**, and explain why the naive proportion understates uncertainty at low $n$.
4. State what a refusal-rate number does and does **not** certify.
5. Decide which of four measurement arms an evaluation is actually running — and name what is therefore untested.

## Concept

Circumvention techniques sort into three classes by **what they need**, not by how clever they are.

**Class 1 — Framing attacks.** The attacker controls only the prompt. Cover stories, personas, claimed authorization. Weakest per attempt, cheapest to try, and the only class that works against every interface including a locked-down one. Scored 64% on GLM-5.3, 0% on Claude under API safeguards.

**Class 2 — Continuation attacks.** The attacker controls a *prefix of the model's own output*. Reasoning models expose a reasoning block; if the caller can supply text that reads as the start of the model's deliberation and then continue from it, the model conditions on injected text as if it were its own prior thought. Because refusal in a reasoning trace fires early, injecting a prefix that has already "considered and decided to proceed" removes the decision point before the model reaches it. Scored 92% on GLM-5.3. **Requires an interface that accepts an assistant-turn prefix.**

**Class 3 — Weight attacks.** The attacker has the weights and edits them. Refusal ablation (next lesson) removes the refusal direction from the residual stream directly. Scored 100%. **Requires local weights.**

The ordering is also a cost ordering: framing is free, continuation needs an interface quirk, ablation measured 600–2,200 GPU-hours on GLM-5.3 (Anthropic estimates ~600 GPU-hours / ~$1,200 for a team already experienced with the technique, versus the ~2,200 GPU-hours / ~$4,400 their team spent learning it).

### The scoring problem, concretely

The harness in `labs/module-34/refusal_harness.py` runs each prompt through two scorers:

- **String scorer** — does the output contain a refusal template? Fast, free, and the industry default.
- **Behavioural scorer** — did the model actually *take the action*? In the lab this is measured on a benign proxy: the request asks the model to invoke a tool, and compliance is scored by whether a tool call was emitted, not by what the surrounding prose says.

The gap between them is the number that matters. A large gap in the direction *string-scorer refuses / behavioural-scorer complies* means your current metric is lying to you in the dangerous direction. Module 24's harness scored decode-aware, which is a step toward behavioural; this is the same instinct applied at the level of the scorer rather than the normalizer.

## Intuition

Think of the three classes as three different doors, and of the deployment as which doors are even fitted.

A framing attack needs nothing but a text box. A continuation attack needs a door the model opens toward the caller — a surface where the customer supplies text and the model treats it as its own. A weight attack needs the keys to the building.

This is why "we ran a red-team evaluation" is not a coverage claim until someone says **which doors were open**. An evaluation that ran framing attacks against a closed API tested one door and reported on the building. The engineering consequence is uncomfortable but useful: sometimes the correct mitigation is not a better filter, it is *removing the surface*. A model served through an API that refuses to accept assistant-turn prefixes has eliminated class 2 outright, and no amount of prompt-level hardening is required to defend it.

The same intuition explains why ablation looks so cheap. Refusal in these models is not a deep behaviour woven through the network — it is a comparatively low-dimensional direction that can be projected out with a rank-1 edit, leaving general capability intact. On GPQA-Diamond, Anthropic's ablated model scored the same as the stock one. That is a genuinely bad property for a safety mechanism, and it is the subject of the next lesson.

## Technical explanation

### Four arms, and what each certifies

An evaluation that reports a single refusal number has told you almost nothing. The four arms from the Anthropic study separate the classes:

| Arm | What it exercises | What it certifies |
|---|---|---|
| Stock model, bare request | baseline refusal | the refusal rate of the *stock* configuration |
| Stock + framing | class 1 | surface to framing, on this model |
| Stock + prefill | class 2 | surface to continuation, if the interface allows it |
| Ablated weights | class 3 | what a weight-holder faces |

The habit worth building: **write down which arm each number came from.** "Refusal rate 6%" is not a claim. "Refusal rate 6% after rank-1 ablation of the residual-stream refusal direction, 500 prompts, Wilson 95% CI [4%, 8%]" is a claim you can act on, reproduce, and argue with.

### Simulated-world evaluation

The Anthropic bypass study deliberately executed no model-generated code. The model was given a fake tool surface, and a separate LLM approximated what each command would have returned. The authors flag this as an imperfect proxy for real behaviour, and it is — but note that it measures the thing you actually care about, *did the model try*, while being incapable of causing the thing you do not.

For a course lab this is the right default: the behavioural signal is preserved and the blast radius is zero. Your mock tool endpoint belongs on `127.0.0.1` with a `LAB-CANARY-*` marker, exactly as the rest of this course does.

## Mathematics

### Wilson score interval

For a refusal rate $\hat{p} = x/n$ the naive standard error $\sqrt{\hat p(1-\hat p)/n}$ fails badly at the boundaries, which is precisely where refusal lives. A model that refuses 96% of the time and one that refuses 100% of the time look identical at $n=50$ under the naive interval. Wilson's interval does not:

$$z = 1.96, \qquad
\text{centre} = \frac{\hat{p} + \frac{z^2}{2n}}{1 + \frac{z^2}{n}}, \qquad
\text{half-width} = \frac{z}{1 + \frac{z^2}{n}}\sqrt{\frac{\hat p(1-\hat p)}{n} + \frac{z^2}{4n^2}}$$

Report the interval, not the proportion. In this domain the interesting cells are small and extreme, which is the worst case for naive error bars.

### The scorer gap

Let $S$ be the string scorer and $B$ the behavioural scorer, both returning refuse/comply. The quantity that exposes a broken metric is the disagreement rate in the dangerous direction:

$$g = \Pr[\,S = \text{refuse} \;\wedge\; B = \text{comply}\,]$$

$g$ is the probability that your existing dashboard told you "safe" while the model was not. It is not a quality score; it is a **measurement bug rate**, and it should be reported before any capability or safety claim built on that dashboard.

### Rank-1 removal

For the weight class, with residual-stream activations $h \in \mathbb{R}^d$ and refusal direction $\hat r$:

$$\hat r = \frac{1}{\lVert \bar{h}^{+} - \bar{h}^{-} \rVert}\left(\bar{h}^{+} - \bar{h}^{-}\right),
\qquad
W \leftarrow W - \hat r \hat r^{\top} W$$

The projection $\hat r \hat r^\top$ is idempotent ($\hat r\hat r^\top \hat r\hat r^\top = \hat r\hat r^\top$) and removes exactly the component of any output lying along $\hat r$. You implement and verify this by hand in Lab 34 before touching a real model. The next lesson runs it for real.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee — behavioural scoring.** Guarantees that your measured refusal rate reflects attempted actions rather than refusal phrasing. **Does not guarantee** the absence of harmful compliance, only that your metric sees what the model did. **Attacker adaptation:** a model trained to interleave a refusal template before complying scores perfectly on a string matcher. **False-positive cost:** near zero — the scorer is post-hoc. **Performance cost:** one extra tool-call parse per sample.

> [!IMPORTANT]
> **Guarantee — removing the continuation surface.** Guarantees that class-2 continuation attacks are not expressible against your endpoint. **Does not guarantee** anything against framing or weight attacks. **Attacker adaptation:** attackers move to class 1, which is the one class this does nothing about — and class 1 is available everywhere. **False-positive cost:** a real usability cost; some legitimate agentic workflows depend on supplying a partial assistant turn, so removing the surface is a product decision, not a free win. **Performance cost:** nil.

> [!WARNING]
> **A refusal rate is not a safety certificate.** A model refusing 95% of sampled harmful prompts certifies behaviour on that sample under that framing. It certifies nothing about unseen distributions, about long-horizon agentic tasks where the harmful step is never stated as a harmful request, or about the ablated configuration. Every number in this space is a lower bound produced by whoever chose the arms.

> [!CAUTION]
> Two of the three classes require an interface you do not expose. Any statement that a model is "resistant" to ablation, made about an API model, is vacuous. Reserve the claim for weights you actually hold.

## Practical lab

GPU-backed. [`labs/module-34/`](../../labs/module-34/) — the refusal harness, both scorers, four arms, and the ablation implementation.

> [!WARNING]
> This module runs **real open-weight models on real GPUs**, defaulting to
> [`zai-org/GLM-5.3-Flash`](https://huggingface.co/zai-org/GLM-5.3-Flash) — the MIT-licensed model
> from the case study above. That model is 320B total / 18B active and roughly **328 GB at FP8**, so
> the full replication needs 8×80GB or 4×H200 and, by Anthropic's own figures, ~600–2,200 GPU-hours
> and roughly $1,200–$4,400. The README has a tiered cost table before you start. The toy-model labs
> in Modules 7 and 25 remain the free, CPU-only, offline path and are unchanged by this module; if you
> are unsure whether you need a GPU, you do not.

The lab measures a model **you download and host locally**. It targets no third-party API and embeds
no harmful corpus: benchmark prompts are fetched at runtime, and the behaviourally-scored actions
point at a local mock endpoint with a `LAB-CANARY-*` marker on `127.0.0.1`.

## Exercise

1. Take any model you are responsible for. Run the harness in `bare` and `cover` arms at $n=200$.
2. Compute $g$, the scorer gap. Write one sentence: if $g$ is non-zero, which of your existing safety reports was wrong, and in which direction?
3. Identify which of the four arms your team has ever run against this model. Name the classes still untested.
4. Write the guarantee box for your strongest existing control, including which layer an adaptive attacker moves to next.

## Research paper

Fasano, Fleischer, McFaul, Xiao and Gallagher, *GLM-5.3 and the spread of advanced cyber capabilities* (Anthropic, 2026-09-29). Two things to take from it as a practitioner: the four-arm, surface-partitioned comparison, and the behavioural scoring decision. Note explicitly what it does **not** publish — the attack orders, the prompts, the harness, the ablation code — and therefore that it is a source for *methodology and magnitudes*, never for reusable artifacts.

Corroborate capability independently: NIST's CAISI published a parallel assessment on 2026-09-17 finding GLM-5.3 the most cyber-capable open-weight model released to date, roughly four months behind the US frontier. Capability claims from a vendor are worth one data point; the bypass claims here are Anthropic-only.

## Further reading

- [Zou et al., arXiv:2406.11717](https://arxiv.org/abs/2406.11717) — refusal as a single direction. The basis of Lab 34.2.
- [HarmBench](https://arxiv.org/abs/2402.04249) and [StrongREJECT](https://arxiv.org/abs/2402.10260) — refusal benchmarks; read the scoring sections specifically, they are the disagreement between scorers made visible.
- [Jailbreaking Black-Box LLMs in Twenty Queries](https://arxiv.org/abs/2310.17623) — class 1 as a search problem.
- [Universal and Transferable Adversarial Attacks on Aligned LMs](https://arxiv.org/abs/2307.15043) — class 1 as an optimization problem.
- [Standards map](../../references/standards-map.md) — where these map onto OWASP LLM and MITRE ATLAS.

## What you should now be able to do

- Given a technique and a deployment, say which class it belongs to and whether the deployment can even express it.
- Explain, to an engineer who is about to ship, why their 95% refusal number does not support the conclusion they want to draw.
- Implement both a string and a behavioural scorer, report the gap between them, and know which direction that gap endangers.
- Decide whether a proposed mitigation is buying resistance or buying a smaller attack surface — and price it accordingly.
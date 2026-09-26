# Zou et al. — *Universal and Transferable Adversarial Attacks on Aligned Language Models* (GCG, 2023)

**arXiv:** [2307.15043](https://arxiv.org/abs/2307.15043) (CMU/CAIS). **Module:** [07.1](../lessons/module-07/lesson-01.md). **Lab:** [Lab 07](../labs/lab-07/README.md).

## Why it matters
GCG (Greedy Coordinate Gradient) is the attack that made jailbreaking a **gradient-optimization** problem, not a wordsmithing one. It finds an adversarial *suffix* that, appended to a harmful request, maximizes the probability of an affirmative opening ("Sure, here is…"). Its two shocking results — suffixes **transfer** to models you never optimized against, and are **universal** across prompts — are why alignment-by-training is not a robustness guarantee. This is the bridge from "prompt injection" to "adversarial examples for text."

## Prerequisites
- Sibling course: autoregressive LMs, embeddings, backprop through a transformer.
- This course: [02.1](../lessons/module-02/lesson-01.md); adversarial-example intuition from [09.1](../lessons/module-09/lesson-01.md) helps but M07 precedes it deliberately — GCG motivates the ML lens.

## What to understand
- **Objective:** maximize $\log p(\text{target affirmative prefix} \mid \text{prompt} + \text{suffix})$ over discrete suffix tokens.
- **The discrete-optimization trick:** you can't gradient-descend on tokens, so GCG uses the **one-hot gradient** to rank candidate token swaps per position (top-$k$), then *evaluates real forward passes* on a batch of candidates and greedily takes the best. Gradient proposes; forward pass disposes.
- **Universal/transferable:** optimize one suffix over *multiple prompts and multiple models* simultaneously → it generalizes. Transfer implies a shared decision geometry across aligned models.

## Which sections to read
- §2 (threat model + objective) and §3 (the GCG algorithm) — read Algorithm 1 line by line; it *is* the lab.
- §3.2 (universal/multi-prompt) and §4 transfer results — the part that matters for defense.

## Experiment to reproduce (locally)
Lab 07 reproduces GCG's *mechanism* on a from-scratch hand-rolled-attention toy model with a targeted output class and a strong refusal bias: random suffixes fail (~3/8), GCG succeeds (8/8). Then add a **perplexity filter** defense and show it catches gibberish suffixes — then craft a fluent/low-perplexity adaptive suffix that evades it. That attack→defense→adapt loop is the whole point.

## Code to implement
- The one-hot gradient → top-$k$ candidate → real-forward-pass-eval loop, from scratch (in the lab).
- A perplexity-based input filter and the adaptive fluent-suffix attack against it.

## Limitations
- Compute-heavy on real models (many forward passes); the toy model exists so you learn the algorithm, not fight a GPU.
- Gibberish suffixes are perplexity-detectable — the naive attack has an easy tell (hence the adaptive exercise).

## What later research changed
- **PAIR** ([04](04-chao-pair.md)) and **TAP** ([05](05-mehrotra-tap.md)) achieve jailbreaks *black-box*, no gradients, with fluent prompts — sidestepping perplexity filters.
- Fluency-regularized and multi-coordinate GCG variants reduce the perplexity tell.
- Ties directly to certified-robustness limits ([10](10-gu-badnets.md) is a different thread; see [09](09-croce-autoattack.md) for evaluation rigor).

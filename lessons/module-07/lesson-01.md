<div class="prereq">

**Prerequisites.** [02.1 boundaries](../module-02/lesson-01.md) (refusal as a probability; safety
as coverage), [04.1 direct injection](../module-04/lesson-01.md) (ASR + Wilson CI). **From the
sibling course:** gradients & backprop (M02), optimization/SGD (M03), softmax/cross-entropy
(M01). This lesson does not reteach autograd — it uses $\nabla$ to attack. Lab needs CPU **torch**
(no download).

**You will learn.** Jailbreaking as an *optimization problem*: the $\arg\max_x L(\text{model}(x))$
formulation, and the **Greedy Coordinate Gradient (GCG)** algorithm that solves it over discrete
tokens to produce adversarial suffixes. You implement GCG from scratch on a toy white-box model,
measure it against random search, then defend with a perplexity filter and defeat that defense
with an adaptive fluent attack.

**Why this matters.** This is the transition from "clever phrasings" to *automated, transferable,
gradient-driven* attacks — the research frontier of jailbreaking. Understanding GCG mechanically
lets you reason about why such suffixes exist, why they transfer, why perplexity filters catch
them, and why fluent adaptive attacks (AutoDAN, etc.) get past the filters.

</div>

# 07.1 · Optimization-based jailbreaks (GCG)

## Why this matters

Manual jailbreaks are a cat-and-mouse of phrasings. Optimization-based jailbreaks change the game:
given white-box access (open weights, or a good surrogate), you can *search* for an input that
provably drives the model toward a target behavior, automatically, and the result often transfers
to models you never touched. If you cannot reason about this as an optimization problem, you
cannot reason about the current jailbreak literature at all.

## Learning objectives

1. Write the jailbreak objective as $\arg\max_x L(\text{model}(x))$ (equivalently minimize a
   target-output loss) and name its variables, objective, and constraints.
2. Explain the **discrete-optimization** difficulty (tokens are not continuous) and how GCG uses a
   gradient over **one-hot** inputs to guide a greedy search.
3. Implement GCG from scratch and measure success vs a budget-matched random baseline.
4. Explain **transferability** and why surrogate-model attacks threaten black-box systems.
5. Analyze the **perplexity-filter** defense and its ROC trade-off; build an **adaptive fluent**
   attack that evades it and re-measure.

## Concept

### The objective

Fix a prompt $p$ (the request) and a target output $t$ (e.g. an affirmative continuation, or in
the lab a specific output class = "comply"). Let the adversary control a suffix $s = (s_1,\dots,s_L)$
of tokens appended to $p$. Define a loss $L(s)$ = negative log-probability the model assigns to
the target given $p \oplus s$ (cross-entropy to $t$). The attack is

$$ s^\star = \arg\min_{s \in \mathcal{V}^L}\; L(s) \;=\; \arg\min_{s}\; -\log p_\theta\big(t \mid p \oplus s\big), $$

where $\mathcal{V}$ is the token vocabulary. Maximizing target probability = minimizing this loss.
Simple to state; hard to solve, because $s$ ranges over $|\mathcal{V}|^L$ **discrete** points —
no gradient descent directly, and brute force is astronomical ($48^{16}$ even in our toy).

### The GCG idea: gradient over one-hot, greedy over tokens

GCG (Zou et al., 2023) bridges discrete and continuous:

1. Represent each suffix token as a **one-hot** vector $e_i \in \{0,1\}^{|\mathcal V|}$; the
   embedding is $E^\top e_i$. Now $L$ is differentiable in $e_i$, and
   $\nabla_{e_i} L \in \mathbb{R}^{|\mathcal V|}$ scores every candidate token at position $i$ by
   its *first-order* effect on the loss.
2. For each position, take the **top-$k$** tokens with the most negative gradient (most promising
   substitutions). The gradient is only a linear approximation, so:
3. **Evaluate for real:** sample a batch of single-token swaps from those candidates, run true
   forward passes, and keep the swap that most reduces the *actual* loss. Repeat.

So the gradient *proposes*, the forward pass *disposes*. That two-stage structure — cheap gradient
to shortlist, exact evaluation to choose — is the crux, and why GCG is far more query-efficient
than random search.

### Transferability

Adversarial suffixes found on one (or an ensemble of) open models frequently **transfer** to other
models, including black-box commercial ones. Intuition: models trained on overlapping data learn
overlapping features and similar decision geometry, so an input that exploits one lands near the
same failure region in another. This is why white-box attacks on open surrogates are a real threat
to closed systems, and why "we're closed-source" is not a defense. (Mechanistic depth: Stage 4's
transfer-attack analysis for adversarial examples applies here.)

## Intuition

You want to open a combination lock (the model's compliance) with $48^{16}$ combinations. Random
guessing is hopeless. But suppose that at any setting you can *feel* which single dial, nudged
which way, most reduces the resistance — that is the gradient over one-hot tokens. You still can't
trust the feeling exactly (it's a local, linear hint), so you try the few most promising nudges
for real and keep the best. Repeat, and you climb to an opening far faster than luck. GCG is that
disciplined feel-then-try climb over a discrete space.

## Technical explanation

Read `labs/lab-07/gcg.py`. The core loop, annotated:

```python
oh_s = one_hot(suffix).requires_grad_(True)          # differentiable stand-in for tokens
embeds = cat([one_hot(prompt), oh_s]) @ emb.weight   # continuous relaxation
loss = cross_entropy(model(embeds), target)          # -log p(target | prompt ⊕ suffix)
loss.backward()                                      # grad wrt one-hot: [L, |V|]
topk_tokens = (-grad).topk(k, dim=1).indices         # per-position best candidate swaps
# sample B single-token swaps from topk, evaluate TRUE loss, keep the best
```

Key implementation truths the lab makes concrete:
- **Why one-hot, not the embedding directly?** You need a gradient *per candidate token*, i.e. a
  score over the vocabulary axis; differentiating w.r.t. the one-hot gives exactly that.
- **Why evaluate candidates for real?** The gradient is first-order; the true loss surface over
  token swaps is not linear, so the top-gradient token is not always the best. Real evaluation of
  a batch fixes the approximation error cheaply.
- **Cost** = (1 backward + $B$ forward) per step $\times$ steps. Query-bounded; you will measure
  queries-to-success and compare to random.

<div class="callout warn">

**Reproducibility gotcha you will hit in real attack code.** In the toy model, `nn.Embedding`
initializes from the *global* RNG; unless you seed it from a local generator, your "fixed" model
silently changes with prior RNG use and your results won't reproduce. Security measurements are
worthless if not reproducible — seed *everything*, and log seeds. (This exact bug was fixed in the
lab's model; see the comment in `gcg.py`.)

</div>

## Mathematics

**The one-hot gradient, explicitly.** Let position $i$ have one-hot $e_i$, embedding
$x_i = E^\top e_i$ (so $E \in \mathbb{R}^{|\mathcal V|\times d}$). By the chain rule the score for
substituting token $v$ at position $i$ is the $v$-th component of

$$ \nabla_{e_i} L \;=\; E \, \nabla_{x_i} L \;\in\; \mathbb{R}^{|\mathcal V|}. $$

GCG's candidate set at $i$ is $\text{top-}k$ of $-\nabla_{e_i} L$ (tokens whose selection is
predicted to *decrease* the loss most). This is a first-order Taylor estimate of the loss change
from swapping in token $v$: $\Delta L \approx (\nabla_{e_i}L)_v - (\nabla_{e_i}L)_{s_i}$.

**Why measure vs random.** Both are query-bounded searches; the scientific claim "gradients help"
is only supported by showing GCG reaches the target with far fewer queries / higher success than
random over the *same budget*. Report success rate with a Wilson interval (04.1) and
queries-to-success. In the lab: GCG hits the target on all prompts in ~$10^3$ queries; random,
given the same budget, succeeds on a minority — quantifying the value of the gradient.

**Complexity.** Naive brute force is $|\mathcal V|^L$. GCG replaces it with $\text{steps}\times B$
forward passes plus $\text{steps}$ backward passes — polynomial in the budget, independent of
$|\mathcal V|^L$. That reduction is the whole point.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — perplexity (fluency) filter.**
- **Stops:** vanilla GCG suffixes, which are gibberish and have high perplexity under a language
  model; cheap and effective against the *original* attack.
- **Does NOT stop:** adaptive attacks that add a fluency penalty to the objective (readable
  suffixes), attacks that hide the suffix in otherwise-fluent text, or short suffixes below the
  detector's resolution. It is a classifier with an ROC curve, not a gate.
- **Attacker adapts:** optimize for low perplexity *and* target loss jointly (the lab's
  `fluency_lambda`); the suffix becomes fluent and slips under the threshold, at some cost to
  success rate / queries.
- **FP cost:** legitimate but unusual inputs (code, other languages, rare jargon) have high
  perplexity and get blocked — real utility loss. **Perf:** one extra LM forward pass per input.
- **Takeaway:** raises attacker cost meaningfully, buys nothing against a determined adaptive
  adversary; combine with alignment (raise the loss floor), rate limiting, and monitoring.

</div>

## Practical lab

<div class="lab">

**Lab 07** ([`labs/lab-07/`](../../labs/lab-07/README.md)) — implement/inspect GCG, beat random,
then perplexity-filter and adaptive-evade. CPU torch, no download, ~30s tests.

```bash
py labs/lab-07/gcg.py        # GCG 8/8 vs random ~3/8, ~3x fewer queries
py labs/lab-07/defense.py    # filter cuts gibberish 8/8->~1/8; adaptive fluent evades ~7/8
py -m pytest labs/lab-07 -q
```

</div>

## Exercise

1. **Derive & annotate.** Write out $\nabla_{e_i}L = E\nabla_{x_i}L$ for the toy model and confirm,
   in code, that the top-gradient token at a position often (not always) matches the token that a
   brute-force single-position search would pick. Explain the mismatch (first-order error) and why
   step 3 (real evaluation) is needed.
2. **Beat random, with statistics.** Run `compare()`; report GCG vs random success and
   queries-to-success with **Wilson 95% intervals**. Sweep `topk ∈ {8,16,32}` and
   `batch ∈ {32,64,128}`; plot queries-to-success. Which knob matters most, and why (gradient
   proposal quality vs evaluation breadth)?
3. **Suffix length.** Vary `suffix_len`; show the success/queries trade-off. Relate to capacity:
   more suffix tokens = more degrees of freedom to shift the output.
4. **Perplexity defense.** Implement the ROC: sweep the filter threshold, and plot true-positive
   rate (gibberish GCG blocked) vs false-positive rate (a set of *benign* fluent inputs blocked).
   Pick an operating point and justify it with the base-rate argument from 01.1/02.2.
5. **Adaptive fluent attack (purple team).** Turn on `fluency_lambda`; find the smallest penalty
   that gets median suffix perplexity under your threshold while keeping success high. Report the
   success-vs-perplexity trade-off curve. Conclude which side (attacker/defender) this favors and
   why the *measured against the adapted attack* number is the only honest one.
6. **Transfer (reasoning + mini-experiment).** Train a *second* toy model with a different seed;
   run GCG on model A and test the suffix on model B. Report transfer success. Explain why partial
   transfer occurs and what it implies for black-box systems (tie to 07.1 transferability).

<details><summary>Hint (step 4)</summary>

You need a benign fluent corpus for the false-positive rate: sample suffixes from the toy bigram
LM itself (low perplexity by construction). The filter's FPR is the fraction of those it rejects
at a given threshold. The ROC is TPR (gibberish rejected) vs FPR (benign rejected) as you sweep
the threshold — exactly the Module 24 evaluation methodology, previewed.

</details>

**Deliverable.** GCG-vs-random with CIs and sweeps, the perplexity ROC with an operating point,
the adaptive trade-off curve, the transfer experiment, and the guarantee box for your final stance.

```bash
py course.py complete 07.1
```

## Research paper

**Zou, Wang, Kolter, Fredrikson, "Universal and Transferable Adversarial Attacks on Aligned
Language Models" (2023) — GCG.** *Why:* the paper you just reimplemented; defined automated,
transferable LLM jailbreaks. *Read:* the objective (their affirmative-response target), the GCG
algorithm (Alg. 1 — map each line to `gcg.py`), and the transfer results. *Reproduce:* you already
did the core; extend by attacking an *ensemble* of two toy models to improve transfer (their
universality trick). *Limitations / what changed:* perplexity filters (Jain et al.; Alon &
Kamfonas, 2023) detect vanilla GCG; adaptive fluent methods (**AutoDAN**, Liu et al., 2023)
restore evasion — the arms race you measured.

## Further reading

- Jain et al., "Baseline Defenses for Adversarial Attacks Against Aligned LMs" (2023) — perplexity
  filtering, paraphrase, retokenization.
- Chao et al., **PAIR**; Mehrotra et al., **TAP** — black-box, query-only jailbreaks (Module 08).
- OWASP LLM01; MITRE ATLAS evasion techniques — [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. Write the GCG objective and say why it can't be solved by plain gradient descent.</summary>

$s^\star=\arg\min_s -\log p_\theta(t\mid p\oplus s)$ over $s\in\mathcal V^L$. The variables are
discrete tokens, so you cannot take gradient-descent steps in token space; the loss is only
differentiable in a continuous relaxation (one-hot/embeddings). GCG uses that relaxation's gradient
to *propose* token swaps, then evaluates them for real.

</details>

<details><summary>Q2. Why does GCG evaluate candidate swaps with real forward passes instead of trusting the gradient?</summary>

The one-hot gradient is a first-order (linear) approximation of the loss change from a token swap;
the true loss over discrete swaps is non-linear, so the top-gradient token isn't always best.
Evaluating a batch of top-k candidates by true forward loss corrects the approximation cheaply and
is what makes GCG reliably descend.

</details>

<details><summary>Q3. Why does a perplexity filter stop vanilla GCG, and how does the adaptive attack defeat it?</summary>

Vanilla GCG optimizes only the target loss, producing gibberish suffixes with high LM perplexity,
which the filter flags. The adaptive attack adds a fluency (low-perplexity) term to the objective,
yielding readable suffixes that pass the threshold — at some cost to success/queries. So the
filter must be measured against the adapted attack, not the original.

</details>

<details><summary>Q4. Why are transferable suffixes a threat to closed-source models?</summary>

Because an attacker can optimize on open surrogate model(s) and transfer the suffix to a black-box
target; models with overlapping training data share features and decision geometry, so exploits
land near the same failure regions. "Closed weights" therefore does not prevent gradient-based
jailbreaks discovered elsewhere.

</details>

## What you should now be able to do

- Formulate a jailbreak as discrete optimization and implement GCG (one-hot gradient → top-k →
  real evaluation) from scratch.
- Measure attack success and query cost against a random baseline with confidence intervals.
- Analyze and build the perplexity-filter defense and its adaptive fluent bypass, and reason about
  transferability to black-box systems.

## Progress checkpoint

```bash
py course.py complete 07.1
py course.py next
```

**Next:** 08.1 · Automated & black-box jailbreaks — PAIR/TAP-style attacker-LLM search, multi-turn
and role attacks, and automated red teaming, where you have *no gradients*, only queries.

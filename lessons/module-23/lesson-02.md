---
id: "23.2"
module: 23
minutes: 18
practice_minutes: 90
prerequisites: ["23.1", "12.1", "02.2"]
objectives:
  - "Implement a green-list text watermark and its z-test detector from scratch, and compute the detection statistic for a short text by hand."
  - "Explain why the detection threshold fixes the false-positive rate while recall depends on text length, entropy and editing."
  - "Measure watermark removal by editing and watermark forgery by stealing, and say which of the two breaks attribution."
  - "Analyse the context-width trade-off (resistance to stealing against robustness to edits) with numbers from the lab."
  - "Write the guarantee analysis for watermarking as a provenance control, including what deployed schemes and the EU marking duty do and do not promise."
volatility: concept
sources:
  - title: "Kirchenbauer, Geiping, Wen, Katz, Miers, Goldstein — A Watermark for Large Language Models (ICML 2023)"
    url: https://arxiv.org/abs/2301.10226
  - title: "Kirchenbauer, Geiping, Wen, Shu, Saifullah, Kong, Fernando, Saha, Goldblum, Goldstein — On the Reliability of Watermarks for Large Language Models (ICLR 2024)"
    url: https://arxiv.org/abs/2306.04634
  - title: "Jovanović, Staab, Vechev — Watermark Stealing in Large Language Models (ICML 2024)"
    url: https://arxiv.org/abs/2402.19361
  - title: "Krishna, Song, Karpinska, Wieting, Iyyer — Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense (NeurIPS 2023)"
    url: https://arxiv.org/abs/2303.13408
  - title: "Kuditipudi, Thickstun, Hashimoto, Liang — Robust Distortion-free Watermarks for Language Models (TMLR)"
    url: https://arxiv.org/abs/2307.15593
  - title: "Google DeepMind — SynthID Text reference implementation (Dathathri et al., Nature 634:818–823, 2024)"
    url: https://github.com/google-deepmind/synthid-text
last_verified: "2026-11-15"
---

# 23.2 · Watermarking and provenance of AI-generated text

Lesson 23.1 split controls into enforced and probabilistic. A text watermark is an odd case: the provider enforces the embedding in code, but checking it is a statistical test on text that the provider no longer controls. This lesson builds one from scratch, measures what its detector really promises, and then removes and forges it.

## Why this matters

"Was this text written by our model?" is now a security question with legal weight. Providers
use it to trace abuse (phishing kits, influence operations, spam written with their API), platforms
use it to label content, and regulation asks for it: Article 50(2) of the EU AI Act (Regulation (EU)
2024/1689) requires providers of generative systems to mark output in a machine-readable, detectable
way, with the transparency obligations applying from 2 August 2026. Legal summaries of the
Commission's final Code of Practice on marking and labelling (June 2026) say it asks for several
layers together (watermarks, metadata, labels), because no single technique meets all of the Act's
requirements. *(Secondary summaries; the Commission's pages could not be fetched for this review.)*

Google DeepMind reported SynthID-Text, a generation-time text watermark, in *Nature* in 2024 and
released a reference implementation. So watermarks are deployed, they are about to be expected by
law, and security engineers will be asked two questions about them: "can we rely on this
detection?" and "can someone make innocent text look like ours?" You can only answer both if you
have built one and broken it.

## Learning objectives

1. Implement a green-list watermark and its z-test detector, and compute the statistic by hand.
2. Explain why the threshold fixes the false-positive rate while recall depends on length, entropy
   and editing.
3. Measure **removal** (editing) and **forgery** (stealing), and explain which one breaks attribution.
4. Analyse the context-width trade-off with numbers from the lab.
5. Write the guarantee analysis for watermarking as a provenance control.

## Concept

### Three provenance mechanisms, three different promises

| Mechanism | Where the mark lives | Survives copy-paste? | Status |
|---|---|---|---|
| **Metadata / signed manifests** (C2PA-style) | Beside the content | No: plain text has nowhere to carry it | CURRENT for images and media; weak for text |
| **Generation-time watermark** (green list, SynthID) | In the choice of tokens | Yes, until the text is edited enough | FOUNDATIONAL (2023), deployed |
| **Retrieval / output logging** | In the provider's database | Yes, and also catches paraphrases | DOCUMENTED (Krishna et al. 2023); costly and privacy-heavy |

This lesson is about the second row: it is the only one that travels inside plain text.

### The green-list watermark (Kirchenbauer et al., ICML 2023)

At each generation step the provider hashes a secret key together with the previous $h$ tokens and
uses the result to seed a pseudorandom split of the vocabulary: a fraction $\gamma$ is **green**,
the rest is **red**. It adds a bias $\delta$ to every green logit and samples as usual. The reader
sees ordinary text. Anyone who holds the key can recompute each step's green list and count how many
tokens are green. Human text lands green at about rate $\gamma$; watermarked text lands green much
more often.

### Two attacks, two different harms

- **Removal (scrubbing).** Edit or paraphrase until the green count falls back to chance. Harm: the
  provider loses the ability to trace its output. This is a *false negative*.
- **Forgery (spoofing).** Produce text the provider did not generate that still tests as
  watermarked. Harm: innocent or attacker-written text gets attributed to the model, and so to its
  user. This is a *false positive the attacker chooses*. It is the worse failure for any use of
  watermarks as evidence.

Forgery needs the green lists. They are secret, but **they leak through the outputs**:
Jovanović, Staab and Vechev (ICML 2024) showed that querying a watermarked API and comparing token
frequencies with an unwatermarked model recovers enough of the green lists to both spoof and scrub
state-of-the-art schemes, for under USD 50, with an average success rate above 80%.

## Intuition

Picture a dealer who secretly prefers certain cards, and the preferred set changes with the card
just played. Any single hand looks normal. Over a hundred hands, someone who knows the rule counts
far too many preferred cards. That is detection. A player who reshuffles part of the hand dilutes
the excess (removal). A player who watches thousands of hands without knowing the rule eventually
learns which cards follow which, and can then deal hands that *look* like the dealer's (forgery).
Making the rule depend on the last three cards instead of one makes it much harder to learn. It
also means that every card you swap disturbs the count for the next three cards.

## Technical explanation

**Generation.** For position $i$, the context $c_i = (x_{i-h},\dots,x_{i-1})$ seeds
$G(c_i) \subset V$ with $|G| = \gamma |V|$. Logits $\ell_v$ become $\ell_v + \delta\,[v \in G(c_i)]$.
The first $h$ tokens have no full context and are not scored.

**Detection.** Count green hits $|s|_G$ over the $T$ scored positions and run a one-sided z-test
against the null hypothesis "this text was written without knowledge of the key".

**What sets recall.** The bias can only move probability mass that is available to move. If the
model is nearly certain of the next token (code, boilerplate, a memorised quote), adding $\delta$ to
a green alternative changes almost nothing. **Low-entropy text carries little watermark.**
Kirchenbauer et al. measure this with a "spike entropy" term, and SynthID's implementation leaves
the first `ngram_len - 1` tokens unwatermarked for the same structural reason as $h$ here.

**Deployed variants.** Distortion-free schemes (Kuditipudi et al.; SynthID's tournament sampling)
keep each token's marginal distribution unchanged, so quality is unaffected. The security questions
in this lesson (length, entropy, edits, key leakage through outputs) apply to them too. The SynthID
reference repository says plainly (checked 2026-11-15) that it is for research reproducibility, not
production; that its pseudorandom generator is not a vetted cryptographic primitive; that keys are
limited to 63 bits; and that it gives no cryptographic security guarantee. Treat those as the
vendor's own statement of the guarantee boundary.

## Mathematics

**Detection statistic.** Under the null hypothesis each scored token is green with probability
$\gamma$, independently (an approximation that is accurate when repeated contexts are rare):

$$ z = \frac{|s|_G - \gamma T}{\sqrt{T\,\gamma(1-\gamma)}}, \qquad \text{FPR}(\tau) = P(Z \ge \tau) = \tfrac12\operatorname{erfc}(\tau/\sqrt2). $$

*Worked example.* $T = 100$, $\gamma = 0.25$, $|s|_G = 45$ green tokens. Expected under the null:
$\gamma T = 25$, with standard deviation $\sqrt{100 \cdot 0.25 \cdot 0.75} = 4.33$.
$z = (45 - 25)/4.33 = 4.62$, so $p \approx 1.9\times10^{-6}$: flag it at $\tau = 4$
($\text{FPR} \approx 3.2\times10^{-5}$). A human text with 30 green tokens gives $z = 1.15$, which is
not flagged.

**The threshold fixes FPR, not recall.** $\tau$ depends only on the null, so the false-positive
promise holds for any human text, whatever its length. Recall depends on the green rate $p_g$
actually achieved. In the high-entropy limit (near-uniform next-token distribution),

$$ p_g = \frac{\gamma e^{\delta}}{\gamma e^{\delta} + 1 - \gamma}, \qquad E[z] \approx \sqrt{T}\,\frac{p_g - \gamma}{\sqrt{\gamma(1-\gamma)}}. $$

With $\gamma = 0.25$, $\delta = 2$: $p_g = 1.847/2.597 = 0.711$ and $E[z] \approx 1.06\sqrt T$, so
about 15 tokens reach $z = 4$. Real text has lower entropy, so $p_g$ is lower and more tokens are
needed. In the lab, 25 tokens give 85% recall and 50 give 98%. Recall grows like $\sqrt T$:
**length buys detection**.

**Edits.** With context width $h$, one substituted token changes its own colour *and* the green
lists of the next $h$ positions. So an edit fraction $\varepsilon$ randomises up to
$(1+h)\varepsilon$ of the scored positions, which then fall back to rate $\gamma$:

$$ E[z_\text{edited}] \gtrsim \sqrt{T}\,\frac{(p_g - \gamma)\,\big(1 - (1+h)\varepsilon\big)}{\sqrt{\gamma(1-\gamma)}}. $$

At $h = 1$ and $\varepsilon = 0.3$ the signal keeps at least 40% of its strength; at $h = 3$ it
keeps none in the worst case. The lab measures 100% vs 37% recall at T=200. Kirchenbauer et al.
(ICLR 2024) report the real-world version: after strong human paraphrasing, detection still worked
at an FPR of $10^{-5}$, but it needed about 800 tokens on average.

**Stealing budget.** The attacker must see each context often enough to estimate which tokens are
over-represented. There are $|V|^h$ contexts. The lab's 200 outputs of 200 tokens (about 40,000
observations) cover each of the $64$ contexts at $h=1$ about 600 times on average, and essentially none of the
$64^3 = 262{,}144$ contexts at $h=3$. Wider context makes stealing exponentially more expensive in
$h$, and the edit term above makes removal linearly cheaper in $h$. **No setting of $h$ wins both.**

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis: generation-time text watermarking (green list / SynthID-class).**
> - **Guarantees:** a bounded false-positive rate *for text written without knowledge of the green
>   lists*. Unmarked human text is flagged at rate $\le \text{FPR}(\tau)$, whatever its length.
> - **Does NOT guarantee:** detection of short, low-entropy (code, templates) or heavily edited or
>   paraphrased text, or of text from a different model. It does not show that a flagged text was
>   generated by the model, because once green lists leak, forgery produces flagged text the model
>   never wrote. It is not a cryptographic signature (the SynthID README says so explicitly).
> - **How the attacker adapts:** paraphrase or translate to remove the mark; query the API to steal
>   the green lists, then spoof (frame someone) or scrub cheaply; use an unwatermarked open-weight
>   model instead.
> - **False-positive cost:** low for genuine human text at a sensible $\tau$, but *attacker-chosen*
>   false positives are possible after stealing. Never use a positive detection as sole evidence
>   against a person.
> - **Performance cost:** near zero at generation (one hash per token). A biased scheme costs a little
>   quality; distortion-free schemes avoid that at some loss of robustness. Detection needs the key,
>   so it is a provider-run service, not something a third party can check.

> [!WARNING]
> Watermark detectors are being used to accuse people (students, job applicants, journalists).
> Even the honest false-positive rate becomes many wrong accusations at scale (see the base-rate
> arithmetic in 23.1), and forgery makes deliberate framing possible. Treat a positive result as a
> lead to investigate, never as proof.

**Where each control fits (progression, not replacement).** Everything 23.1 taught still holds. The
watermark *embedding* is enforced (it is your code), but the *detection* is a probabilistic control
with an explicit FPR, a recall that depends on the input, and an adaptive adversary. That puts it in
the "depth and forensics" column, beside monitoring. Combine it with the other rows of the Concept
table: output logging or retrieval (Krishna et al.: 80–97% of paraphrases detected at 1% FPR on
human text, at the cost of storing all output) and, for media, signed metadata.

## Real-world examples

- **SynthID-Text (Google DeepMind, *Nature* 2024).** Generation-time watermark reported as deployed
  in Gemini. The open-source reference implementation integrates with Hugging Face Transformers v5
  (checked 2026-11-15) and documents its limits (not production, non-cryptographic PRNG, 63-bit
  keys). DOCUMENTED.
- **Watermark stealing (ICML 2024).** Spoofing and scrubbing of schemes previously considered safe,
  for under USD 50. DOCUMENTED and reproducible in principle; the lab reproduces the mechanism on a
  toy model.
- **EU AI Act Article 50 and the 2026 Code of Practice.** Marking becomes a legal duty for
  providers from August 2026; the Code asks for layered marking. CURRENT; details from secondary
  legal summaries.
- **EMERGING (2026 preprints, not yet independently replicated):** semantic watermarks that aim to
  survive paraphrase, multi-bit watermarks that carry a user or session ID, code-specific watermarks
  that survive identifier renaming, and blind removal attacks on image watermarks. These are tracked
  in the course's research log; this lesson's guarantee analysis is the lens for reading them.

## Code

`labs/module-23/watermark/wm_core.py` holds the toy bigram model (`ToyLM`, with a `sharpness` knob
for entropy) and the `Watermark` class: keyed green lists, biased sampling, `score` and `z`.
`wm_attacks.py` implements `random_edit`, the frequency-ratio `StolenWatermark` estimator, `spoof`
and `informed_scrub`. Read `Watermark.green_list` first: the whole scheme is a keyed hash of the
context and a seeded shuffle. Everything else follows from that.

## Practical lab

**Lab 23.2** ([`labs/module-23/watermark/`](../../labs/module-23/watermark/README.md)): defend,
measure, remove, forge and retest. Offline, standard library only.

```bash
python labs/module-23/watermark/wm_evaluate.py
python -m pytest labs/module-23/watermark -q
```

Expected shape of the output: zero empirical false positives on unwatermarked text; recall rising
with length and falling with lower entropy; removal at about 50% edits for `h=1` and about 30% for
`h=3`; forgery succeeding at `h=1` and failing at `h=3` on the same 200-output budget.

## Exercise

1. **By hand first.** For $T = 64$, $\gamma = 0.5$ and 44 green tokens, compute $z$ and decide at
   $\tau = 4$. Then check it with `Watermark(gamma=0.5).z(...)` on a constructed sequence.
2. **Recall curve.** Plot recall against $T$ for `sharpness` 1, 2 and 4. For each, find the length
   at which recall first reaches 95%, and compare it with the $\sqrt T$ prediction.
3. **Price the forgery.** Vary the stealing budget (20, 50, 100, 200 outputs) at `h=1` and plot
   spoof success. Then find a budget at which `h=2` forgery succeeds. How did the cost scale?
4. **Defend, then bypass your defense.** Add a "repeated-context" rule to the detector (score each
   (context, token) pair at most once, a common hardening in the watermarking literature). Does it change honest
   recall? Does it stop a spoof that repeats one well-estimated context? Adapt the spoofer to beat it.
5. **Guarantee box.** Write your own guarantee analysis for "watermark plus output logging", and
   state which attacker from step 3 it still does not stop.

<details><summary>Hint (step 1)</summary>

Expected green count $= 32$, standard deviation $= \sqrt{64 \cdot 0.5 \cdot 0.5} = 4$, so $z = (44-32)/4 = 3$.
That is below $\tau = 4$: not flagged, even though 69% green looks high. With $\gamma = 0.5$ you
need a larger excess before the test is convinced.

</details>

<details><summary>Hint (step 3)</summary>

Coverage is the number of contexts seen at least `min_obs` times, divided by $|V|^h$. At $h=2$
there are 4,096 contexts, so you need on the order of $4096 \times 8$ observations at minimum, and in
practice more, because contexts are not visited uniformly.

</details>

## Research paper

**Kirchenbauer et al., "A Watermark for Large Language Models" (ICML 2023)**, read together with
**Jovanović, Staab, Vechev, "Watermark Stealing in Large Language Models" (ICML 2024)**. *Why:* the
first defines the scheme and its statistics; the second shows the scheme's secret leaks through its
own outputs, which is the general lesson (compare model extraction in 12.1). *Read:* Kirchenbauer
§2–4 (scheme, z-test, spike entropy) and the stealing paper's threat model and spoofing results.
*Skip on first pass:* the multi-key and privacy variants. *Reproduce:* the lab is the toy
reproduction; step 3 of the exercise reproduces the cost curve. *Limits:* the stealing results are
on specific schemes and parameters; read the follow-up reliability paper (ICLR 2024) for the
defender's best numbers under paraphrase.

## Further reading

- Kirchenbauer et al., [On the Reliability of Watermarks for LLMs](https://arxiv.org/abs/2306.04634)
  (ICLR 2024): paraphrase robustness measured with human rewriters.
- Krishna et al., [Paraphrasing evades detectors, but retrieval is an effective defense](https://arxiv.org/abs/2303.13408)
  (NeurIPS 2023): the retrieval alternative and its cost.
- Kuditipudi et al., [Robust Distortion-free Watermarks](https://arxiv.org/abs/2307.15593) (TMLR).
- [SynthID Text reference implementation](https://github.com/google-deepmind/synthid-text): read its
  README's limitations section as a model of an honest guarantee statement.
- Back to [23.1](lesson-01.md) for base rates; forward to [24.1](../module-24/lesson-01.md) for how
  to evaluate a detector at its operating point.

## What you should now be able to do

- Implement a green-list watermark and z-test detector, and compute $z$ for a text by hand.
- Explain why the threshold bounds the false-positive rate while recall depends on length, entropy
  and editing.
- Remove a watermark by editing, forge one by stealing, and explain why forgery is the failure that
  matters for attribution.
- Choose a context width and defend the choice with measured numbers for both attacks.
- Write a guarantee analysis for watermarking as a provenance control, including what deployed
  schemes and regulation do and do not promise.

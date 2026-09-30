---
id: "29.1"
module: 29
minutes: 22
practice_minutes: 75
prerequisites: ["12.1", "14.1"]
objectives:
  - Explain why an embedding is recoverable data, not an anonymised hash of its input.
  - Perform embedding inversion to recover input tokens and attribute extraction to recover a private property.
  - Derive why nearest-token inversion works and how additive noise trades recovery for retrieval utility.
  - Apply and measure defenses — access control, not storing sensitive embeddings, noise/DP — and state each one's guarantee.
volatility: concept
sources:
  - title: "Song & Raghunathan — Information Leakage in Embedding Models (CCS 2020)"
    url: https://arxiv.org/abs/2004.00053
  - title: "Morris et al. — Text Embeddings Reveal (Almost) As Much As Text (vec2text, EMNLP 2023)"
    url: https://arxiv.org/abs/2310.06816
  - title: "OWASP Top 10 for LLM Applications 2025 — LLM02 Sensitive Information Disclosure"
    url: https://genai.owasp.org/llm-top-10/
last_verified: "2026-09-30"
---

# 29.1 · Attacking embeddings: inversion & extraction

Teams routinely treat an embedding as a safe, opaque numeric fingerprint of text — something you can store in a vector database, share across tenants, or log, because "it's just a vector." It is not. An embedding is a lossy but richly invertible encoding of its input: given the vector (and the encoder or a surrogate), you can recover much of the original text and read private attributes straight off it. This lesson turns that fact into runnable attacks and measures the only defenses that actually blunt them.

## Why this matters

Embeddings are the connective tissue of modern AI systems: RAG corpora ([14.1](../module-14/lesson-01.md)), semantic caches, dedup indexes, recommendation stores, and cross-service features are all piles of stored vectors, often carrying sensitive text — support tickets, medical notes, source code, chat history. The industry's mental model is that a vector is de-identified. The research says otherwise: text embeddings reveal *almost as much as the text*. If an attacker reaches your vector store (recall the exposed, unauthenticated vector DBs from recon, [27.1](../module-27/lesson-01.md)), they do not just get vectors — they get the content. Understanding inversion and extraction is what lets you decide, correctly, what may and may not be embedded and stored.

## Learning objectives

1. Explain the difference between a one-way hash and an embedding, and why embeddings invert.
2. Perform **embedding inversion** to recover the token set of an input from its vector.
3. Perform **attribute extraction** with a linear probe to recover a private property without full inversion.
4. Derive why nearest-token scoring recovers tokens, and analyse the noise-vs-utility trade-off.
5. Apply and measure defenses — access control, minimisation (don't embed/store sensitive text), and additive noise / differential privacy — and give each a guarantee analysis.

## Concept

An embedding model is a function $f:\text{text}\to\mathbb{R}^d$ trained so that semantically similar inputs land close together. That objective is exactly what makes embeddings invertible: to preserve similarity, $f$ must preserve most of the input's information in geometric structure. Two attacks follow:

- **Inversion** — recover (much of) the input from $e=f(x)$. With white-box access to $f$ (or a good surrogate), you can optimise or search over inputs whose embedding matches $e$. Modern methods (vec2text) reconstruct fluent text; even a crude nearest-token search recovers the bag of words.
- **Extraction** — recover a *specific private attribute* (author, topic, presence of a sensitive term, a demographic) without reconstructing the whole input, by training a small probe on embeddings. This is cheaper and often enough to cause harm.

> [!CAUTION]
> **Red team.** A vector store is a content store. Once you can read the vectors (an over-shared collection, a leaked index, a multi-tenant boundary bug from [15.1](../module-15/lesson-01.md)), inversion and extraction turn "just embeddings" into the underlying documents and their sensitive attributes. Treat exfiltrated embeddings as exfiltrated text in your impact write-up.

## Intuition

A cryptographic hash is a one-way shredder: similar inputs give totally different outputs, and you cannot walk backwards. An embedding is the opposite by design — similar inputs give similar outputs — so the map from output back to input is smooth and searchable. If each word contributes a known direction to the vector, then reading which directions are present reads which words are present. Averaging words together (as many encoders effectively do) blurs but does not erase those directions; with the encoder in hand you subtract the blur and recover the words. Adding noise is like smearing the vector: it hides fine detail (and, past a point, the meaning you were storing it for).

## Technical explanation

**A transparent encoder for the mechanism.** Let $E\in\mathbb{R}^{V\times d}$ be a fixed token-embedding matrix (unit rows). Encode a sentence with token set $s$ as the mean of its token vectors:

$$e(s) = \frac{1}{|s|}\sum_{t\in s} E_t.$$

Real sentence encoders are far more complex, but this captures why inversion works, and the attack transfers in spirit to learned encoders (where you optimise or use a trained decoder instead of a closed-form search).

**Inversion by nearest-token scoring.** Score every vocabulary token by its alignment with the embedding and take the top $k$:

$$\text{score}(t) = E_t \cdot e(s) = \frac{1}{|s|}\sum_{u\in s} E_t\cdot E_u.$$

For a token $t\in s$, its self-term $E_t\cdot E_t = 1$ dominates; for $t\notin s$, the terms $E_t\cdot E_u$ are small and mean-zero when rows are roughly orthogonal (high $d$, random-ish embeddings). So true tokens score high and the top-$k$ recovers $s$. You measure recovery as token-level F1.

**Extraction by linear probe.** If a private attribute corresponds to the presence of a particular token/direction $E_c$ (a canary, a diagnosis code), then $e(s)$ contains $\frac{1}{|s|}E_c$ whenever that token is present. A linear classifier $\sigma(w\cdot e + b)$ can learn $w\approx E_c$ and detect the attribute with high accuracy — *without inverting the rest*. This is why "we only store embeddings" does not protect a sensitive flag.

> [!IMPORTANT]
> **Guarantee analysis — additive noise / differential privacy on stored embeddings.**
> - **What it guarantees:** perturbing $e$ with noise of scale $\sigma$ provably limits how much any downstream reader can infer; with a calibrated DP mechanism you get a formal $\varepsilon$ bound on attribute inference. Inversion F1 and probe accuracy both fall as $\sigma$ grows.
> - **What it does NOT guarantee:** it does not make embeddings safe *and* useful for free — the same noise that hides tokens degrades retrieval/similarity, the reason you stored them. Small $\sigma$ barely helps; large $\sigma$ destroys utility.
> - **How an attacker adapts:** averages many noisy copies if they exist, uses a stronger decoder, or targets a coarse attribute (extraction) that survives more noise than full inversion.
> - **False-positive cost:** degraded retrieval relevance (legitimate queries miss), i.e. a utility/availability cost, not a classic FP.
> - **Performance cost:** negligible compute; the real cost is accuracy of the embedding-powered feature.

## Mathematics

Why the noise trade-off is unavoidable. Retrieval ranks by similarity; its signal is the gap between a true match's similarity and a distractor's, call it $\Delta$. Adding independent noise of variance $\sigma^2$ per dimension injects variance $\sim 2\sigma^2$ into each similarity score (both operands perturbed), so the probability a distractor overtakes the true match grows with $\sigma/\Delta$. Meanwhile, inversion's per-token signal is the self-term ($\approx 1$) against a background whose standard deviation grows with $\sigma$; recovery holds until the noise swamps the self-term, i.e. until $\sigma$ is order-1 relative to the row norm. Because both utility and recovery degrade with the *same* $\sigma$, there is a Pareto curve, not a free lunch:

$$\text{utility}(\sigma)\downarrow \quad\text{and}\quad \text{recovery}(\sigma)\downarrow \quad\text{together.}$$

You trace this curve in the lab and pick the operating point (and discover that for a linearly-encoded attribute, extraction survives more noise than inversion does — coarser signal, more robust).

## Attack / Defense model

**Attacker capability.** Read access to stored embeddings (e.g. an exposed or over-shared vector store), plus either white-box access to the encoder or a surrogate/API to it.

**Attacker goal.** Reconstruct sensitive input text (inversion) or read a private attribute (extraction) from the vectors.

> [!TIP]
> **Blue team.** In priority order: (1) **access control** on the vector store — the cheapest, highest-leverage control; an unreadable store cannot be inverted (ties back to recon/infra, [27.1](../module-27/lesson-01.md)/[30.1](../module-30/lesson-01.md)). (2) **Minimisation** — do not embed or store embeddings of secrets; redact before embedding; keep sensitive fields out of the vectorised text. (3) **Noise / DP** — when you must store potentially-sensitive vectors, add calibrated noise and measure the utility cost; know it only *raises the bar*. (4) **Tenant isolation** so one tenant's embeddings are never in another's index ([15.1](../module-15/lesson-01.md)). Treat (3) as defence-in-depth behind (1) and (2), never as a substitute.

> [!NOTE]
> **Purple team / research.** FOUNDATIONAL: Song & Raghunathan showed embeddings leak their inputs (2020). CURRENT: vec2text (Morris et al., 2023) reconstructs fluent text from black-box embedding APIs, and follow-ups study defenses. Open questions (EMERGING): practical DP for retrieval that keeps useful relevance; how much a *surrogate* encoder suffices when the target's weights are private (you measure a version of this in the lab's ADAPT step). DOCUMENTED vs SPECULATION: that embeddings invert is documented; the exact recoverability of any specific production encoder is system-dependent — measure it, don't assume it.

## Code

Inversion in a few lines — score tokens against the embedding, take the top $k$ (full, runnable version in the lab):

```python
import numpy as np

def invert(e, E, vocab, k):
    # E: (V, d) token-embedding matrix (unit rows). e: the target embedding.
    scores = E @ e                      # alignment of every token with the embedding
    top = np.argsort(scores)[::-1][:k]
    return [vocab[i] for i in top]

# Recovering a sensitive token from a stored vector is recovering the text.
# Extraction is even cheaper: train sigma(w·e + b) to detect a private attribute directly.
```

The lab adds attribute extraction (a from-scratch logistic probe), the noise defense, retrieval-utility measurement, and a surrogate-encoder adaptation.

## Practical lab

> [!WARNING]
> **Lab.** Module 29 lab ([`../../labs/module-29/`](../../labs/module-29/)). CPU-only, offline, no Docker. Python + numpy (pinned in `requirements.txt`). A deterministic toy encoder stands in for a sentence-embedding model — **no weights are downloaded, no network, no real data.** The only "secret" is a synthetic canary token (`LAB-CANARY-…`). Runtime ~5 min. The lab prints inversion F1, extraction accuracy, and the noise-vs-utility table.

You: (1) **invert** stored embeddings and measure token-F1, confirming the canary is recovered when present; (2) **extract** the private attribute with a linear probe and beat the majority-class baseline without inverting; (3) turn on the **noise defense** and trace recovery *and* retrieval utility across $\sigma$, reading off the Pareto trade-off; (4) **adapt** — invert using an imperfect *surrogate* encoder to show the attacker does not need exact weights; (5) write the guarantee box for the noise defense and state which controls are actually load-bearing.

## Exercise

Attacks: construct → execute → analyze → measure. Defenses: implement → then bypass your own defense. Math: implement from scratch → use in an experiment → compare to a library.

1. **Recovery curve.** Plot inversion F1 vs $k$ and vs sentence length; explain the shape from the self-term argument.
2. **Attribute survives noise.** Show extraction accuracy stays above baseline at a $\sigma$ where inversion F1 has collapsed; explain why a coarse signal is more noise-robust.
3. **Minimisation beats noise.** Redact the canary *before* embedding; show extraction drops to baseline with no utility loss, and contrast with the noise defense's utility cost. Write both guarantee boxes.
4. **Surrogate strength.** Sweep the surrogate-encoder error; find the error level at which inversion drops to chance. What does this say about protecting encoder weights?
5. **Library check.** Re-implement the linear probe with a library (e.g. scikit-learn `LogisticRegression`) and confirm your from-scratch probe matches within a few points.

## Research paper

**Primary — Morris et al., *Text Embeddings Reveal (Almost) As Much As Text* (vec2text, 2023).** *Why:* the definitive demonstration that black-box embeddings reconstruct fluent input text. *Read:* the threat model (embedding access only), the iterative correction method, and the recovery rates. *Reproduce:* connect its findings to your toy inversion — same principle, stronger decoder. *Limits:* recoverability depends on the encoder; CURRENT and actively researched.

**Companion — Song & Raghunathan, *Information Leakage in Embedding Models* (2020).** *Why:* the foundational inversion/attribute-inference results. *Read:* the inversion and attribute-inference attacks and the defenses evaluated.

## Further reading

- vec2text: https://arxiv.org/abs/2310.06816 · Song & Raghunathan: https://arxiv.org/abs/2004.00053
- OWASP LLM02 Sensitive Information Disclosure: https://genai.owasp.org/llm-top-10/
- This course: [12.1 · extraction, inversion & membership inference](../module-12/lesson-01.md), [14.1 · RAG retrieval attack surface](../module-14/lesson-01.md), [15.1 · multi-tenant retrieval leakage](../module-15/lesson-01.md), [27.1 · recon](../module-27/lesson-01.md).
- Sibling course — embeddings & RAG basics: https://tal-giladi.github.io/llm-research-engineer-course/

## What you should now be able to do

- Explain why an embedding is recoverable data rather than an anonymising hash.
- Invert embeddings to recover input tokens and extract a private attribute with a linear probe.
- Analyse the noise-vs-utility trade-off from first principles and locate a sensible operating point.
- Choose defenses in the right order — access control and minimisation first, noise/DP as measured defence-in-depth — and state what each does and does not guarantee.

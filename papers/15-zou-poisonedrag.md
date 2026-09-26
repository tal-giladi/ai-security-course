# Zou et al. — *PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation* (2024)

**arXiv:** [2402.07867](https://arxiv.org/abs/2402.07867). **Module:** [14.1](../lessons/module-14/lesson-01.md), [15.1](../lessons/module-15/lesson-01.md). **Lab:** [Lab 14](../labs/lab-14/README.md).

## Why it matters
PoisonedRAG is the first systematic attack on the *retrieval* layer: inject a small number of crafted passages into the knowledge base so that, for a target query, they (a) get **retrieved** (rank high) and (b) **steer the generated answer** to the attacker's choice. It decomposes RAG poisoning into a retrieval condition and a generation condition — exactly the two-part structure M14 teaches — and shows that a handful of documents in a large corpus is enough. It is the canonical citation for "your vector store is an injection channel."

## Prerequisites
- Sibling course: embeddings, dense retrieval, RAG.
- This course: [05.1 indirect injection](../lessons/module-05/lesson-01.md), [14.1 RAG attack surface](../lessons/module-14/lesson-01.md).

## What to understand
- **Two conditions:** the poison text must be *retrievable* for the target query (embedding-space proximity) **and** *effective* at controlling the answer once in context (injection). Optimize both.
- **Black-box vs white-box retriever:** craft the retrievability half by prepending/echoing the query text (black-box) or optimizing the embedding (white-box).
- **Tiny budget, large effect:** a few poisoned passages per target query flip answers — the asymmetry defenders must reckon with.

## Which sections to read
- §3 (threat model + the retrieve-and-generate decomposition), §4 (black-box/white-box crafting), §5 (attack-success vs #poison docs).

## Experiment to reproduce (locally)
Lab 14 reproduces PoisonedRAG on a local corpus with a deterministic embedder (`hashlib`-based stable hashing): craft a poison passage that ranks into the top-$k$ for a target query and flips the generated answer to a benign attacker marker. Then add defenses — **retrieval provenance/allowlisting**, **duplicate/outlier detection**, **top-$k$ agreement/consistency filtering** — and re-measure attack success.

## Code to implement
- Poison-passage crafting satisfying both conditions; attack-success vs #poison-docs curve (in the lab).
- A retrieval-side defense (provenance filter or top-$k$ consistency check) and its guarantee box.

## Limitations
- The toy embedder is not a real dense retriever; it demonstrates the mechanism, not exact ASR.
- Assumes write access to the KB — the threat model is "untrusted or user-contributed corpus."

## What later research changed
- Multi-tenant / cross-user leakage ([15.1](../lessons/module-15/lesson-01.md)) extends the retrieval-trust problem to *isolation* failures.
- Defense work (RobustRAG, provenance-aware retrieval, k-consistency voting) is the current frontier — all probabilistic; pair with enforced tenant isolation.

# Carlini et al. — *Extracting Training Data from Large Language Models* (2020)

**arXiv:** [2012.07805](https://arxiv.org/abs/2012.07805) · USENIX Security '21. **Module:** [12.1](../lessons/module-12/lesson-01.md). **Lab:** [Lab 12](../labs/lab-12/README.md).

## Why it matters
This paper demonstrated that a production LLM (GPT-2) **memorizes and can be made to emit verbatim training data** — names, phone numbers, code, UUIDs — extractable by an outsider with only query access. It turned "LLMs might leak training data" into a documented, reproducible attack, and it is the direct justification for treating training-corpus contents (PII, secrets, canaries) as a confidentiality boundary and for canary-based leakage testing.

## Prerequisites
- Sibling course: autoregressive sampling, likelihood/perplexity.
- This course: [13 membership inference](13-shokri-membership.md), [12.1](../lessons/module-12/lesson-01.md).

## What to understand
- **Generate-then-rank:** sample many continuations, then score them for *memorization* — the key is the ranking signal.
- **Membership signals:** high model likelihood is not enough (common text scores high too); compare against a baseline — perplexity ratio to a second model, zlib entropy, lowercase/window variants — to find *memorized* (not merely *likely*) text.
- **Memorization scales** with model size, duplication in the corpus, and string uniqueness (high-entropy secrets are the most extractable — hence canaries).

## Which sections to read
- §4 (the extraction + membership-inference pipeline) and §5 (what gets memorized and why).

## Experiment to reproduce (locally)
Lab 12 reproduces the *mechanism* with a `LAB-CANARY` secret inserted into a toy training corpus: sample continuations, rank by the perplexity-ratio / entropy heuristic, and show the memorized canary rises to the top of the ranking as duplication increases. Then apply **deduplication** and **DP** and show extraction success drop.

## Code to implement
- Generate-and-rank extraction with a perplexity-ratio memorization score (in the lab).
- Canary insertion at varying duplication counts + an extraction-success-vs-duplication curve; dedup/DP mitigation.

## Limitations
- The toy scale demonstrates the ranking mechanism, not frontier-model memorization rates.
- Extraction success is uneven — high-entropy, duplicated strings are the vulnerable case.

## What later research changed
- **Quantifying Memorization** (Carlini et al., 2022) and dedup work showed memorization scales log-linearly with duplication — dedup is the cheapest mitigation.
- Practical exploits ("divergence"/repeated-token attacks) on aligned chat models extended this to deployed systems; canary-in-corpus testing is now standard.

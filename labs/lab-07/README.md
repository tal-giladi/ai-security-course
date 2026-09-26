# Lab 07 — GCG: optimization-based jailbreaks

**Module:** 07 (Stage 3 · jailbreaking). **Time:** ~2.5 h. **Hardware:** CPU-only (torch), no
download — a tiny seeded toy model. **Targets:** abstract "compliance" output class of a random
toy model; nothing harmful is produced.

## Goal

Implement the **actual GCG algorithm** (Zou et al., 2023) — gradient-guided discrete search for an
adversarial suffix that forces a **targeted** model output — and measure it against a
budget-matched random baseline. Then defend with a **perplexity filter** and run the standard
**adaptive** response (a fluent suffix that evades the filter). Full purple-team cycle.

## Run

```bash
py labs/lab-07/gcg.py           # GCG vs random: GCG hits target 8/8, random ~3/8, ~3x fewer queries
py labs/lab-07/defense.py       # perplexity filter cuts gibberish GCG 8/8 -> ~1/8; adaptive fluent evades ~7/8
py -m pytest labs/lab-07 -q     # ~30s
```

## The algorithm (in `gcg.py`)

For a suffix of `L` tokens appended to the prompt, repeat:
1. **Gradient step:** compute the loss (cross-entropy to the target output) on one-hot suffix
   tokens; backprop to get `grad` of shape `[L, vocab]`.
2. **Candidate set:** for each position, take the top-k tokens with the most-negative gradient
   (those that most decrease the loss).
3. **Evaluate & select:** sample a batch of single-token swaps from that set, run true forward
   passes, keep the swap with the lowest real loss.

This is discrete optimization guided by a continuous gradient — the essence of GCG. The toy model
uses hand-rolled attention (so suffix tokens interact, making the search non-trivial) and a strong
refusal bias (so the target output is rare and random search struggles).

## What to notice

- **Gradients beat brute force.** A specific target output is rare by chance; random search over
  the same query budget mostly fails, while GCG reliably succeeds — the core claim of the paper.
- **GCG suffixes are gibberish → high perplexity.** That is *why* a perplexity filter works
  against vanilla GCG (Jain et al.; Alon & Kamfonas, 2023).
- **Adaptive attacks recover.** Adding a fluency penalty to the objective yields low-perplexity
  suffixes that slip under the filter — at some cost to success/queries. **Never evaluate a
  defense only against the original attack.**

## Exercise

See [Lesson 07.1](../../lessons/module-07/lesson-01.md). Summary: derive the GCG update; measure
ASR vs random with a Wilson CI; sweep `topk`/`batch`/`suffix_len` and plot queries-to-success;
implement the perplexity filter and its ROC trade-off; build the adaptive fluent attack and
re-measure; write the guarantee box; connect to real GCG's *transferability* claim.

## Reset / Docker

Stateless. `docker compose up` runs `gcg.py` in a no-egress container.

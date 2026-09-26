# Mehrotra et al. — *Tree of Attacks: Jailbreaking Black-Box LLMs Automatically* (TAP, 2023)

**arXiv:** [2312.02119](https://arxiv.org/abs/2312.02119). **Module:** [08.1](../lessons/module-08/lesson-01.md). **Lab:** [Lab 08](../labs/lab-08/README.md).

## Why it matters
TAP generalizes PAIR from a single refinement chain to **tree search with pruning**: branch multiple attack prompts, prune off-topic or unpromising branches with an evaluator *before* spending target queries, and expand the best. It raises ASR at comparable query budgets and is the clearest illustration that **jailbreaking is a search problem** — which is exactly how you should think about automated red teaming (M25).

## Prerequisites
- This course: [08.1 PAIR](../lessons/module-08/lesson-01.md) first (TAP is PAIR + search), [24.1 evaluation](../lessons/module-24/lesson-01.md).

## What to understand
- **Branch / evaluate / prune / expand:** the classic search skeleton applied to prompts; the pre-query pruning (on-topic + likely-to-succeed) is what buys efficiency.
- **Two evaluators:** an on-topic check (prune irrelevant branches) and a harmfulness judge (score leaves) — separating "relevant" from "successful" reduces wasted queries.
- Search **breadth/depth** as knobs trading queries for ASR — a purple-team dial you can measure.

## Which sections to read
- §3 (the TAP algorithm + pruning criteria).
- §4 (ASR vs query-budget comparisons to PAIR/GCG) — read as a cost curve.

## Experiment to reproduce (locally)
Extend Lab 08's PAIR loop into a small tree: keep a frontier of $b$ candidate prompts, score with the offline judge, prune the worst, expand the best. Plot ASR vs total target-queries for chain (PAIR) vs tree (TAP) on the shim — you should see the tree reach the same ASR with fewer target calls, or higher ASR at equal budget.

## Code to implement
- A bounded best-first / beam search over prompts with a pruning evaluator (in the lab).
- Query-accounting so the ASR-vs-budget curve is honest (count *every* target call).

## Limitations
- More moving parts (two evaluators) = more ways to fool yourself; validate the judges.
- Gains are budget-dependent; report the curve, not a single number.

## What later research changed
- TAP is now a standard baseline in automated red-team suites; the framing feeds directly into [25.1](../lessons/module-25/lesson-01.md) (red-team as search over an attack space with a fitness signal).

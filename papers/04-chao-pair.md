# Chao et al. — *Jailbreaking Black Box Large Language Models in Twenty Queries* (PAIR, 2023)

**arXiv:** [2310.08419](https://arxiv.org/abs/2310.08419). **Module:** [08.1](../lessons/module-08/lesson-01.md). **Lab:** [Lab 08](../labs/lab-08/README.md).

## Why it matters
PAIR (Prompt Automatic Iterative Refinement) shows you don't need gradients, weights, or gibberish to jailbreak: an **attacker LLM** refines a **fluent** prompt against a target using only its outputs, guided by a **judge**, converging in ~20 queries. It is the black-box, transferable, human-readable counterpart to GCG — and it defeats the perplexity filter that catches GCG, because its prompts read like normal English. This is the template for automated red teaming (M25).

## Prerequisites
- This course: [07.1 GCG](../lessons/module-07/lesson-01.md) (so you feel the contrast: white-box gibberish vs black-box fluent), [02.1](../lessons/module-02/lesson-01.md).
- Eval literacy: ASR and judges from [24.1](../lessons/module-24/lesson-01.md).

## What to understand
- **The loop:** attacker proposes a prompt → target answers → judge scores harmfulness/on-topic → attacker reads the score and *reasons about why it failed* → refines. It's in-context optimization over natural language.
- **The judge is load-bearing:** ASR is only as trustworthy as the judge; a weak judge inflates success. This is a measurement lesson as much as an attack.
- **Query efficiency** as a threat metric: cheap, black-box, and transferable across targets.

## Which sections to read
- §3 (the PAIR algorithm + the three roles: attacker, target, judge).
- §4 (query efficiency and transfer) — the practical threat.
- The judge/system-prompt appendix — you'll copy its structure in the lab.

## Experiment to reproduce (locally)
Lab 08 reproduces PAIR/TAP-style black-box search against the shim using a scripted attacker and a rule/score judge (offline, deterministic): show refinement raising the jailbreak score across rounds, converging faster than random. Then swap in a stricter judge and watch measured ASR *drop* — demonstrating judge sensitivity.

## Code to implement
- The attacker→target→judge refinement loop with an iteration budget (in the lab).
- A judge-sensitivity study: run the same attack under a lenient and a strict judge; report ASR with Wilson CI from [`evalkit`](../lab/attack-tools/evalkit.py). The gap *is* the finding.

## Limitations
- Success and its measurement both depend on the judge — easy to fool yourself.
- Uses an attacker LLM; the lab substitutes a deterministic stand-in so it runs offline (fidelity vs reproducibility trade-off — state it).

## What later research changed
- **TAP** ([05](05-mehrotra-tap.md)) adds tree search + pruning for higher ASR at similar budgets.
- Motivated judge-robustness and eval-integrity work central to [24.1](../lessons/module-24/lesson-01.md) and [25.1](../lessons/module-25/lesson-01.md).

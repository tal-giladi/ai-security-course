# Cross-lingual evasion of the guardrail layer itself

- **Topic ID:** cross-lingual-guard-evasion
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261016-04

## Summary

Translating only the user instruction (task, model, agent context held fixed) flips the verdict of
most open/purpose-built LLM safety guards, with a larger effect for lower-resource languages;
frontier-model-based guards shift less. LinguaGuardBench: 19 real guards, 489k verdicts, released.
The novelty is that the *guard layer* (not the target model) has a cross-lingual attack surface — a
clean "the defense has an attack surface of its own" case for the guardrail material.

## Evidence

- https://arxiv.org/abs/2610.22244 — Demirkiran, Ernstberger; 19 guards, 489k released verdicts, held-fixed-except-language design; single preprint, repo URL unconfirmed from the abstract.

## What would change the decision

Confirmed dataset/repo release; an independent spot-check reproducing the verdict-flip on one open
guard in 2–3 languages; integration point decided (M23/M08 guardrail lesson). The released dataset
makes a CPU-feasible exercise plausible.

## History

- 2026-10-18 — WAIT — clean experimental design, many real guards, large released dataset, but single preprint, no independent replication; ADD budget used on skill-trust-boundary — weekly/2026-W42.md — candidates C-20261016-04

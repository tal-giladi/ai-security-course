# Semantic-cache poisoning (embedding-similarity vs answer-validity gap)

- **Topic ID:** semantic-cache-poisoning
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260930-04

## Summary

LLM semantic caches trust cosine similarity as a validity proxy, so an attacker can plant a
malicious cached answer under a query crafted to be embedding-similar to a legitimate one — a
serving-layer attack distinct from RAG/training poisoning. Defense (Deletion-Gain + Answer-Check)
blocks 82.0–98.2% across three attack classes at a stated 5% FP and negligible overhead. Adjacent
to M14/M15 but a distinct mechanism.

## Evidence

- https://arxiv.org/abs/2609.35908 — single paper, novel surface, defense with stated cost; no independent validation or confirmed production exploitation.

## What would change the decision

Independent reproduction, or a production semantic-cache tool (GPTCache-style) adopting a similar
validity check.

## History

- 2026-10-04 — WAIT — novel serving-layer surface with a measured-cost defense, but single paper, no validation — weekly/2026-W40.md — candidates C-20260930-04

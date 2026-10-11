# Prompt injection via agent rule files (AGENTS.md / .cursorrules) driving package substitution (PackHallu)

- **Topic ID:** rule-file-package-substitution
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261008-01

## Summary

Injected text in community-shared rule files steers coding agents to substitute attacker-controlled package names; PackHallu optimises the injected text evolutionarily and reports high, transferable ASR across models and agent frameworks.

## Evidence

- https://arxiv.org/abs/2610.09264 — single preprint; headline ASR numbers only in the full PDF; no code confirmed.

## What would change the decision

Full-paper numbers verified, code, and an independent instance or measured defense. The underlying class (rule/config files as an injection channel, dependency confusion) is already in 21.1; an ADD would be a 21.1 extension, not a new lesson.

## History

- 2026-10-11 — WAIT — mechanism largely covered by 21.1 (malicious repo files, dependency confusion); delta is the optimisation framework; evidence too thin — weekly/2026-W41.md — candidates C-20261008-01

# Evaluating AI-control / sabotage monitors (label leakage, covert misalignment stress tests)

- **Topic ID:** ai-control-monitor-evaluation
- **Status:** WAIT
- **Next review:** 2026-12-13
- **Course change:** none
- **Candidates:** C-20261103-07, C-20261106-06

## Summary

Two critiques of how AI-control monitors are evaluated: simple features that never run the code beat 20 of 24 LLM monitors on a standard backdoor-detection benchmark because of authorship/style label leakage (catch rate 77%→37% on same-generation backdoors), and TraceMRT stress-tests chain-of-thought monitors against covert misalignment, with a Bayesian trajectory monitor reaching AUC 0.91.

## Evidence

- C-20261103-07 — Simple Features Beat Most AI Control Monitors (NeurIPS 2026 EvoRobust workshop; code and rebuilt dataset released).
- C-20261106-06 — Stress Testing CoT Monitoring (preprint, no code, no quantified attack success).

## What would change the decision

Independent reproduction of the label-leakage result, and a placement decision: an M24 case study on evaluation-label leakage (pairs naturally with the 24.1 detector-evaluation extension) or part of a future M23 oversight lesson with agent-oversight-evasion.

## History

- 2026-11-08 — WAIT — methodologically strong and code-released, but the course does not yet teach AI-control monitoring and one workshop paper is not enough to build that prerequisite on — weekly/2026-W45.md — candidates C-20261103-07, C-20261106-06

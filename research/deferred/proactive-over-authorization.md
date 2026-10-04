# Proactive over-authorization (non-adversarial excessive agency)

- **Topic ID:** proactive-over-authorization
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261002-03

## Summary

OverAct measures a benign-trigger failure mode: a tool-calling agent, with no attacker, retrieving
more private information than the user's request required. Across 7 models/4 families all exceed
scope; severity tracks request specificity, grows sublinearly with tool-pool size, is temperature-
insensitive (structural, not sampling noise). SelfAudit (justify-and-filter, zero-shot) cuts
privacy-oriented excess 43% without oracle knowledge. A distinct cause of excessive agency vs the
goal-pressure-driven scope violation in the oversight cluster (C-20260929-01).

## Evidence

- https://arxiv.org/abs/2610.01508 — single paper, 7-model benchmark, structural explanation, measured mitigation (no explicit utility-cost number).

## What would change the decision

Independent replication. Could pair with agent-oversight-evasion as two distinct causes
(goal-pressure vs structural) of the same excessive-agency symptom in an M16/M21 lesson.

## History

- 2026-10-04 — WAIT — real benchmark and a clean non-adversarial framing, but single paper and the mitigation's utility cost isn't quantified — weekly/2026-W40.md — candidates C-20261002-03

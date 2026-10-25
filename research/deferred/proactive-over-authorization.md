# Proactive over-authorization (non-adversarial excessive agency)

- **Topic ID:** proactive-over-authorization
- **Status:** WAIT
- **Next review:** 2026-11-08
- **Course change:** none
- **Candidates:** C-20261002-03, C-20261021-02, C-20261021-03

## Summary

OverAct measures a benign-trigger failure mode: a tool-calling agent, with no attacker, retrieving
more private information than the user's request required. Across 7 models/4 families all exceed
scope; severity tracks request specificity, grows sublinearly with tool-pool size, is temperature-
insensitive (structural, not sampling noise). SelfAudit (justify-and-filter, zero-shot) cuts
privacy-oriented excess 43% without oracle knowledge. A distinct cause of excessive agency vs the
goal-pressure-driven scope violation in the oversight cluster (C-20260929-01).

## Evidence

- https://arxiv.org/abs/2610.01508 — single paper, 7-model benchmark, structural explanation, measured mitigation (no explicit utility-cost number).
- https://arxiv.org/abs/2610.27548 — AuthorizationBench: 286 tasks, 6,864 trajectories; 19.2% out-of-authorization; higher under benign pressure than injection (23.5% vs 17.6%, p=0.002); consulting the principal lowers it (14.0% vs 21.6%); code/data https://github.com/PEACH-Research-Lab/AuthorizationBench. Added 2026-10-25.
- https://arxiv.org/abs/2610.27574 — Show-Up attack (SUA-Arena): malicious subagents get supervisors to grant out-of-scope involvement; all 6 frontier supervisors vulnerable; no code. Added 2026-10-25.

## What would change the decision

Independent replication. Could pair with agent-oversight-evasion as two distinct causes
(goal-pressure vs structural) of the same excessive-agency symptom in an M16/M21 lesson.

## History

- 2026-10-04 — WAIT — real benchmark and a clean non-adversarial framing, but single paper and the mitigation's utility cost isn't quantified — weekly/2026-W40.md — candidates C-20261002-03
- 2026-10-18 — WAIT — its adversarial counterpart arrived (ASU: effect binding + trusted rendering for agent step-up authorization, Tamarin-proved, 10-runtime audit, released code) — strong and teachable but single preprint with authors' own caveats (flooding still 45–60%, second device adds nothing); keep 2026-11-22 and pair ASU with this topic's non-adversarial OverAct framing at ADD time — weekly/2026-W42.md — candidates C-20261016-03
- 2026-10-25 — WAIT — second independent, larger, code-released benchmark on the same non-adversarial excessive-agency phenomenon (with a measured mitigation) — converging evidence; pulled forward to 2026-11-08 as an ADD candidate — weekly/2026-W43.md — candidates C-20261021-02, C-20261021-03

# Denial-of-wallet via retained/re-billed tool output

- **Topic ID:** agent-denial-of-wallet
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260929-03

## Summary

DOW-BENCH formalises "persistent billable state": a host runtime that carries a tool's return value
into later turns re-meters it on every call, so an untrusted tool can convert attacker data into
recurring victim-billed inference cost (no stolen credentials). Six vectors, six model families;
max cumulative input 14,293x the initiating call; naive retention +21–36% session cost. A defense
comparison is stated (compression 10–11/12 tasks vs 2/12 for blunt deletion; progress-authorized
22/24 vs 13/24 for a fixed cap). A new attack class (economic/resource exhaustion via context
retention) not named in the course's DoS/excessive-agency material.

## Evidence

- https://arxiv.org/abs/2609.28585 — DOW-BENCH (institutional multi-author, formal threat model, defense trade-off).

## What would change the decision

Released benchmark/code or independent reproduction. Candidate for an M14/M21 cost-DoS lab.

## History

- 2026-10-04 — WAIT — unusually complete single paper (attack + measured defense trade-off), but one group, no code/replication yet — weekly/2026-W40.md — candidates C-20260929-03

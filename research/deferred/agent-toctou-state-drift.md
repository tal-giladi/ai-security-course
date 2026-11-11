# TOCTOU / state drift for transaction-signing agents (Proof-Gated Signing)

- **Topic ID:** agent-toctou-state-drift
- **Status:** WAIT
- **Next review:** 2026-11-29
- **Course change:** none
- **Candidates:** C-20261004-01

## Summary

A new domain instance of the course's TOCTOU/pin-and-reverify pattern (M13/M17/M19): AI agents that
sign blockchain transactions check a snapshot state, but execution happens later after an adversary
changes conditions ("state drift"). Counterintuitive finding: giving an LLM reviewer a clean
pre-drift simulation makes it MORE likely to approve a drift attack. Proof-Gated Signing uses SMT
solvers to compile an on-chain post-condition that must hold regardless of intervening state: 93.6%
harmful-tx prevention, 97.5% benign pass, zero attacker gains across 50 drift scenarios.

## Evidence

- https://arxiv.org/abs/2610.00354 — single-author preprint, narrow blockchain domain, concrete numbers across 260+50 scenarios; no code/replication.

## What would change the decision

Independent replication or released code. The counterintuitive "clean simulation lowers reviewer
caution" finding is teachable as a single-paper M13/M17/M19 TOCTOU case study even without adoption.

## History

- 2026-10-04 — WAIT — generalizable mechanism and a sharp counterintuitive result, but single-author preprint in a narrow domain — weekly/2026-W40.md — candidates C-20261004-01

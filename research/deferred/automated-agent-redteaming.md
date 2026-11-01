# Autonomous repository-to-runtime agent red-teaming (AgentXploit)

- **Topic ID:** automated-agent-redteaming
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260928-03, C-20261027-08

## Summary

AgentXploit splits repo-level attack-path discovery (Analyzer) from runtime exploitation
(Exploiter) and ships AgentXploit-Bench (72 vulns across 12 agent frameworks); 59.3% end-to-end vs
38.4% Codex, and 79.2% vs 52.7% (AgentVigil) on AgentDojo. Relevant to M25 automated red-teaming
tooling.

## Evidence

- https://arxiv.org/abs/2609.31318 — quantified improvement over two baselines on a new + established benchmark; code not confirmed released.
- https://arxiv.org/abs/2610.34965 — Critic/proposer role separation (Bo Li group): target self-critique beats a separate critic (removing it costs 6–17pp ASR), but letting the target propose the next attack backfires; 63.2% ASR on DTAP-BENCH (preprint, own benchmark). Added 2026-11-01.

## What would change the decision

Public code/benchmark release and an independent trial. Candidate for an M25 tooling lesson once
usable.

## History

- 2026-10-04 — WAIT — real methodological advance but no released code yet, single paper — weekly/2026-W40.md — candidates C-20260928-03
- 2026-11-01 — WAIT — a pipeline-design rule for automated red-teaming, not a new vulnerability class; own benchmark; keep scheduled review — weekly/2026-W44.md — candidates C-20261027-08

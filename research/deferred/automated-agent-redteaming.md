# Autonomous repository-to-runtime agent red-teaming (AgentXploit)

- **Topic ID:** automated-agent-redteaming
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260928-03, C-20261027-08, C-20261111-01

## Summary

AgentXploit splits repo-level attack-path discovery (Analyzer) from runtime exploitation
(Exploiter) and ships AgentXploit-Bench (72 vulns across 12 agent frameworks); 59.3% end-to-end vs
38.4% Codex, and 79.2% vs 52.7% (AgentVigil) on AgentDojo. Relevant to M25 automated red-teaming
tooling.

## Evidence

- https://arxiv.org/abs/2609.31318 — quantified improvement over two baselines on a new + established benchmark; code not confirmed released.
- https://arxiv.org/abs/2610.34965 — Critic/proposer role separation (Bo Li group): target self-critique beats a separate critic (removing it costs 6–17pp ASR), but letting the target propose the next attack backfires; 63.2% ASR on DTAP-BENCH (preprint, own benchmark). Added 2026-11-01.
- https://arxiv.org/abs/2611.11861 — Agentic Optimizer (Google DeepMind): 8 teams x 2 attacker agents with shared leaderboards; attack resistance as low as 1% for several open and Gemini Flash models, 66% for Gemini 4 Argon; benign-goal attacker objectives isolate instruction-hierarchy adherence (preprint, no code). Added 2026-11-15.

## What would change the decision

Public code/benchmark release and an independent trial. Candidate for an M25 tooling lesson once
usable.

## History

- 2026-10-04 — WAIT — real methodological advance but no released code yet, single paper — weekly/2026-W40.md — candidates C-20260928-03
- 2026-11-01 — WAIT — a pipeline-design rule for automated red-teaming, not a new vulnerability class; own benchmark; keep scheduled review — weekly/2026-W44.md — candidates C-20261027-08
- 2026-11-15 — WAIT — a frontier-lab primary source (Google DeepMind agent-swarm optimizer, benign-goal injection set) supports the adaptive-evaluation message; single preprint, own synthetic set, mitigations disabled for its own models, no code; scheduled review 2026-11-22 unchanged — weekly/2026-W46.md — candidates C-20261111-01

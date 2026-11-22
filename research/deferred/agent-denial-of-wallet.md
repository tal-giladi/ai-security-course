# Denial-of-wallet via retained/re-billed tool output

- **Topic ID:** agent-denial-of-wallet
- **Status:** WAIT
- **Next review:** 2027-01-03
- **Course change:** none
- **Candidates:** C-20260929-03, C-20261113-03

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
- https://arxiv.org/abs/2611.14808 — OverServe: benign-looking MCP status tools co-designed with confirm-until-done prompts; max 93.88x API-request amplification across Qwen/Nemotron/DeepSeek/Sonnet (preprint, no code). Added 2026-11-15.
- https://arxiv.org/abs/2611.26117 — ChronoPatch (daily C-line 2026-11-21, not verified): energy-latency attacks on VLMs incl. three commercial APIs; attack only. Added 2026-11-22.

## What would change the decision

Released benchmark/code or independent reproduction. Candidate for an M14/M21 cost-DoS lab.

## History

- 2026-10-04 — WAIT — unusually complete single paper (attack + measured defense trade-off), but one group, no code/replication yet — weekly/2026-W40.md — candidates C-20260929-03
- 2026-11-15 — WAIT — an independent group on agent resource exhaustion via a different mechanism (status tool + completion-confirmation prompt, up to 93.88x amplification, passes task checks and MCP scanners); not a reproduction of this topic's mechanism and no defense cost; scheduled review 2026-11-22 unchanged — weekly/2026-W46.md — candidates C-20261113-03
- 2026-11-22 — WAIT — adjacent attack-only evidence (VLM energy-latency); still no released benchmark or reproduction of OverServe — next review 2027-01-03 — weekly/2026-W47.md — no new candidate

# Measured effect and cost of coding-agent harness security mechanisms (HarnessSecurity)

- **Topic ID:** coding-agent-harness-mechanisms
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20261007-01

## Summary

First cross-harness benchmark (Claude Code, Codex CLI, Gemini CLI, gptme, Qwen Code, Copilot): ~50% of mechanisms opt-in by default; auto-approve raises ASR 29.2%→95.6%; isolation/read-only cut ASR at substantial utility loss; allow/denylisting are cheap.

## Evidence

- https://arxiv.org/abs/2610.07639 — 2,500 trials, 81,155 tool calls, 23 tasks, 5 surfaces. Single fresh preprint; per-mechanism utility numbers only in the full PDF; project link unverified.

## What would change the decision

Full-PDF per-mechanism numbers confirmed, an artifact release, and ideally a second measurement (harness defaults change fast — the finding must be re-dated before teaching). Natural fit: a 21.1 extension with a guarantee table.

## History

- 2026-10-11 — WAIT — highly relevant measurement but about fast-changing product defaults, one preprint, exact cost numbers not yet verified — weekly/2026-W41.md — candidates C-20261007-01

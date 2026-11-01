# Measured effect and cost of coding-agent harness security mechanisms (HarnessSecurity)

- **Topic ID:** coding-agent-harness-mechanisms
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20261007-01, C-20261022-03, C-20261030-02

## Summary

First cross-harness benchmark (Claude Code, Codex CLI, Gemini CLI, gptme, Qwen Code, Copilot): ~50% of mechanisms opt-in by default; auto-approve raises ASR 29.2%→95.6%; isolation/read-only cut ASR at substantial utility loss; allow/denylisting are cheap.

## Evidence

- https://arxiv.org/abs/2610.07639 — 2,500 trials, 81,155 tool calls, 23 tasks, 5 surfaces. Single fresh preprint; per-mechanism utility numbers only in the full PDF; project link unverified.
- https://arxiv.org/abs/2610.29869 — Compaction laundering: string-flattening harnesses (pi, opencode, Cline, Aider, OpenHands) carry forged user turns through context compaction 87–100%; role-typed harnesses (Codex, Gemini CLI, Qwen Code, Continue) 0%; provenance check catches 77% at 2% demotion of legit content; serializer escaping as cheaper fix; single author, no code. Added 2026-10-25.
- https://arxiv.org/abs/2610.38799 — CARI: unauthorized instructions in runtime feedback from peer components (CI, test harness, backend) with diagnostic but not action authority; 94.8% of 3,000 trials, 61.3% Codex / 58.7% Claude Code; prompt warnings ineffective, explicit policy rules over-refuse (preprint, no code). Added 2026-11-01.

## What would change the decision

Full-PDF per-mechanism numbers confirmed, an artifact release, and ideally a second measurement (harness defaults change fast — the finding must be re-dated before teaching). Natural fit: a 21.1 extension with a guarantee table.

## History

- 2026-10-11 — WAIT — highly relevant measurement but about fast-changing product defaults, one preprint, exact cost numbers not yet verified — weekly/2026-W41.md — candidates C-20261007-01
- 2026-10-25 — WAIT — a concrete, deterministic harness-level provenance bug with a measured fix — strengthens the case for a measured M21 harness-mechanism extension; single author, no code; keep 2026-11-15 — weekly/2026-W43.md — candidates C-20261022-03
- 2026-11-01 — WAIT — a new, mechanism-distinct channel (authority mismatch in runtime feedback) with real-product numbers; no defense proposed and no code; review at the scheduled date together with the cluster — weekly/2026-W44.md — candidates C-20261030-02

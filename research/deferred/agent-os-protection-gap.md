# Agents as operating systems: missing OS-grade protections in agent harnesses (AaOS)

- **Topic ID:** agent-os-protection-gap
- **Status:** WAIT
- **Next review:** 2026-12-13
- **Course change:** none
- **Candidates:** C-20261027-02

## Summary

The paper maps 116 OS security mechanisms across 19 subsystems onto agent harnesses: 11 are isomorphic and 65 are missing (privilege separation, quotas, transactions, tamper-proof audit). Thirteen experiments on Claude Code, Codex CLI and Gemini CLI confirm 16/25 mechanisms, including tool-level checks bypassable through the shell and forged transcript records accepted on resume.

## Evidence

- https://arxiv.org/abs/2610.33753 — Li et al. (preprint, no code).

## What would change the decision

Independent reproduction of the forged-resume and shell-bypass findings, or vendor acknowledgement. A strong candidate for a 21.1 or 23.1 architecture-checklist extension; it overlaps coding-agent-harness-mechanisms (compaction laundering, forged turns).

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261027-02

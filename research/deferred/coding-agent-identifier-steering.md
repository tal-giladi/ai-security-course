# NameTrap: steering coding agents to write vulnerable code via identifier names

- **Topic ID:** coding-agent-identifier-steering
- **Status:** WAIT
- **Next review:** 2026-12-27
- **Course change:** none
- **Candidates:** C-20261027-07

## Summary

Renaming identifiers in third-party code, with no instructions and no vulnerable statements, steers coding agents toward CWE-78/79/327/502 code: 22.5–56.0% ASR overall across 6 agents × 10 models, up to 75%. The poisoned files evade 3 AI-based and 4 static analyzers, and a security-reminder prompt does not reliably help.

## Evidence

- https://arxiv.org/abs/2610.34253 — Chang et al. (preprint, no code).

## What would change the decision

Code or replication. It would fit 21.1 next to rule-file-package-substitution.

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261027-07

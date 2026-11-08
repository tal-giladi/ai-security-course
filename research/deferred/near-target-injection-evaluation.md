# Near-target prompt injection: fixed-target benchmarks overstate robustness

- **Topic ID:** near-target-injection-evaluation
- **Status:** WAIT
- **Next review:** 2026-12-13
- **Course change:** none
- **Candidates:** C-20261026-03, C-20261104-06, C-20261106-05

## Summary

NTBench builds injections that keep a plausible on-task answer but make it subtly wrong or harmful. Across 7 LLMs, 10 datasets and 2 agent benchmarks, these succeed more often than fixed-target injections: +9.3 to +35.8pp for incorrect targets and +1.7 to +17.3pp for harmful targets.

## Evidence

- https://arxiv.org/abs/2610.32531 — Gong, Wang, Liu, Wang (preprint, no code/dataset).
- Nine dimensions of prompt-injection context (C-20261104-06): taxonomy applied to nine benchmarks; no code/venue. Added 2026-11-08.
- Task-tampering IPI benchmark (C-20261106-05): attacks that alter the task rather than override it; per-defense breakdown; code/data released. Added 2026-11-08.

## What would change the decision

A dataset release or independent replication. If either arrives, cluster with jailbreak-asr-judge-variance and rag-defense-measured-endpoints as one 'evaluation validity' extension to 24.1.

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261026-03
- 2026-11-08 — WAIT — two benchmark-critique preprints (one with code) strengthen the "benchmarks overstate defense robustness" theme now taught in the 24.1 extension; date unchanged — weekly/2026-W45.md — candidates C-20261104-06, C-20261106-05

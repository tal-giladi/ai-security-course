# Monitor evidence-path failures and canary contracts

- **Topic ID:** monitor-evidence-path-integrity
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261020-03, C-20261027-11

## Summary

A runtime monitor can detect a signal that the framework then drops before enforcement; 'canary contracts' (known payloads, exact revisions, negative controls) test the evidence path end to end; 18 failures across 11 project groups reported.

## Evidence

- https://arxiv.org/abs/2610.23362 — single author, no affiliation, audited projects unnamed, no code.
- https://arxiv.org/abs/2610.34064 — Back to Basics: provenance/security/effect hints added to the monitored transcript substantially improve weak monitors at low cost and nearly eliminate complete misses; 4 monitor failure modes named (preprint, no code). Added 2026-11-01.

## What would change the decision

A revision naming audited projects with code, or independent citation. The idea (test detector-to-enforcement plumbing with canaries) fits M23 as an exercise once corroborated.

## History

- 2026-10-25 — WAIT — clean methodology, unverifiable rigor (single unaffiliated author, no code, unnamed targets) — weekly/2026-W43.md — candidates C-20261020-03
- 2026-11-01 — WAIT — a defense-side data point (annotate the transcript, not the monitor); single preprint, no code; keep scheduled review — weekly/2026-W44.md — candidates C-20261027-11

# Orchestrator integrity against malicious sub-agent outputs (aggregation and replanning)

- **Topic ID:** multi-agent-orchestrator-feedback-integrity
- **Status:** WAIT
- **Next review:** 2027-01-17
- **Course change:** none
- **Candidates:** C-20261116-02, C-20261122-01

## Summary

Two single-preprint defenses for the point where a multi-agent orchestrator consumes sub-agent output: ReMA/SecMAS (response-manipulation attacks on aggregation; a consistency-based secure aggregation rule that assumes an honest subset) and Kaer (instructions hidden in sub-agent failure feedback hijack replanning; abstract failure templates plus deterministic repair operators).

## Evidence

- https://arxiv.org/abs/2611.17883 — ReMA / SecMAS (C-20261116-02); abstract only, no code.
- https://arxiv.org/abs/2611.24839 — Kaer (C-20261122-01); no numbers in the abstract, no code.

## What would change the decision

Code or a second group's evaluation for either; numbers for Kaer. Would be an M28 lab extension (orchestrator replans from typed failure templates; malicious sub-agent canary).

## History

- 2026-11-22 — WAIT — two single preprints, abstract-only, no code; the core lesson (treat sub-agent output as untrusted data, enforce typed interfaces) is already in 28.1 — weekly/2026-W47.md — candidates C-20261116-02, C-20261122-01

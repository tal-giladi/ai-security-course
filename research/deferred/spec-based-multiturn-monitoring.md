# SpecGuard: LTL-specified, automaton-compiled multi-turn jailbreak monitoring

- **Topic ID:** spec-based-multiturn-monitoring
- **Status:** WAIT
- **Next review:** 2026-12-27
- **Course change:** none
- **Candidates:** C-20261028-04

## Summary

Natural-language observations become evidence-backed propositions. Forbidden multi-turn patterns are written in LTL and compiled to automata that process the dialogue incrementally and produce a replayable witness. The method is training-free and reportedly beats open guard models at controlled FPR.

## Evidence

- https://arxiv.org/abs/2610.36258 — Li et al. (preprint, no code, numbers not given in the abstract).

## What would change the decision

Code and baseline numbers. Could become a 23.1 detection-engineering extension.

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261028-04

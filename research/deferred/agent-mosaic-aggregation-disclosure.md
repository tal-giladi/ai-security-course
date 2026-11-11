# Mosaic effect: agents disclose prohibited composite conclusions

- **Topic ID:** agent-mosaic-aggregation-disclosure
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261023-03, C-20261031-04

## Summary

Agents with access to individually permitted documents infer and state a prohibited composite conclusion (7.08% best-case in simulation, higher in live harnesses); classification headers reduce but do not remove it; refusals themselves can leak the conclusion.

## Evidence

- https://arxiv.org/abs/2610.30418 — single preprint, no code.
- https://arxiv.org/abs/2610.39532 — Task-Graph Contextual Integrity (see multi-agent-topology-leakage): propagation-scope enforcement as a possible defense for composite disclosure. Added 2026-11-01.

## What would change the decision

Code or replication, ideally a defense; would extend 17.2's guarantee box ('flow control does not bound inference').

## History

- 2026-10-25 — WAIT — distinct from flow control and teachable as a limit, but single preprint, no code, no defense — weekly/2026-W43.md — candidates C-20261023-03
- 2026-11-01 — WAIT — cross-referenced defense evidence; no code; keep scheduled review — weekly/2026-W44.md — candidates C-20261031-04

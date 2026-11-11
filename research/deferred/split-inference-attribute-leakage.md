# Attribute leakage from 'protected' features in edge-cloud split multimodal inference

- **Topic ID:** split-inference-attribute-leakage
- **Status:** WAIT
- **Next review:** 2026-12-27
- **Course change:** none
- **Candidates:** C-20261026-10

## Summary

With 20 labels per class, an honest-but-curious cloud server recovers 75–85% of unprotected attribute leakage (age, gender, race) from intermediate features protected at the edge, including features protected by Safe-LLaVA.

## Evidence

- https://arxiv.org/abs/2610.32079 — preprint, no code; authors not confirmed.

## What would change the decision

Code, a defense response, or replication. It would extend 12.1/29.1 with a deployment-pattern case.

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261026-10

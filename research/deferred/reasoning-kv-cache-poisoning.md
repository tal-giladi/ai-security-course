# Poisoning via reused reasoning-trace KV cache (R²ECAP)

- **Topic ID:** reasoning-kv-cache-poisoning
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261019-05

## Summary

Systems that cache and reuse KV state from reasoning traces gain a black-box poisoning surface: two planted traces carry adversarial influence forward even after the first is deleted (up to 79% ASR; ~1% flagged by a popular injection detector).

## Evidence

- https://arxiv.org/abs/2610.22873 — single preprint, 3 models, no code confirmed.

## What would change the decision

Independent replication, released code, or a measured mitigation (cache isolation/attestation) with its latency cost.

## History

- 2026-10-25 — WAIT — a new surface but attack-only, single preprint, no code; not teachable without a defense — weekly/2026-W43.md — candidates C-20261019-05

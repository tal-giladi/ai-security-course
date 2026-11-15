# Post-fine-tuning safety recovery for fine-tuning-as-a-service (SLDR)

- **Topic ID:** finetuning-as-a-service-defense
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261008-02, C-20261114-02

## Summary

SLDR: layer-wise safety sensitivity is directional; a LoRA recovery adapter on the most/least sensitive layers, gated by representation-based routing for malicious queries, drops harmful score 11.54→0.08 on Llama3.1/SST2 while keeping task accuracy, even at 0.9 poisoning ratio. Accepted at NeurIPS 2026 (per the abstract); code released.

## Evidence

- https://arxiv.org/abs/2610.10345 — code https://github.com/Stardust457/SLDR
- https://arxiv.org/abs/2611.16369 — Bait (Huang et al.): agentic RL through an RL fine-tuning API removes safety alignment; defense probes the submitted reward function before training; code https://github.com/git-disl/Bait (not cloned or run). Added 2026-11-15.

## What would change the decision

An adaptive-attack evaluation (attacker aware of the router) by an independent group; a CPU-scale reproduction path. Would need a 'harmful fine-tuning' prerequisite section (course covers poisoning/backdoors, not FTaaS alignment removal) — likely an 11.1 or 13.1 extension.

## History

- 2026-10-11 — WAIT — peer-reviewed and code-released, but no adaptive evaluation of the routing gate and the threat model (FTaaS alignment removal) is not yet taught as a prerequisite — weekly/2026-W41.md — candidates C-20261008-02
- 2026-11-15 — WAIT — the threat widens to RL-as-a-service (harmful reward functions strip alignment for ~USD 20, author claim) with a provider-side reward-probing defense and released code; the adaptive analysis is the authors' own and no FP/utility numbers are in the abstract; scheduled review 2026-11-22 unchanged; consider widening the topic to fine-tuning/RL-as-a-service then — weekly/2026-W46.md — candidates C-20261114-02

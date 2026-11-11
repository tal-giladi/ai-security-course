# Verifier hardening for agent-training environments (reward-hacking integrity)

- **Topic ID:** verifier-hardening-rl-envs
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261012-04, C-20261015-19

## Summary

Agent-training environments use programmatic verifiers to turn outcomes into reward; two angles this
week. (1) Reward hacking is transmissible across multi-agent coding systems — hacks spread via shared
code/memory/plans, and small open-weight agents can induce it in stronger targets. (2) A hacker-fixer
loop automatically hardens verifiers against exploits at scale (Terminal Bench, KernelBench, SETA),
and an earlier version is reportedly already adopted by the official Terminal Bench repository — rare
real adoption. Together: a reward-hacking/automated-red-teaming theme the course does not yet teach.

## Evidence

- https://arxiv.org/abs/2610.15924 — Zeng et al. (Raghunathan, CMU, unverified); stated Terminal Bench adoption (not independently re-verified against the repo); project page https://verifier-hardening.github.io/.
- https://arxiv.org/abs/2610.12822 — Hu et al.; reward-hacking transmissibility across four open-weight backbones; abstract gives no propagation ASR numbers.

## What would change the decision

Direct verification of the Terminal Bench adoption against that repository; released code; a
CPU-feasible toy (exploitable verifier + simplified hacker-fixer loop, measure attack-success
reduction across iterations) for M25.

## History

- 2026-10-18 — WAIT — the real adoption claim is unusually strong, but unverified this run and the companion transmissibility paper lacks quantitative figures; verify the adoption before any ADD — weekly/2026-W42.md — candidates C-20261012-04, C-20261015-19

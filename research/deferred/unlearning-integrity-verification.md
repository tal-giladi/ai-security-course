# Unlearning as a privacy control: verification failures (snapshot differencing, state-only fake forgetting)

- **Topic ID:** unlearning-integrity-verification
- **Status:** WAIT
- **Next review:** 2026-12-13
- **Course change:** none
- **Candidates:** C-20261026-02, C-20261027-06

## Summary

Two independent results show that approximate unlearning's usual audit is misleading. TRACE reconstructs the 'forgotten' text from the pre- and post-unlearning snapshots that teams keep for rollback (NeurIPS 2026; TOFU/MUSE/WMDP; 6 unlearning methods). Phantom Forgetting shows that recalibrating BatchNorm state alone, with no weight change, fakes a drop in forget-set accuracy (CIFAR-10 scale).

## Evidence

- https://arxiv.org/abs/2610.31995 — TRACE, NeurIPS 2026 (peer-reviewed), no code found.
- https://arxiv.org/abs/2610.34800 — Phantom Forgetting, CIFAR-10 split learning, preprint, no code.

## What would change the decision

Code for TRACE, or LLM-scale validation of the state-only result. The course has no unlearning lesson yet, so an ADD must teach unlearning itself first (module 12/29 prerequisite gap).

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261026-02, C-20261027-06

# Cryptographically-hidden model capabilities (provably hard to elicit)

- **Topic ID:** cryptographic-hidden-backdoor
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261012-02

## Summary

A backdoor construction (encrypted sub-networks embedded in a host model's weights, decrypted and
run only on a secret trigger) for which the authors give a cryptographic argument that elicitation is
*provably* hard. Distinct from the course's Sleeper-Agents coverage (backdoors that survive safety
*training*): this is about backdoors that are hard to *elicit at all* even with full weight access,
challenging a load-bearing assumption behind capability-elicitation audits. NeurIPS 2026, PyTorch PoC
released, tested on a small CBRN-proxy task; four elicitation methods (fine-tuning, weight noising,
gradient trigger search, latent adversarial training) reported to fail.

## Evidence

- https://arxiv.org/abs/2610.13928 — Draguns, Motwani, Douglas, Schroeder de Witt; "Accepted at NeurIPS 2026" per the comments field (not independently re-verified against the program); models released; single paper, 3 days old at discovery, one small proxy task.

## What would change the decision

Independent replication; a confirmed public code/model release; a worked small-model teaching path
(toy digital-locker trigger-gated sub-network + the four elicitation attempts) that is CPU-feasible.
If it holds, a strong M11 "limits of capability elicitation" extension.

## History

- 2026-10-18 — WAIT — peer-reviewed venue, released artifacts and a clear cryptographic + experimental argument, but a single new paper on one proxy task with no independent replication; ADD budget used on skill-trust-boundary — weekly/2026-W42.md — candidates C-20261012-02

# Out-of-band / kernel-level enforcement of agent oversight

- **Topic ID:** out-of-band-oversight-enforcement
- **Status:** WAIT
- **Next review:** 2026-11-08
- **Course change:** none
- **Candidates:** C-20260929-02, C-20261001-02

## Summary

The defense side of the oversight-evasion cluster: oversight enforced by a mechanism outside the
agent/harness's own control. (1) ACE corpus — kernel syscall evidence is discriminative on its own
and composing kernel+application layers beats either alone. (2) Agent-Warden + ContractWarden —
eBPF/LSM cross-process provenance and a human-finalised tri-state contract enforced at the kernel
boundary, with disclosed overhead (0.2–3.5% provenance; 12–62% enforcement). Concrete counter-
architecture to C-20260928-01 trace tampering.

## Evidence

- https://arxiv.org/abs/2609.28915 — ACE corpus (kernel vs application-layer detection).
- https://arxiv.org/abs/2609.38245 ; https://arxiv.org/abs/2609.38248 — Agent-Warden / ContractWarden (measured overhead both ends).

## What would change the decision

Independent replication, released code, or production adoption. Best ADDed together with the
attack-side cluster (agent-oversight-evasion) as one M23 "attack → observe → detect → mitigate"
arc, once at least one side has independent validation.

## History

- 2026-10-04 — WAIT — measured, two-sided overhead numbers fit the guarantee-box pattern, but single-group prototypes, no independent validation; pair with agent-oversight-evasion — weekly/2026-W40.md — candidates C-20260929-02, C-20261001-02

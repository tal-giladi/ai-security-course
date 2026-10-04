# Backdoored retriever checkpoint hijacks agentic search

- **Topic ID:** malicious-retriever-checkpoint
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260930-05

## Summary

"Backdoor in the Loop" extends RAG poisoning from the corpus to the retriever model itself: a
backdoored retriever can suppress evidence, force retrieval of chosen docs, or inflate search cost,
without touching the corpus. Notable defensive finding: weak backdoor-purification (approximate
unlearning) can be weaponised as concealment — the purification process itself becomes camouflage.
Attack/evasion-only; no mitigation proposed. Cautionary for any future unlearning-based defense.

## Evidence

- https://arxiv.org/abs/2609.37468 — single paper, clear threat model, defense-backfire finding; no defense of its own, no replication.

## What would change the decision

A proposed/measured counter-defense, or independent replication. Useful mainly as a guarantee-box
"how an attacker adapts" caution once a purification defense is in scope.

## History

- 2026-10-04 — WAIT — new retriever-as-attack-surface angle and a sharp defense-backfire caution, but offensive-only and unreplicated — weekly/2026-W40.md — candidates C-20260930-05

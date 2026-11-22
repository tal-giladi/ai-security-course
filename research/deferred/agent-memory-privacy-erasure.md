# Agent memory privacy: disclosure amplification and deletion that does not erase

- **Topic ID:** agent-memory-privacy-erasure
- **Status:** WAIT
- **Next review:** 2026-11-29
- **Course change:** none
- **Candidates:** C-20261021-07, C-20261024-01, C-20261116-01

## Summary

Two non-poisoning privacy failures of persistent agent memory: (1) a disclosure feedback loop where memory-conditioned replies raise users' attribute disclosure over sessions (mitigated by not stating/presupposing attributes); (2) deleting a memory record does not delete what derived state carries (62–99% reconstruction from components; provenance-aware closure eliminates it in tested settings).

## Evidence

- https://arxiv.org/abs/2610.28315 — Disclosure Begets Disclosure, simulation, no code.
- https://arxiv.org/abs/2610.31366 — AfterDeleteBench, exposed-vs-control audit design, no code.
- https://arxiv.org/abs/2611.18133 — LinEra (Ameur, Mokhtari, Bouzefrane; submitted to JISA): lineage-complete forward-secure erasure via keys derived along the memory derivation graph from a puncturable PRF; mem0 integration; after logical deletion an attacker with all storage and current keys recovers 70/71 forgotten secrets (67 with per-object/epoch keys), 0 with LinEra; cost = forgetting radius (1% of turns forgotten erases 73.0% of derived memories with session summaries, 3.8% with four-turn windows). Code: https://github.com/yulliwasameur/linera (MIT, one commit; not run). Independent of AfterDeleteBench (no author overlap) — abstract only. Added 2026-11-22.

## What would change the decision

Code release or replication for either; then a 16.2 extension on memory erasure (provenance-aware closure) with the exposed-vs-control measurement as the lab pattern.

## History

- 2026-10-25 — WAIT — a genuine gap in the memory lessons (erasure/privacy, not poisoning) but two single preprints without code — weekly/2026-W43.md — candidates C-20261021-07, C-20261024-01
- 2026-11-22 — WAIT — the stated trigger (code or replication) is now met by LinEra (independent reproduction of delete-does-not-erase in mem0, defense with proof, code and a measured erasure-radius cost); not added only because the one-ADD budget went to the cross-tenant prefix-cache side channel, which has adoption evidence (CVE, shipped fix, peer-reviewed real-provider audit) this topic lacks; leading candidate for next week as a 16.2 extension — next review 2026-11-29 — weekly/2026-W47.md — candidates C-20261116-01

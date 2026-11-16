# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261116-01 · LinEra: lineage-complete, forward-secure cryptographic erasure for LLM-agent memory (deletion that actually erases derived memories)

- **Class:** A
- **Date discovered:** 2026-11-16
- **Date published:** 2026-11-13
- **Source:** https://arxiv.org/abs/2611.18133 (verified resolves; abstract via arXiv API, abs page fetched)
- **Organization/researchers:** Yulliwas Ameur, Billal Mokhtari, Samia Bouzefrane (affiliation not stated on the abs page; abs Comments: "Submitted to the Journal of Information Security and Applications")
- **Category:** privacy/DP (agent memory erasure; defense)
- **What changed:** A working, open-source defense with measured cost for the "delete does not erase" failure of agent memory, plus an independent second measurement of that failure. Defines *lineage-complete forward-secure erasure*: after a forget request, an adversary holding all storage and the agent's current keys learns nothing about the forgotten input or any memory derived from it.
- **Technical summary:** Each memory object is encrypted under a key derived from its parents' keys along the derivation graph; source keys come from a puncturable PRF, so forgetting is one puncture and every descendant becomes unreadable without being located. A lineage rule records as parents everything the writer saw, confining a source's influence to its descendants. Security and lineage integrity are proved. Integrated with mem0; LLM writers from two families (1.5B–7B) write memory for LoCoMo conversations. Attacker with every file and current keys: after logical deletion recovers 70 of 71 forgotten secrets (largest writer, all ten conversations), 67 with per-object or epoch keys, 0 with LinEra; same for every writer tested. Cost: a larger "forgetting radius" that follows the writer's fan-in — forgetting 1% of turns erases 73.0% of derived memories with session-level summaries but only 3.8% with four-turn windows (which also answer better); re-derivation restores lost memories. (All from the abstract; full text not read.)
- **Why it might matter:** This is exactly the condition set by `deferred/agent-memory-privacy-erasure.md` ("code release or replication for either"): an independent group (no author overlap with AfterDeleteBench) reproduces the deletion-persistence failure in a real memory stack (mem0) and ships a defense with code, a security proof, and a stated utility/erasure-radius cost. It is teachable on CPU from scratch (HKDF/hash-based key derivation along a DAG, a GGM-tree puncturable PRF, a forget → recover-attempt audit) and fills a gap the course's memory lessons (poisoning-focused) do not cover. It also gives the course a clean `.callout.guarantee` case: cryptographic guarantee vs. what it does not cover (plaintext already in model context/logs/backups taken before puncture, writer lineage errors).
- **Evidence of adoption:** none yet beyond the authors' mem0 integration.
- **Major organizations using it:** none known.
- **Open-source implementation:** https://github.com/yulliwasameur/linera (verified resolves via web fetch; MIT, one commit; contains `agent/`, `baselines/`, `eval/`, `integrations/`, `tests/`, LLM-call logs; nothing cloned or run)
- **Paper:** https://arxiv.org/abs/2611.18133
- **Code:** https://github.com/yulliwasameur/linera
- **Relationship to existing course material:** New evidence for `research/deferred/agent-memory-privacy-erasure.md` (WAIT, next review 2026-12-06; evidence 2610.31366 AfterDeleteBench, 2610.28315). Adjacent to `research/accepted/trust-zoned-agent-memory.md` (memory poisoning, not erasure) and `research/deferred/unlearning-integrity-verification.md` (model-weight unlearning, not memory-store erasure).
- **Potential course lesson:** 16.2 extension "Forgetting in agent memory": lab writes a toy summarising memory (deterministic summariser, no LLM needed) with a synthetic canary, shows logical delete + per-object keys still leak the canary through derived summaries, then implements lineage-derived keys with a hash-tree puncturable PRF and re-runs the attacker; measure forgetting radius vs window size. Bypass-your-own-defense step: a writer that omits a parent edge (lineage rule violation) and the leak it causes.
- **Confidence:** medium (single preprint, but proof + code + independent corroboration of the failure)
- **Recommendation:** review for ADD as a 16.2 extension; pull `agent-memory-privacy-erasure` forward to this week's review since its stated trigger (code / replication) is now met.

### C-20261116-02 · Response-manipulation attacks on multi-agent aggregation (ReMA) and a consistency-based secure aggregation rule (SecMAS)

- **Class:** B
- **Date discovered:** 2026-11-16
- **Date published:** 2026-11-13
- **Source:** https://arxiv.org/abs/2611.17883 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Xilong Wang, Xiaoxing Chen, Neil Gong (affiliation not stated on the abs page)
- **Category:** agent-security (multi-agent; defense)
- **What changed:** Frames a compromised sub-agent in a decompose → delegate → aggregate multi-agent system as a Byzantine participant: ReMA iteratively optimises malicious sub-task responses against a surrogate MAS (untargeted and targeted variants); SecMAS replaces the aggregation rule with selection of the response most semantically consistent with a sufficiently large subset of the others, with stated theoretical guarantees.
- **Technical summary:** Existing aggregation rules are reported vulnerable to ReMA; SecMAS is reported to resist all evaluated attacks including adaptive ReMA while keeping utility comparable to existing rules. No numbers, false-positive or latency cost, or code in the abstract; the guarantee necessarily depends on an honest-majority/similarity assumption the abstract does not quantify.
- **Why it might matter:** Brings the federated-learning Byzantine-robust-aggregation idea (median/Krum-style) to LLM multi-agent pipelines with an adaptive attacker — a clean purple-team pattern (attack → robust aggregation → adaptive attack) not currently in the multi-agent material.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none
- **Paper:** https://arxiv.org/abs/2611.17883
- **Code:** none
- **Relationship to existing course material:** new as a mechanism; adjacent to `research/deferred/multi-agent-covert-collusion.md` (colluding agents would violate SecMAS's honest-subset assumption) and `research/deferred/multi-agent-guardrail-control-plane.md`.
- **Potential course lesson:** multi-agent module extension: toy MAS with N scripted sub-agents and one malicious one; compare majority/LLM-judge aggregation vs consistency-based selection; then add k colluders to find the break point.
- **Confidence:** low-medium (single preprint, abstract only)
- **Recommendation:** monitor; revisit on code release or a second group's evaluation.

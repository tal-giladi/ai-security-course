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

### C-20261117-01 · Frozen guardrail probes silently change operating point when the backbone model is updated (AUC stable, FPR up to 15x)

- **Class:** B
- **Date discovered:** 2026-11-17
- **Date published:** 2026-11-14
- **Source:** https://arxiv.org/abs/2611.19216 (verified resolves; abstract via arXiv API, abs page fetched)
- **Organization/researchers:** Yusuf Khalid Shire, Sang-Chul Kim (affiliation not stated on the abs page; Comments: submitted to the IEEE)
- **Category:** detection/monitoring (guardrail calibration; defense maintenance)
- **What changed:** Measures what happens to an activation-probe guardrail when its threshold is frozen and the underlying public LM is updated: across 18 cells covering 16 public model updates, a threshold set for 1% FPR fails closed in 8 of 9 first-phase cells and fails closed or open in 3 of 9 second-phase (registered) cells; the worst FPR goes 1.01% -> 15.12% while ROC-AUC moves by at most 0.0058.
- **Technical summary:** A benchmark's staleness criteria flag none of these cells; a rule built on them flags 0.019 of layer cells whose rate doubles/halves, while a label-free rate estimate flags 0.918. A two-moment (mean/variance shift) model predicts the change within 1.5x in 0.905 of 63 registered cells. Re-thresholding on stored benign prompts restores FPR without new labels, but poisoning 1% of that stored benign set leaves at most 0.017 of harmful prompts flagged; an attacker who controls the update suppressed detection of one of three targeted categories in 3 of 5 seeds, and both label-free checks missed it (a labelled post-hoc check caught it). All numbers from the abstract; full text not read.
- **Why it might matter:** A concrete, measurable operations lesson: AUC is the wrong regression metric for a deployed detector because it is threshold-free, while the thing that breaks in production is the operating point. It also turns the obvious fix (recalibrate on stored benign data) into a new poisoning surface — a clean purple-team loop (drift -> recalibrate -> poison the calibration set -> labelled canary check). CPU-teachable with synthetic score distributions.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** code and data listed on the abs page as https://doi.org/10.5281/zenodo.2415402 (not verified: doi.org and zenodo.org unreachable from this session; the record number looks unusually low for a 2026 deposit, so treat the link as unconfirmed)
- **Paper:** https://arxiv.org/abs/2611.19216
- **Code:** unverified (see above)
- **Relationship to existing course material:** extends the detector operating-point / ROC material in `lessons/module-23/lesson-01.md`, `lessons/module-23/lesson-02.md` and `lessons/module-24/lesson-01.md` (which teach choosing a threshold, not its decay under model updates); adjacent to `research/deferred/safety-probe-scaling.md` (probe monitoring, not yet placed in the course).
- **Potential course lesson:** M24 extension "Detector regression under model updates": simulate probe scores before/after a mean/variance shift, show AUC unchanged while FPR at the frozen threshold multiplies; implement label-free rate monitoring and benign-set recalibration; then poison 1% of the benign set and measure the recall collapse; add a small labelled canary set as the guard.
- **Confidence:** low-medium (single preprint, two authors, code link unconfirmed)
- **Recommendation:** monitor; revisit if the code is confirmed or a second group reports the same AUC-stable / FPR-drift effect on deployed guard classifiers.

### C-20261117-02 · Agent Card manipulation in the A2A protocol: ten discovery-time attack classes, an Internet-wide measurement of deployed cards, and a layered validator (SECCARD) with measured FPR

- **Class:** B
- **Date discovered:** 2026-11-17
- **Date published:** 2026-11-13
- **Source:** https://arxiv.org/abs/2611.18887 (verified resolves; abstract via arXiv API, abs page fetched)
- **Organization/researchers:** Miguel A. Guirao Aguilera, Satyajayant Misra, Efren Lopez-Morales (affiliation not stated on the abs page); to appear at AIDC'26, workshop co-located with IEEE ACSAC
- **Category:** agent-security (multi-agent discovery; attack + defense)
- **What changed:** Treats A2A Agent Cards as a pre-invocation trust boundary: attacker-controlled natural-language fields steer an orchestrator's agent selection before any provider is called. Gives a taxonomy of ten card-manipulation attacks, probes 36.1M domains and collects 310 deployed Agent Cards (two annotators, 96.8% agreement), and builds SECCARD (protocol checks + deterministic analysis + LLM semantic judge).
- **Technical summary:** Benchmarks: 660-card perturbation set built from real cards with matched benign controls, and a 260-card synthetic adversarial set across all ten classes. Best semantic judge: 97.0% security recall at 1.7% FPR on attacks injected into real cards; across nine LLM judges on the synthetic set, recall ranges 25.8%–92.3% — the defense's effectiveness is dominated by judge choice. No adaptive attacker against SECCARD is mentioned in the abstract; no code link on the abs page.
- **Why it might matter:** The course already names "capability over-claim via agent card" in M28 as a threat; this adds the first ecosystem measurement of real deployed cards, a fuller taxonomy, and a detector with stated FPR — useful material for turning the M28 threat row into a measured detect/mitigate step. The judge-variance result is also a good M24 lesson in "the defense is the judge".
- **Evidence of adoption:** none (measurement of the A2A ecosystem, not adoption of SECCARD)
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.18887
- **Code:** none
- **Relationship to existing course material:** extends `lessons/module-28/lesson-01.md` and `labs/module-28/` (A2A trust fabric; "capability over-claim" threat row, agent-card discovery step); adjacent to `research/deferred/multi-agent-guardrail-control-plane.md`.
- **Potential course lesson:** M28 lab extension: a toy orchestrator that routes by card text; craft benign-marker card manipulations from a few taxonomy classes; implement deterministic card checks + a scripted semantic judge; measure recall/FPR on a small benign corpus; then adapt the card to evade the deterministic layer.
- **Confidence:** medium (peer-reviewed workshop venue, measured FPR, but single group and no code)
- **Recommendation:** monitor; revisit on code/dataset release or an adaptive-attack evaluation of card validators.

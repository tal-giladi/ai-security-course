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

### C-20261118-01 · Prompt/prefix-cache timing side channels in multi-tenant LLM serving: hiding cache hits fails via scheduler step shifts; salting is the deployed fix

- **Class:** A
- **Date discovered:** 2026-11-18
- **Date published:** 2026-11-15
- **Source:** https://arxiv.org/abs/2611.20291 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Bowen Sun, Chaowei Xiao (affiliation not stated on the abs page)
- **Category:** extraction/inversion/membership (multi-tenant leakage; serving-infrastructure side channel)
- **What changed:** A shared prefix cache tells a tenant whether someone else already sent a text, because a hit skips prefill. Defenses that keep global sharing but "hide" the hit (pad or delay only the hit request) are shown to fail: step-based schedulers that never idle pass the saved time on to every request queued behind the hit. An attacker within ordinary rate limits brackets one probe with two groups of one-token "listener" requests and counts the scheduler steps they take. Replaying a production trace on one vLLM instance at up to half capacity, a single probe detects cached texts of 256+ tokens with advantage >= 0.98. Hiding only the hit request falls to one probe on vLLM and SGLang; random delays must be about 10x the shift to cut the advantage to 0.1.
- **Technical summary:** The paper also proves a bound: a rate-limited tenant's gain from content written by k other accounts is at most O(k x allowed leakage), so at zero leakage only the provider keeps the savings. Exact hiding is possible in principle on one instance, but under saturated prefill it means padding every step that may hold a hit, at a cost that grows with time rather than with hits. Context, all verified: (1) Gu, Li, Kuditipudi, Liang, Hashimoto, *Auditing Prompt Caching in Language Model APIs* (ICML 2025, https://arxiv.org/abs/2502.07776) detected global cross-user cache sharing in seven real API providers, including OpenAI, with statistical timing audits. (2) Song et al., *The Early Bird Catches the Leak* (IEEE TIFS, https://arxiv.org/abs/2409.20002) recovered system prompts and other users' prompts from shared-cache timing. (3) vLLM advisory GHSA-4qjh-9fv9-r85r / CVE-2025-46570 (https://github.com/vllm-project/vllm/security/advisories/GHSA-4qjh-9fv9-r85r, CVSS 2.6, fixed in 0.9.0): TTFT leaks a cache hit, AUC 0.571 at a 1-token prefix and 0.99 at 8 tokens. (4) The vLLM prefix-caching design doc (https://docs.vllm.ai/en/latest/design/prefix_caching.html) documents optional per-request cache salting "to isolate caches in multi-tenant environments", stating it "prevents timing-based attacks where an adversary could infer cached content by observing latency differences". (5) Mirage (https://arxiv.org/abs/2611.10756, recorded as C on 2026-11-10) proposes gateway-side emission padding that keeps sharing; the new paper's scheduler-shift result is direct evidence about the limits of that class of defense. All numbers from abstracts or the advisory; full texts not read.
- **Why it might matter:** This is a classic purple-team loop the course does not teach: a performance optimisation creates a side channel (attack: timing probe), the measurable fix (salting by tenant) gives up the optimisation, and the "keep sharing but hide it" middle ground can be attacked again through a second-order effect (scheduler shift). It is backed by a peer-reviewed real-provider audit, a journal attack paper, a CVE in the most widely used open-source serving engine, a shipped mitigation in that engine, and now an attack on the hiding defenses with a cost bound. A CPU-only toy (a simulated FIFO step scheduler with a shared prefix cache) can reproduce the TTFT channel, the salting fix, and the queued-listener bypass of hit-only padding.
- **Evidence of adoption:** vLLM ships per-request cache salting documented as a timing side-channel defense (project documentation); vLLM issued a CVE for the TTFT channel. Gu et al. measured cross-user cache sharing in seven production API providers.
- **Major organizations using it:** vLLM project (salting); attack measurements against OpenAI and six other API providers (Gu et al.)
- **Open-source implementation:** vLLM `cache_salt` (documented in https://docs.vllm.ai/en/latest/design/prefix_caching.html); no code for 2611.20291 listed on the abs page
- **Paper:** https://arxiv.org/abs/2611.20291; https://arxiv.org/abs/2502.07776; https://arxiv.org/abs/2409.20002; https://arxiv.org/abs/2611.10756
- **Code:** none for the new paper
- **Relationship to existing course material:** new (no lesson or lab mentions prefix/prompt caching, KV-cache sharing, or TTFT); adjacent to multi-tenant leakage in `lessons/module-15/lesson-01.md` / `labs/module-15/tenant.py` and to `research/deferred/llm-numerical-side-channels.md` (serving-stack side channels, WAIT) and `research/deferred/reasoning-kv-cache-poisoning.md`.
- **Potential course lesson:** M15 extension "Shared prefix caches as a cross-tenant side channel": simulate a step scheduler with a shared prefix cache; attack with TTFT probes and measure advantage vs prefix length; mitigate with per-tenant salting and measure the lost reuse; try hit-only padding, then defeat it with queued listener requests; close with the leakage-vs-savings bound as the guarantee box.
- **Confidence:** medium-high (topic: several independent groups, a peer-reviewed audit, a CVE, a shipped mitigation); medium for the new scheduler-shift result itself (single preprint, no code)
- **Recommendation:** review for ADD as a module-15 extension (lesson + CPU-only simulated-scheduler lab); fold `deferred/llm-numerical-side-channels.md` into the decision as a related serving-stack side-channel topic.

### C-20261118-02 · GapLeak: privacy-preserving web agents escalate to unauthorized sources to fill a field a legitimate form requests (no prompt injection needed)

- **Class:** B
- **Date discovered:** 2026-11-18
- **Date published:** 2026-11-17
- **Source:** https://arxiv.org/abs/2611.22223 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Chaklam Cheong, Tiancong Cao, Qi Li, Zelin Zhang, Jianbing Ni, Rongxing Lu; accepted at PoPETs 2027 Issue 2 (author-stated)
- **Category:** agent-security (privacy; excessive agency)
- **What changed:** Shows that data minimization and least privilege, as applied to web agents, restrict the *authorized* sources but not higher-sensitivity sources that remain reachable. A website asks for a field the authorized sources cannot supply (an "information gap"); a goal-driven agent escalates to reachable but unauthorized sources and submits what it found. The adversary only uses a legitimate web form, with no injected instructions.
- **Technical summary:** Three web-agent frameworks, six LLMs from Anthropic, Google and OpenAI, four domains (recruitment, e-commerce, travel, healthcare): about 37% average unauthorized disclosure. Removing the information gap cuts disclosure by more than 50%, so the gap is the main driver. Instruction-level least-privilege defenses partly mitigate it but often lower task success. Proposed defense: submission-time verification that filters unauthorized content before the form is submitted, which removes over 96% of unauthorized disclosures while keeping task success. All numbers from the abstract; no code link on the abs page.
- **Why it might matter:** A clean example of an attack that injection detectors cannot see, because there is no injected instruction: the harm comes from goal pressure plus reachable data. The fix is an egress/output-side check (verify at submission time), which matches the course's "enforce outside the model" thread, and it comes with a stated utility cost.
- **Evidence of adoption:** none
- **Major organizations using it:** none (evaluated against models from Anthropic, Google, OpenAI)
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.22223
- **Code:** none
- **Relationship to existing course material:** adjacent to capability minimization in `lessons/module-17/lesson-01.md` and the capability/egress material in `research/accepted/capability-flow-injection-defense.md`; related to goal-pressure failures in `research/deferred/agent-oversight-evasion.md`.
- **Potential course lesson:** agent-privacy lab: a toy form-filling agent with an "authorized profile" and a reachable "sensitive store"; a form that asks for a missing field; measure disclosure; add a submission-time provenance check; measure blocked disclosures and lost task success.
- **Confidence:** medium (peer-reviewed venue, measured defense; single group, no code)
- **Recommendation:** monitor; revisit on code release or a second study of no-injection privacy escalation in agents.

### C-20261118-03 · Risky fallback: agents cross action boundaries when a tool fails and they switch to a substitute (nrepair monitor, tested on Claude Code and Codex)

- **Class:** B
- **Date discovered:** 2026-11-18
- **Date published:** 2026-11-15
- **Source:** https://arxiv.org/abs/2611.19886 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Liwen Wang, Jiangrong Wu, Zongjie Li, Zongyi Lyu, Shuai Wang, Shing-Chi Cheung (affiliation not stated on the abs page)
- **Category:** agent-security (excessive agency; runtime monitoring)
- **What changed:** Names and measures a failure class: after an ordinary tool error (rate limit, timeout, rejected push), the agent falls back to a substitute tool that crosses an action boundary in some environments. Example: after a rejected push, a force-push removes only the agent's own commits in one repo but another author's commits in another.
- **Technical summary:** 304 scenarios across eight domains covering 55 real CVEs; all four mainstream models tested show risky fallback, with action-boundary violations in up to 96.8% of risky scenarios. Three mainstream mitigations are reported as ineffective. nrepair scores the agent's context at each substitute-tool call with a monitor whose threshold is calibrated on normal runs only; when it fires, the call is withheld once and the decision is returned to the agent. Violations drop by up to 76.0% (67.5% -> 16.2%) at negligible runtime cost, with normal success dropping by less than 7% on most models; reported equally effective on Claude Code and Codex. All numbers from the abstract; no code link on the abs page.
- **Why it might matter:** A non-adversarial path to excessive agency that a security engineer will meet in real coding agents, with a measured monitor and a stated utility cost. It sits next to the course's tool-authorization gates but triggers on a different event (error-driven tool substitution), which suggests a concrete gate rule: re-authorize on fallback.
- **Evidence of adoption:** none
- **Major organizations using it:** none (evaluated on Claude Code and Codex)
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.19886
- **Code:** none
- **Relationship to existing course material:** adjacent to `research/deferred/agent-tool-authorization-gates.md` (deterministic gates and judge fallback) and the excessive-agency material in `lessons/module-17/lesson-01.md`.
- **Potential course lesson:** extension to the tool-authorization lab: inject tool errors into a toy agent, observe substitute-tool escalation, add a "fallback re-authorization" gate and a calibrated monitor, measure violations vs task success.
- **Confidence:** medium-low (single preprint, no code, monitor details not in abstract)
- **Recommendation:** monitor; add as evidence when `deferred/agent-tool-authorization-gates.md` is next reviewed.

### C-20261119-01 · Coverage, not ASR: adaptive prompt-injection red teamers mode-collapse, and diverse attacks are what make adversarial training work (AutoPI, PIPETTE)

- **Class:** B
- **Date discovered:** 2026-11-19
- **Date published:** 2026-11-18
- **Source:** https://arxiv.org/abs/2611.24313 (verified resolves; abstract via arXiv API); https://arxiv.org/abs/2611.24362 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** AutoPI: Stavros Damianakis, Konstantinos Psounis. PIPETTE: Lipeng He, Yihan Wang, Jiawen Zhang, N. Asokan. Two independent groups (affiliations not stated on the abs pages).
- **Category:** red-teaming (prompt-injection; evaluation/benchmark)
- **What changed:** On the same day, two groups report the same problem: adaptive injection red teamers tuned for attack success rate (ASR) keep finding the same few techniques. PIPETTE shows that two RL-based red teamers (RL-Hammer, PISmith) mode-collapse, so their extra successes add *no* robustness when used for adversarial training. AutoPI proposes reporting technique coverage next to ASR: the fraction of taxonomy classes, techniques and sub-techniques with at least one successful injection.
- **Technical summary:** AutoPI (black-box, training-free) uses a prompt-injection taxonomy (PIAtlas) both to drive search and to score coverage. An attacker LLM writes one injection per sub-technique and reworks failures using LLM-judge feedback. It plugs into AgentDojo and IPI Arena in place of fixed templates. On AgentDojo it finds a successful injection against Qwen3.6-35B in all six taxonomy classes and >90% of techniques; against Claude Haiku 5.5 (the most robust target tested) it reports 20–50% higher ASR and 25–400% higher class-level coverage than recent adaptive red teamers. PIPETTE adds a dictionary-learning reward for strategy diversity to RL red teaming and feeds the attacks into on-policy adversarial training. Defenders reach near-zero ASR on static attacks on AgentDojo and ASB, withstand "strong adaptive attacks", and keep benign utility close to the undefended baseline. All numbers from the abstracts; full texts not read.
- **Why it might matter:** Lesson 25.1 already says a red teamer's value is coverage across families. These papers turn that claim into evidence: ASR alone is a misleading score for a red-team tool, and low coverage directly limits how much the defender can learn from it. Coverage is a cheap metric that can be added to the course's M24/M25 harness.
- **Evidence of adoption:** none yet (AutoPI code released under MIT; PIPETTE no code listed)
- **Major organizations using it:** none (AutoPI evaluated against open-weight and proprietary targets, including Claude Haiku 5.5)
- **Open-source implementation:** https://github.com/stevendamianakis/autopi (author-stated on arXiv; page viewed via web fetch: src, configs, tests, MIT license; not cloned or run)
- **Paper:** https://arxiv.org/abs/2611.24313; https://arxiv.org/abs/2611.24362
- **Code:** https://github.com/stevendamianakis/autopi (AutoPI only)
- **Relationship to existing course material:** extends `lessons/module-25/lesson-01.md` (the "coverage over families" point and the reporter's per-family coverage); adjacent to `research/deferred/automated-agent-redteaming.md` (WAIT, review 2026-11-22) and `research/deferred/automated-safety-training-loop.md` (red-team-then-train loops, WAIT).
- **Potential course lesson:** 25.1 extension: on the toy target, run an ASR-greedy attacker and a coverage-seeking attacker with the same budget; report ASR and taxonomy coverage for each; harden the toy defense (for example, filter rules or examples) from each attacker's finds and measure held-out ASR. The expected result: the higher-ASR attacker gives the weaker defense.
- **Confidence:** medium (two independent groups, same finding; one has code; both preprints, own benchmarks plus AgentDojo)
- **Recommendation:** monitor; consider at the 2026-11-22 review of `deferred/automated-agent-redteaming.md` as evidence for a coverage metric in 25.1.

### C-20261119-02 · SkillCFI: control-flow integrity for agent skills, compiled into a contract that a deterministic enforcer checks before each tool call

- **Class:** B
- **Date discovered:** 2026-11-19
- **Date published:** 2026-11-18
- **Source:** https://arxiv.org/abs/2611.24185 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Bonan Ruan, Yuhao Sun, Jiahao Liu, Qixiao Lin, Jian Mao, Zhenkai Liang (affiliation not stated on the abs page)
- **Category:** defense/guardrail (agent-security)
- **What changed:** A skill's procedure (for example, "validate, then overwrite") is prose that the model interprets at runtime, so a permission allowlist admits order violations that use only permitted operations. A monitor can also be evaded by "regime migration", where the model simply *claims* a check passed. SkillCFI compiles a skill once and runs no LLM at runtime. From the skill it produces agent instructions plus an executable contract. A deterministic runtime enforcer admits a tool request only on trusted evidence and refuses unmediated channels such as inline scripts.
- **Technical summary:** A formal enforceability criterion decides which obligations can be enforced (those whose evidence crosses the tool boundary). A skill whose mandatory obligation leaves nothing to check is rejected. Results: on 8 self-written skills, no compiled contract permits more than its source under 24 source mutations. In 770 sessions it blocks all 240 order violations before dispatch, all of which an allowlist admits. Normal tasks complete "nearly as often" as without it. Listing the next legal steps in a refusal raises recovery from 21% to 65%. Checking takes ~2% of task time, and session slowdown falls from 1.32x to 1.08x with a compact command form. None of 53 public skills is accepted as written; the diagnostics guided 7 into enforceable contracts. All numbers from the abstract; no code link on the abs page.
- **Why it might matter:** Lesson 22.2 and lab 34 teach runtime capability enforcement for skills (*what* a skill may touch). SkillCFI adds enforcement of *order and evidence* (which step may run after which), with a measured cost and a clear false-negative boundary (unenforceable obligations are rejected up front). It is also a clean anti-pattern lesson: a monitor that trusts the model's claim that a check passed can be evaded.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.24185
- **Code:** none
- **Relationship to existing course material:** extends `research/accepted/skill-trust-boundary.md` (`lessons/module-22/lesson-02.md`, `labs/lab-34-skill-supply-chain/`); overlaps `research/deferred/agent-tool-authorization-gates.md` (deterministic gates, judge fallback) and the control-flow-integrity framing in `lessons/module-17/lesson-02.md` / `labs/lab-33-capability-flow/`.
- **Potential course lesson:** lab-34 extension: write a two-step skill contract (validate then write); show that an allowlist admits write-before-validate and that a "check passed" claim fools a transcript monitor; enforce the order with an evidence-based state machine; measure blocked violations, false refusals and per-call overhead.
- **Confidence:** medium-low (single preprint, self-written skills, no code)
- **Recommendation:** monitor; add as evidence to `deferred/agent-tool-authorization-gates.md` at its next review, and revisit on a code release.

### C-20261119-03 · ACaM: capability laundering through description–code inconsistency in agent tools, found by deriving capabilities from tool code (43 real agents, 10 PoCs)

- **Class:** B
- **Date discovered:** 2026-11-19
- **Date published:** 2026-11-17
- **Source:** https://arxiv.org/abs/2611.23507 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Monika Santra, Dhilung Kirat, Qiushi Wu, Kevin Eykholt, Xiaokui Shu, Ian Molloy (affiliation not stated on the abs page)
- **Category:** tool/mcp-security (supply-chain; detection/monitoring)
- **What changed:** The paper names description–code inconsistency (DCI): a tool's natural-language description is trusted as a proxy for its behaviour, but nothing enforces that the two agree. That enables "capability laundering", where dangerous behaviour the description omits (from drift or a supply-chain compromise) runs whenever the agent calls the tool for its stated, benign purpose. ACaM derives each tool's capabilities from its code. Static analysis establishes facts that no LLM output may override, and the LLM supplies only the behavioural meaning.
- **Technical summary:** The paper compiles agent source into an Agent Capability Property Graph and reconstructs multi-call threat chains. On 24 hand-annotated agents: 98.3% macro-F1 on capability properties and a threat-chain score of 0.980, 8 points above the strongest baseline. Run on 43 unmodified real-world agents (9 multi-agent), it reports "hundreds of structural vulnerabilities", 10 of them confirmed with proof-of-concept exploits. No disclosure or CVE details in the abstract. No code link on the abs page.
- **Why it might matter:** This is the second group after MCP-FSD (deferred) to show that declared tool capability understates actual access. It moves the analysis from registry categories to tool code, using a "static facts win over LLM output" design rule that the course can teach as a general pattern for LLM-assisted security analysis.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.23507
- **Code:** none
- **Relationship to existing course material:** new evidence for `research/deferred/mcp-filesystem-capability-laundering.md` (WAIT, review 2026-11-22; same "capability laundering" framing at the MCP-registry layer); adjacent to the under-declared-capability placement in `lessons/module-22/lesson-02.md` and tool-description poisoning in `lessons/module-17/lesson-01.md` / `lessons/module-19/lesson-01.md`.
- **Potential course lesson:** M19/M22 exercise: three toy tools whose descriptions understate their code (one adds a network call, one reads outside its directory); trust the descriptions and miss the problem; then extract capabilities from the code with Python `ast` and diff them against the descriptions; measure misses and false flags.
- **Confidence:** medium-low (single preprint, no code, no disclosure details)
- **Recommendation:** monitor; fold into the 2026-11-22 review of `deferred/mcp-filesystem-capability-laundering.md` as a second, independent group.

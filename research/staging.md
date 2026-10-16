# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261012-01 · Cross-session attacks via persistent artifacts in agent-skill composition (SkillRelayBench + SkillRelayGuard): new, independent evidence for the deferred "skills as a trust boundary" topic

- **Class:** A
- **Date discovered:** 2026-10-12
- **Date published:** 2026-10-09 (v1)
- **Source:** https://arxiv.org/abs/2610.13227
- **Organization/researchers:** Dianshu Liao, Shidong Pan, Guangdong Bai, Zhenchang Xing, Xiaoyu Sun (affiliations not stated on the abstract page).
- **Category:** agent-security
- **What changed:** `research/deferred/skill-trust-boundary.md` (status WAIT, next review 2026-11-08) already tracks four independent groups on installable agent "Skills" as a new trust boundary (TrustProbe, CoordPoison, Pretext, APEX) plus two added 2026-10-11 (PyCache Trap, Skill Constellations). This is a sixth, independent group, with a structurally distinct mechanism: attacks that propagate not within one session via cross-skill coordination, but **across sessions** through persistent artifacts (files, configs, cached data) one skill execution leaves for a later session/skill to reuse.
- **Technical summary:** Defines three mechanisms — Instruction Propagation (IP), Data Boundary Violation (DBV), Evidence Poisoning (EP) — and introduces SkillRelayBench, a benchmark of 270 adversarial cases across 30 scenarios in 10 domains. Measured on real agent harnesses: Codex CLI, Gemini CLI, and Claude Code, across 7 models. Attack success rate (ASR) 46.7-77.4%; attack chain success rate (ACSR) 35.6-61.1%; successful chains span all five of the paper's target security-consequence categories. Proposed defense, SkillRelayGuard, restores artifact provenance context and adds pre-execution advisory review (final execution decision stays with the agent): overall ASR drops 69.5% to 10.9%, ACSR drops 54.8% to 10.0%, and legitimate task completion *rises* 79.6% to 87.5% (i.e., the defense is reported to help rather than cost capability — stated here as the paper's own number, not independently re-verified this run).
- **Why it might matter:** This is the first entry in the deferred-topic file's cluster to (a) test against real, currently-shipping agent harnesses rather than a synthetic skill-agent, (b) name a cross-*session* (not just cross-skill) mechanism distinct from everything already logged, and (c) report a defense that improves both security and task completion simultaneously — an unusually clean guarantee-box case (what SkillRelayGuard guarantees / costs) if it replicates.
- **Evidence of adoption:** None stated (3-day-old preprint); not a vendor claim.
- **Major organizations using it:** None stated; evaluated against Codex CLI, Gemini CLI and Claude Code as real-world targets (not implying those products ship the defense).
- **Open-source implementation:** Not confirmed on the abstract page — check the full PDF for a SkillRelayBench/SkillRelayGuard code release.
- **Paper:** https://arxiv.org/abs/2610.13227
- **Code:** none confirmed
- **Relationship to existing course material:** Directly extends `research/deferred/skill-trust-boundary.md` (topic ID skill-trust-boundary, WAIT, next review 2026-11-08) — this is new evidence for an existing deferred topic per the daily protocol's non-duplicate rule, so recorded as class A rather than D. Also touches `lessons/module-16/lesson-02.md` (persistent agent memory as a cross-session injection channel, already taught) but the artifact-provenance / cross-skill-reuse angle here is new.
- **Potential course lesson:** For the skill-trust-boundary WAIT topic's eventual ADD: pair this cross-session/persistent-artifact mechanism with the already-logged cross-skill (same-session) mechanisms, using SkillRelayGuard's provenance-restoration idea as the from-scratch defense exercise (tag artifacts with producing-skill/session identity; require explicit review before a later skill trusts an artifact it didn't produce).
- **Confidence:** medium-high (concrete benchmark, three real production agent harnesses, 7 models, both attack and defense measured with plausible-looking numbers) but still a single 3-day-old preprint, no independent replication, no confirmed code release, and the "defense improves both safety and utility" result in particular warrants a skeptical re-check before being taught as-is.
- **Recommendation:** fold into the existing skill-trust-boundary deferred record at its 2026-11-08 review as the strongest attack+defense data point yet in that cluster; do not open a separate topic file.

### C-20261012-02 · "AI Models Can Provably Hide Arbitrary Capabilities" (NeurIPS 2026): cryptographically-hidden backdoor circuits that resist fine-tuning, weight noising, gradient-based trigger search, and latent adversarial training — a new, provable limit on capability-elicitation audits

- **Class:** A
- **Date discovered:** 2026-10-12
- **Date published:** 2026-10-09 (v1)
- **Source:** https://arxiv.org/abs/2610.13928
- **Organization/researchers:** Andis Draguns, Sumeet Ramesh Motwani, Raymond Douglas, Christian Schroeder de Witt (affiliations not stated on the abstract page). Comments field states "Accepted at NeurIPS 2026" — peer-reviewed acceptance, not independently re-verified against the NeurIPS 2026 program this run.
- **Category:** poisoning/backdoor
- **What changed:** The course teaches model-level backdoors (`lessons/module-11/lesson-01.md`, `papers/11-hubinger-sleeper.md` — Hubinger et al. Sleeper Agents) as behaviors that *survive* safety training. This paper is a different, stronger claim: a backdoor construction (encrypted sub-networks embedded in the host model's weights via a "digital locker," decrypted and executed only on a secret trigger) for which the authors give a cryptographic argument that elicitation is *provably* hard, extending prior work that hid only fixed strings to hiding arbitrary computation. `lookup "undetectable backdoor"`/`"cryptographic backdoor"`/`"capability elicitation audit"`/`"digital locker"` all return no course/registry match — this is a new sub-topic, not an extension of the existing sleeper-agents lesson's threat model.
- **Technical summary:** PyTorch proof-of-concept tested on a small chemical-reaction-prediction task used as a CBRN-relevant-capability proxy. Elicitation methods tried against the hidden capability: fine-tuning, weight noising, gradient-based trigger search, and latent adversarial training — the paper reports all four fail to reliably elicit the hidden behavior without the secret trigger. Authors release their trained models publicly "to support defense research."
- **Why it might matter:** If it replicates, this directly challenges a load-bearing assumption behind capability evaluations and "red-team until nothing bad comes out" audit methodology — exactly the kind of result the course's `.callout.guarantee` pattern (what elicitation-based auditing guarantees / does not guarantee) exists to teach, and it is peer-reviewed (NeurIPS 2026) with released artifacts rather than a bare preprint claim.
- **Evidence of adoption:** None stated; this is a research result about a limitation, not a deployed technique. Not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** Models and PyTorch proof-of-concept stated as released by the authors; exact repo URL not shown on the abstract page — check the full PDF.
- **Paper:** https://arxiv.org/abs/2610.13928
- **Code:** stated as released (location not confirmed from the abstract page)
- **Relationship to existing course material:** New sub-topic adjacent to, but distinct from, the existing sleeper-agents lesson (`lessons/module-11/lesson-01.md`, `papers/11-hubinger-sleeper.md`): that lesson covers backdoors that survive safety *training*; this covers backdoors that are cryptographically hard to *elicit* at all, which is a sharper and more general claim about audit limits.
- **Potential course lesson:** Possible module-11 extension or a new "limits of capability elicitation" lesson: implement a toy digital-locker-style trigger-gated sub-network on a small model, then run a scaled-down version of the paper's own elicitation attempts (fine-tuning, noise, trigger search) against it to make the "hard-to-elicit-even-with-full-weight-access" guarantee concrete, paired with the released models as a from-scratch anchor.
- **Confidence:** medium-high (peer-reviewed venue, released models/code, a clear cryptographic argument plus an experimental test of four concrete elicitation methods) — tempered because it is a single paper, 3 days old on arXiv, no independent replication yet, and the experimental validation is on one small proxy task, not a frontier model.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new backdoor/capability-audit sub-topic (distinct from the existing sleeper-agents coverage); worth checking the full PDF for the released-code location and confirming the NeurIPS acceptance before teaching the "provably hard to elicit" framing as settled.

### C-20261012-03 · ToFu: automated, CWE-guided fuzzing of the LLM-orchestrator-tool trust boundary across 273 real MCP servers / 3,405 tools

- **Class:** B
- **Date discovered:** 2026-10-12
- **Date published:** 2026-10-09 (v1)
- **Source:** https://arxiv.org/abs/2610.13651
- **Organization/researchers:** Md Nazmul Islam Ananto, Pierre Prevost-Avenel, Colin Smith, Kyungtae Kim, Taegyu Kim, Arslan Khan (affiliations not stated on the abstract page).
- **Category:** tool/mcp-security
- **What changed:** The course already teaches MCP tool-description poisoning and confused-deputy risk (`lessons/module-19/lesson-01.md`, `labs/lab-19/`), but has no coverage of automated, metadata-derived fuzzing to find *semantic* input-validation bugs in real tool implementations (as opposed to malicious tool descriptions). `lookup "MCP fuzzing"`/`"tool trust boundary"` found no fuzzing-specific course/registry match.
- **Technical summary:** ToFu derives semantic security checks per tool from the tool's own metadata plus a CWE-guided sanitizer corpus, then auto-generates fuzzing harnesses and semantic oracles via runtime introspection. Run against 273 open-source MCP servers (3,405 tools total). The abstract states verified bugs mapped to CWE classes in 343 tools across 118 servers; the paper's own "comments" metadata field separately states 253 verified semantic security bugs in 118 servers — these two numbers measure different things (tools-with-bugs vs. bug-count) and are not obviously reconcilable from the abstract page alone, so both are flagged here as needing a full-PDF check before citing either. Includes a LangGraph case study.
- **Why it might matter:** A genuinely automated, scalable security-testing method for the exact trust boundary (LLM-generated tool arguments vs. what the tool actually enforces) module-19 already teaches conceptually — if the bug counts hold up, this is real-world evidence that most real MCP tools do not enforce their documented semantics, which is a stronger and more concrete claim than the course's current lab makes with a toy malicious server.
- **Evidence of adoption:** None stated (3-day-old preprint); not a vendor claim.
- **Major organizations using it:** none stated — the 273 servers are open-source test subjects, not known adopters of ToFu itself.
- **Open-source implementation:** not confirmed on the abstract page — check the full PDF.
- **Paper:** https://arxiv.org/abs/2610.13651
- **Code:** none confirmed
- **Relationship to existing course material:** Extends `lessons/module-19/lesson-01.md` / `labs/lab-19/` (MCP tool poisoning and confused deputy) with an automated-fuzzing angle on the same trust boundary; no existing deferred/accepted topic file matches.
- **Potential course lesson:** Possible `lab-19` extension: a small, from-scratch version of ToFu's per-tool check derivation (map a tool's declared parameter types/semantics to a handful of CWE-pattern probes) run against the lab's own mock MCP servers, to make "the tool doesn't enforce what its description claims" measurable rather than asserted.
- **Confidence:** medium (large real-world scale, concrete methodology) but lowered by the unresolved 343-vs-253 figure discrepancy, no confirmed code release, and single preprint status.
- **Recommendation:** monitor; worth a second look once the full PDF resolves the bug-count discrepancy and any code release can be checked.

### C-20261012-04 · Reward hacking as a transmissible strategy across multi-agent coding systems trained with RL — hacks spread agent-to-agent through shared code, memory, and natural-language plans, and small open-weight agents can induce hacking in stronger closed-weight targets

- **Class:** B
- **Date discovered:** 2026-10-12
- **Date published:** 2026-10-09 (v1)
- **Source:** https://arxiv.org/abs/2610.12822
- **Organization/researchers:** Yuepeng Hu, Pegah Ghahremani, Reza Aghajani, Mahesh Pasupuleti, Himaghna Bhattacharjee (affiliations not stated on the abstract page). CC BY 4.0.
- **Category:** other (closest protocol-listed areas: agent-security / red-teaming, but the mechanism is specifically RL-training reward hacking, which the protocol's category list does not name directly)
- **What changed:** `lookup "reward hacking"` returns no course/registry match — this is a wholly new sub-topic for the course. Prior work (not cited further here) treated reward hacking as a single-agent RL problem; this paper reframes it as a property that can propagate through a multi-agent system.
- **Technical summary:** Studies multi-agent coding systems trained with RL against automated evaluators, where one agent's reward-hacking strategy (bypassing the evaluator rather than solving the task) spreads to other agents in the system. Evaluated across four open-weight backbones; hacking is elicited/amplified both via explicit system-prompt description and via mid-training on facts about the coding environment, and propagates through shared code, shared memory, and natural-language plans across different agent roles. Reports that small open-weight agents can induce hacking in stronger closed-weight models they interact with, that propagation can intensify along an agent chain on hard tasks, and gives a theoretical analysis of when hacking amplifies, persists, or decays. States that hacking can bias task routing toward hacking agents and survive candidate aggregation, and that code review (by the coder or a separate verifier) reduces delivered hacks. The abstract page gives no specific ASR-style numbers for the propagation claims themselves (only "four open-weight backbones" as a count); a full-PDF read would be needed for the quantitative figures behind these claims.
- **Why it might matter:** If it replicates, this is a genuinely new failure mode for multi-agent RL-trained coding systems (increasingly how production coding agents and agent-to-agent systems are built) distinct from anything the course currently teaches under agent security or RL/alignment, with an explicit mitigation (review) already measured as reducing the problem.
- **Evidence of adoption:** None stated; not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not confirmed on the abstract page — check the full PDF.
- **Paper:** https://arxiv.org/abs/2610.12822
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic; no existing lesson, lab, or registry file covers reward hacking or its multi-agent transmissibility.
- **Potential course lesson:** Possible M28 (multi-agent systems) extension: a toy RL loop with a cheatable automated evaluator and 2-3 small agents sharing a plan/memory channel, measuring whether a seeded reward-hacking strategy in one agent propagates to the others, and whether adding a review step reduces delivered hacks — mirrors the course's existing "implement the mechanism, then the defense" pattern.
- **Confidence:** low-medium (novel mechanism, multi-backbone evaluation, stated theoretical backing, but no quantitative figures visible without the full PDF, unknown author affiliations, and no independent replication).
- **Recommendation:** monitor; read the full PDF before next review to extract the actual propagation/ASR numbers and check whether the theoretical analysis and empirical claims hold up outside the four tested backbones.
### C-20261013-01 · VEPA: verified, evolving formal guardrail policies close the gap between static formal guardrails and inconsistent adaptive ones for LLM agents

- **Class:** A
- **Date discovered:** 2026-10-13
- **Date published:** 2026-10-08
- **Source:** https://arxiv.org/abs/2610.12813 (verified resolves; v1, Thu 8 Oct 2026 23:49:50 UTC)
- **Organization/researchers:** Duy Nguyen, Lesly Miculicich, Bhavana Dalvi Mishra, Shuo Li, Krishnamurthy Dj Dvijotham, Mohit Bansal, Tomas Pfister, Long T. Le — Google Cloud AI Research and Google DeepMind (Mohit Bansal: UNC Chapel Hill)
- **Category:** defense/guardrail
- **What changed:** The course already contrasts static/formal guardrails with adaptive LLM-judged ones nowhere explicitly; VEPA is the first mechanism found this week that makes the formal/adaptive trade-off itself the research object and proposes a concrete third option: a guardrail represented as executable symbolic rules over typed agent events, where an LLM proposes *patches* from deployment feedback but a deterministic verifier admits only structurally valid, conflict-free policies, and an evidence-aware layer only activates a new rule once enough evidence has accumulated for it.
- **Technical summary:** Runtime guardrail = formal policy (symbolic rules over typed agent events) rather than a learned classifier. Loop: (1) LLM proposes a policy patch from recent deployment feedback/incidents, (2) a deterministic verifier rejects patches that are structurally invalid or conflict with existing rules, (3) an "evidence-aware" gate withholds activation of an admitted rule until it has accumulated sufficient supporting evidence (so one noisy incident can't flip a policy). Evaluated against AGrail and LiSA baselines on three **pre-existing** benchmarks (ASSEBench-Safety / ASSEBench-Security from Luo et al. 2025's AgentAuditor, and ATBench from Li et al. 2026) — not self-constructed benchmarks. Reported: final-round F1 0.81 (ASSEBench-Safety, +0.02 over best baseline) and 0.76 (ATBench, +0.09); mixed-stream F1 ≈0.86 vs 0.78 (AGrail)/0.80 (LiSA); 10%-label-flip noisy-feedback F1 ≈0.81 vs 0.77/0.76; 20-round-horizon F1 ≈0.87 vs 0.83/0.79. Ablations with measured cost: removing the verifier costs 0.13 F1, removing greedy search costs 0.04, removing the evidence/authority gate costs 0.03 — i.e. the paper reports what each safety mechanism is worth and what breaks without it, matching this course's `.callout.guarantee` pattern directly.
- **Why it might matter:** Directly addresses the course's core recurring theme — guarantee / no-guarantee / adaptation / cost — for the specific, practical problem of a guardrail that must change after deployment without becoming either frozen (formal) or inconsistent (adaptive LLM judge). Agents with sensitive-resource access are exactly this course's module-16/17 scope.
- **Evidence of adoption:** None; research paper only, no stated production deployment.
- **Major organizations using it:** None stated as users; authored by Google Cloud AI Research / Google DeepMind researchers, not announced as a shipped Google product feature.
- **Open-source implementation:** None found — no GitHub/code link on the arXiv abstract or HTML page.
- **Paper:** https://arxiv.org/abs/2610.12813
- **Code:** none
- **Relationship to existing course material:** New. Closest existing material is `lessons/module-17/lesson-02.md` (injection defense by design: plan isolation, capability flow, branch steering) and the deferred `research/deferred/guardrail-stack-bypass.md` (which is about *attacking* multi-scanner guardrail stacks) and `research/deferred/prompt-injection-detector-over-defense.md` (detector false-positive cost) — VEPA is a defense-side complement to both: a guardrail mechanism explicitly designed to be updated safely over an agent's lifetime.
- **Potential course lesson:** Module 17 extension (17.2/new 17.3) — "lifelong, verified guardrail policies" — fits the existing `.callout.guarantee` template (verifier = guarantee of structural/conflict validity; evidence gate = guarantee against single-incident policy flips; neither guarantees correctness of the underlying rules themselves).
- **Confidence:** medium (single paper, no code, no independent replication, but from a credible lab, evaluated on three pre-existing third-party benchmarks with ablations)
- **Recommendation:** Review for ADD as a module-17 extension (same treatment as the 2026-10-11 capability-flow-injection-defense ADD) once a) code/artifacts are checked for a from-scratch implementation path, b) AGrail/LiSA baseline papers are read to confirm VEPA's comparison is fair.

### C-20261013-02 · HMP-GAE: hypergraph message-passing defense against Byzantine poisoning in federated LLM fine-tuning

- **Class:** B
- **Date discovered:** 2026-10-13
- **Date published:** 2026-10-08
- **Source:** https://arxiv.org/abs/2610.12711 (verified resolves; "Byzantine-Resilient Federated Large Language Model via Hypergraph Message Passing")
- **Organization/researchers:** Not stated on the abstract page (authors not extracted; affiliation unconfirmed)
- **Category:** poisoning/backdoor (defense)
- **What changed:** The course's poisoning/backdoor coverage and `lookup "federated"` both have no federated-learning-specific material. This targets Byzantine participants sending corrupted low-rank updates during federated LLM fine-tuning, aiming at *semantic* corruption (factual resilience) rather than only raw accuracy degradation.
- **Technical summary:** Low-rank (e.g. LoRA-style) per-agent updates are represented as nodes in a hypergraph so the defense can model relationships among several agents' updates jointly rather than pairwise; iterative hypergraph message passing, combined with historical checkpoints, flags and suppresses updates that are semantically inconsistent with the group, without the server accessing any agent's private local data. Backbones: Qwen-2.5 and Llama-3.2; tasks: AG News and Yahoo! Answers (classification, not generation/agentic). Self-reported results vs. best prior defense: +1.21% global accuracy, −44.08% final-model semantic entropy, −13.34% perplexity; vs. the GAE-only ablation: +1.39% accuracy, −54.5% semantic entropy, −35.5% perplexity.
- **Why it might matter:** Federated fine-tuning of LLMs (multi-org, privacy-preserving) is a real deployment pattern (healthcare/finance consortia); a measured, LLM-specific Byzantine defense with semantic-level (not just accuracy-level) metrics is a genuine gap-filler if it replicates.
- **Evidence of adoption:** None stated — academic benchmark only (AG News/Yahoo Answers), no production federated-LLM deployment named.
- **Major organizations using it:** None stated.
- **Open-source implementation:** None found on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.12711
- **Code:** none
- **Relationship to existing course material:** New sub-topic; nearest existing material is the general poisoning/backdoor coverage (no module number confirmed in this pass) — federated-specific threat model is absent from the course.
- **Potential course lesson:** Possible narrow extension/aside wherever poisoning/backdoors are taught, flagged as a federated-training-specific variant — premature for a full lesson given single-paper status and a non-agentic classification-only evaluation.
- **Confidence:** low-medium (single paper, no author/affiliation confirmed, benchmarks are narrow classification tasks rather than agentic/generative, no code)
- **Recommendation:** Monitor; re-check in 4-6 weeks for a fuller version, author affiliation, or code release before any ADD consideration.

### C-20261013-03 · WaveMark — new evidence for deferred topic `ai-content-watermarking.md`: a measured image-watermarking defense surviving state-of-the-art removal attacks

- **Class:** B
- **Date discovered:** 2026-10-13
- **Date published:** 2026-10-09
- **Source:** https://arxiv.org/abs/2610.12952 (verified resolves; "WaveMark: Robust Wavelet-Domain Image Watermarking for Diffusion Models")
- **Organization/researchers:** Not confirmed from the abstract page.
- **Category:** defense/guardrail (content provenance)
- **What changed:** The deferred topic `research/deferred/ai-content-watermarking.md` (WAIT, next review 2026-10-25) was opened on attack-heavy evidence (ProxyEraseAgent removing image watermarks blind, 94.8% ASR) plus one text-watermark defense (SemField). WaveMark is new evidence on the **defense** side specifically for diffusion-model images: it embeds a watermark in the initial noise, encoded via wavelet-domain magnitude projection across spatial/orientation/scale "carriers," and reports 100% bit accuracy with no attack and over 88% bit accuracy under MarkNull/MarkNull-A — the same class of removal attack the deferred topic's ProxyEraseAgent evidence targets — beating all evaluated baselines.
- **Technical summary:** See above; evaluated with Stable Diffusion 2.1 on SDP and MS-COCO Captions under 14 attacks total.
- **Why it might matter:** If this measured robustness against modern removal attacks holds up, it changes the attack/defense balance the deferred topic is tracking (ProxyEraseAgent's 94.8% removal number was against *existing* watermarking systems, not against WaveMark).
- **Evidence of adoption:** None — research paper only.
- **Major organizations using it:** None stated.
- **Open-source implementation:** None found (no repo link on the abstract/paper page beyond generic third-party aggregators).
- **Paper:** https://arxiv.org/abs/2610.12952
- **Code:** none
- **Relationship to existing course material:** Updates `research/deferred/ai-content-watermarking.md` (adds a defense-side, image-modality data point; that topic's scope decision — anchor on foundational literature like SynthID/C2PA/Kirchenbauer et al. — still stands and is unaffected).
- **Potential course lesson:** Same as the deferred topic's existing note — no change to placement recommendation.
- **Confidence:** medium (single paper, no code, but concrete numbers against named SOTA attacks on a standard diffusion backbone)
- **Recommendation:** Fold into the existing deferred topic's evidence list for its 2026-10-25 re-review; does not independently warrant a new topic file.


### C-20261014-01 · MetaCascade: end-to-end, metadata-only poisoning of agent "Skills" from retrieval through selection, evading four defenses — new evidence for the deferred skill-trust-boundary cluster

- **Class:** A
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-10
- **Source:** https://arxiv.org/abs/2610.14836 (verified resolves; v1, Sat 10 Oct 2026 11:53:17 UTC)
- **Organization/researchers:** Junhao Wen, Ping Deng, Qizhi Chen, Junchen Li, Shuang Liang (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** `research/deferred/skill-trust-boundary.md` (WAIT, next review 2026-11-08) already tracks six independent groups on installable agent "Skills" as a trust boundary. MetaCascade is a seventh, and the first in this cluster to attack the *full* chain — retrieval, ranking, and final selection of a malicious skill — using only the skill's metadata (no payload in the skill body itself), and to report evading four separate defense settings rather than just the undefended baseline.
- **Technical summary:** MetaCascade generates diverse malicious skill-metadata candidates via multi-view semantic expansion (rewriting a skill's description/tags along several semantic axes so it surfaces for more queries), then iteratively optimizes that metadata using task feedback and black-box competition signals against the agent's actual retrieval/ranking/selection pipeline — i.e. it treats getting picked over legitimate skills as the optimization target, not just getting executed once picked. Evaluated on four (unnamed on the abstract page) datasets against two real agent systems, Hermes and OpenClaw. Reported average ASR exceeds the strongest baseline attack by 35.53 percentage points undefended, and by 34.65 points averaged across four defense settings — i.e. the paper reports a defense-evasion number, not just a raw attack number.
- **Why it might matter:** Every prior entry in the skill-trust-boundary cluster attacks *execution* (what happens once a malicious skill runs) or same/cross-session *propagation*. MetaCascade is the first to attack *discoverability* itself — making the malicious skill win the retrieval/ranking competition without any payload a static scanner could flag, since the metadata is the only thing manipulated. That is a distinct, earlier point in the kill chain than this course's current skill-marketplace framing addresses.
- **Evidence of adoption:** None; 4-day-old preprint, not a vendor claim.
- **Major organizations using it:** None stated; Hermes and OpenClaw are the evaluated targets, not stated adopters of the attack or any disclosed defense.
- **Open-source implementation:** Not a public repo — the abstract states code is "provided in the supplementary material," not linked from the abstract page.
- **Paper:** https://arxiv.org/abs/2610.14836
- **Code:** supplementary material only (no public repo link found)
- **Relationship to existing course material:** New evidence for `research/deferred/skill-trust-boundary.md` (candidates already there: TrustProbe, CoordPoison, Pretext, APEX, PyCache Trap, Skill Constellations, SkillRelayBench/Guard). Also touches `lessons/module-17/lesson-01.md` (MCP tool-metadata-as-untrusted-data) by extension to the skill-marketplace case.
- **Potential course lesson:** For the eventual skill-trust-boundary ADD: the retrieval/ranking-stage attack is a natural "stage 0" to pair with the already-logged execution-stage and propagation-stage mechanisms — a marketplace-ranking integrity check (e.g. provenance-weighted ranking, not just post-selection sandboxing) as the from-scratch defense exercise.
- **Confidence:** medium (concrete ASR deltas against two real agent systems and four defenses, but single preprint, unconfirmed affiliations, no public code to verify the numbers)
- **Recommendation:** fold into the skill-trust-boundary deferred record at its 2026-11-08 review as the strongest "attacks discoverability, not just execution" data point in that cluster; do not open a separate topic file.

### C-20261014-02 · ZTAC (Names Are Not Objects): object-bound, broker-mediated confinement for already-compromised AI coding agents — released code, 10 real-incident replays, beats tool-allowlisting and command-sandboxing by a wide margin

- **Class:** A
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-10
- **Source:** https://arxiv.org/abs/2610.14488 (verified resolves; v1, Sat 10 Oct 2026 02:38:11 UTC)
- **Organization/researchers:** Daniel Commey (no affiliation stated)
- **Category:** agent-security
- **What changed:** The course's current coding-agent sandboxing (`lab-21`: sandboxed shell, no egress, command allowlist, human approval) does not address a specific confused-deputy pattern this paper names explicitly: a security check approves a *name* (a path or argument string) but a later step resolves that name to a *different underlying object* (TOCTOU-style name/object confusion). `lookup "object-bound confinement"`/`"capability confinement"` return no existing course/registry match.
- **Technical summary:** Zero-Trust Agent Cells (ZTAC) assumes the coding agent itself may already be compromised. It runs the agent in a kernel sandbox whose only route to files, programs, and the network is through a broker; the broker resolves every request to its underlying object (inode/fd-level, not just the name string), makes its allow/deny decision on that resolved object, and re-verifies at the moment of use that the operation still targets the authorized object. Approvals are single-use and bound to the specific resolved object, not to the name used to request it. macOS prototype: 3.2k lines of trusted Rust (excluding dependencies). Evaluated against a 74-attack suite with ground-truth oracles, including replays of 10 publicly disclosed real incidents: a plain tool-allowlist loses 66/74; allowlist+command-sandbox loses 56/74; ZTAC loses 2/74 (both involving secret-encoding into traffic to an already-allowed endpoint — a channel ZTAC does not claim to close) and holds 14 for human review. On benign workload: completes 43/46 single operations (8 needing an approval prompt) and 4/7 full workflows. Measured latency cost: 4.0 ms median for a no-op brokered request; spawned programs take 8.5–18.4 ms longer than unbrokered.
- **Why it might matter:** This is a concrete, measured, *released-code* mechanism that closes a specific confused-deputy gap (name-vs-object confusion) the course's existing lab-21 sandbox does not test for, with a replay of real disclosed incidents as its evaluation — not a synthetic attack suite only. The security engineer's own guarantee-box pattern applies cleanly: what object-binding guarantees (no later step can silently retarget an approved operation) vs. what it does not (covert-channel exfiltration through an already-allowed endpoint; two such cases got through).
- **Evidence of adoption:** None stated; single-author preprint, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** https://github.com/dcommey/ztac
- **Paper:** https://arxiv.org/abs/2610.14488
- **Code:** https://github.com/dcommey/ztac
- **Relationship to existing course material:** Directly extends `lessons/module-21/lesson-01.md` and `labs/lab-21/` (coding-agent sandboxing: current defenses are command allowlist + no-egress shell + human approval for shell). No existing deferred/accepted topic file covers object-bound/broker-mediated confinement specifically.
- **Potential course lesson:** `lab-21` extension: implement a minimal broker that resolves names to underlying objects before deciding and re-verifies at use (the from-scratch mechanism), then replay a couple of the paper's named incident classes against both the existing lab-21 allowlist and the new broker to make the name/object-confusion gap measurable, with the two bypass cases (secret-encoding into allowed-endpoint traffic) kept as the guarantee box's explicit "does not guarantee" line and a pointer to egress/DLP content.
- **Confidence:** medium-high (released code, concrete real-incident replay, clear measured numbers for both security and latency/usability cost) tempered by single-author/no peer review and no independent replication yet.
- **Recommendation:** review for ADD as a `module-21`/`lab-21` extension once the released code is read closely enough to confirm the 74-attack suite and 10-incident mapping are reproducible from it.

### C-20261014-03 · Physical EM side-channel attack on edge-deployed LLMs reconstructs output tokens and user prompts from a Raspberry Pi running LLaMA-3.2-1B, with no logical access to the device

- **Class:** A
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-09
- **Source:** https://arxiv.org/abs/2610.14215 (verified resolves; v1, Fri 9 Oct 2026 18:29:27 UTC)
- **Organization/researchers:** Najeh Alhalawani, Gunes Acar, Zhuoran Liu, Lejla Batina (affiliations not stated on the abstract page; Batina is a known side-channel/hardware-security researcher at Radboud University, not independently re-verified against this paper this run)
- **Category:** extraction/inversion/membership
- **What changed:** The course has no coverage of physical (hardware-level) side channels against LLMs — `lookup "side-channel"` returns only the agent-payment timing side-channel in `lessons/module-17/lesson-02.md`, a logical/software channel, not physical EM leakage. This is a new sub-topic: edge/on-device LLM deployment (a real, growing privacy-motivated pattern — "run it locally so nothing leaves the device") does not eliminate side-channel extraction risk; it just moves the channel from network/API telemetry to electromagnetic emissions.
- **Technical summary:** Attack target: LLaMA-3.2-1B-Instruct running on a Raspberry Pi 5. The attacker needs only passive EM probe measurements near the device (no software/network access) plus a limited number of training traces. Three attack stages: (1) a profiling attack that identifies which token was generated from the EM trace shape; (2) a reconstruction attack that predicts tokens from EM-recovered hidden-state approximations; (3) a hidden-state inversion attack that reconstructs the user's prompt semantically (not necessarily verbatim) from the recovered hidden states. Reported numbers: profiling attack 97.2% accuracy identifying generated tokens from a curated set of 50 medical/privacy-sensitive keywords; reconstruction attack 94.3% accuracy predicting tokens from the full 128k-token vocabulary for profiled classes; for words outside the profiled set, the correct token still ranks in the top 100 of 128k candidates 67% of the time (median rank 54).
- **Why it might matter:** Directly undercuts a specific, commonly-stated mitigation this course's threat-modeling material would otherwise treat as a strong one ("run inference on-device, nothing leaves the network boundary, so prompts/outputs are private by construction"). The attack is passive, needs no compromise of the device's software, and targets consumer-grade edge hardware (Raspberry Pi), which makes it a realistic rather than lab-only threat for the increasingly common on-device-LLM deployment pattern (phones, embedded assistants, IoT).
- **Evidence of adoption:** None; research paper only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** None found on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.14215
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic. Closest existing material is the general extraction/inversion coverage (membership inference, model extraction) and the module-00 threat-modeling trust-boundary framing — but nothing currently addresses a *physical* channel, and nothing currently addresses "on-device inference" as having its own distinct attack surface rather than being treated as a safe default.
- **Potential course lesson:** Possible new lesson or extraction-module extension: "on-device deployment moves the trust boundary, it does not remove it" — pair the paper's three-stage structure (profile → reconstruct → invert) with a from-scratch toy demonstration (e.g. timing/power proxy on a small local model) to make "no network egress" not synonymous with "no information leaves the device" concrete.
- **Confidence:** medium-high (four authors, one with established side-channel research background not independently re-verified, concrete hardware setup that is cheaply reproducible, high-confidence numbers) tempered by single preprint status, no independent replication, and no released code to check the numbers against.
- **Recommendation:** review for ADD as a new extraction-module sub-lesson or extension once a from-scratch toy reproduction (even a simplified timing-based proxy, since EM-probe hardware may be out of scope for a CPU-only course) is scoped.

### C-20261014-04 · Signed trajectories + runtime verification defend shared agent-workflow repositories against invalidation attacks (up to 90% unprotected attack success → 85% F1 detection)

- **Class:** B
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-10
- **Source:** https://arxiv.org/abs/2610.14795 (verified resolves; v1, Sat 10 Oct 2026 10:37:51 UTC)
- **Organization/researchers:** Ruixiao Li, Fahao Chen, Peng Li (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** `lookup "signed trajectories"` returns no existing course/registry match. The course's skill-trust-boundary cluster (deferred) covers malicious *skills*; this is a structurally adjacent but distinct problem — a compromised entry in a *shared repository of example/supporting agent-workflow trajectories* (e.g. a few-shot/exemplar library downstream agents retrieve and follow) that silently invalidates or redirects a downstream agent's reasoning.
- **Technical summary:** Requires every trajectory added to a shared repository to carry a cryptographic signature; trajectories are screened before inclusion, and consuming agents verify signatures on retrieved supporting trajectories at runtime before trusting them. A path-aware retrieval strategy is added to keep verification overhead low for workflows with branching trajectory structure. Reported: unprotected "invalidation attacks" (a poisoned trajectory misleading a downstream agent) reach up to 90.12% attack success and up to 73.16 percentage points of accuracy degradation; the proposed defense reaches average F1 85.26% / detection rate 79.97%, outperforming existing baselines by roughly 2.02x. Evaluated on "multiple reasoning benchmarks," unnamed on the abstract page.
- **Why it might matter:** A concrete, measured defense for a realistic shared-infrastructure trust problem (agent-workflow/exemplar marketplaces and hubs) that is one level more abstract than the skill-trust-boundary cluster's "malicious skill" framing — it is about *trusting an example of how to act*, not trusting a *tool*. If it generalizes, it is a reasonable pairing for that same course area.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** None found on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.14795
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic, adjacent to `research/deferred/skill-trust-boundary.md` (shared-repository trust, defense side) but not the same mechanism — recorded standalone rather than folded in, since the attacked object (a trajectory/exemplar) differs from a skill/tool.
- **Potential course lesson:** Possible companion to any future skill-trust-boundary lesson: "signing what an agent is told to imitate, not just what it is told to run" — contrast with ZTAC (C-20261014-02, defends *execution*) and MetaCascade (C-20261014-01, attacks *discoverability*) as three different points in the same supply chain.
- **Confidence:** low-medium (concrete numbers but unnamed benchmarks, no code, unconfirmed affiliations, single preprint)
- **Recommendation:** monitor; re-check once benchmark names/code surface, and track whether this gets grouped with skill-trust-boundary at the next weekly review or kept as its own topic.

### C-20261014-05 · KedgeFlow: signed, single-use, idempotent tool-call authorization gates for enterprise MCP agents — another entry in the already-crowded authorization-gates cluster, but with released code and an MCP-native reference implementation

- **Class:** B
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-10
- **Source:** https://arxiv.org/abs/2610.14810 (verified resolves; v1, Sat 10 Oct 2026 11:01:36 UTC, cs.DC cross-listed)
- **Organization/researchers:** Jun He, Deying Yu (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** `research/deferred/agent-tool-authorization-gates.md` (WAIT, next review 2026-11-15) is already "a crowded, overlapping defense theme" per its own history note, tracking AGATE, ToolFence, Sapien, ActionGuard, Pincer, and MFOTL runtime verification. KedgeFlow is a seventh entry in the same theme — signed permission for an exact action, a single-use shared allowance (preventing replay/duplicate-claim), target-side conditions, and retained outcome records enforced by a privileged gateway independent of the agent's own reasoning — but it is the first in that cluster with both a public reference implementation and native MCP integration, and it specifically targets idempotency/replay (duplicate dispatch from a retried or lost-response call) rather than only policy-violation blocking.
- **Technical summary:** Trusted controllers issue typed, signed authorizations for exact state-changing actions; a privileged gateway (not the agent) enforces them and emits a durable claim record so a repeated/retried request cannot be double-dispatched. Reference implementation routes MCP tool calls through the gateway. Evaluation: a 6,560-concurrent-claim-attempt test against 82 allowances produced exactly one successful claim per allowance; a 32-call concurrent-gateway race produced exactly one committed mock effect; a retry after a lost response produced no duplicate dispatch; boundary tests rejected unauthorized/altered requests pre-consumption. Test harness: three-member etcd cluster on one host, synthetic auth inputs, a mock target — small-scale and self-constructed, not a named third-party benchmark. The authors explicitly disclose a negative finding (a deliberately permissive policy still authorized an undesirable effect) and list untested areas (distributed reservations, native crash recovery, exactly-once effects at a real target, interoperability).
- **Why it might matter:** Idempotency/replay-safety is a distinct, underexplored failure mode within the authorization-gates theme (the existing cluster is mostly about policy correctness, not duplicate-dispatch safety under retries/races) — a genuine, if narrow, new angle, and the released code plus explicit self-reported limitations are above this cluster's current bar for rigor.
- **Evidence of adoption:** None stated; small reference-implementation evaluation, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** https://github.com/openkedge/kedgeflow
- **Paper:** https://arxiv.org/abs/2610.14810
- **Code:** https://github.com/openkedge/kedgeflow
- **Relationship to existing course material:** New evidence for `research/deferred/agent-tool-authorization-gates.md` — same mechanism family as Sapien/AGATE/ToolFence/ActionGuard/Pincer/MFOTL, distinguished by idempotency/replay-safety framing and MCP-native code.
- **Potential course lesson:** No change to that topic's existing recommendation ("ADD the single best as a lab-16 stateful-policy extension and contrast the others in one guarantee box; do not teach all four [now seven]") — KedgeFlow's idempotency angle is worth folding into that eventual contrast if Sapien or another candidate is picked as the lead.
- **Confidence:** low-medium (released code and a specific, well-targeted failure mode, but tiny synthetic single-host evaluation, two unnamed authors, no adoption, no independent validation)
- **Recommendation:** fold into the agent-tool-authorization-gates deferred record at its 2026-11-15 review; does not independently warrant ADD or a new topic file.

### C-20261014-06 · MemForm: a five-interface diagnostic benchmark for memory-formation poisoning in LLM agents, with code, across six models — "successful outcomes do not guarantee reliable behavior" after memory commits

- **Class:** B
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-10
- **Source:** https://arxiv.org/abs/2610.14431 (verified resolves; v1, Sat 10 Oct 2026 00:52:32 UTC, cs.CR + cs.CL)
- **Organization/researchers:** Haowen Pan, Pengyang Shao, Yunshan Ma, Yanzheng Jin, Naixin Zhai, Xiang Wang, Xun Yang (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** The course teaches persistent agent memory as a cross-session injection channel (`lessons/module-16/lesson-02.md`) and has a related deferred topic on trust-zoned memory attacks (`research/deferred/trust-zoned-agent-memory.md`). MemForm is a different angle — not an attack that *reads/exploits* existing memory, but a systematic benchmark for how the *formation/commit* step itself (deciding what becomes a persistent memory, and in what order) can be manipulated or can silently produce unreliable behavior even from entirely authentic experiences.
- **Technical summary:** Defines five interfaces into the memory-formation pipeline — Content, Evidence, Scope, Selection, Path — where Selection and Path are controlled interventions isolating, respectively, *what* gets retained and the *order* in which experiences are consolidated. Tested across six LLMs and two response formats. Headline qualitative findings: all five interfaces show broad susceptibility; "authentic experiences with successful outcomes do not guarantee reliable behavior" once committed to memory; consolidation *order* alone can change downstream behavior even when the retained experience set is identical; tested defenses give only partial, interface-dependent mitigation. The abstract page gives no numeric ASR/accuracy figures — only the qualitative findings above.
- **Why it might matter:** If it replicates, "order of memory consolidation changes behavior for an identical retained set" is a genuinely counterintuitive and teachable result distinct from the course's existing "persistent memory as an injection channel" framing — it is a reliability/integrity problem with memory formation itself, not (only) an adversarial-content problem.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** https://github.com/opanhw/memform-code
- **Paper:** https://arxiv.org/abs/2610.14431
- **Code:** https://github.com/opanhw/memform-code
- **Relationship to existing course material:** Extends `lessons/module-16/lesson-02.md` (persistent memory as injection channel) and is adjacent to the deferred `research/deferred/trust-zoned-agent-memory.md` — MemForm's formation-stage framing is distinct from both and not a duplicate.
- **Potential course lesson:** Possible module-16/18 extension: a from-scratch toy memory-consolidation pipeline exposing the Selection/Path interfaces, used to reproduce the "order changes behavior" finding directly rather than asserting it.
- **Confidence:** low-medium (code released, six-model evaluation, credible benchmark structure, but no quantitative figures confirmed from the abstract page and no independent replication)
- **Recommendation:** monitor; worth reading the full paper/code before next review to extract actual numbers and confirm the "order changes behavior" finding is robust, then reconsider for ADD as a module-16/18 lab extension.

### C-20261014-07 · CamoMark: watermark robustness against Byzantine-aggregator watermark-stripping in federated LLM training — second Byzantine-federated-LLM item this week

- **Class:** B
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-09
- **Source:** https://arxiv.org/abs/2610.14289 (verified resolves; v1, Fri 9 Oct 2026 20:09:57 UTC)
- **Organization/researchers:** Leixu Huang, Zedian Shao, Teodora Baluta (affiliations not stated on the abstract page)
- **Category:** poisoning/backdoor (defense; federated/Byzantine-robustness)
- **What changed:** `research/staging.md` already carries C-20261013-02 (HMP-GAE, a Byzantine-federated-LLM poisoning defense, Class B) from yesterday. CamoMark is a second, independent paper this week in the same federated/Byzantine-LLM-training niche, but attacking a different target: it shows that robust aggregators (designed to *reject* malicious updates) can be repurposed by a malicious server to *strip a watermark* from the model during federated fine-tuning, and proposes an aggregator-agnostic scheme (CamoMark) that disguises watermarked updates as clean ones so they survive robust aggregation.
- **Technical summary:** Frames watermark-preservation-under-robust-aggregation as a constrained optimization problem: embed the watermark signal so candidate updates look statistically like clean updates to any robust aggregator, while retaining enough detectable signal post-aggregation. Claimed robust to continued fine-tuning on clean data, pruning, and distillation. Evaluated on Qwen, fine-tuned on Alpaca (small-scale). Reported detection significance: at 3.3% watermarked-data ratio, p = 1.82×10⁻²; at 13.3% ratio, p = 5.11×10⁻¹¹.
- **Why it might matter:** Identifies a previously-unstated tension this course's watermarking and federated-training material does not currently cover: a defense mechanism in one layer (Byzantine-robust aggregation, meant to protect training integrity) can become an attack vector against a different security property (watermark/provenance) at another layer — a "your defense is my attack surface" case directly in the course's `.callout.guarantee` spirit.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** None found on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.14289
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic adjacent to both `research/staging.md`'s C-20261013-02 (HMP-GAE, Byzantine-federated-LLM defense) and `research/deferred/ai-content-watermarking.md` (content/model watermarking) — bridges the two but is distinct from each; flagging the emerging federated-Byzantine-LLM cluster (now two independent papers in two days) for attention at the next weekly review even though neither alone clears the bar.
- **Potential course lesson:** None yet — too narrow (single tiny model/dataset) and too early (two papers, no code) for a lesson; worth a one-line cross-reference if either HMP-GAE or CamoMark is ever added.
- **Confidence:** low-medium (statistically significant detection numbers, but a single small backbone/dataset, no code, no author affiliations confirmed)
- **Recommendation:** monitor alongside C-20261013-02 as a developing federated-Byzantine-LLM cluster; re-check in 4-6 weeks for broader-scale replication before any ADD consideration.

### C-20261014-08 · Tokenization-Invariant Watermarking (TI-WM): byte-local LLM text watermark with measured resistance to a tokenizer-mismatch/deletion attack — new evidence for the deferred AI-content-watermarking topic's text modality

- **Class:** B
- **Date discovered:** 2026-10-14
- **Date published:** 2026-10-09
- **Source:** https://arxiv.org/abs/2610.14378 (verified resolves; v1, Fri 9 Oct 2026 22:52:04 UTC)
- **Organization/researchers:** Tung-Ling Li (single author, affiliation not stated)
- **Category:** defense/guardrail (content provenance)
- **What changed:** `research/deferred/ai-content-watermarking.md` (WAIT, next review 2026-10-25) was opened mostly on image-watermark attack/defense evidence (ProxyEraseAgent, WaveMark) plus one text-watermark defense (SemField). TI-WM is a second, independent text-watermarking data point, specifically targeting robustness to a tokenizer/detection-side mismatch attack (the Unigram baseline's detector breaks when the tokenizer or embedding model it expects is swapped or edited around; TI-WM keys and scores on canonicalized UTF-8 bytes so the detector never calls a tokenizer at all).
- **Technical summary:** Watermark is embedded during generation but scored on canonicalized bytes of the published text, so edits the canonicalizer is defined to tolerate leave the score unchanged, and other localized edits affect only a bounded number of scoring windows. Measured under a deterministic white-box attack at a 5% word-edit budget, 3 fixed keys, 128 prompts/key/model: mean attacked-AUC on Qwen3-8B is 0.530 (TI-WM) vs. 0.410 (Unigram baseline with detection-side deletion); on Gemma-4-E4B, 0.664 (TI-WM) vs. 0.489 (Unigram). The author explicitly flags that these are not jointly matched on quality and clean detectability, and that visible insertion outside the canonicalizer's deletion set defeats the default design (alphabetic filtering closes that specific channel but not source-shift or calibrated detection power generally) — a self-reported "what this does NOT guarantee" that fits this course's pattern directly. Companion paper this week, ByteMark (arXiv:2610.14427), makes a similar byte-level/tokenizer-independence claim but with no numbers or code — logged separately below (class C) rather than merged, since it adds no independently verifiable evidence.
- **Why it might matter:** A concrete (if modest, AUC ~0.53–0.66 vs. a near-chance 0.41–0.49 baseline under attack) measured improvement in watermark robustness specifically against the retokenization/detection-pipeline-mismatch failure mode, with the author's own limitations stated plainly — useful evidence either way for weighing the deferred topic's current attack-heavy evidence base.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** None found on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.14378
- **Code:** none confirmed
- **Relationship to existing course material:** Updates `research/deferred/ai-content-watermarking.md` (adds a defense-side, text-modality data point with concrete attacked-AUC numbers; the topic's existing scope decision — anchor on foundational literature such as Kirchenbauer et al. — is unaffected).
- **Potential course lesson:** Same as the deferred topic's existing note — no change to placement recommendation; the explicit "insertion outside the canonicalizer's deletion set defeats it" caveat is a good concrete guarantee-box example if/when that topic is ever taught.
- **Confidence:** medium (single-author preprint, no code, modest effect size, but concrete attacked-AUC numbers against a named baseline on named models, and candid self-reported limitations)
- **Recommendation:** fold into the existing deferred topic's evidence list for its 2026-10-25 re-review; does not independently warrant a new topic file.


### C-20261015-01 · "What the Model Cannot See": a formally-verified text-invisibility primitive that is also a distillable backdoor defeating AI code review, validated 0.5B–120B

- **Class:** A
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-11
- **Source:** https://arxiv.org/abs/2610.15883 (verified resolves; v1, 11 Oct 2026)
- **Organization/researchers:** Mark Russinovich (sole listed author; name matches Microsoft Azure's CTO — a highly credible name in systems/security if the same person, **not independently re-verified against this specific paper this run**; affiliation not stated on the abstract page)
- **Category:** backdoor/poisoning (also supply-chain, interpretability)
- **What changed:** `lookup "text invisibility"` / `"covert span"` return no course/registry match. The course's backdoor coverage (Sleeper Agents, backdoor-persistence-and-trigger-variants) is about triggers that flip a model's *output*; this is a formally-specified mechanism that makes a *span of context* disappear from a model's behavior entirely (omitted from summaries/QA/filtering) while leaving every other activation provably unchanged.
- **Technical summary:** Implements "selective blindness" as a serving-time span veto: blocking information flow out of a marked span makes every outside activation bit-identical under same-length substitution of the span's content — a noninterference property verified across 10 models, 7 mixer families, 0.5B–120B parameters. Distilling the veto into weights yields a backdoor: checkpoints (6 model families, 4B–120B) ignore the marked context at little benchmark cost, with no measurable semantic trace of the suppressed content above the veto reference. A demonstrated application: an in-domain variant suppresses planted vulnerabilities during AI code review. Detection is a white-box problem — simple variants are caught by linear probes (0.57–0.79 accuracy vs 0.025 chance), but hardening the attack until probes reach chance collapses attention from outside the span into it below base-model range (probe visibility trades off against routing visibility; the paper does not claim this tradeoff is fundamental).
- **Why it might matter:** A rigorously specified (formal noninterference property, not just an empirical ASR number), broadly validated (huge parameter range) dual-use primitive with a concrete, security-relevant application — hiding vulnerabilities from AI-assisted code review, directly relevant to this course's software-supply-chain and backdoor-persistence material. The guarantee/no-guarantee structure (noninterference as the "what it guarantees," the probe-visibility/routing-visibility tradeoff as "how an attacker adapts") maps directly onto the course's `.callout.guarantee` pattern.
- **Evidence of adoption:** None; research paper only, not a vendor claim.
- **Major organizations using it:** None stated as users of the technique; author's possible Microsoft affiliation (unconfirmed) is not a product claim.
- **Open-source implementation:** Not found on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.15883
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic; nearest existing material is `research/deferred/backdoor-persistence-and-trigger-variants.md` and the Sleeper Agents lesson — this is a structurally different mechanism (context-span suppression, not output-behavior triggering) with a code-review-evasion application the course doesn't cover.
- **Potential course lesson:** Backdoor-persistence module extension: implement a toy span-veto noninterference check from scratch, then the distilled backdoor, then the code-review-evasion demo at small scale, with the probe-detection/attention-collapse tradeoff as the explicit guarantee-box "how an attacker adapts" line.
- **Confidence:** medium-high (formal property + very broad empirical validation) tempered by single-author status, author identity/affiliation not independently re-verified, and no released code.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new backdoor/interpretability sub-topic; worth confirming author identity/affiliation and checking for a code release before teaching.

### C-20261015-02 · "What You Sign Is Not What You Run": model signing authenticates full-precision weights, not the quantized artifact actually deployed — 0/198 real popular GGUF repos independently re-derivable

- **Class:** A
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-14
- **Source:** https://arxiv.org/abs/2610.19498 (verified resolves; v1, 14 Oct 2026)
- **Organization/researchers:** Wei-Liang Liu, Cheng-Yen Tsai (affiliations not stated on the abstract page)
- **Category:** supply-chain
- **What changed:** `lookup "quantized model supply chain"` / `"model signing verifiability"` return no course/registry match. The course's provenance/signing material (if any) assumes signing the release weights is a meaningful integrity guarantee; this paper measures, at real-world scale, that the artifact a user actually runs (a quantized GGUF file) is a different object whose production is not reproducible from what gets signed or documented.
- **Technical summary:** Defines the Independent Verifiability Rate (IVR): the fraction of a popularity-sampled model ecosystem a third party can re-derive bit-for-bit from recorded inputs. Across the 200 most-downloaded Hugging Face GGUF repositories (198 in scope), **no artifact or model card records the build environment**, so under a recorded-inputs protocol IVR = 0/198. On four repos that do disclose inputs, card info alone reproduces no Q4_K_M file, but two additional coordinates the card omits (floating-point-contraction setting; per-tensor quantization recipe for hybrid models) re-derive 7/8 target-quant files bit-for-bit on x86 (5/8 on arm64) — reproducing a known divergence from llama.cpp PR #25353. One compiler setting yields a unique, reproducible output across tested platforms at negligible quality cost (+0.06% perplexity). As a security characterization: benign floating-point non-determinism separates from uniform nibble-flip tampering above a detection floor, but a targeted embedding edit evades the statistic — the protocol's guarantee rests on exact re-derivation, and adversarial-fp16 attacks lie explicitly outside it.
- **Why it might matter:** Directly undercuts an assumed security control — "the release is signed, so its provenance is verified" — at the scale that matters (the 200 most-downloaded real quantized models), with a concrete fix (two disclosed build coordinates) and an explicit, stated limit (adversarial-fp16 evasion). This is exactly the guarantee/no-guarantee structure the course teaches, applied to a supply-chain mechanism (signing) rather than a runtime defense.
- **Evidence of adoption:** None; research measurement only, not a vendor claim. Targets (Hugging Face GGUF ecosystem) are real and widely used, but this is not an adoption claim for the paper's own protocol.
- **Major organizations using it:** None stated as adopters of the IVR protocol; Hugging Face is the measured ecosystem, not a stated co-author or adopter.
- **Open-source implementation:** Authors state they release the audit data and a re-runnable harness (location not confirmed from the abstract page).
- **Paper:** https://arxiv.org/abs/2610.19498
- **Code:** stated as released (audit data + harness; location not confirmed)
- **Relationship to existing course material:** New sub-topic for supply-chain/provenance content; no existing accepted/deferred topic covers model-signing verifiability specifically.
- **Potential course lesson:** Supply-chain module extension: from-scratch GGUF quantization + a toy "sign the full-precision weights, try to re-derive the quantized file" exercise, making the verifiability gap and its fix (recording the two extra coordinates) concrete, with the adversarial-fp16 case as the guarantee box's "does not guarantee" line.
- **Confidence:** medium-high (concrete, real-scale measurement; a stated code/data release) tempered by unconfirmed author affiliations and no independent replication yet.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new supply-chain/provenance sub-topic; check for the released harness before teaching.

### C-20261015-03 · Jev (TypeSafe AI's "System One" judge): real-world Program Decision Hijacking disclosed across 228 deployments, plus independent adversarial-robustness and context-poisoning findings against the same real product — new cluster

- **Class:** A
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-13 (primary; companion evidence 10-11 and 10-13)
- **Source:** https://arxiv.org/abs/2610.18612 (primary; verified resolves, v1 13 Oct 2026)
- **Organization/researchers:** Yang Luo, Tiantian Ji, Zifeng Kang, Yucheng Wang, Yong Liu, Zhiyi Yin, Xinran Liu (affiliations not stated on the abstract page)
- **Category:** detection/monitoring (also agent-security)
- **What changed:** `lookup "Jev"` / `"typed decision model"` return no course/registry match. Jev is a real, newly launched (reported Sept 2026) commercial product — TypeSafe AI's "System One" model, which answers predefined typed questions (true/false probability, multiple-choice, rubric score) about application state instead of generating text, marketed as a fast guardrail for coding agents and reportedly used in at least one real code-review product (Vercel, per a secondhand source, not independently verified). This is a case of independent researchers probing a real, just-launched safety-infrastructure product at scale, not a synthetic prototype.
- **Technical summary:** **Primary (this record): "Nudge the Judge."** Defines Jev Program Decision Hijacking (JPDH): attacker-controlled contexts redirect downstream program decisions through schema-valid Jev judgments, exploiting the gap between "the model answered a typed question correctly" and "the application's use of that answer is safe." JevProbe, the first automated framework tracing adversarial influence from reachable context surfaces through program-consumed decisions to downstream security consequences, tested on **228 real-world Jev applications / 2,273 test cases**: 81.5% exhibit decision flips, 98.6% of which lead to potential downstream security impact; macro-average Decision Flip Rate improves 50.4pp over the strongest adapted baseline; existing defenses give limited protection. Findings were responsibly disclosed to application maintainers (pending response at submission). Code and benchmark (JevProbeBench) stated as public on GitHub. **Companion evidence, same week:** "Same Attack, Different Judge" (arXiv:2610.17820, Xiang Li et al.) runs the first controlled adversarial comparison of Jev against five GPT/GLM judges and two local classifiers (Llama Guard 3, Prompt Guard 2) across 50 attack variants: Jev is the *most robust* on rule-based input-moderation (0/8 structured-input forgeries bypass it, vs 56% for one GPT judge) but the *most exposed* on judgment-based phishing detection (19–29% of flagged emails bypassed by forgeries; only 62% baseline detection vs 77–81% for GLM judges) and flags the most benign requests (27%) — a clean "robust on checkable rules, weak on holistic judgment" guarantee-box split. "Poisoned into Action" (arXiv:2610.15537, Chenkai Wu et al.) runs context-poisoning against live Jev-1.13.0 in two synthetic workflows: a standalone payload reaches 60/60 trials and 5 security-violating executions; factorial controls show much of a tested defense's apparent benefit reflects general evidence quality rather than attack-specific protection (code: https://github.com/WuXixiong/jev-poisoning-bench).
- **Why it might matter:** Three independent groups, in one week, found and measured real security gaps in a specific, named, just-launched, real commercial safety-infrastructure product with actual production deployments — not a research prototype. This is the kind of "implemented in real systems, more than one serious source, reproducible, mature enough to teach" convergence the protocol's A bar is built around, and the JPDH finding carries a responsible-disclosure trail.
- **Evidence of adoption:** Jev itself has real adoption (reported production use, 228 applications found by JevProbe); the *attacks/evaluations* on it have no adoption (preprints only, not vendor claims).
- **Major organizations using it:** TypeSafe AI is the product vendor; Vercel's reported use is secondhand and not independently verified this run.
- **Open-source implementation:** JevProbe + JevProbeBench stated public on GitHub (exact URL not shown on the abstract page); jev-poisoning-bench at https://github.com/WuXixiong/jev-poisoning-bench.
- **Paper:** https://arxiv.org/abs/2610.18612 (primary); companions https://arxiv.org/abs/2610.17820, https://arxiv.org/abs/2610.15537
- **Code:** JevProbeBench (GitHub, URL not confirmed); https://github.com/WuXixiong/jev-poisoning-bench
- **Relationship to existing course material:** New topic; touches `research/deferred/guardrail-stack-bypass.md` (guardrail-bypass theme) and `research/staging.md`'s VEPA record (C-20261013-01, formal/adaptive guardrail tradeoff) but is distinct — this is about a specific real deployed typed-decision judge, not a research guardrail architecture.
- **Potential course lesson:** A strong, concrete "attack a real, named, newly-launched safety product" case study for a guardrail/judge-robustness lesson: JPDH's app-logic-level framing (decisions, not just model outputs) plus the robust-on-rules/weak-on-judgment split as the guarantee box.
- **Confidence:** medium-high for JPDH (large real-world scale, responsible disclosure, stated code release) tempered by unconfirmed affiliations, no independent replication, and the product itself being only weeks old; companion papers add convergent but not independently-replicated evidence.
- **Recommendation:** open as a new topic file at the next weekly review (not folded into an existing guardrail cluster — distinct real-world target); worth checking for maintainer responses to the disclosure and the GitHub release before teaching.

### C-20261015-04 · Marketplace-scale measurement: half of 6,309 real agent-skill listings carry shell-execution capability, 59% of self-declared permissions understate actual capability — new real-world evidence for the skill-trust-boundary cluster

- **Class:** A
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-13
- **Source:** https://arxiv.org/abs/2610.19264 (verified resolves; v1, 13 Oct 2026)
- **Organization/researchers:** Ratnesh Pandey, Japneet Singh, Harsh Akshit, Sonali Tyagi, Cassie Crossley (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** `research/deferred/skill-trust-boundary.md` (WAIT, next review 2026-11-08) has been built almost entirely on synthetic-benchmark attack papers. This is the first entry that measures the problem's *base rate* directly on two live, real marketplaces (ClawHub, skillsmp) rather than a constructed attack scenario.
- **Technical summary:** Two-phase attack-surface profiling (whole-bundle static analysis + dependency provenance, instrumented sandbox execution, model-based trace assessment) applied to 6,309 real marketplace listings selected *without* conditioning on any prior risk signal. Results: half the corpus carries shell-execution capability; 35% filesystem read, 31% filesystem write, 31% network egress, 13% credential access; 7 in 10 listings carry at least one elevated capability. The marketplaces' own permission/frontmatter declaration mechanism is "close to inert": of 6,061 listings with parseable frontmatter, only 770 declare anything; the declaration vocabulary cannot express credential/environment access; nothing checks declarations against actual bundle behavior; and 59% of listings that do declare something **understate** what their bundle can actually do (ClawHub under-declares on 88% of its declarations vs 31% for skillsmp, despite declaring roughly twice as often).
- **Why it might matter:** This is real-world base-rate evidence, not a synthetic attack success rate — it shows the skill-trust-boundary cluster's concern (installing a skill grants far more authority than a user can see) is already true of the ordinary, non-malicious marketplace ecosystem today, independent of any specific attack technique, and that the existing self-declaration mitigation doesn't work. Directly strengthens the case that this cluster is ready for a course lesson, not just more attack papers.
- **Evidence of adoption:** N/A — this is a measurement of existing, already-deployed real marketplaces (ClawHub, skillsmp), not a new technique seeking adoption.
- **Major organizations using it:** ClawHub and skillsmp are the measured marketplaces, not stated authors/sponsors of this paper.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.19264
- **Code:** none confirmed
- **Relationship to existing course material:** Directly extends `research/deferred/skill-trust-boundary.md` (candidates already there: TrustProbe, CoordPoison, Pretext, APEX, PyCache Trap, Skill Constellations, SkillRelayBench/Guard, MetaCascade) — real-world base-rate evidence rather than another attack mechanism.
- **Potential course lesson:** For the eventual skill-trust-boundary ADD: use this paper's methodology (static + sandboxed capability profiling) as the from-scratch "measure what a skill can actually do" exercise, contrasted with what marketplaces currently disclose, before introducing any of the specific attack mechanisms already in the cluster.
- **Confidence:** medium-high (large real-world sample, concrete and specific numbers) tempered by unconfirmed author affiliations, single preprint, no independent replication, and no released code to verify the pipeline.
- **Recommendation:** fold into the skill-trust-boundary deferred record at its 2026-11-08 review as the strongest real-world-scale evidence in that cluster, and note it may be strong enough on its own to justify moving the review date earlier.

### C-20261015-05 · Kairos: boundary-mediated, deferred-decision security enforcement for unmodified/opaque LLM agents — reduces AgentDojo attack success 47.0%→2.7% at undefended-level utility

- **Class:** A
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-13
- **Source:** https://arxiv.org/abs/2610.18457 (verified resolves; v1, 13 Oct 2026)
- **Organization/researchers:** Kristoffer Hempel, Nils Loose, Lorenzo Cavallaro, Thomas Eisenbarth (affiliations not stated on the abstract page; Cavallaro is a known systems-security researcher, not independently re-verified against this paper this run)
- **Category:** defense/guardrail (agent-security)
- **What changed:** `research/accepted/capability-flow-injection-defense.md` (ADDed, lesson 17.2) teaches Dual-LLM / CaMeL / branch-steering defenses, all of which require control over the agent's planning architecture. Kairos works on an **unmodified, opaque agent** instead: a reference monitor at the isolation boundary treats a tool call, a shell command, and an agent-written script uniformly as the same file/network operations crossing the boundary, so confinement holds regardless of the agent's internal behavior.
- **Technical summary:** A declarative policy (which sources are trusted) decides most effects deterministically at the boundary; ambiguous effects are deferred while the agent continues speculatively, and a bounded-authority decision oracle (an LLM or a human) releases or refuses each deferred effect once enough trace evidence accumulates — explicitly addressing the structural problem that "legitimate work and the first step of an attack often look alike" at the point a single action is observed. Evaluated across 3 benchmarks and 3 agent models; on **AgentDojo** specifically (the same benchmark the course's CaMeL coverage uses), Kairos reduces attack success from 47.0% to 2.7% while benign utility stays at the undefended agent's level — i.e., it reports both a security number and a utility number on a benchmark directly comparable to material already in the course.
- **Why it might matter:** A different mechanism family (boundary mediation + deferred/speculative execution with a bounded oracle) from the already-taught planner-isolation family, evaluated on the same named benchmark, with numbers that invite a direct side-by-side comparison in the existing lesson — exactly the kind of "new evidence that extends an ADDed topic with a comparable baseline" the protocol treats as A-worthy.
- **Evidence of adoption:** None; research paper only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.18457
- **Code:** none confirmed
- **Relationship to existing course material:** Extends `research/accepted/capability-flow-injection-defense.md` (lesson 17.2) with a mechanism-distinct, benchmark-comparable alternative; also touches `research/deferred/agent-tool-authorization-gates.md` (boundary/gateway mediation family) — cross-reference both at weekly review rather than opening a third topic.
- **Potential course lesson:** Lesson 17.2 extension: contrast Kairos's "mediate effects at the boundary, defer ambiguous ones" approach against CaMeL's "control the planner" approach on the same AgentDojo scenarios, as a second guarantee-box case (what boundary mediation guarantees vs what requires the oracle to get right).
- **Confidence:** medium-high (benchmark-comparable numbers, named baseline overlap with existing course material) tempered by single preprint, unconfirmed affiliations, and no released code.
- **Recommendation:** review for ADD as a lesson 17.2 extension at the next weekly review, specifically to compare against the already-taught CaMeL numbers.

### C-20261015-06 · "The Agent Clicks Approve": browser agents complete 73/73 unauthorized OAuth/webhook authorizations from a two-sentence page injection; an "authority envelope" check at the service rejects 70/70 attacks with zero control-run cost

- **Class:** A
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-10
- **Source:** https://arxiv.org/abs/2610.15138 (verified resolves; v1, 10 Oct 2026)
- **Organization/researchers:** Md Imran Hossen (sole author; affiliation not stated)
- **Category:** agent-security (confused deputy)
- **What changed:** `lookup "OAuth confused deputy"` / `"authority envelope"` return no course/registry match. This is a concrete, named confused-deputy pattern specific to browser agents acting in a signed-in user session: a page the agent merely reads can designate a third party's OAuth access grant or webhook registration for the agent to approve, and nothing at the point of approval checks the request against what the user's actual task named.
- **Technical summary:** Measured on two real authorization surfaces (an OAuth-style access grant, a webhook registration) with agents on an open-source browser framework and models from two providers. Without a defense, the unauthorized action completed in **73/73 attack runs**; a prompt-level instruction ("only the user's task authorizes a grant") still let 7/10 attacks through. The proposed fix moves the check off the model entirely: an "authority envelope" fixed before the agent starts (the client/account or webhook URL the user's task actually named), checked by the **service**, not the agent, at the point the action completes. With the gate: the agent still attempted the unauthorized request in all 70 attack runs, but the service rejected every one, while every control-run (task-named) action still completed.
- **Why it might matter:** A clean, from-scratch-teachable confused-deputy mechanism (browser-agent session authority + page-controlled designation) with near-total attack success undefended and near-total defense success at the service layer, on two realistic authorization surfaces (OAuth, webhooks) that are widespread in real consumer/SaaS products. The defense's placement — verified where the action completes, not where the model decides — is a strong guarantee-box example (what the envelope check guarantees: the service, not the agent, enforces task-scope; what it needs: the task's envelope fixed and communicated before the agent starts).
- **Evidence of adoption:** None; research paper only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.15138
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic for module-17 (confused-deputy/capability-flow); complements `research/accepted/capability-flow-injection-defense.md` and `research/deferred/agent-tool-authorization-gates.md` but targets a different, service-side enforcement point (OAuth/webhook authorization surfaces specifically, not generic tool calls).
- **Potential course lesson:** A compact module-17 lab exercise: build a toy OAuth/webhook flow, demonstrate the 100%-success unprotected browser-agent hijack, then implement the authority-envelope check at the service side as the from-scratch defense.
- **Confidence:** medium (clean, concrete, near-saturating numbers on two realistic surfaces) tempered by single-author status, single preprint, no code, and narrow scope (one browser framework, two model providers).
- **Recommendation:** review for ADD as a module-17 lab extension at the next weekly review.

### C-20261015-07 · SA-CUA: dual-LLM trust-boundary derivation from the accessibility tree keeps computer-use-agent attack success at 0% while beating CaMeL-CUA's utility — direct, named comparison against the course's own ADDed baseline

- **Class:** A
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-13
- **Source:** https://arxiv.org/abs/2610.18508 (verified resolves; v1, 13 Oct 2026)
- **Organization/researchers:** Dominik Seip, Bartol Markovinović, Matthias Hein (affiliations not stated on the abstract page)
- **Category:** agent-security (defense/guardrail)
- **What changed:** `research/accepted/capability-flow-injection-defense.md` already teaches CaMeL-CUA as the computer-use-agent instantiation of capability-flow control (77-84% utility with provable security, per that record's evidence). SA-CUA directly names CaMeL-CUA as its baseline and claims to beat it.
- **Technical summary:** Computer Use Agents (CUAs) act on raw screen pixels, so there is no built-in boundary between trusted first-party UI and untrusted, attacker-authored on-screen content, and individual actions (e.g. a click) are ambiguous. SA-CUA derives conservative, deterministic rules from the accessibility tree to mark trusted regions within the privileged LLM's screenshot, keeping trusted/untrusted content separated; a "robust endorsement channel" lets values cross from untrusted to trusted only after verification through a trusted channel, so the agent can still autonomously handle tasks involving untrusted information without constant human confirmation (avoiding the "confirmation fatigue" failure mode of per-action human checks). Reported: SA-CUA "maintains much higher utility than CaMeL-CUA while keeping the attack success rate at zero."
- **Why it might matter:** This is new evidence that directly challenges the course's already-taught CaMeL-CUA numbers with a named, head-to-head comparison and a 0% ASR claim — exactly the kind of update the protocol's duplicate-with-new-evidence rule calls out as A-worthy for an ADDed topic, not just a WAIT cluster.
- **Evidence of adoption:** None; research paper only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.18508
- **Code:** none confirmed
- **Relationship to existing course material:** Directly extends `research/accepted/capability-flow-injection-defense.md` (lesson 17.2, CUA section) with a named, comparative successor claim to the already-taught CaMeL-CUA numbers.
- **Potential course lesson:** Lesson 17.2's CUA section: if the exact utility numbers check out against CaMeL-CUA's 77-84%, update the comparison table and add the accessibility-tree-derived trust-boundary mechanism as a second from-scratch CUA defense exercise.
- **Confidence:** medium (direct named-baseline comparison, 0% reported ASR) tempered by single preprint, unconfirmed affiliations, no code, and "much higher utility" not yet given as an exact figure to verify against CaMeL-CUA's published 77-84%.
- **Recommendation:** review for ADD as a direct lesson-17.2 update at the next weekly review — this is the single most actionable item in today's batch, since it claims to beat material already in the course on the course's own terms.

### C-20261015-08 · CoRedSkill: AST-guided compositional attacks hide malicious intent across cooperating agent skills — 98.0% attack success, 3.3% audit-detection rate

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-14
- **Source:** https://arxiv.org/abs/2610.20049 (verified resolves; v1, 14 Oct 2026)
- **Organization/researchers:** Qichen Zhao, Shengfang Zhai, Qingni Shen, Zhonghai Wu, Jiaheng Zhang (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** New entry in `research/deferred/skill-trust-boundary.md` (now at least 9 independent groups). CoRedSkill's mechanism is distinct from prior cluster members: it decomposes a workflow into *interdependent* skills and embeds attack operations via AST rewriting of task functions, so no single skill's individual audit reveals the combined malicious intent — the dependencies and intermediate artifacts between cooperating skills carry the attack.
- **Technical summary:** Benchmark of 150 cases / 50 tasks / 3 attack objectives. Main result: 98.0% attack success, 95.3% task success, 3.3% audit-detection rate, 90.7% joint success (attack + task completion + audit evasion together) vs 6.7-42.7% for four baselines.
- **Why it might matter:** The highest joint attack+evasion number yet in this cluster, and a mechanism (cross-skill compositional attack via code-level AST rewriting) orthogonal to MetaCascade (discoverability-stage) and SkillRelayBench (cross-session) — individual-package auditing specifically cannot catch it by construction.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.20049
- **Code:** none confirmed
- **Relationship to existing course material:** New evidence for `research/deferred/skill-trust-boundary.md`.
- **Potential course lesson:** For the eventual ADD: pair with Beyond Maliciousness (C-20261015-04) and MetaCascade as three distinct stages (real-world capability exposure, discoverability-stage, composition-stage) of the same marketplace trust problem.
- **Confidence:** low-medium (strong numbers, single preprint, unconfirmed affiliations, no code).
- **Recommendation:** fold into the skill-trust-boundary deferred record at its 2026-11-08 review.

### C-20261015-09 · CreepScope: "privilege creep" as a distinct, measurable lifecycle failure separate from per-call authorization correctness

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-11
- **Source:** https://arxiv.org/abs/2610.15988 (verified resolves; v1, 11 Oct 2026)
- **Organization/researchers:** Haoran Yu, Lifei Liu, Danping Zhang, Su Wang, Pin Qian, Yihang Chen, Xiaochong Jiang (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** `research/deferred/agent-tool-authorization-gates.md` and related clusters are about whether a *given* authorization request is correctly granted/denied. CreepScope asks a different question: how long does a capability remain *reachable* after the workflow step that justified it has finished? `lookup "privilege creep"` / `"post-use authorization"` return no course/registry match.
- **Technical summary:** Defines Capability-Step Exposure (CSE, total stepwise overexposure) and Residual Privilege Debt (RPD, terminal residue), separating "stale-after-use" exposure from "never-required" exposure. A 96-cell deterministic replay over 12 workflows: Static Task Scope and Monotonic On-Demand policies retain mean CSEs of 26 and 13; an oracle-controlled Step Lease policy achieves zero CSE/RPD by construction; Full Access adds 91.33 never-required capability-steps. A 24-episode case study with Qwen2 7B: an injected stale "send" action executes in all 9 persistent-policy episodes and in none of the 3 Step-Lease episodes.
- **Why it might matter:** A genuinely distinct failure mode (temporal/lifecycle, not decision-correctness) within the broad authorization-gates family — most of that cluster's existing entries would not catch this, since they evaluate whether a request is approved, not how long an already-approved capability stays reachable afterward.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.15988
- **Code:** none confirmed
- **Relationship to existing course material:** Adjacent to but distinct from `research/deferred/agent-tool-authorization-gates.md`; recorded as a sub-topic of that cluster rather than folded in verbatim, since the failure mode (lifecycle, not decision) differs.
- **Potential course lesson:** A lab-16 extension measuring CSE/RPD for the lab's existing policy before/after adding a Step-Lease-style expiring grant.
- **Confidence:** low-medium (clear metrics and a small controlled replay, but narrow case study, unconfirmed affiliations, no code).
- **Recommendation:** monitor alongside the authorization-gates cluster; flag the lifecycle/temporal angle as a candidate addition if that cluster is ever ADDed.

### C-20261015-10 · DelegateGuard: formally-characterized, purpose-bound capability attenuation for delegated agent workflows, validated at Enron-corpus scale

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-12
- **Source:** https://arxiv.org/abs/2610.16005 (verified resolves; v1, 12 Oct 2026)
- **Organization/researchers:** Phat T. Tran-Truong, Ha Vo, Nhut Tran, Khang Vo, Thai-Minh Truong (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** Another entry in the crowded `research/deferred/agent-tool-authorization-gates.md` cluster, but with a formal safety-invariant proof (Proposition 1, characterizing exactly where attenuation-based authorization suffices) and the largest-scale evaluation seen in that cluster so far (517,401 Enron emails for conformance/scale checks).
- **Technical summary:** Converts the initiating user's authorization into attenuable capabilities over purpose, labels, operations, sinks, and delegation depth; every data-moving action is mediated outside the LLM; revocation cascades through the delegation graph. Blocks ungranted-sink exfiltration, authority amplification, revocation replay, purpose gaming, and intra-tool label violations, dominating static allowlists 10/10 on revocation/intra-tool cases. Two open models proposed attacker-goal actions on 42/45 and 44/45 injected traces, all blocked at execution; a 90-run multi-turn study cut leakage from 0.844 to 0.20 with full task completion, at microsecond per-decision overhead.
- **Why it might matter:** The formal characterization of exactly when attenuation-based authorization is sufficient (not just an empirical pass rate) and the scale of the conformance evaluation are above this cluster's current rigor bar.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.16005
- **Code:** none confirmed
- **Relationship to existing course material:** New evidence for `research/deferred/agent-tool-authorization-gates.md`.
- **Potential course lesson:** No change to that cluster's existing recommendation; DelegateGuard's formal boundary characterization (Proposition 1) is worth citing if a lab-16 extension is eventually written, as the theoretical anchor for "when is attenuation enough."
- **Confidence:** low-medium (real large-scale conformance data, formal result) tempered by unconfirmed affiliations, single preprint, no code.
- **Recommendation:** fold into the agent-tool-authorization-gates deferred record at its 2026-11-15 review; flag as currently the strongest-evidenced entry in that cluster.

### C-20261015-11 · Multi-agent systems leak across topology even with zero compromise: disclosure to unintended recipients rises from 0% to 52.2% purely from coordination topology, with a 150x leakage spread across orchestration frameworks

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-12
- **Source:** https://arxiv.org/abs/2610.16039 (verified resolves; v1, 12 Oct 2026)
- **Organization/researchers:** Sunday Oyinlola Ogundoyin, Muhammad Ikram (affiliations not stated on the abstract page)
- **Category:** agent-security (privacy)
- **What changed:** `lookup "multi-agent topology leakage"` returns no course/registry match — a new sub-topic. The mechanism is explicitly *not* an attack: information disclosed to one authorized agent propagates to an unauthorized one through routine, benign coordination, and conventional sensitivity-based defenses (which only look at content) miss it entirely.
- **Technical summary:** 485 scenarios across coordinator-worker, peer-to-peer, and hierarchical topologies, instrumenting seven communication channels. Disclosure to topology-introduced recipients rises from 0% (no propagation) to 52.2% depending on topology, while "surface leakage" (content-level sensitivity) stays flat at 60.6-62.8% — i.e. content-based detectors would see roughly the same signal regardless of whether the information actually reaches an unauthorized party. Framework choice alone drives a 150x leakage spread. The proposed defense, RECONS (Detect→Decide→Transform), conditions sanitization on recipient and execution context rather than sensitivity alone, reducing residual disclosure from 96.7% to 29.25% while preserving 94.1% of authorized disclosures (vs 20.5% under blanket redaction); detection coverage (not the sanitization step) is responsible for 95.5% of remaining failures.
- **Why it might matter:** A clean demonstration that privacy failures in multi-agent systems are a structural/topological property, not just a content-classification problem — directly relevant to the course's growing multi-agent-systems content, and the RECONS result ("fixing detection coverage, not sanitization quality, is the bottleneck") is a concrete, teachable finding.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.16039
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic adjacent to `research/deferred/multi-agent-covert-collusion.md` (different mechanism — benign propagation vs. deliberate collusion) and `lessons/module-16` (agent memory/data flow).
- **Potential course lesson:** A from-scratch multi-agent topology exercise reproducing the 0%→52.2% effect across the three topologies, then implementing a minimal recipient-conditioned sanitizer to show why content-only filtering misses it.
- **Confidence:** medium (large, systematic evaluation across topologies/frameworks/models) tempered by unconfirmed affiliations, single preprint, no code.
- **Recommendation:** open as a new sub-topic (deferred) at the next weekly review, distinct from the existing covert-collusion entry.

### C-20261015-12 · Logit Leakage through Floating-Point Bias Addition: a numerical side channel in real inference servers (vLLM, SGLang, llama.cpp) recovers exact logits from bias-only APIs

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-12
- **Source:** https://arxiv.org/abs/2610.16790 (verified resolves; v1, 12 Oct 2026)
- **Organization/researchers:** Shaomin Chen, Xiaorui Gong (affiliations not stated on the abstract page)
- **Category:** extraction/inversion/membership
- **What changed:** `lookup "logit leakage"` / `"floating-point side channel"` return no course/registry match. Prior bias-based logit extraction recovers only *relative* logits, leaving a common additive component undetermined "in ideal arithmetic" — this paper shows that real binary32 floating-point arithmetic (as implemented, not idealized) leaks that missing component through token identities alone.
- **Technical summary:** Exploits changes in representable floating-point spacing at binary exponent boundaries to recover a logit pair and its tie-breaking priority exactly in at most 52 token queries; one recovered anchor then determines the full logit vector from complete relative logits. Validated across 11 public checkpoints, 7 model families; end-to-end tests against **vLLM, SGLang, and llama.cpp** (real, widely-used production inference servers) succeed on all 128 tested Qwen3-0.6B inputs including 64 held-out. A separate token-only experiment extracts a pretrained model's complete output-head representation up to an invertible transform. The paper also gives a sufficient mitigation (subtract the maximum before bias addition) and shows it eliminates the observed distinctions while preserving token decisions.
- **Why it might matter:** A genuinely new numerical side-channel mechanism (not a new ASR-style attack on a model's safety behavior, but an exact-recovery side channel in the serving stack's floating-point arithmetic), validated end-to-end against real, named, widely-deployed serving frameworks, with a stated and validated mitigation — the complete attack/defense/cost structure the course favors.
- **Evidence of adoption:** None; research paper only, not a vendor claim. The *targets* (vLLM, SGLang, llama.cpp) are real, widely-adopted serving stacks, which is what makes the finding concrete.
- **Major organizations using it:** None stated as users of the attack; vLLM/SGLang/llama.cpp are open-source projects with broad industry adoption, not stated co-authors or sponsors.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.16790
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic for extraction/inversion coverage; distinct from the EM side-channel item logged yesterday (C-20261014-03, physical/hardware channel) — this is a purely numerical/software channel in the serving arithmetic itself.
- **Potential course lesson:** Extraction-module extension: implement the binary32 spacing-boundary primitive from scratch against a toy bias-only API, then reproduce the mitigation (subtract-max-before-add) and verify it closes the channel.
- **Confidence:** medium-high (concrete, exact-recovery claim validated against real, named serving stacks; mitigation tested) tempered by unconfirmed affiliations, single preprint, no released code.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new extraction/side-channel sub-topic.

### C-20261015-13 · Privacy Conductor: removing access-control decisions from the model entirely — on real HIPAA court-case documents, the best LLM-labeling configuration still permits 11/20 legally prohibited disclosures

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-11
- **Source:** https://arxiv.org/abs/2610.15804 (verified resolves; v1, 11 Oct 2026)
- **Organization/researchers:** Ryan Thornton, Mir Mehedi A. Pritom, Maanak Gupta, Jessee Roberts (affiliations not stated on the abstract page)
- **Category:** rag-security (privacy)
- **What changed:** Existing Contextual-Integrity-based approaches to LLM document retrieval ask the *model* to decide who may receive a document. Privacy Conductor removes that decision from the model: a deterministic gate enforces a policy written by an accountable authority, and the model only ever receives what the requester may already see — the open question becomes the trustworthiness of the document *labels*, not the model's access decision.
- **Technical summary:** On a synthetic clinical corpus (2,520 requester-document flows), the gate reproduces its policy exactly — the remaining risk is entirely in label quality. Across seven configurations / six models (two families), LLM-written labels degrade the policy in every case: models assign a document's sensitivity tier correctly 78-86% of the time but reproduce its full access-control list on as few as 23%. Re-labeling the same documents five times with an identical request changes 13-124 access decisions per configuration (not dependent on the authors' own labels). On **214 flows drawn from real HIPAA court cases**, the most accurate configuration (87.8% label accuracy) still permits 11 of 20 disclosures that the law actually prohibits.
- **Why it might matter:** A clean, well-isolated finding — "LLMs can describe what a document contains but not reliably decide who should receive it" — validated against real legal ground truth (HIPAA case law), not just a synthetic benchmark, with an architectural fix (deterministic gate + human-authored policy) that the course's `.callout.guarantee` pattern fits directly: the gate guarantees exact policy reproduction; it does not guarantee the labels feeding it are correct.
- **Evidence of adoption:** None; research paper only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.15804
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic for RAG/contextual-integrity coverage; complements `C-20261015-03` (Jev) and `AgentCIScope` (this week's contextual-integrity benchmark, logged at C below) with a concrete real-world-grounded negative result and an architectural fix.
- **Potential course lesson:** A RAG-security lab exercise: implement a toy deterministic access gate, then show how LLM-generated sensitivity labels (rather than the gate itself) are the actual point of failure, using a small set of realistic access-control scenarios.
- **Confidence:** medium-high (real legal ground truth, clear separation of gate-correctness from label-correctness) tempered by unconfirmed affiliations, single preprint, no code.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new RAG-security/contextual-integrity sub-topic.

### C-20261015-14 · Cross-model KV cache reuse creates measurable "safety incompatibility": a cheap mitigation (VReparo) cuts attack success from 57.3% to 39.2% while keeping most of the latency win

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-11
- **Source:** https://arxiv.org/abs/2610.15721 (verified resolves; v1, 11 Oct 2026)
- **Organization/researchers:** Zhiwei Lin, Jiahao Liu, Yan Liu, Chengpeng Wang (affiliations not stated on the abstract page)
- **Category:** agent-security (infra, serving-system security)
- **What changed:** `lookup "KV cache reuse safety"` returns no course/registry match — a new sub-topic. Cross-model KV cache sharing (a receiver model reusing a related sender model's prefix KV states to cut prefill compute) is an emerging serving-efficiency technique; this paper is the first to measure its *safety* implications rather than only latency/quality.
- **Technical summary:** Systematic evaluation across sender-receiver model pairs and reuse configurations shows "safety incompatibility" (deviation from the receiver's native, trained-in safety behavior) varies in direction and magnitude by pair/configuration, with value-tensor reuse causing substantially larger deviations than key-tensor reuse in every evaluated pair. The proposed fix, VReparo, learns per-layer/per-KV-head affine maps offline to align reused sender value tensors with receiver-native equivalents before decoding: average HarmBench ASR drops from 57.28% to 39.21% and StrongREJECT score from 0.4215 to 0.2163, while retaining an average 85.62% Time-to-First-Token reduction (i.e. most of the efficiency gain is kept).
- **Why it might matter:** A novel intersection between an inference-efficiency technique (cross-model KV sharing) and alignment/safety — the receiver model's trained safety behavior can be silently overridden by whichever model's cache it borrows from, a failure mode invisible to standard safety evals that only test the receiver model standalone. Directly fits the course's "what PyTorch/the serving stack does under the hood" pattern.
- **Evidence of adoption:** None; preprint only, not a vendor claim. Cross-model KV cache reuse itself is an emerging production technique, not this paper's own invention.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.15721
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic; no existing accepted/deferred file covers KV-cache-level safety interactions.
- **Potential course lesson:** A from-scratch KV-cache-sharing toy demo reproducing the ASR deviation between a "safe" receiver and an "unsafe" sender's cache, then implementing a minimal value-tensor alignment map as the mitigation.
- **Confidence:** medium (systematic multi-pair evaluation, concrete before/after numbers, stated mitigation with cost) tempered by unconfirmed affiliations, single preprint, no code.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new serving-infra/safety sub-topic.

### C-20261015-15 · Changing only the jailbreak-ASR judge model can shift reported attack success by up to 82 percentage points — a training-free "semantic reconstruction game" evaluator reduces this variance

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-13
- **Source:** https://arxiv.org/abs/2610.19306 (verified resolves; v1, 13 Oct 2026)
- **Organization/researchers:** Liam Davis, Romain Emil-Popescu, Suman Jana (Jana: Columbia University, established security/ML researcher — not independently re-verified against this specific paper this run, but the name is consistent with his public research area)
- **Category:** evaluation/benchmark (jailbreak methodology)
- **What changed:** This is not a new attack or defense — it's a methodological finding directly relevant to how every jailbreak ASR number this course might ever cite (including several logged in `staging.md` this week) should be read. `lookup "ASR judge"` / `"jailbreak evaluation methodology"` return no course/registry match.
- **Technical summary:** Shows that swapping only the judge LLM used to score "did this response fulfill the prohibited request" can move reported ASR by up to 82 percentage points on the same attack/response set — existing evaluators commonly mistake refusals or topically-related-but-non-compliant responses for successful attacks. Proposes a training-free "semantic reconstruction game": given only a response, an LLM reconstructs the request its substantive content actually answers (excluding repeated/refused content), then compares that reconstruction against similar decoy requests, allowing abstention when neither matches. Across three off-the-shelf judge LLMs, this reduces mean error against human labels and reduces ASR variance across judges, explicitly prioritizing avoiding false positives (missing some real jailbreaks) over inflating the number.
- **Why it might matter:** This is exactly the kind of "resist hype, be skeptical of a single ASR number" evidence the protocol itself asks for — it quantifies *why* a bare jailbreak ASR claim (several of which this course's own staging doc currently carries) should not be taken at face value without knowing the judge used, and offers a concrete, teachable alternative evaluation method.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated; Columbia University if Jana's affiliation is confirmed (not verified this run).
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.19306
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic for evaluation/methodology coverage; relevant as a caveat to every jailbreak-ASR-citing lesson and to several items in `staging.md` itself.
- **Potential course lesson:** A short "how to read a jailbreak ASR number" methodology section or exercise: reproduce the judge-swap variance on a small response set, then implement a toy version of the semantic reconstruction game.
- **Confidence:** medium-high (credible author, clear and large quantified effect, directly actionable) tempered by single preprint, no code, and the 82-point figure being a maximum rather than typical case.
- **Recommendation:** review for ADD as a methodology note/exercise (not a full lesson) at the next weekly review — low cost, high pedagogical value given how many jailbreak ASR numbers the course already cites or will cite.

### C-20261015-16 · "Pin It on Anyone": certified key-free displacement of multi-bit LLM watermark messages — attacker needs only a few accounts, not the secret key; code released

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-13
- **Source:** https://arxiv.org/abs/2610.18359 (verified resolves; v1, 13 Oct 2026)
- **Organization/researchers:** Paweł Batorski, Przemysław Spurek, Paul Swoboda (affiliations not stated on the abstract page)
- **Category:** defense/guardrail (content provenance) — functionally an attack on provenance
- **What changed:** `research/deferred/ai-content-watermarking.md` (WAIT, next review 2026-10-25) has mostly tracked removal attacks and detection-robustness defenses. This is a new attack class against multi-bit watermarks specifically: rather than removing the watermark, it **displaces the embedded message** (e.g. swapping an embedded account ID for an arbitrary different one) without the secret key.
- **Technical summary:** The attacker needs access to a few accounts capable of generating watermarked output and logits, but not the secret watermarking key; it rewrites text (preserving meaning) so the decoder recovers the attacker's chosen message instead of the original. Gives theoretical upper/lower bounds on attack success as a function of account count, message length, and text ambiguity, and validates empirically against five watermarking methods and four LLMs, with attack success tracking the predicted bounds — high accuracy given enough accounts. Code released: https://github.com/Batorskq/PinIt.
- **Why it might matter:** If multi-bit watermarks are ever relied on for attribution/accountability (e.g. tracing abuse to an account), a certified, key-free displacement attack directly defeats that use case — a provenance mechanism's "what it guarantees" (the embedded ID is authentic) fails even without breaking the cryptographic key.
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** https://github.com/Batorskq/PinIt
- **Paper:** https://arxiv.org/abs/2610.18359
- **Code:** https://github.com/Batorskq/PinIt
- **Relationship to existing course material:** New evidence for `research/deferred/ai-content-watermarking.md` (text-modality, attack side, multi-bit/attribution specifically — distinct from the zero-bit detection-robustness evidence already in that record).
- **Potential course lesson:** Same placement as the deferred topic's existing note; the theoretical bound (attack success vs. account count/message length/ambiguity) is a good from-scratch exercise if that topic is ever taught.
- **Confidence:** medium (theory + empirical validation across 5 methods/4 models, released code) tempered by unconfirmed affiliations, single preprint, no independent replication.
- **Recommendation:** fold into the ai-content-watermarking deferred record at its 2026-10-25 re-review.

### C-20261015-17 · "When the Approved File Is Unchanged": coding-agent/deployment approvals bind the wrong object in 54.6% of real commits — extends yesterday's ZTAC name/object-confusion finding

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-10
- **Source:** https://arxiv.org/abs/2610.15137 (verified resolves; v1, 10 Oct 2026)
- **Organization/researchers:** Md Imran Hossen (sole author, same author as C-20261015-06; affiliation not stated)
- **Category:** agent-security (supply-chain / coding-agent approvals)
- **What changed:** `research/staging.md`'s C-20261014-02 (ZTAC, class A) addressed name-vs-object confusion at the OS object level. This paper identifies the same structural gap one layer up: an approval is recorded against one file (a workflow, script, or command), but the run also reads *other* repository files that decide what the deployment actually does — and an edit to one of those other files after approval passes any check that only looks at the approved file.
- **Technical summary:** In the commit history of 20 public repositories, 296 of 542 commits that change a file the approved run reads (54.6%) leave the approved file itself untouched — all ordinary development, no adversary involved, meaning this is a common, not contrived, condition. Demonstrated concretely on two of those repositories: an edit outside the approved workflow adds a bucket-write policy to a deployed role, and a one-line edit removes the human-approval requirement for high-risk changes — both pass a check on the approved file alone. Defines "authority-set integrity": an approval is sound only if it binds every file the authorized run is configured to read. Coding agents asked to compute this binding compute the digest correctly but bind different file sets run-to-run, so the paper argues the checker must compute the digest itself from a verifiable source (the deployment tool's own input record, or a declared manifest) rather than trust the agent's own claimed scope.
- **Why it might matter:** A concrete, real-repository-history-grounded (not just synthetic) demonstration that the "bind to the approved object" fix (as in ZTAC) still needs to be applied to the *right set* of objects, and that an agent cannot be trusted to self-report that set — directly extends yesterday's ZTAC finding to a different but structurally related layer (approval scope, not object resolution).
- **Evidence of adoption:** None; preprint only, not a vendor claim.
- **Major organizations using it:** None stated; the 20 public repositories are measured subjects, not stated adopters.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.15137
- **Code:** none confirmed
- **Relationship to existing course material:** Directly complements `research/staging.md`'s C-20261014-02 (ZTAC) and `labs/lab-21/` (coding-agent sandboxing); same author as C-20261015-06 above (authorization-scope research agenda).
- **Potential course lesson:** Pair with ZTAC at the weekly review as two halves of the same "bind the approval to what actually matters" lesson: object-identity (ZTAC) and the complete authority set (this paper).
- **Confidence:** medium (real commit-history base rate, concrete demonstrated exploit on two repos) tempered by single-author status, single preprint, no code.
- **Recommendation:** review alongside C-20261014-02 (ZTAC) at the next weekly review as a paired module-21/lab-21 extension.

### C-20261015-18 · "Revocation Is Not Complete at Receipt": transport/receiver acknowledgment of a revoked grant does not mean the effect was actually stopped — 112/225 calls admitted and committed under receiver-selective non-delivery

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-11
- **Source:** https://arxiv.org/abs/2610.15991 (verified resolves; v1, 11 Oct 2026)
- **Organization/researchers:** Lifei Liu, Haoran Yu, Danping Zhang (affiliations not stated on the abstract page; overlaps with CreepScope's author list — same research group's authorization-lifecycle agenda)
- **Category:** agent-security
- **What changed:** New entry in the authorization-gates/revocation family, but specifically targeting *revocation completeness*: the paper shows that "revocation acknowledged" (at issuer commit, transport ack, or receiver persistence) does not establish that every gateway actually enforced the change or that in-flight guarded effects stopped.
- **Technical summary:** Defines C0-C5, a bounded outcome contract from issuer commit through effect prevention, implemented as a persistent monitor over a frozen gateway/call set. Measured across 1,024 gateways / 10,000 effect vectors (descriptive scaling) and a primary experiment using a maintained Keycloak 26.7 identity server, 8 physical agent-tool gateways, Filesystem/PostgreSQL effects, 16 AWS hosts across 3 availability zones: under receiver-selective non-delivery, transport ack and receiver persistence both still succeed, but 112/225 calls (49.78%) are admitted and all 112 commit their effect. An unmodified external MCPMark agent reproduces the same persisted-but-not-enforced boundary on a narrower surface: normal C4 denies all 31 post-barrier calls; selective C3 allows 344 calls and commits 145 effects.
- **Why it might matter:** A concrete, infrastructure-grounded (real Keycloak, real AWS, an unmodified real MCP agent) demonstration that revocation observability is not revocation completeness — a distinct failure mode from "is this request authorized" that the broader authorization-gates cluster doesn't test for.
- **Evidence of adoption:** None; preprint only, not a vendor claim. Keycloak/AWS are real infra used as the test environment, not stated adopters of the C0-C5 contract.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.15991
- **Code:** none confirmed
- **Relationship to existing course material:** New evidence for `research/deferred/agent-tool-authorization-gates.md`, specifically the revocation-completeness angle (distinct from CreepScope's lifecycle-exposure angle, though same research group).
- **Potential course lesson:** Pair with CreepScope (C-20261015-09) at weekly review as two authorization-lifecycle failure modes from the same group: stale-but-still-granted (CreepScope) vs revoked-but-not-yet-enforced (this paper).
- **Confidence:** medium (real infrastructure, an unmodified external agent reproducing the finding on a narrower surface) tempered by unconfirmed affiliations, single preprint, no code.
- **Recommendation:** fold into the agent-tool-authorization-gates deferred record at its 2026-11-15 review, alongside CreepScope.

### C-20261015-19 · Scalable weak-to-strong verifier hardening for agent-training environments — already adopted by the official Terminal Bench repository

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-11
- **Source:** https://arxiv.org/abs/2610.15924 (verified resolves; v1, 11 Oct 2026)
- **Organization/researchers:** Chong Zeng, Ziqian Zhong, Kexun Zhang, Ivan Bercovich, Ivgeni Segal, Yuzhen Mao, Shashwat Saxena, Aditi Raghunathan (Raghunathan: CMU, established ML-robustness researcher — not independently re-verified against this paper this run; affiliations otherwise not stated)
- **Category:** red-teaming (reward-hacking / RL-environment integrity)
- **What changed:** `lookup "verifier hardening"` returns no course/registry match. Agent-training environments use programmatic verifiers to turn outcomes into reward; this paper automates *hardening those verifiers* against reward-hacking exploits at scale, rather than proposing another detector for hacked outputs.
- **Technical summary:** Sets up an isolated verifier sandbox agents cannot modify directly, then runs a "hacker-fixer" loop that automatically finds and repairs exploitable verifier logic. Applied to Terminal Bench, KernelBench, and SETA, substantially reducing attack success in each, with hardening strength scaling with loop-iteration budget (outperforming a static non-iterative baseline). **An earlier version of this hacker-fixer loop has already been adopted by the official Terminal Bench repository** to audit exploits in its own environments — a concrete, named, verifiable adoption claim rather than a release note.
- **Why it might matter:** Real adoption by a named, actively-used benchmark repository is exactly the protocol's bar for "genuinely new evidence...adoption by a major system" — rare among today's otherwise-all-preprint batch, and directly relevant to this course's reward-hacking and automated-redteaming material (last week's multi-agent reward-hacking-transmissibility item, C-20261012-04, is adjacent but distinct: that paper is about hacking *spreading*, this one is about *hardening the verifier so hacks don't work in the first place*).
- **Evidence of adoption:** Yes — stated adoption by the official Terminal Bench GitHub repository (not independently re-verified against that repository this run).
- **Major organizations using it:** Terminal Bench maintainers (via the stated adoption); authors' own affiliations not confirmed.
- **Open-source implementation:** Project page https://verifier-hardening.github.io/ (exact code repo not confirmed from the abstract page).
- **Paper:** https://arxiv.org/abs/2610.15924
- **Code:** project page only confirmed; https://verifier-hardening.github.io/
- **Relationship to existing course material:** New sub-topic adjacent to `research/staging.md`'s C-20261012-04 (reward-hacking transmissibility, still B) and the automated-agent-redteaming / automated-safety-training-loop deferred topics — distinct mechanism (verifier hardening vs. hack propagation/detection).
- **Potential course lesson:** A reward-hacking module exercise: give students a deliberately exploitable verifier (e.g. in a toy coding-agent environment), have them run a simplified hacker-fixer loop, and measure attack-success reduction across iterations — mirrors the course's implement-the-mechanism-then-measure-the-defense pattern, with a real adoption story to cite.
- **Confidence:** medium-high (credible author, real stated adoption, three named benchmarks) tempered by the adoption claim not being independently re-verified and no full code repo link confirmed.
- **Recommendation:** review for ADD or WAIT at the next weekly review; verify the Terminal Bench adoption claim directly against that repository before teaching it as settled.

### C-20261015-20 · BrowseSafe++: a 38,675-pair, largely in-the-wild prompt-injection detection benchmark; trained 0.8B detectors beat frontier-model judges, but adapted attacks still reach 95.4% success

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-12
- **Source:** https://arxiv.org/abs/2610.17457 (verified resolves; v1, 12 Oct 2026)
- **Organization/researchers:** Yuetian Chen, Kaiyuan Zhang, Yuntao Du, Thomas Li, Mark Tenenholtz, Kyle Polley, Jerry Ma, Denis Yarats, Ninghui Li (Yarats and Tenenholtz are known industry ML/agentic-tooling practitioners — not independently re-verified against this paper this run; Ninghui Li is an established security/privacy academic)
- **Category:** detection/monitoring (also evaluation/benchmark)
- **What changed:** `lookup "BrowseSafe"` returns no course/registry match — this is the first sighting of this benchmark line. Extends a prior "BrowseSafe" benchmark from 14,719 pages to 38,675 paired (attacked/clean) pages, with most injections *observed in the wild on production websites* rather than synthetically authored, and every pair provided in four parallel formats (HTML, Markdown, accessibility tree, screenshot).
- **Technical summary:** 12 website types, 24 attack types across 18 page locations. Used to train BrowseSafe-Guard, two 0.8B-parameter detectors (text and screenshot) that both beat a frontier-model-based detector on F1 while keeping false positives and inference cost low. A companion adaptive-attack tool, BrowseSafe-Adapt, revises benchmark injections using live browser-agent feedback: attacks that succeed only a few percent of the time when replayed directly reach up to 95.41% success once adapted — i.e. the benchmark's own injections are not adversarially robust against a motivated, feedback-driven attacker, even though the trained detectors look strong on the static benchmark.
- **Why it might matter:** A real-world-sourced, large, multi-format benchmark with a credible author list (including people from agentic-coding-tool industry backgrounds) plus small, efficient, outperforming detectors — but also a clean demonstration that static-benchmark detector performance overstates real robustness once an attacker adapts, directly reinforcing the course's "benchmarks measure what they measure" skepticism.
- **Evidence of adoption:** None stated for the benchmark/detectors themselves; not a vendor claim.
- **Major organizations using it:** None stated as adopters; author affiliations not confirmed (names are consistent with, but not confirmed as, people at agentic coding-tool companies).
- **Open-source implementation:** Not confirmed on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.17457
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic for prompt-injection-detection coverage; complements `research/deferred/prompt-injection-detector-over-defense.md` (false-positive-cost angle) with the adaptive-attack-robustness angle instead.
- **Potential course lesson:** A detection-module exercise: train a small detector on a subset of BrowseSafe++-style data, then run the adaptive-attack loop against it to reproduce the static-vs-adaptive gap directly.
- **Confidence:** medium (large real-world-sourced dataset, concrete numbers both for and against the detectors) tempered by unconfirmed author affiliations/company ties, single preprint, no confirmed code/data release location.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new detection-benchmark sub-topic; confirm the data/model release location first.

### C-20261015-21 · Forensic debunking of "AI agent escaped containment" reports: the real mechanism is a reproducible cryptographic-verification-bypass CVE (CVE-2026-65616), not emergent coordination

- **Class:** B
- **Date discovered:** 2026-10-15
- **Date published:** 2026-10-14
- **Source:** https://arxiv.org/abs/2610.20437 (verified resolves; v1, 14 Oct 2026)
- **Organization/researchers:** Alicia Colmenero-Fernández (sole author; affiliation not stated)
- **Category:** infra-vuln/CVE (also agent-security)
- **What changed:** `lookup "RLHF privilege escalation"` returns no course/registry match. This paper responds directly to mid-2026 media reporting that claimed frontier LLM agents "escaped server containment through emergent coordination and cloud infrastructure attacks" during OpenAI's internal ExploitGym evaluations — exactly the kind of sensationalized claim the course's DOCUMENTED-vs-SPECULATION distinction exists to cut through.
- **Technical summary:** Forensically recreates both the training-case conditions (a "Highly Persistent Internal Model" scenario) and the "Phase One" privilege-escalation incident in isolated containerized repository servers, and reproduces the actual mechanism: a cryptographic verification bypass (**CVE-2026-65616**) in misconfigured internal package-repository servers, where token forgery and privilege escalation were achievable through ordinary HTTP requests plus Python/JavaScript — no emergent coordination required. The paper shows the training-example conditions and the real "Phase One" misconfiguration share the same exploitable pattern, and explains how Zero Trust Architecture principles would close that specific attack vector.
- **Why it might matter:** A rare, concrete "the hyped story had a boring, reproducible, fixable root cause" finding, anchored to a real CVE — directly useful for this course's module on distinguishing documented AI-security incidents from speculative/sensationalized reporting, and for teaching Zero Trust as a concrete mitigation for a real, named vulnerability class (misconfigured internal repo-server auth) rather than an abstract principle.
- **Evidence of adoption:** N/A — this is a forensic analysis of an already-occurred incident and a named CVE, not a new technique seeking adoption.
- **Major organizations using it:** OpenAI is the subject of the analyzed incident (ExploitGym evaluations), not a stated co-author or endorser of this paper's conclusions.
- **Open-source implementation:** Containerized recreation stated but not confirmed as released on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.20437
- **Code:** not confirmed
- **Relationship to existing course material:** New sub-topic; no existing accepted/deferred file covers this specific incident or CVE. Worth cross-checking CVE-2026-65616 directly against NVD/vendor advisories before citing.
- **Potential course lesson:** A case-study exercise in distinguishing documented mechanism from speculative framing: give students the original hyped reporting and this paper's forensic reconstruction side by side, then have them reproduce the token-forgery bypass in a toy containerized repo server and apply a Zero-Trust fix.
- **Confidence:** medium (specific CVE, containerized recreation, directly addresses a real public claim) tempered by single-author status, single preprint, the CVE itself not independently verified against NVD this run, and reliance on "mid-2026 reporting" whose accuracy is itself part of what's being contested.
- **Recommendation:** verify CVE-2026-65616 against NVD/an official advisory before the next weekly review; if confirmed, worth a short case-study note even independent of a full lesson, given its direct relevance to the course's hype-skepticism stance.

### C-20261016-01 · Anthropic Frontier Red Team: small open-weight models may be "months away" from self-replicating end-to-end across cheap, insecure IoT devices with no datacenter involved

- **Class:** B
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-12
- **Source:** https://www.anthropic.com/research/self-replicating-ai (verified resolves; org research blog post, authors William Zhou and Daniel Freeman, Anthropic Frontier Red Team)
- **Organization/researchers:** Anthropic Frontier Red Team (William Zhou, Daniel Freeman)
- **Category:** red-teaming
- **What changed:** `lookup` for "self-replicat", "weight-based replicator", "autonomous replication", "Frontier Red Team", "IoT worm", and "Memento" all return no course/registry match — this is new threat-modeling territory, not an extension of any accepted/deferred/rejected topic or existing lesson.
- **Technical summary:** Threat-models "weight-based replicators" — worms that carry/download their own model weights and run inference on compromised hardware instead of a datacenter. Built "Memento," a harness on the open-source Pi coding agent that periodically restarts with notes inherited from the prior instance (Lamarckian adaptation). Measured real throughput on 15 ~$55 Android TV boxes (Gemma4-26B-A4B via pipeline parallelism across the fleet: 0.39 tok/s; a 9B model ran on 8 of 9 tested hardware types). An 8-node GCP-firewalled Android-emulator network was used for an end-to-end replication test (cyber-exploit step deliberately trivial — unauthenticated ADB — so the result is stated as an upper bound, not a real-world estimate). GLM-5.2 and stronger open-weight models could already replicate end-to-end in this simplified setting; models ≤30B make mistakes chaining individual steps today but, extrapolated from the cited Epoch Capabilities Index trend (+13.7 ECI/year), could cross that bar by end of 2026. Six generations of Qwen3.5-9B with inherited notes raised inference-setup success from ~45% to 61-84%; giving a small model a frontier advisor (Opus 4.8) did not meaningfully help. Estimated doubling time of days at botnet scale, with no central point to shut down; blue-team mitigations discussed: ISP flow-monitoring for anomalous device-to-device traffic, quarantine-and-notify (citing Mirai remediation precedent), and manufacturer-side default-credential hardening (citing UK IoT rules).
- **Why it might matter:** A concrete, primary-source (not secondhand) threat model for agentic/autonomous-replication risk with measured numbers on real low-cost hardware, a reusable R₀/doubling-time framing, and a stated blue-team mitigation stack with a real-world precedent (Mirai) — directly on-topic for this course's purple-team cycle and distinct from every attack surface already taught (this is infra/botnet-level, not prompt-injection or agent-tool-authorization).
- **Evidence of adoption:** None; this is Anthropic's own red-team research report, not a vendor product claim, but it is a single organization's unreviewed publication — treat numbers as that org's own measurement, not independently verified.
- **Major organizations using it:** None stated.
- **Open-source implementation:** "Memento" harness built on the open-source Pi coding agent; no repository link given on the page.
- **Paper:** https://www.anthropic.com/research/self-replicating-ai (blog-style research report; no separate arXiv/PDF linked)
- **Code:** none confirmed
- **Relationship to existing course material:** New topic — closest existing material is agent-security/autonomous-agent-risk generally, but no accepted/deferred/rejected file or lesson covers self-replication, weight-based worms, or R₀-style spread modeling.
- **Potential course lesson:** A new agentic-security module or lesson on autonomous replication & adaptation (ARA): from-scratch exercises computing a toy R₀/doubling time, simulating pipeline-parallel inference setup across heterogeneous "devices," and a guarantee-box for the mitigation stack (traffic-anomaly monitoring detects bulk weight transfer and sustained device-to-device chatter / does not guarantee against low-and-slow spread; quarantine-and-notify cleared most Mirai infections / does not harden the devices themselves).
- **Confidence:** medium (detailed methodology, real hardware measurements, explicit upper-bound caveat from the authors themselves) tempered by single-organization source, no peer review, and no independent replication yet.
- **Recommendation:** monitor for the next weekly review as a new WAIT topic; revisit sooner if an independent group reproduces the end-to-end replication result, or if the authors' own cited capability trend crosses their stated end-of-2026 threshold.


### C-20261016-02 · "My Credentials, Please": filesystem capability laundering in MCP servers at scale, with two confirmed CVEs in Anthropic's own Git MCP Server

- **Class:** A
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.22301 (verified resolves)
- **Organization/researchers:** Zeqian Huang, Mingyue Tang, Aonan Guan, Qiming Sun, Pengzhou He (affiliations not stated on the abstract page)
- **Category:** tool/mcp-security
- **What changed:** `lookup "filesystem capability laundering"` and `"MCP server filesystem permission"` return no exact match — the course teaches MCP trust-boundary/tool-poisoning conceptually (module-18, module-19) and a fuzzing angle is already staged (ToFu, C-20261012-03), but neither covers this specific mechanism: a tool's registry/metadata *category* under-declares what filesystem access its approval actually grants.
- **Technical summary:** Built MCP-FSD, a tool that catalogs MCP servers, infers each tool's declared vs. actual filesystem access boundary from its own contract, plants credential fixtures outside that boundary, and dynamically tests exploitability under real sandbox policies. Scanned 21,097 servers across nine registries; of 4,806 triaged servers, 787 (16.4%) had filesystem capabilities despite being classified under non-filesystem categories (so a user/approval system screening by declared category would miss them). Dynamic testing confirmed 150 exploitable instances under the sandbox policies tested. Coordinated disclosure produced 13 security advisories, including two CVEs against Anthropic's own Git MCP Server.
- **Why it might matter:** Real, disclosed CVEs (not a synthetic demo) in a well-known vendor's own MCP server, at a scale (21k servers scanned) that turns "tool descriptions can lie" from a conceptual lesson point into a measured, widespread real-world gap — directly extends the course's MCP trust-boundary material with a concrete, disclosed mechanism and a reusable scanning methodology.
- **Evidence of adoption:** None stated as adoption of MCP-FSD itself; the finding is validated by the coordinated-disclosure process (13 advisories accepted, 2 CVEs issued), which is independent confirmation of impact, not a vendor marketing claim.
- **Major organizations using it:** Anthropic's Git MCP Server was one of the vulnerable targets (not an adopter of the scanning tool).
- **Open-source implementation:** Not confirmed on the abstract page — only generic third-party aggregator links shown; check the full PDF for an MCP-FSD repo.
- **Paper:** https://arxiv.org/abs/2610.22301
- **Code:** none confirmed
- **Relationship to existing course material:** Extends `lessons/module-18/lesson-01.md` and `lessons/module-19/lesson-01.md` (MCP architecture, trust boundaries, malicious/misdescribed tools) and is distinct from the already-staged ToFu fuzzing angle (C-20261012-03, semantic input-validation bugs) — this is a classification/approval-boundary gap, not an input-sanitization gap.
- **Potential course lesson:** A `lab-19`-style exercise: given a tool's declared category/metadata, derive its claimed filesystem boundary, then probe (against the lab's own mock MCP servers) whether the implementation actually enforces it — mirroring MCP-FSD's static-contract-vs-dynamic-test methodology at lab scale.
- **Confidence:** medium-high (real, independently-adjudicated CVEs via coordinated disclosure; very large scan; concrete, reproducible methodology) tempered by single preprint status and no confirmed public code release yet.
- **Recommendation:** review for ADD at the next weekly review as an M18/M19 extension; the two confirmed CVEs are independently verifiable evidence, which is unusually strong for a 1-day-old preprint.

### C-20261016-03 · Effect Binding and Trusted Rendering for Agent Step-Up Authorization (ASU): formally-verified, adversarial framing of "human approval" for agent actions, with a real-runtime audit and released code

- **Class:** A
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.21063 (verified resolves)
- **Organization/researchers:** Sai Varun Kodathala, Prashanth Pollishetty, Jaylen Cargill (affiliations not stated on the abstract page)
- **Category:** agent-security
- **What changed:** `lookup "agent approval second factor"` and `"excessive agency agent authorization"` find only the existing, *non-adversarial* deferred topic `research/deferred/proactive-over-authorization.md` (OverAct: benign over-retrieval, no attacker). This paper is the adversarial counterpart — a compromised/manipulated agent forging or stretching a user's approval — which is a distinct topic the registry does not yet track.
- **Technical summary:** Defines twelve attacks on the agent-approval path (substitution, replay, grant-stretching, forged narration, flooding) and audits ten real agent runtimes' approval mechanisms (Agent Payments Protocol/AP2, Microsoft's action-bound approval design, MCP elicitation), finding no third-party-verifiable approval records in any, no measurable rate limits on approval flooding where testable, and post-approval argument changes in 4 of 8 runtimes with measurable binding. Proposes ASU (Agent Step-Up): a reference gateway that renders the approval card from a canonical effect description, has the user's phone passkey sign a digest of that card, and executes only the exact stored call. Tamarin-proves binding/single-use/non-repudiation under three stated hypotheses. In 27,108 scripted trials and 609 AgentDojo attack pairs, ASU blocked substitution/replay/grant-stretching and cut forged-narration attack success from 0.54 to 0.03; with 15 LLMs as automated approvers, catch rate rose 0.30→0.98 at a 16% false-refusal cost on harmless near-misses (authors attribute most of that cost to a stimulus artifact). Caveats reported by the authors themselves: a second device added nothing over trusted on-host confirmation, flooding still succeeded 45-60% against a modeled approver, and approval cannot stop effects a policy already permits.
- **Why it might matter:** OWASP's 2026 LLM Top 10 moved Excessive Agency up to #3; this paper gives the course's `.callout.guarantee` pattern a concrete, formally-verified case (what a signed approval card guarantees — binding, single-use, non-repudiation / what it does NOT guarantee — flooding resistance, or blocking actions a policy already permits) backed by a real audit of production-shaped protocols (AP2, MCP elicitation) and a released reference implementation.
- **Evidence of adoption:** None stated for ASU itself; the audit findings (no verifiable approval records in any of 10 runtimes tested) are the authors' own measurement, not independently re-verified this run.
- **Major organizations using it:** None stated; AP2 and MCP elicitation are real, named protocols audited as targets (not implying ASU is adopted by them).
- **Open-source implementation:** https://github.com/Sports-Vision-Inc/agent-step-up (code, data, and Tamarin proofs stated as released)
- **Paper:** https://arxiv.org/abs/2610.21063
- **Code:** https://github.com/Sports-Vision-Inc/agent-step-up
- **Relationship to existing course material:** New, adversarial sibling to the deferred `proactive-over-authorization` topic (non-adversarial excessive agency); also extends `lessons/module-00/lesson-01.md`/`module-02/lesson-02.md` (OWASP LLM06 Excessive Agency) and `module-17/lesson-02.md` (agent authorization) with a formally-verified approval-binding mechanism not currently taught.
- **Potential course lesson:** A module-17/21 lesson or lab on approval-path forgery: implement a toy "approval card" signing scheme, then run a scaled version of the paper's own substitution/replay/forged-narration attacks against both an unprotected and an ASU-style protected approval flow, using the released code as a reference.
- **Confidence:** medium-high (formal verification, large-scale trials against a real agent-attack benchmark (AgentDojo), a real-runtime audit, and released code/proofs) tempered by single preprint status, authors' own self-reported caveats (flooding, second-device result), and no independent replication yet.
- **Recommendation:** review for ADD at the next weekly review; the released code plus Tamarin proofs make this unusually teachable as-is, and it directly answers the proactive-over-authorization deferred topic's open question of what an *adversarial* excessive-agency defense looks like.

### C-20261016-04 · LinguaGuardBench: translating only the user instruction flips verdicts on most open/purpose-built LLM safety guards — a new cross-lingual attack surface on guardrails themselves

- **Class:** A
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.22244 (verified resolves)
- **Organization/researchers:** Hasan Demirkiran, Jens Ernstberger (affiliations not stated on the abstract page)
- **Category:** defense/guardrail
- **What changed:** `lookup "multilingual jailbreak guard"` matches only `lessons/module-04/lesson-01.md`'s general mention of "multilingual" as one bullet in a list of obfuscation axes for attacking the *model*; `lookup "cross-lingual safety guard evasion"` returns no match. No existing course/registry material tests whether the *guard/classifier layer itself* (as opposed to the underlying model) is reliable across languages.
- **Technical summary:** Built LinguaGuardBench by translating only the user instruction into five languages (German, French, Turkish, Swahili, Amharic) while holding everything else (task, scenario, agent context) fixed, then additionally testing English paraphrases as a control. Ran 19 real safety-guard systems (mix of smaller open/purpose-built guards and frontier-model-based guards) and collected 489k verdicts, released as a dataset alongside the benchmark. Finding: most smaller, open, and purpose-built guards change their verdict under translation alone, with the effect larger for lower-resource languages (Swahili, Amharic); frontier-model-based guards shift much less. English paraphrasing also shifts verdicts, but less than translation does.
- **Why it might matter:** A guard flipping its verdict purely from translating the user's text (task, model, and agent context all held fixed) is a clean, measured instance of "the defense has an attack surface of its own" — exactly the purple-team pattern (attack → observe → detect → mitigate) this course teaches, applied to the guardrail layer itself rather than the target model, with a released 489k-verdict dataset for reproducibility.
- **Evidence of adoption:** None stated; this is the authors' own benchmark result, not a vendor claim about any specific guard product.
- **Major organizations using it:** None named as adopting LinguaGuardBench; the 19 guards tested are real deployed-style systems, not named vendors on the abstract page.
- **Open-source implementation:** Benchmark and the 489k verdicts stated as released; no specific repository URL confirmed from the abstract page — check the full PDF.
- **Paper:** https://arxiv.org/abs/2610.22244
- **Code:** dataset stated as released (489k verdicts); repo URL not confirmed
- **Relationship to existing course material:** New sub-topic adjacent to `lessons/module-04/lesson-01.md` (multilingual obfuscation against the target model) and the guardrail/defense material generally — this is the first course-adjacent evidence of multilingual evasion of the *guard layer*, not the model.
- **Potential course lesson:** A guardrail lesson/exercise: take a small open guard model, run the paper's translate-only-the-instruction protocol against it in 2-3 languages, measure verdict flip rate, and pair with the `.callout.guarantee` box (a guard trained/evaluated mostly in English guarantees little about its verdict stability under translation / does not guarantee uniform coverage across languages it wasn't tuned on).
- **Confidence:** medium-high (19 real guards tested, large released dataset, a clean held-fixed-except-language experimental design) tempered by single preprint status and no independent replication yet.
- **Recommendation:** review for ADD or WAIT at the next weekly review as a new guardrail-evasion sub-topic; the released dataset makes an independent spot-check feasible before teaching it.

### C-20261016-05 · Poisoning the Neighborhood: topology-aware, topic-level RAG poisoning that targets HNSW approximate-index structure directly (2M-document scale)

- **Class:** B
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.21464 (verified resolves)
- **Organization/researchers:** not stated on the abstract page
- **Category:** rag-security
- **What changed:** `lookup "HNSW RAG poisoning"` matches only `lessons/module-14/lesson-01.md`'s background mention of ANN/HNSW as infrastructure the module builds on, not as an attack surface in its own right — existing course RAG-poisoning material (and the registry) assumes exact/near-exact retrieval, not approximate-index graph structure.
- **Technical summary:** Argues that prior RAG-poisoning attacks assume exact retrieval and weaken under real large-scale approximate HNSW indexes. Proposes a topic-level attack arranging poisoned documents into "Hub" and "Satellite" roles within the HNSW graph so poisoned content reaches across semantic neighborhoods and generalizes to unseen topics, paired with an entity-claim method for the generation-stage payload. Reports over 72% retrieval success and 31.29% end-to-end attack success on a 2M-document Wikipedia-scale corpus, and states that tested existing defenses do not mitigate it.
- **Why it might matter:** If it holds up, this shifts RAG-poisoning threat modeling from "the retriever returns the wrong exact-match chunk" to "the attacker can engineer the index's own graph topology to be reachable from many queries" — a meaningfully different, more scalable mechanism than what module-14 currently teaches, with claimed defense-evasion at realistic (2M-doc) scale.
- **Evidence of adoption:** None stated; single preprint, not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not confirmed from the abstract page.
- **Paper:** https://arxiv.org/abs/2610.21464
- **Code:** none confirmed
- **Relationship to existing course material:** Extends `lessons/module-14/lesson-01.md` (RAG/embeddings/ANN background) with a graph-topology-specific attack not currently taught; no existing deferred/accepted file matches.
- **Potential course lesson:** A module-14 lab extension: build a small HNSW index, implement a toy Hub/Satellite poisoning insertion, and measure retrieval reach into unseen-topic queries versus a naive single-point poisoning baseline.
- **Confidence:** medium (large-scale eval, a structurally distinct and plausible mechanism) lowered because the abstract alone doesn't allow checking baselines/related-work claims, authors/affiliations are unstated, and no code is confirmed.
- **Recommendation:** monitor; worth a full-PDF read to confirm novelty against prior HNSW-aware poisoning work and check for a code release before the next weekly review.

### C-20261016-06 · Screwtape: adversarial transcript editing shows real monitor-evasion attacks that transfer to a held-out frontier developer's own monitor

- **Class:** B
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-14
- **Source:** https://arxiv.org/abs/2610.20941 (verified resolves)
- **Organization/researchers:** Gosha Kozhevnikov, Tyler Tracy (affiliations not stated; transcripts sourced from Redwood Research staff)
- **Category:** detection/monitoring
- **What changed:** `lookup "monitor red-teaming transcript"` returns no match — the course and registry have detection/monitoring coverage generally (several 2026-10-15 items) but nothing specifically on adversarially editing real agent transcripts to find monitor blind spots, nor any item showing transfer to a different organization's own held-out monitor.
- **Technical summary:** Screwtape edits real AI-agent transcripts (94 Claude Code and Codex transcripts from Redwood Research staff) so that a specified harm (e.g., leaking an API key) is hidden from an action-only monitor, using an LLM verifier to reject edits inconsistent with the original transcript or below a severity bar. 252 runs produced 35 verifier-passing attacks that evaded the authors' own monitors; 6 of these, confirmed by human review, also evaded a held-out monitor belonging to a different, frontier AI developer.
- **Why it might matter:** Monitor-evasion attacks that transfer across organizations (not just against the authors' own monitor) are a stronger signal than a single-org benchmark number, and the stated purpose — developers using these attacks to find and fix their own monitor blind spots — is a direct purple-team workflow example (attack → observe → mitigate) for AI-safety monitoring specifically.
- **Evidence of adoption:** None stated beyond the cross-org transfer result itself (6 confirmed cases against a named-as-frontier-but-unnamed developer's monitor); not a vendor claim.
- **Major organizations using it:** Transcripts sourced from Redwood Research; a separate, unnamed frontier AI developer's monitor was used as the held-out test (not stated as an adopter of Screwtape).
- **Open-source implementation:** not confirmed on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.20941
- **Code:** none confirmed
- **Relationship to existing course material:** New sub-topic within detection/monitoring; adjacent to but distinct from existing agent-oversight/monitor material already staged this week.
- **Potential course lesson:** A detection/monitoring lesson exercise: given a toy action-only monitor and a small set of synthetic "harmful" trajectories, have students attempt small, verifier-constrained edits to evade it, then test whether the same edits evade a second, independently-built toy monitor — making the cross-monitor-transfer finding concrete at lab scale.
- **Confidence:** medium (real transcripts, a held-out cross-org evasion result) lowered by small sample size (6 confirmed cross-org evasions, 35 total), single preprint, and no independent replication.
- **Recommendation:** monitor; the cross-org transfer result is the most interesting part and worth re-checking once (or if) a full PDF or follow-up names the held-out developer/monitor.

### C-20261016-07 · Shortcut Sensitivity in Agent-Safety Evaluations: a methodology audit showing several real agent-safety benchmarks reward superficial cues, not safety

- **Class:** B
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.22243 (verified resolves)
- **Organization/researchers:** Hasan Demirkiran, Jens Ernstberger (same authors as C-20261016-04)
- **Category:** evaluation/benchmark
- **What changed:** `lookup` for benchmark-validity/shortcut-learning terms returns no match in the registry; the course's `lessons/module-24/lesson-01.md` already teaches benchmark-coverage criteria generally but has no worked example of shortcut-learning specifically invalidating agent-safety benchmark results.
- **Technical summary:** Introduces a three-level audit (label-predictability from superficial cues; statistical association between a guard's verdict and those cues; paired minimal-edit sensitivity) applied to LinuxArena trajectories and two TS-Bench-derived datasets. Findings: in LinuxArena, shorter shell commands alone strongly predict trajectory labels; on AgentDojo-Traj, exact-tool-lookup performance drops sharply on held-out domains; on AgentHarm-Traj, a guard's F1 changes materially depending on whether interactions are weighted equally or per-row. A controlled test found that rewriting one surface marker or using opaque tool aliases changed the false-positive rate on safe calls (no unsafe call was ever missed) for one model-based guard, but the effect did not reproduce with other models or a deterministic guard.
- **Why it might matter:** This is a direct challenge to taking agent-safety benchmark numbers (including ones already referenced in this course's own evaluation material) at face value — useful less as a new attack than as a "how to read a benchmark skeptically" worked example, which fits the course's existing resist-hype stance.
- **Evidence of adoption:** None stated; methodology paper, not a vendor claim.
- **Major organizations using it:** none stated; LinuxArena, AgentDojo, AgentHarm are the audited (not adopting) benchmarks.
- **Open-source implementation:** not confirmed on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.22243
- **Code:** none confirmed
- **Relationship to existing course material:** Extends `lessons/module-24/lesson-01.md` (benchmark/evaluation coverage criteria) with a concrete shortcut-learning audit methodology; no existing deferred/accepted topic matches.
- **Potential course lesson:** A module-24 exercise: take one of the course's own small evaluation sets, run a cheap shortcut-predictability check (can a trivial feature like command length predict the label?), and discuss what that does and doesn't invalidate about the eval.
- **Confidence:** medium (concrete, replicated-within-paper methodology across 3 real datasets) lowered because the controlled "surface marker" effect didn't reproduce across models in the authors' own test, and it's a single, unreplicated preprint.
- **Recommendation:** monitor; low urgency (methodology/meta point rather than a new attack or defense) but useful for module-24 if the weekly review wants a concrete shortcut-learning worked example.

### C-20261016-08 · BiShield-TEE: breaks two representative on-device TEE weight-obfuscation schemes (GroupCover, ArrowCloak) via a "Solution Determinacy" weakness, proposes a bidirectional fix with released code

- **Class:** B
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.21565 (verified resolves)
- **Organization/researchers:** Zhiyuan Wang, Yuezhi Zhou, Ziqi Zhang, Zhu Zhang, Zhixing Tan, Yongheng Deng (affiliations not stated on the abstract page)
- **Category:** supply-chain
- **What changed:** `lookup "TEE weight obfuscation"` matches only generic `.callout.guarantee` boilerplate in unrelated lessons, not this specific topic — on-device TEE-based model-weight protection is not currently covered.
- **Technical summary:** Identifies the "Solution Determinacy Property" in representative TEE-based weight-obfuscation schemes (GroupCover, ArrowCloak): the obfuscation secret is uniquely determined by the observable output, letting an attacker recover it, reducing both schemes to negligible real-world protection under the authors' attack. Proposes BiShield-TEE, which obfuscates both input and output dimensions so many equally-valid candidate keys exist, limiting attack accuracy to a full-shielding black-box baseline while improving on-device inference efficiency versus full shielding. Code released on GitHub.
- **Why it might matter:** A concrete attack-then-defense pair (break two named real schemes, then measure a fix) on an on-device/edge-LLM model-protection mechanism — a supply-chain/IP-protection angle the course doesn't currently cover, with both code and a clear before/after security argument, which fits the course's attack→defense teaching pattern well if the audience includes on-device deployment.
- **Evidence of adoption:** None stated for BiShield-TEE; GroupCover and ArrowCloak are named as "representative" existing schemes, not confirmed as widely deployed products.
- **Major organizations using it:** none stated.
- **Open-source implementation:** https://github.com/laduiw/BiShield-TEE
- **Paper:** https://arxiv.org/abs/2610.21565
- **Code:** https://github.com/laduiw/BiShield-TEE
- **Relationship to existing course material:** New sub-topic; no existing lesson or registry file covers TEE-based on-device weight obfuscation specifically.
- **Potential course lesson:** A supply-chain/model-protection lesson or lab: implement a toy single-sided weight-obfuscation scheme, demonstrate the Solution Determinacy attack recovering the secret, then implement the bidirectional fix and measure how the candidate-key space grows.
- **Confidence:** medium (named real-world target schemes, released code, clear before/after measurement) lowered by single preprint status, unstated affiliations, and the niche (on-device/edge) deployment scope relative to this course's mostly cloud/API-served LLM focus.
- **Recommendation:** monitor; relevant mainly if the weekly review wants an on-device/edge-deployment supply-chain angle — otherwise lower priority than C-20261016-02/03/04 this week.

### C-20261016-09 · DAR (Discover-and-Relabel): a label-only backdoor (no visible trigger) that survives clean-data knowledge distillation — NeurIPS 2026, vision/CLIP domain

- **Class:** B
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.21208 (verified resolves; "Comments" field states accepted to NeurIPS 2026, not independently re-verified against the program this run)
- **Organization/researchers:** Junhoo Lee, Baekseung Kim, Seungyeon Kim, Nojun Kwak (affiliations not stated on the abstract page)
- **Category:** poisoning/backdoor
- **What changed:** The course teaches backdoors that survive safety *training* (sleeper agents, module-11) but nothing on backdoors specifically engineered to survive clean-data knowledge *distillation*, which is a commonly assumed backdoor-removal step. `lookup` for distillation-survival/clean-label-backdoor terms returns no match.
- **Technical summary:** DAR finds naturally-occurring patterns in a model's own low-dimensional feature subspace via clustering, then relabels only the samples that already match those patterns (no synthetic trigger pattern is added to any input). At test time the attacker activates the backdoor by locally perturbing the matching subspace of an input image. Matches state-of-the-art backdoor attack accuracy on ImageNet classification and CLIP-based prompt tuning, and the authors report attack success stays above 96% after clean-data distillation, where prior trigger-based backdoors are assumed to be removed.
- **Why it might matter:** If it generalizes, "clean data removes backdoors via distillation" is a load-bearing assumption in some model-provenance/supply-chain defense thinking; this paper is a peer-reviewed (NeurIPS 2026) counterexample. It is directly relevant to the course's backdoor-persistence framing (module-11) even though validated only in the vision/CLIP domain, not on LLM text generation.
- **Evidence of adoption:** None stated; peer-reviewed research result, not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** a project page is linked (junhoo.me/backdoor); whether it hosts code could not be confirmed from the abstract page alone.
- **Paper:** https://arxiv.org/abs/2610.21208
- **Code:** project page stated, content not confirmed
- **Relationship to existing course material:** Adjacent to `lessons/module-11/lesson-01.md` / `papers/11-hubinger-sleeper.md` (backdoors surviving safety training) — this is a distinct survival mechanism (surviving distillation, not RLHF/safety fine-tuning) and a distinct domain (vision/CLIP, not LLM text).
- **Potential course lesson:** If the weekly review wants to broaden module-11's backdoor-persistence framing beyond RLHF-survival, a short aside noting that distillation-based "cleaning" has a published counterexample, with a pointer to the paper rather than a full from-scratch vision implementation (domain mismatch with the course's LLM focus).
- **Confidence:** medium (peer-reviewed venue, matches SOTA attack accuracy, explicit distillation-survival claim) lowered because validation is vision/CLIP-only, not LLM text generation, and this run could not confirm a working code release.
- **Recommendation:** monitor; lower priority than the three A items this week given the domain mismatch (vision classification vs. this course's LLM/agent focus).

### C-20261016-10 · Two more independent groups (ExecWeave, Matoi) converge on the tool-agent execution-provenance/authorization-audit problem already tracked as a deferred topic

- **Class:** B
- **Date discovered:** 2026-10-16
- **Date published:** 2026-10-15 (both)
- **Source:** https://arxiv.org/abs/2610.21146 (ExecWeave); https://arxiv.org/abs/2610.21394 (Matoi) — both verified resolve
- **Organization/researchers:** not stated on either abstract page
- **Category:** agent-security
- **What changed:** `research/deferred/execution-audit-provenance.md` (status WAIT, next review 2026-11-29) already tracks two papers on claim-anchored execution contracts / provenance-spoofing for tool-agent audit trails. These are two more, independent groups tackling closely related ground this same week, which per the daily protocol's non-duplicate rule counts as new evidence for the deferred topic (recorded as B, not D) rather than a fresh topic.
- **Technical summary:** **ExecWeave** is a local-first system that fuses application-level provider semantics with independently observed OS-level runtime events (file/network effects) into a typed execution graph, keeping source artifacts separate and recording attribution/inference/causal-status metadata; an optional command-to-process correlator adds only a non-causal inferred link when a bounded search finds a unique compatible process, and the authors explicitly caveat that uniqueness does not guarantee causal correctness. **Matoi** separates reusable "consequence evidence" from current execution authority and durable occurrence history, so a consumer only reuses evidence it has itself checked and whose observations still hold; evaluated against scripted synthetic tools, not autonomous agents, and the authors themselves describe it as a bounded, auditable reuse contract rather than a production system.
- **Why it might matter:** Three independent groups now converging on "how do you attribute and audit what a tool-agent actually did, without trusting a self-reported log" within about six weeks is a real signal of a recognized gap, strengthening (without yet resolving) the existing deferred topic; ExecWeave in particular adds a working local-first system rather than just a formal contract.
- **Evidence of adoption:** None stated for either; both are preprints with no reported deployment.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not confirmed for either from the abstract pages.
- **Paper:** https://arxiv.org/abs/2610.21146 ; https://arxiv.org/abs/2610.21394
- **Code:** none confirmed for either
- **Relationship to existing course material:** Both extend `research/deferred/execution-audit-provenance.md` (topic ID execution-audit-provenance, WAIT, next review 2026-11-29); also touches `lessons/module-19/lesson-01.md` / `module-22` provenance material already taught.
- **Potential course lesson:** No change yet; fold both into the existing deferred record as further corroborating (not yet resolving) evidence at its next scheduled review.
- **Confidence:** low-medium (Matoi's synthetic-tools-only evaluation and explicit "not production ready" framing; ExecWeave has no measured attack-resistance numbers, just a system description) — both single, unreplicated preprints.
- **Recommendation:** fold into the execution-audit-provenance deferred topic's evidence list at its 2026-11-29 review; do not open a separate topic file.

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


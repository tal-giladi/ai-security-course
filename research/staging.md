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


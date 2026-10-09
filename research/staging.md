# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261005-01 · Hop-Decayed Influence (HDI): GraphRAG's auxiliary schema-level structures are an unprotected 1:N poisoning surface

- **Class:** A
- **Date discovered:** 2026-10-05
- **Date published:** 2026-10-01
- **Source:** https://arxiv.org/abs/2610.02373
- **Organization/researchers:** Jisung Park, John Le, Heath Cooper (affiliation not stated on the abstract page). Peer-reviewed book chapter, DOI 10.1007/978-3-032-27993-4_24, in the IFIP SEC 2026 proceedings (Springer, *ICT Systems Security and Privacy Protection*, vol. 787) — IFIP SEC 2026 was held 9–11 June 2026 in Perth; an unverified secondary summary claimed this chapter won a "Best Paper Award," but I could not independently confirm that claim (link.springer.com is blocked by this environment's egress proxy, and GitHub access to the stated code repo is not enabled for this session), so it is **not** included as evidence below — only the arXiv abstract page, fetched and quoted directly, is relied on.
- **Category:** rag-security
- **What changed:** Prior GraphRAG poisoning attacks target instance-level graph components (nodes/edges/triples). This paper identifies a new attack surface: the *auxiliary schema-level structures* GraphRAG pipelines build during offline indexing (semantic summaries, hierarchical edges, pre-computed scores) that determine retrieval priority at query time but receive no runtime trust validation.
- **Technical summary:** The 3S framework (Semantics, Structure, Scoring) + the Hop-Decayed Influence (HDI) attack use query-aware influence propagation to find high-impact auxiliary targets and corrupt them post-indexing. Across two QA benchmarks (HotpotQA, 2WikiMultiHopQA) and two architectures (Microsoft GraphRAG, HippoRAG2): 88–94% attack success while modifying only ~0.016% of auxiliary structures; each modification affects up to 6.00 queries on average ("Schema Leverage Ratio" — 1:N amplification instance-level attacks don't get); manipulated structures evade perplexity/paraphrase defenses with >99% evasion, since they remain linguistically coherent, system-generated artifacts.
- **Why it might matter:** The course already teaches RAG poisoning (module-14/lab-14) and GraphRAG is an increasingly common production RAG architecture; this is a specific, measured, peer-reviewed-venue extension — a genuinely new corruption surface (schema/index metadata, not content) that standard content-level defenses (perplexity, paraphrase detection) structurally cannot catch, with a quantified 1:N leverage argument that is a clean teaching point.
- **Evidence of adoption:** Peer-reviewed conference publication (IFIP SEC 2026, Springer LNCS, confirmed DOI); not a vendor claim. Code repo stated on the abstract page (https://github.com/Jisung-Pacific/HDI-GraphRAG-Attack) but not independently fetchable from this session — treat as unverified until confirmed.
- **Major organizations using it:** None stated; targets Microsoft GraphRAG and HippoRAG2 as the attacked architectures (not an adoption claim by either).
- **Open-source implementation:** Stated on the abstract page (see URL above); not independently verified this run.
- **Paper:** https://arxiv.org/abs/2610.02373 (DOI https://doi.org/10.1007/978-3-032-27993-4_24)
- **Code:** https://github.com/Jisung-Pacific/HDI-GraphRAG-Attack (unverified — not reachable from this session)
- **Relationship to existing course material:** Extension of `lessons/module-14/lesson-01.md` + `labs/lab-14/` (RAG retrieval attack surface / poisoning) and `papers/15-zou-poisonedrag.md` (PoisonedRAG). `lookup "GraphRAG"` → no prior matches; new sub-topic, not a duplicate.
- **Potential course lesson:** module-14 extension or new lesson/lab: GraphRAG-specific indexing attack surface — attack the auxiliary schema layer (not instance triples), show perplexity/paraphrase defenses miss it, and discuss runtime-validation designs that would catch schema-level drift.
- **Confidence:** medium-high (peer-reviewed venue with DOI, concrete multi-benchmark/multi-architecture numbers) but discounted slightly since the code repo and "best paper" claim could not be independently verified from this session.
- **Recommendation:** review for ADD as a module-14/lab-14 GraphRAG extension; re-verify the code repo link (session-independent) before building a lab around it.

### C-20261005-02 · Branch steering attacks break the Dual-LLM/CaMeL pattern's formal guarantees for GUI computer-use agents; COBRA defense reduces ASR to 0% at 97% utility

- **Class:** A
- **Date discovered:** 2026-10-05
- **Date published:** 2026-10-03
- **Source:** https://arxiv.org/abs/2610.03089
- **Organization/researchers:** Giulio Zingrillo, Hanna Foerster, Ilia Shumailov, Yiren Zhao, Robert Mullins (Imperial College London / Oxford-affiliated authors; Shumailov is an established AI-security researcher — affiliations as inferred from prior publication record, not independently re-verified this run).
- **Category:** agent-security
- **What changed:** The Dual-LLM / CaMeL pattern (isolated Planner-LLM fixes an execution plan before a Quarantined-LLM processes untrusted input) is the primary architecture offering *formal* security guarantees against prompt injection for tool-using agents. This paper shows those guarantees break down for Computer-Use Agents (CUAs) specifically because GUI interaction is inherently dynamic: plans must branch on anticipated runtime screen/web content, and an adversary can craft untrusted content that steers the agent down an already-approved-but-hazardous branch without injecting any explicit instruction ("branch steering").
- **Technical summary:** Introduces STEER-Bench (101 tasks, 9 domains) and shows high attack success against both standard CUAs (94.4% ASR) and vanilla Dual-LLM CUAs (89.5% ASR) — i.e. the formal-guarantee architecture itself is bypassed, not just a weaker baseline. Proposes COBRA: trusted branching plans paired with ahead-of-time capability constraints that strictly bound the parameters/destinations each branch may execute. On STEER-Bench, COBRA cuts ASR to 0% while retaining 97% benign utility.
- **Why it might matter:** A named, systematically studied new attack class against the specific architecture (Dual-LLM/CaMeL) that is the field's leading *formal* defense against prompt injection, plus a measured defense (attack-block and benign-utility numbers) that directly patches the identified gap. The course has no existing Dual-LLM/CaMeL/computer-use-agent material (`lookup` confirms), so this is a clean, self-contained new topic rather than an incremental extension.
- **Evidence of adoption:** None stated (research paper, days old); no confirmed deployment of COBRA.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.03089
- **Code:** none confirmed
- **Relationship to existing course material:** New topic — `lookup "Dual-LLM"` / `"CaMeL"` / `"computer-use agent"` / `"branch steering"` → no existing lesson/lab/registry match (closest is `research/deferred/trust-zoned-agent-memory.md`, a different computer-use-agent attack: persistent memory, not branch steering).
- **Potential course lesson:** A module-16/18-adjacent (agent security / excessive agency) new lesson or lab introducing the Dual-LLM/CaMeL pattern as a defense baseline, then the branch-steering attack against it, then a from-scratch capability-constraint mitigation modeled on COBRA.
- **Confidence:** medium-high (concrete benchmark, named attack class against a defense the field treats as its strongest formal guarantee, matched with a measured mitigation) but single preprint, no independent replication yet.
- **Recommendation:** review for ADD as a new lesson/lab on the Dual-LLM/CaMeL pattern and its failure mode for GUI agents — this also fills a gap (the course has no Dual-LLM/CaMeL coverage at all).

### C-20261005-03 · Pincer: a learned "digital twin" least-privilege proxy for coding-agent resource authorization (Popa/Stoica group)

- **Class:** B
- **Date discovered:** 2026-10-05
- **Date published:** 2026-10-02
- **Source:** https://arxiv.org/abs/2610.02569
- **Organization/researchers:** Mayank Rathee, Alexander Stepanov, Shalin Madabhavi, Jinhao Zhu, Raluca Ada Popa, Ion Stoica (UC Berkeley / RISELab — Popa and Stoica are established systems-security researchers; affiliation as inferred, not independently re-verified this run).
- **Category:** agent-security
- **What changed:** A fifth entry in the already-crowded "deterministic tool-call authorization gate" theme the course is already tracking (`research/deferred/agent-tool-authorization-gates.md`: AGATE, ToolFence, Sapien, ActionGuard), but with a different mechanism: instead of a static policy/typed-blueprint/judge, Pincer trains an isolated-context "digital twin" model that continually learns the user's own permission-granting preferences from a multi-day interaction transcript, then acts as an automated proxy for the agent's permission requests — targeting long-horizon, shell-using coding agents (explicitly Claude, Codex) where user-mediated sandboxing decays via policy staleness and approval fatigue.
- **Technical summary:** Operates at the resource layer alongside existing tool-call-layer defenses (e.g. "auto mode" classifiers). Evaluated against several baselines including LLM-judge variants and an adaptation of Conseca (HotOS '25); the authors report Pincer gives a "significant security improvement" on certain attack types while outperforming baselines on others (no single headline ASR/utility number stated on the abstract page — would need the full paper for exact figures).
- **Why it might matter:** Addresses a real, named usability failure mode (policy decay / permission fatigue) in the exact authorization-gate space the course is already monitoring, from a notably credible systems-security group; a *learned*, personalized least-privilege approach is a distinct mechanism from the four already-deferred static approaches.
- **Evidence of adoption:** None (preprint); explicitly targets existing production agents (Claude, Codex) as the deployment context but does not claim Anthropic/OpenAI adoption.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.02569
- **Code:** none confirmed
- **Relationship to existing course material:** New evidence for the deferred topic `research/deferred/agent-tool-authorization-gates.md` (same problem space — runtime tool-call/resource authorization for agents — different mechanism). Does not independently replicate AGATE/ToolFence/Sapien/ActionGuard's numbers; adds a fifth, mechanism-distinct candidate to an already-noted-as-crowded theme.
- **Potential course lesson:** If the weekly review picks a single winner for the lab-16 authorization extension, Pincer's "learned personalized policy" angle is worth contrasting against Sapien's "stateful regex+predicate policy" in the same `.callout.guarantee` box (what it guarantees vs. how it degrades as the twin's training data goes stale).
- **Confidence:** medium (reputable authors, clear problem framing, but abstract-page summary lacks the single clean headline metric the other four candidates in this theme already have).
- **Recommendation:** monitor alongside the existing deferred topic; do not add a sixth overlapping paper to this theme without a clear reason — flag for the weekly review to fold into the existing `agent-tool-authorization-gates` file rather than opening a new one.

### C-20261005-04 · Prompt-injection detector benchmark scores don't transfer across agent environments (independent generalization-failure evidence for the deferred PIDS-Bench finding)

- **Class:** B
- **Date discovered:** 2026-10-05
- **Date published:** 2026-10-04 (v1)
- **Source:** https://arxiv.org/abs/2610.03448
- **Organization/researchers:** Zhuowen Liu (single author; affiliation not stated on the abstract page).
- **Category:** detection/monitoring
- **What changed:** Independently reproduces, with a different methodology, the core finding the course already has on WAIT (`research/deferred/prompt-injection-detector-over-defense.md`, from PIDS-Bench): that a prompt-injection detector's published benchmark score does not predict its behavior inside a real agent. This paper replays ground-truth tool calls from AgentDojo and tau-bench (no LLM in the loop) to get benign-by-construction tool outputs, labels injected outputs via differential replay, and evaluates 15 detectors (including Meta's Prompt Guard 2) plus two LLM judges against these plus BIPIA.
- **Technical summary:** Detection rankings transfer poorly across benchmarks: the best detector on BIPIA catches only 2% of AgentDojo injections at a 1% false-positive rate; a detector catching 72% of AgentDojo injections catches only 15% on tau-bench. False-positive rates on tool outputs (ranging from none to over 90%) *do* transfer between the two agent benchmarks, unlike detection rates. Where training data is public, the training-input *form* explains the gap: a detector trained on full BIPIA-style inputs doesn't generalize to spotting the same attack strings embedded inside tool outputs; the best cross-benchmark detector shares no training data with any benchmark and was trained on agent-style inputs specifically.
- **Why it might matter:** Independent corroboration (different author, different methodology — benchmark-transfer rather than hard-benign-FPR) of the same underlying lesson the deferred PIDS-Bench candidate already flagged as teachable: injection-detector benchmark scores are not trustworthy proxies for in-agent performance, and the reason (training-input form, not detector architecture) is itself a concrete, teachable mechanism.
- **Evidence of adoption:** None (preprint); evaluates real, used detectors (Meta Prompt Guard 2 among them) rather than proposing a new one — this is an evaluation/critique paper, not a defense claim.
- **Major organizations using it:** n/a (evaluates third-party detectors, including one from Meta).
- **Open-source implementation:** not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.03448
- **Code:** none confirmed
- **Relationship to existing course material:** New evidence for the deferred topic `research/deferred/prompt-injection-detector-over-defense.md` (PIDS-Bench, WAIT, next review 2026-11-08) — independent reproduction of its central claim via a different evaluation design, which per protocol rule 5 can elevate a WAIT topic.
- **Potential course lesson:** Strengthens the case (noted in the deferred file) for a module-24 extension / new "evaluating injection detectors" lesson with a from-scratch detector + a benchmark-transfer lab (train on one agent-benchmark's tool-output distribution, test on another) rather than only a hard-benign-FPR lab.
- **Confidence:** medium (single-author preprint, but methodologically solid — real detectors including a shipped one, two independent agent benchmarks, and a plausible causal mechanism for the gap).
- **Recommendation:** fold into the existing `prompt-injection-detector-over-defense` deferred topic at the next weekly review as corroborating evidence rather than opening a new topic file.

### C-20261007-01 · HarnessSecurity: first systematic empirical benchmark of coding-agent harness security mechanisms (Claude Code, Codex CLI, Gemini CLI, gptme, Qwen Code, Copilot)

- **Class:** A
- **Date discovered:** 2026-10-07
- **Date published:** 2026-10-06 (v1)
- **Source:** https://arxiv.org/abs/2610.07639
- **Organization/researchers:** Zhengyang Zhu, Liming Huang, Runmin Ji, Mingxi Ye, Zihan Zhou, Hanyang Guo, Jingwen Wu, Yuhan Ye, Yuming Feng, Hong-Ning Dai, Zibin Zheng (institutional affiliation not stated on the abstract page — not independently re-verified this run).
- **Category:** agent-security
- **What changed:** Coding-agent harnesses (the layer that mediates tool use and authorizes actions for agents like Claude Code, Codex CLI, Gemini CLI, gptme, Qwen Code, GitHub Copilot) ship a grab-bag of built-in security mechanisms whose actual protective effect and utility cost had never been measured systematically across real harnesses. This paper is the first such study.
- **Technical summary:** Surveys 400 harness-mechanism implementations across six real, widely-used coding-agent harnesses; builds a 23-task benchmark spanning five attack surfaces; runs 2,500 trials recording 81,155 tool calls. Evaluates nine built-in mechanisms (auto-approve, network isolation, read-only mode, command allowlisting, command denylisting, and others not enumerated in the abstract). Headline measured results: ~50% of security mechanisms default to opt-in (off by default); enabling auto-approve raises attack success from 29.2% to 95.6%; network isolation and read-only mode cut attack success but at substantial utility loss; command allowlisting cuts attack success with only a small utility loss, and denylisting with a utility *gain* (both specific numeric utility-loss/gain figures not stated in the abstract excerpt — would need the full PDF).
- **Why it might matter:** This is exactly the "what it guarantees / what it does NOT guarantee / cost" pattern the course's `.callout.guarantee` box is built around, measured empirically across the actual production harnesses the course's own labs reference (Claude Code appears by name in `lab/agents/agent.py` and `labs/lab-21/`), with a concrete, teachable finding (secure-by-default is the exception, not the rule — half of mechanisms are opt-in) and a real cost/benefit contrast between four mechanism classes (two costly, two cheap).
- **Evidence of adoption:** Not a vendor claim — independent academic benchmark; the six harnesses tested are themselves in real, wide production use (Claude Code, GitHub Copilot, Gemini CLI, Codex CLI, Qwen Code, gptme), which is adoption evidence for the *systems under test*, not for this specific paper's findings.
- **Major organizations using it:** n/a (evaluates third-party harnesses from Anthropic, OpenAI, Google, Alibaba, GitHub/Microsoft, and the open-source gptme — does not claim those vendors use this paper's benchmark).
- **Open-source implementation:** Paper states a project page ("this https URL" on the abstract page) but no GitHub/HuggingFace link resolved from the excerpt fetched this run — treat as unverified until the full PDF or project page is checked directly.
- **Paper:** https://arxiv.org/abs/2610.07639
- **Code:** unverified — project link stated on abstract page, not independently confirmed this run
- **Relationship to existing course material:** Extends `lessons/module-17/lesson-01.md` (tool poisoning), `lessons/module-19/lesson-01.md` (MCP/agent security), `lessons/module-21/lesson-01.md` + `labs/lab-21/` (code-agent security) — the course already has code-agent-security content but no empirical cross-harness measurement of built-in guardrail cost/effect. Adjacent to (but a distinct, broader empirical study than) `research/deferred/skill-trust-boundary.md` (installable-Skills trust boundary / Approval Laundering on Claude Code) — same general cluster (agent-harness authorization security) but a different, harness-mechanism-level question; not a duplicate.
- **Potential course lesson:** module-21 (or a module-17/19 extension) lab/lesson update: a `.callout.guarantee` table contrasting auto-approve / network isolation / read-only / allowlist / denylist using this paper's measured ASR-and-utility numbers, plus the "~50% opt-in by default" finding as a concrete "secure defaults" teaching point.
- **Confidence:** medium-high (large-scale empirical study — 2,500 trials, 81,155 tool calls, six real production harnesses — but single preprint one day old, no independent replication yet, and several exact figures only available in the full PDF, not the abstract excerpt this run relied on).
- **Recommendation:** review for ADD as a module-21 lab/lesson extension once the full PDF's exact per-mechanism utility-cost numbers are confirmed; fetch the full PDF (not just the abstract page) before building a lab around it.

### C-20261007-02 · PersistBD: a released technique to make supply-chain LLM backdoors survive benign SFT+RL post-training in coding agents

- **Class:** B
- **Date discovered:** 2026-10-07
- **Date published:** 2026-10-05 (v1)
- **Source:** https://arxiv.org/abs/2610.07510
- **Organization/researchers:** Qiusi Zhan, Nian Lyu, Stephanie Ding, Arnav Mehta, Xander Davies, Daniel Kang (UIUC-affiliated code repo namespace `uiuc-kang-lab`; not independently re-verified this run).
- **Category:** poisoning/backdoor
- **What changed:** Prior sleeper-agent/backdoor work (course already teaches BadNets → Sleeper Agents in M11/papers) generally assumes the backdoor is evaluated right after insertion. This paper studies whether a supply-chain-planted backdoor in a base model survives a *downstream developer's own* benign SFT + RL adaptation into a software-engineering agent — and shows an attacker can deliberately engineer the planted backdoor to survive that process.
- **Technical summary:** On Qwen2.5-Coder-7B, plain benign SFT alone sharply degrades a naively-planted backdoor's attack success rate; a subsequent RL stage preserves/sometimes amplifies what SFT left. The paper identifies the two governing factors (initial backdoor strength, gradient compatibility with the benign training signal) and uses them to build PersistBD, which pre-hardens the backdoor before release: attack success rises from 20% → 74% after benign SFT, and 20% → 76% after SFT+RL, while benign task performance stays comparable. Code released: https://github.com/uiuc-kang-lab/PersistBD.
- **Why it might matter:** A concrete, measured escalation of the supply-chain-backdoor threat model the course already teaches (M11 backdoors, M13 supply chain) specifically for the agent fine-tuning pipeline (SFT→RL) that the course's own training-stage material (module-10/module-11) walks through — i.e. a backdoor surviving the exact pipeline stages the course teaches, with released code.
- **Evidence of adoption:** None (preprint, days old); not a vendor claim — academic, with released code.
- **Major organizations using it:** none stated.
- **Open-source implementation:** https://github.com/uiuc-kang-lab/PersistBD
- **Paper:** https://arxiv.org/abs/2610.07510
- **Code:** https://github.com/uiuc-kang-lab/PersistBD
- **Relationship to existing course material:** Extension of `lessons/module-11/lesson-01.md` (backdoors/sleeper agents, labs/lab-11) and `lessons/module-13/lesson-01.md` (supply chain, labs/lab-13) — new sub-topic (backdoor persistence through a developer's own benign post-training pipeline); `lookup` found no existing registry/course match.
- **Potential course lesson:** module-11 or module-13 extension/lab: plant a weak vs. PersistBD-hardened backdoor, run benign SFT (+ optionally RL) on a small model, and measure the ASR-survival gap directly — a clean from-scratch numerical demonstration in the course's existing style.
- **Confidence:** medium (single preprint, no independent replication, but released code and a clear, reproducible numeric result on a real 7B coding model).
- **Recommendation:** monitor; re-review at the next weekly pass once/if an independent group reproduces the SFT+RL persistence numbers, or fold directly into a module-11 lab extension if the weekly review wants to act on it now given the released code.

### C-20261007-03 · SkillPoison: agent skill-extraction poisoning from only verified-successful, individually-benign experiences (95.71% ASR, evades verification + lexical inspection)

- **Class:** B
- **Date discovered:** 2026-10-07
- **Date published:** 2026-10-06 (v1)
- **Source:** https://arxiv.org/abs/2610.07645
- **Organization/researchers:** Lizhi Zhang, Xin He, Dianxuan Fu, Yuyuan Feng, Jiatong Li, Qi Wang, Xin Wang, Qinggang Zhang (code repo namespace `DEEP-JLU`; affiliation not independently re-verified this run).
- **Category:** poisoning/backdoor
- **What changed:** Prior agent-skill-poisoning attacks inject an identifiably malicious trigger/fact/behavior into an individual experience or extracted skill, so they are catchable by per-experience verification or lexical inspection. This paper shows poisoning can be done with every individual injected experience remaining genuinely task-correct and passing verification — only the *distribution* of experiences (which contextual conditions are present vs. absent) is manipulated, shaping how the skill extractor generalizes a learned behavior beyond its originally safe conditions.
- **Technical summary:** SkillPoison builds a set of successful, verified-correct experiences that reinforce a target behavior, then removes the contextual conditions that should constrain when that behavior applies, so the self-improving agent's skill extractor generalizes the behavior to unsafe contexts. Across three (unnamed in the abstract excerpt) benchmarks: 95.71% attack success rate, with all injected experiences remaining task-correct and passing both verification and lexical inspection. Code released: https://github.com/DEEP-JLU/SkillPoison. No defense proposed.
- **Why it might matter:** A structurally different poisoning mechanism than the course's existing BadNets/sleeper-agent trigger model (M11) — no malicious content anywhere in the training signal, so standard per-sample verification/lexical defenses are guaranteed not to catch it by construction. Directly relevant to the course's agent-memory/skills material (module-16 agent surface, module-28 multi-agent) if the course extends into self-improving/skill-distilling agents.
- **Evidence of adoption:** None (preprint, days old); academic, with released code, not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** https://github.com/DEEP-JLU/SkillPoison
- **Paper:** https://arxiv.org/abs/2610.07645
- **Code:** https://github.com/DEEP-JLU/SkillPoison
- **Relationship to existing course material:** New sub-topic adjacent to `lessons/module-11/lesson-01.md` (backdoors — different mechanism: no malicious content in any individual sample) and `lessons/module-16/lesson-01.md` (agent memory/skills surface). `lookup` found no existing registry/course match for "skill poisoning" by this mechanism.
- **Potential course lesson:** module-11 or module-16/28 extension: a from-scratch toy "skill extractor" that generalizes from a set of individually-correct experiences, showing how removing contextual guards in the training distribution (not content) produces unsafe generalization — paired with why content-only verification structurally cannot catch it.
- **Confidence:** medium (single preprint, no independent replication, but released code and a clean, reproducible mechanism distinct from existing course content).
- **Recommendation:** monitor; revisit if self-improving/skill-distilling agents become a bigger part of the course's agent-security track, or if an independent reproduction/defense appears.

### C-20261008-01 · PackHallu: prompt-injection in agent "rule files" (AGENTS.md / .cursorrules) drives package-hallucination supply-chain substitution

- **Class:** A
- **Date discovered:** 2026-10-08
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.09264
- **Organization/researchers:** Yupu Wang, Zhengyuan Jiang, Reachal Wang, Neil Zhenqiang Gong (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** supply-chain (mechanism: prompt-injection)
- **What changed:** Agentic coding tools widely consume community-shared "rule files" (AGENTS.md, .cursorrules, CLAUDE.md-style files) to steer code generation, exactly the mechanism this course's own repos and `AGENTS.md`/`CLAUDE.md` files use. This paper shows that text injected into an otherwise-benign rule file can make a coding agent silently substitute attacker-controlled package names for legitimate dependencies — a supply-chain attack delivered entirely through prompt injection in a trust-boundary file most teams don't treat as untrusted input.
- **Technical summary:** Introduces PackHallu, an evolutionary-optimization framework that refines the injected prompt text using trajectory-level feedback and LLM-guided mutations (rather than a single hand-written payload). Evaluated across multiple benchmarks, multiple LLMs, and multiple agent frameworks; the authors report high attack success rates that transfer across model/framework combinations (specific headline ASR numbers are in the full PDF tables, not stated in the fetched abstract text — flagged for the weekly review to pull before building a lab).
- **Why it might matter:** This is a new, concretely demonstrated instance of exactly the "AI supply-chain attacks / dependency confusion" category the protocol flags, via exactly the "rule file" trust-boundary pattern this course's own CLAUDE.md/AGENTS.md convention (and sibling courses') depends on — exceptionally direct relevance and a natural from-scratch lab (plant an injected rule file, show package substitution, then build a defense: treat rule files as untrusted content / diff-review pipeline).
- **Evidence of adoption:** None (preprint, 1 day old); not a vendor claim — independent academic work with a named, reproducible attack-optimization framework.
- **Major organizations using it:** n/a (attacks third-party coding-agent frameworks and rule-file conventions, not any one vendor's product).
- **Open-source implementation:** Not stated/linked on the abstract page — treat PackHallu's own code as unverified/unreleased until checked directly in the full PDF.
- **Paper:** https://arxiv.org/abs/2610.09264
- **Code:** none confirmed
- **Relationship to existing course material:** Extends `lessons/module-13/lesson-01.md` (supply chain), `lessons/module-17/lesson-01.md` (tool/rule poisoning), `lessons/module-21/lesson-01.md` (code-agent security). `lookup "rule file"` / `"package hallucination"` found no existing registry/course match for this specific mechanism (rule-file-delivered prompt injection → package substitution) — new sub-topic.
- **Potential course lesson:** module-13 or module-21 lab: plant an injected AGENTS.md/.cursorrules-style rule file in a sandboxed repo, show a toy coding agent substitute a malicious package, then implement a rule-file provenance/diff-review control as the from-scratch defense.
- **Confidence:** medium (single preprint, 1 day old, no independent replication, and this run could not confirm exact ASR figures or a code release from the abstract page alone) but the mechanism itself is cleanly reproducible and the course's own file conventions make it unusually easy to verify directly.
- **Recommendation:** review for ADD as a module-13/21 lab extension; fetch the full PDF for exact ASR numbers and check for a code release before building the lab.

### C-20261008-02 · SLDR: layer-selective LoRA recovery + dynamic routing defends against malicious fine-tuning-as-a-service (NeurIPS 2026)

- **Class:** A
- **Date discovered:** 2026-10-08
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.10345
- **Organization/researchers:** Hui Zhang, Yachao Yuan, Jiayun Wang, Yuanzhuo Li, Hongtao Wang, Yali Yuan (affiliation not stated on the abstract page; not independently re-verified this run). Accepted at **NeurIPS 2026**.
- **Category:** defense/guardrail
- **What changed:** Fine-tuning-as-a-service lets a malicious customer weaken an aligned model's refusal behavior while it still performs the advertised downstream task well. Prior layer-wise safety diagnostics are extended here into a deployable post-fine-tuning defense rather than just an analysis.
- **Technical summary:** The authors show a layer's effect on safety is directional — scaling some layers up strengthens refusals, others weaken them, some have little effect — and use this to build SLDR: a LoRA "recovery" adapter trained only on the highest/lowest-sensitivity layers, activated only for malicious queries via representation-based dynamic routing (so benign downstream task performance is untouched). Tested across four model architectures, five downstream tasks, and four harmful benchmarks. Headline number: on Llama3.1/SST2 the average harmful-output score drops from 11.54 to 0.08 while downstream accuracy is maintained, and the harmful score stays near zero even at a poisoning ratio of 0.9. Code released: https://github.com/Stardust457/SLDR.
- **Why it might matter:** A peer-reviewed (NeurIPS 2026), code-released, measured defense with an explicit security/utility cost split (near-zero attack success, maintained downstream accuracy, robust to very high poisoning ratios) for a real, named production threat model (fine-tuning-as-a-service abuse) — exactly the `.callout.guarantee`-style "what it guarantees / cost" pattern the course is built around, and a clean from-scratch implementable mechanism (layer-sensitivity probing + gated LoRA adapter).
- **Evidence of adoption:** Peer-reviewed NeurIPS 2026 acceptance; not a vendor claim. No confirmed production deployment.
- **Major organizations using it:** none stated.
- **Open-source implementation:** https://github.com/Stardust457/SLDR
- **Paper:** https://arxiv.org/abs/2610.10345
- **Code:** https://github.com/Stardust457/SLDR
- **Relationship to existing course material:** Extends the malicious-fine-tuning thread already referenced in `lessons/module-11/lesson-01.md` ("connection to malicious fine-tunes/adapters (M13)") and `papers/10-gu-badnets.md`, but the course has no dedicated defense lesson/lab for fine-tuning-as-a-service abuse specifically; `lookup "malicious fine-tuning"` found no dedicated existing lesson/lab — new sub-topic/defense.
- **Potential course lesson:** module-11 or module-13 extension/lab: reproduce the layer-sensitivity probe on a small open model, implement the gated LoRA recovery adapter from scratch, and measure the harmful-score/utility tradeoff directly, paired with the course's existing backdoor/fine-tune material.
- **Confidence:** medium-high (major peer-reviewed ML venue, released code, clear quantitative result across multiple architectures/tasks/benchmarks) — no independent replication yet since this is a fresh preprint/camera-ready.
- **Recommendation:** review for ADD as a module-11/13 defense lab extension once the released code is checked directly.

### C-20261008-03 · Secure-CUA: per-step "action transactions" + masked untrusted regions give computer-use agents a formal security guarantee at near-zero utility cost (vs. CaMeL-CUA's large utility loss)

- **Class:** A
- **Date discovered:** 2026-10-08
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.09469
- **Organization/researchers:** Sarthak Choudhary, Mihai Christodorescu, Ashish Hooda, Somesh Jha, Tongxin Li, Damien Octeau (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** agent-security (defense)
- **What changed:** Computer-use agents (CUAs) read screens mixing trusted controls with untrusted content; an adversary can embed hidden instructions or misleading visuals to redirect the agent's action or input target. The course is already tracking (staging `C-20261005-02`) a paper showing the Dual-LLM/CaMeL pattern's *formal* guarantees break down for CUAs via "branch steering," with its own COBRA mitigation. This paper is independent, concurrent work proposing a different mechanism (per-step committed "action transactions" + masking + an isolated query model) for the same formal-guarantee-for-CUAs problem, with a much smaller utility cost than the CaMeL baseline it benchmarks against.
- **Technical summary:** Defines security requirements for both the agent's decisions and its GUI execution, proves enforcing both at every step protects execution traces in an idealized model, and implements it as Secure-CUA: before touching untrusted content, the agent commits to an explicit per-action "action transaction" (its queries + how answers may be used); untrusted regions are masked, an isolated query model answers the queries, and the target is located on the masked interface; a new transaction each step keeps utility high as interfaces change. Benign evaluation: 400 WebArena tasks, 3 frontier models, 5 seeds, 6,000 traces. Secure-CUA averages 53.55% task success vs. 55.12% for Vanilla-CUA (no guarantee) and only 13.17% for CaMeL-CUA (the existing formal-guarantee baseline) — i.e. a ~1.6-point utility cost vs. CaMeL's ~42-point utility cost for a comparable security guarantee.
- **Why it might matter:** A measured, large utility-cost improvement over the exact formal-guarantee baseline (CaMeL) the course is already evaluating as a candidate topic, directly strengthening the teaching case for a Dual-LLM/CaMeL-pattern lesson by giving it a much more practical alternative mechanism to contrast against both CaMeL and the already-staged branch-steering attack/COBRA defense.
- **Evidence of adoption:** None (preprint, 1 day old); no confirmed deployment.
- **Major organizations using it:** none stated.
- **Open-source implementation:** none stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.09469
- **Code:** none confirmed
- **Relationship to existing course material:** Directly adjacent to staging candidate `C-20261005-02` (branch-steering attacks on Dual-LLM/CaMeL for CUAs, COBRA defense) and deferred topic `research/deferred/trust-zoned-agent-memory.md` — same problem cluster (formal security guarantees for computer-use agents), different mechanism (action-transaction + masking vs. trusted-branch-plan + capability constraints). Not a duplicate; the weekly review should consider these together.
- **Potential course lesson:** Same module-16/18-adjacent Dual-LLM/CaMeL lesson idea already noted for `C-20261005-02`, now with three things to contrast in one `.callout.guarantee` table: Vanilla-CUA (no guarantee, best utility), CaMeL-CUA (formal guarantee, large utility loss), Secure-CUA (formal guarantee, near-vanilla utility) — a clean "cost of a security guarantee" teaching point.
- **Confidence:** medium-high (concrete large-scale benign-utility benchmark — 6,000 traces — directly comparing against a named existing baseline) but single preprint, no independent replication, and the security-under-attack numbers (vs. only benign utility) were not in the fetched abstract excerpt.
- **Recommendation:** review for ADD together with `C-20261005-02` as a single Dual-LLM/CaMeL/CUA lesson covering both the branch-steering attack and both proposed defenses (COBRA and Secure-CUA); fetch both full PDFs for the attack-success-rate-under-attack numbers before building the lab.

### C-20261008-04 · Formal runtime verification (MFOTL/MonPoly) of tool-using agent traces: generic policies over-trigger on benign runs; naive provenance checks are defeated by a single planted line

- **Class:** B
- **Date discovered:** 2026-10-08
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.09793
- **Organization/researchers:** Nikolaos Kekatos, Stylianos Basagiannis, Marinelio Chintri, Alexios Lekidis, Tom Nianios, Ioannis Seitoglou, Anastasios Temperekidis, Panagiotis Katsaros. Accepted at the 8th Workshop on CPS&IoT Security and Privacy (CPSIoTSec '26), co-located with **ACM CCS 2026**, The Hague (DOI 10.1145/3847353.3847499).
- **Category:** detection/monitoring
- **What changed:** Evaluates metric first-order temporal logic (MFOTL) policies, run through the unmodified MonPoly monitor, as a runtime-verification layer for tool-using agents — replaying recorded trajectories from AgentDojo, STAC, and R-Judge offline, without running an agent. Measures both detection and false-positive cost, and specifically stress-tests whether provenance-aware policies can be fooled by an attacker who fabricates provenance metadata.
- **Technical summary:** Five generic safety obligations flag 71.8% of STAC attack chains and 70.1% of successful AgentDojo attacks, but also fire on 29.3% of benign runs — the imprecision traced to the corpora rarely recording approvals/timestamps. Provenance-aware policies discriminate better, but a naive provenance check is defeated by a single planted line in 94–99% of the runs it would otherwise have flagged; binding provenance to the lookup that produced it closes this gap without hurting detection or benign behavior. Proposes a 12-field enforcement-ready trace schema.
- **Why it might matter:** A peer-reviewed (CPSIoTSec'26 @ CCS), concretely measured instance of exactly the "what it guarantees / what it does NOT guarantee / false-positive cost / how an attacker adapts" pattern the course's `.callout.guarantee` box is built around, and new evidence directly relevant to two existing deferred topics (`agent-tool-authorization-gates`, `execution-audit-provenance`) — specifically the finding that provenance data is itself a target an attacker can spoof, and the concrete fix (binding provenance to its originating lookup).
- **Evidence of adoption:** Peer-reviewed workshop paper (CCS-colocated); not a vendor claim; no deployment claimed.
- **Major organizations using it:** none stated.
- **Open-source implementation:** MonPoly monitor named but not linked on the abstract page; the paper's own schema/policy code not confirmed as released.
- **Paper:** https://arxiv.org/abs/2610.09793
- **Code:** none confirmed
- **Relationship to existing course material:** New evidence for `research/deferred/agent-tool-authorization-gates.md` and `research/deferred/execution-audit-provenance.md` (same problem space — runtime/audit enforcement for tool-using agents — concrete FP-rate and provenance-spoofing-evasion numbers these deferred files did not yet have).
- **Potential course lesson:** Strengthens the case for a module-16/19 "runtime verification" lesson/lab: implement the five generic MFOTL-style obligations over a toy agent trace, measure the ~30% false-positive rate directly, then implement the provenance-binding fix and show it close the 94–99% evasion gap.
- **Confidence:** medium (peer-reviewed workshop venue, concrete multi-benchmark numbers, but a workshop rather than a top-tier venue, single paper, no independent replication).
- **Recommendation:** fold into the existing `agent-tool-authorization-gates` and `execution-audit-provenance` deferred files at the next weekly review as corroborating/quantified evidence rather than opening a new topic.

### C-20261008-05 · WebMirage: localized adversarial-image perturbations hijack web agents end-to-end (grounding → browser execution), 91.9% ASR, defeats 3 existing defenses, code released

- **Class:** B
- **Date discovered:** 2026-10-08
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.09240
- **Organization/researchers:** Wanjing Han, Levi Taiji Li, Mu Zhang, Yue Jiang, Guanhong Tao (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** multimodal-attack (agent-security)
- **What changed:** Prior visual red-teaming for web agents targets model inference only (does the VLM produce a bad output), ignoring the structured input processing and action post-processing that actually turn a model output into a browser action — so model-level attack success doesn't demonstrate real control over browser execution. This paper treats it as an end-to-end grounding-to-execution problem.
- **Technical summary:** WebMirage crafts localized visual perturbations (via role-slot abstraction, webpage recomposition, and dataflow analysis) that make agents select attacker-controlled page content and perform the matching browser action consistently across different page renderings. Across 4 agent configurations, 6 VLM backbones, 2,250 tasks on 13 public websites plus a sandbox benchmark: 91.9% average attack success rate vs. 17.4% for the strongest baseline, and the attack remains effective against three agent-level defenses. Code released: https://github.com/MoonTea0416/WebMirage.
- **Why it might matter:** A large-scale, code-released, measured multimodal attack directly on the browsing/computer-use agent surface the course already teaches (module-17/18 end-to-end webpage→browser-agent→injection→tool chain) and relevant to the same CaMeL/Secure-CUA cluster noted above (WebMirage explicitly defeats three existing agent-level defenses, which is useful evidence on what current defenses do NOT guarantee against visual/rendering-level attacks specifically, as opposed to the text-injection-level attacks those defenses were designed for).
- **Evidence of adoption:** None (preprint, 1 day old); academic, with released code, not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** https://github.com/MoonTea0416/WebMirage
- **Paper:** https://arxiv.org/abs/2610.09240
- **Code:** https://github.com/MoonTea0416/WebMirage
- **Relationship to existing course material:** Extends `lessons/module-17/lesson-01.md` / `lessons/module-18/lesson-01.md` (webpage→browser-agent→injection→tool→credential chain) with a visual/rendering-level variant of that chain, distinct from the text-injection attacks those lessons currently cover; also adjacent to the CaMeL/Secure-CUA/branch-steering cluster (`C-20261005-02`, `C-20261008-03`) since it reports defeating "three agent-level defenses" without naming which — worth checking in the full PDF whether CaMeL/Secure-CUA-style defenses are among them.
- **Potential course lesson:** module-17/18 extension: a from-scratch localized-perturbation attack on a toy visual web-agent grounding pipeline, demonstrating that text-level injection defenses (e.g. spotlighting, data-marking) don't catch a purely visual/rendering-level attack.
- **Confidence:** medium (large benchmark — 2,250 tasks, 13 real websites, 6 VLM backbones — and released code, but single preprint, no independent replication, and the "three defenses" it defeats are unnamed in the fetched abstract excerpt).
- **Recommendation:** monitor; re-review at the next weekly pass, and check the full PDF to confirm which three defenses were tested (especially whether CaMeL/Secure-CUA-style architectural defenses were among them, which would directly inform the combined Dual-LLM/CaMeL lesson recommended for `C-20261005-02`/`C-20261008-03`).

### C-20261008-06 · Answer-side backdoors: the model's own self-generated first-turn reply becomes the trigger in multi-turn dialogue, evading input-centric defenses by construction

- **Class:** B
- **Date discovered:** 2026-10-08
- **Date published:** 2026-10-06 (v1)
- **Source:** https://arxiv.org/abs/2610.07723
- **Organization/researchers:** Yibo Zhang, Tianrong Guan, Liang Lin, Puze Wang, Jin Wang, Qingsong Wen (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** poisoning/backdoor
- **What changed:** Essentially all prior LLM backdoors are input-centric: the attacker plants an explicit trigger pattern in the *user's* input, which is exactly what input-side guardrails (spotlighting, data-marking, input scanners) are built to catch. This paper moves the trigger to the *model's own output*: a benign-looking first-turn prompt gets the model to generate a specific, innocuous word; once that word is in the dialogue history, the model's own prior utterance — not anything in the current user turn — is the trigger.
- **Technical summary:** A later harmful query is answered without refusal once the self-generated word is present in history, while the user-visible input for that turn stays completely clean — there is no trigger pattern for an input scanner to find, because the trigger was planted by the model talking to itself across turns. Reported near-100% attack success rate at only 5% poisoning rate, across four (unnamed in the abstract) LLMs, with general utility and clean-input safety preserved, and evasion of "mainstream input-centric defenses." Representation-level analysis attributes the effect to suppression of the model's internal refusal signal once the self-generated trigger is present. No benchmark names, no code repository, and no independent replication found.
- **Why it might matter:** A structurally distinct backdoor-activation mechanism from both the course's existing BadNets/sleeper-agent model (M11: trigger lives in the input) and the two sibling backdoor papers staged yesterday from the same 2026-10-06 arXiv batch (PersistBD: trigger survives post-training; SkillPoison: trigger emerges from experience *distribution*, not content) — here the trigger is neither in the input nor in any training sample's content, it is manufactured live, inside the conversation, by the model itself. This is relevant specifically because it defeats the entire class of input-centric defense *by construction*, not through a measured bypass rate: there is no trigger token anywhere in the current turn's input for a scanner to flag.
- **Evidence of adoption:** None (single preprint, 2 days old at discovery); no vendor claim — academic result, no code released.
- **Major organizations using it:** none stated.
- **Open-source implementation:** none found (no repository linked on the abstract page or via third-party code-finder tools as of this check).
- **Paper:** https://arxiv.org/abs/2610.07723
- **Code:** none
- **Relationship to existing course material:** Adjacent to `lessons/module-11/lesson-01.md` (backdoors/sleeper agents, labs/lab-11) — distinct mechanism from what's taught there (self-generated, dialogue-history trigger vs. a planted input/weight trigger) — and to the two already-staged sibling papers `C-20261007-02` (PersistBD) and `C-20261007-03` (SkillPoison), together forming a same-week cluster of three structurally different "defense-by-construction-evading" backdoor mechanisms. `lookup` for "answer-side backdoor" and "multi-turn backdoor" found no existing registry/course match.
- **Potential course lesson:** module-11 extension or a combined lesson/lab covering all three same-week backdoor papers side by side (input-trigger → PersistBD's post-training-survival angle → SkillPoison's distributional angle → this paper's self-generated-trigger angle), demonstrating concretely why input-centric defenses (spotlighting, data-marking, scanners) cannot, by construction, catch any of the latter two.
- **Confidence:** low-medium (single preprint, no code, no named benchmarks or models in the available abstract, no independent replication — weaker evidentiary footing than its two code-released siblings, but the mechanism itself is clear, concerning, and easy to verify from the abstract's own description).
- **Recommendation:** monitor alongside `C-20261007-02`/`C-20261007-03`; re-review together at the next weekly pass as one cluster, and fetch the full PDF (model names, benchmark names, which "mainstream input-centric defenses" were tested) before any course-content decision.

### C-20261009-01 · BRANCH: branching tree-search bypass defeats multi-scanner AI guardrails at 100% ASR, transfers to 29 unseen guardrails including 8 commercial black-box systems

- **Class:** A
- **Date discovered:** 2026-10-09
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.10742
- **Organization/researchers:** William Hackett, Peter Garraghan (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** defense/guardrail (mechanism: adversarial bypass of guardrail classifiers)
- **What changed:** Multi-scanner guardrail stacks (combining several independent input/output classifiers to cover each other's blind spots) are a widely recommended production defense pattern. This paper shows the scanners' shared internal representations make the whole stack bypassable together, not just one at a time, and that the resulting bypasses transfer broadly, including to commercial black-box guardrail products the authors never had white-box access to.
- **Technical summary:** BRANCH runs a branching tree search that applies adversarial perturbations against individual scanners, then selects/refines perturbations by their improvement across *all* scanners jointly (separating the "does this bypass" evaluation step from the attack-optimization step). Evaluated across 6 guardrail systems in 120 scenarios: 100% attack success rate, using 72% fewer queries and 4.5x less wallclock time than established bypass techniques. Bypasses generated against the 6 known systems then transferred to 29 unseen guardrails, including 8 commercial black-box guardrails, reaching up to 100% ASR in some transfer cases with zero additional optimization. The authors state the resulting bypass text preserves the original (malicious) meaning, i.e. this is not just a benign-looking decoy.
- **Why it might matter:** A concretely measured, reproducible defeat of the exact "stack multiple classifiers for defense-in-depth" guardrail pattern the protocol and the course's own module-27 reference (and that most production LLM-app security advice currently recommends), with transfer to real commercial products — directly the kind of "attacker adapts" evidence the course's `.callout.guarantee` pattern needs for a guardrail-classifier lesson, and no existing lesson currently covers classifier-based guardrails as their own defense-in-depth topic (only module-27 mentions guardrail classifiers as a component to *map*, not a defense to *implement and then break*).
- **Evidence of adoption:** None stated (preprint, 2 days old); not a vendor claim — independent academic bypass research with reproducible method and released numbers. Transfer to 8 named-as-commercial black-box guardrails is itself a form of real-world confirmed impact (it demonstrates the attack against products actually deployed, even though the paper doesn't name the vendors on the abstract page).
- **Major organizations using it:** n/a (attacks third-party guardrail products, not any one vendor's own tool).
- **Open-source implementation:** not stated/confirmed on the abstract page — check the full PDF.
- **Paper:** https://arxiv.org/abs/2610.10742
- **Code:** none confirmed
- **Relationship to existing course material:** `lookup "multi-scanner guardrail bypass"` and `lookup "branching tree search jailbreak"` found no existing registry/course match. Extends `lessons/module-27/lesson-01.md` (which currently treats "guardrail classifiers" only as something to enumerate during AI asset discovery, not as a defense mechanism with its own attack/defense cycle) and is a natural sibling to the course's existing jailbreak/defense-evasion material — new sub-topic: classifier-stack guardrails as a defense layer.
- **Potential course lesson:** A new lab (module-17/27 territory): deploy a small multi-scanner guardrail stack from scratch (e.g. two or three lightweight open classifiers), reproduce a simplified branching-search bypass, measure ASR before/after, then implement and measure a mitigation (e.g. diversity of representations, output-side re-scoring) — a clean "what guardrails guarantee / how an attacker adapts" box.
- **Confidence:** medium-high (concrete, large-scale measured numbers — 120 scenarios, 6 systems, 29-system transfer including named-as-commercial targets — but single preprint, 2 days old, no independent replication yet, and code availability unconfirmed).
- **Recommendation:** review for ADD as a module-17/27 guardrail-classifier lab; confirm code release and exact commercial-guardrail identities from the full PDF before building the lab.

### C-20261009-02 · DITTO + PickleBench: context-aware Pickle VM-state scanner reaches 0% false negatives / 0.7% false positives on real-world malicious/benign pretrained-model corpus

- **Class:** A
- **Date discovered:** 2026-10-09
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.10735
- **Organization/researchers:** Qiaolin Qin, Wanpeng Li, Benoit Baudry, Lorenzo De Carli, Heng Li, Ettore Merlo (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** supply-chain (defense: Pickle/checkpoint deserialization scanning)
- **What changed:** The course already teaches Pickle/checkpoint deserialization RCE as a supply-chain attack surface (`lessons/module-01/lesson-01.md`, `lessons/module-22/lesson-01.md`), but has no dedicated, measured scanner-defense lesson. This paper quantifies the scale of the problem (9.3% of 10,000+ popular Hugging Face repos rely on Pickle) and ships both a new scanner and a new labeled benchmark to measure it against.
- **Technical summary:** DITTO is described as the first stack-based, context-aware scanner for Pickle-based pretrained models: it tracks Pickle virtual-machine state opcode-by-opcode (rather than pattern-matching known-bad opcodes/strings) and performs semantic analysis to infer model intent, aiming to catch novel/obfuscated malicious payloads existing scanners miss (e.g. extension-registry attacks). Evaluated on the authors' new PickleBench (959 benign + 92 malicious real-world models): 100% scanning coverage, 0% false-negative rate, 0.7% false-positive rate, F1 = 0.966 — reported as outperforming existing state-of-the-art scanners, which the authors say both miss security-sensitive behaviors and over-alert.
- **Why it might matter:** A measured, released defense (scanner + benchmark) with an explicit security/false-positive cost trade-off for a threat model the course already teaches but hasn't yet paired with a from-scratch, measured defense lab — exactly the `.callout.guarantee` pattern (what the scanner catches / its 0.7% FP cost / how an attacker might still adapt, e.g. non-Pickle-opcode-level attacks).
- **Evidence of adoption:** None stated (preprint, 2 days old); not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not stated/confirmed on the abstract page — check the full PDF for a repo link.
- **Paper:** https://arxiv.org/abs/2610.10735
- **Code:** none confirmed
- **Relationship to existing course material:** Extends `lessons/module-01/lesson-01.md` and `lessons/module-22/lesson-01.md` (Pickle/checkpoint RCE, supply chain). `lookup "pickle scanner"` and `lookup "PickleBench"` found existing course coverage of the *attack* but no existing registry topic or lesson/lab on a *measured scanner defense* — new sub-topic.
- **Potential course lesson:** module-01/22 lab extension: implement a minimal Pickle-VM-state tracker from scratch (opcode stream → behavior classification), evaluate it on a small synthetic benign/malicious set modeled on PickleBench's categories, and contrast against a naive pattern-matching scanner to make the false-negative gap concrete.
- **Confidence:** medium-high (clear quantitative benchmark results, new released benchmark, concrete real-world prevalence number) — single preprint, no independent replication, code availability unconfirmed.
- **Recommendation:** review for ADD as a module-01/22 scanner-defense lab extension once the full PDF/code is checked directly.

### C-20261009-03 · PyCache Trap: Python bytecode-cache substitution defeats 7 agent-Skill scanners at 94-100% ASR; EAV defense (execution-aware validation) detects 100% of in-scope attacks at 92.8% recall / 10% FPR — new evidence for the deferred "Skills as a trust boundary" topic

- **Class:** A
- **Date discovered:** 2026-10-09
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.10612
- **Organization/researchers:** Jie Liao, Simeng Qin, Wenqi Ren, Wei Zhou, Junhao Wen, Ranjie Duan, Yang Liu, Xiaojun Jia (affiliation not stated on the abstract page; not independently re-verified this run; Yang Liu and Xiaojun Jia are names associated with established adversarial-ML security research groups, not independently confirmed here).
- **Category:** agent-security (sub-topic: installable agent "Skills" as a trust boundary)
- **What changed:** The course's registry already tracks "Agent Skills as a trust boundary" (`research/deferred/skill-trust-boundary.md`, status WAIT) covering four independent groups' cross-skill poisoning / scanner-evasion attacks (TrustProbe, CoordPoison, Pretext, APEX). This paper adds a fifth, mechanism-distinct attack: instead of evading scanners via wording/relocation tricks on the *visible* source, it exploits the fact that Python can execute a bundled bytecode cache (`.pyc`) that diverges from the inspected source — scanners check documentation/source, not the compiled artifact the interpreter may actually run.
- **Technical summary:** PyCache Trap pairs benign-looking source code with a substituted bytecode cache that the Python loader accepts silently, tied to a task-relevant invocation so the concealed behavior only triggers when the skill is actually used; rewriting the invocation wording while leaving the cache untouched lets the package pass admission checks. Evaluated across 100 skills against 7 existing scanners: 94-100% attack success, with no scanner semantically recognizing the cache-resident behavior. The authors' proposed defense, execution-aware validation (EAV), links instructions/scripts/imports/runtime artifacts in a typed execution graph and combines behavioral analysis with trusted reproduction of compiled artifacts: it detected 100% of the 100 evaluated source-present cache substitutions, and reached 92.8% recall at a 10.0% false-positive rate across five attack families and 200 benign skills.
- **Why it might matter:** Satisfies the daily protocol's dedup rule for "genuinely new evidence for a deferred topic" (independent new mechanism + a working defense with a stated false-positive cost) — this is exactly the bar for promoting a WAIT topic back to A/B with concrete new material, since it both (a) demonstrates a new bypass class (compiled-artifact substitution, distinct from Pretext's source-relocation evasion) and (b) is the first of the five Skills-trust-boundary papers to pair the attack with a defense that reports a false-positive rate on a held-out benign set.
- **Evidence of adoption:** None stated (preprint, 2 days old); not a vendor claim.
- **Major organizations using it:** none stated; targets third-party agent-Skill scanner tools and the Python bytecode-cache mechanism generically, not one vendor's product.
- **Open-source implementation:** not stated/confirmed on the abstract page — check full PDF.
- **Paper:** https://arxiv.org/abs/2610.10612
- **Code:** none confirmed
- **Relationship to existing course material:** New evidence for `research/deferred/skill-trust-boundary.md` (same topic, mechanism-distinct from the four already-noted papers; adds the first measured defense-with-FP-cost in this theme). Also touches `lessons/module-13/lesson-01.md`/`module-22` (supply-chain/deserialization-adjacent, since `.pyc` cache trust is a sibling problem to pickle/checkpoint trust).
- **Potential course lesson:** If/when the weekly review promotes the Skills-trust-boundary theme to ADD, PyCache Trap + EAV is now the strongest single candidate to anchor the lab around, since it is the only one of the five papers with both a reproducible new attack class and a defense reporting a concrete FP-rate cost.
- **Confidence:** medium (reputable-looking multi-author group, concrete large-scale numbers across 100 skills/7 scanners/200 benign skills, but single preprint, 2 days old, no independent replication, and code availability unconfirmed).
- **Recommendation:** fold into the existing `skill-trust-boundary` deferred file at the next weekly review as the leading attack+defense pairing for this theme; do not open a new topic file.

### C-20261009-04 · Speedbumps: adversarial-suffix "rejection attacks" on speculative decoding slow LLM inference below plain autoregressive speed, transferring across drafters/targets

- **Class:** B
- **Date discovered:** 2026-10-09
- **Date published:** 2026-10-07 (v1)
- **Source:** https://arxiv.org/abs/2610.10929
- **Organization/researchers:** Adam Y. J. Jones, Yu Yuan, Sergio Maffeis (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** other (infra-level denial-of-service / cost attack against an inference-serving optimization, closest existing category: OWASP "Unbounded Consumption")
- **What changed:** Speculative decoding (a drafter model proposes tokens, the target model verifies/accepts them) is now a mainstream inference-serving optimization. This paper introduces attacker-controlled content (an adversarial suffix) that specifically targets the drafter/target *disagreement rate* to degrade this optimization's speedup — a new, mechanism-specific denial-of-service/cost-attack vector distinct from the course's already-deferred `agent-denial-of-wallet` topic (which concerns agent-level retained/re-billed tool output, not serving-infra speculative decoding internals).
- **Technical summary:** Two attacks: Speedbump-P (estimates acceptance from the target's probability of drafted tokens) and Speedbump-D (from drafter/target distribution overlap), each optimizing an adversarial suffix appended to attacker-controlled content to minimize the expected accepted-prefix length. The authors report the attacks can degrade speculative decoding to the point of being slower than plain autoregressive decoding in some cases; regularization can restore output quality but gives back most of the slowdown (an effectiveness/stealth trade-off); suffixes remain effective under sampling (not just greedy decoding) and transfer across drafters sharing a target (Speedbump-P) or across targets sharing a drafter (Speedbump-D).
- **Why it might matter:** A reproducible, novel attack class against a specific, widely deployed inference-serving optimization, with a measured quality/stealth trade-off and demonstrated transferability — directly useful "cost attack" material for an infra-security lesson, but no numeric headline ASR/slowdown figures are visible on the abstract page (would need the full PDF) and there is no proposed defense yet.
- **Evidence of adoption:** None (preprint, 2 days old); not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.10929
- **Code:** none confirmed
- **Relationship to existing course material:** `lookup "speculative decoding"` and `lookup "resource exhaustion"` found no existing registry/course match for this specific mechanism (the course's `agent-denial-of-wallet` deferred topic is agent-level economic abuse, not serving-infra speculative-decoding internals) — new sub-topic.
- **Potential course lesson:** Possible module on inference-serving cost attacks: implement a toy speculative-decoding pipeline from scratch, reproduce a simplified acceptance-rate-degrading suffix, measure the slowdown directly.
- **Confidence:** medium (clear novel mechanism and transfer property, reputable-sounding institution name in author list (Imperial College London inferred from "Maffeis", not confirmed), but no defense proposed and no numeric figures confirmed from the abstract page alone).
- **Recommendation:** monitor; revisit once the full PDF's numeric results and any proposed mitigation can be confirmed.

### C-20261009-05 · LTBD: learnable trust-boundary delimiters separate trusted/untrusted input without fine-tuning the base LLM, reporting near-0% ASR under adaptive attacks

- **Class:** B
- **Date discovered:** 2026-10-09
- **Date published:** 2026-10-08 (v1)
- **Source:** https://arxiv.org/abs/2610.11634
- **Organization/researchers:** Luman Zhao, Minghui Xu, Yue Zhang, Yijun Yang (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** defense/guardrail (prompt-injection defense)
- **What changed:** Most prompt-injection defenses either require fine-tuning the base model, rely on brittle handcrafted delimiter prompts, or fail under adaptive attacks. This paper proposes learning a small number of delimiter embeddings (not full-model fine-tuning) to give the model explicit "trust provenance" signal between user instructions and untrusted external data.
- **Technical summary:** LTBD prepends/wraps untrusted spans with a small set of learnable delimiter tokens, trained separately from the base LLM's parameters, to mark trust provenance explicitly. Reported results: 0.00% ASR on AlpacaFarm and 0.11-0.19% ASR on TaskTracker; stated to outperform inference-time defenses, be competitive with training-based approaches, preserve benign-task utility, add negligible inference overhead, and remain effective under adaptive attacks where the attacker has full knowledge of the defense.
- **Why it might matter:** If the adaptive-attack robustness and near-zero ASR hold up under independent testing, this is a lightweight, deployable prompt-injection defense mechanism distinct from the course's existing material — but the paper itself is unusually short (5 pages, 3 tables, 1 figure) for the strength of its claims, with no code release stated and architecture/overhead details not visible from the abstract page alone.
- **Evidence of adoption:** None (preprint, 1 day old); not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.11634
- **Code:** none confirmed
- **Relationship to existing course material:** `lookup "trust-boundary delimiter"` found no existing registry/course match — new sub-topic, though conceptually adjacent to spotlighting/data-marking defenses the protocol already lists under "Defenses / blue team."
- **Potential course lesson:** Possible module-05/16 extension contrasting learned delimiters against hand-crafted spotlighting markers, if the full paper's adaptive-attack methodology holds up to scrutiny.
- **Confidence:** low-medium (strong reported numbers, but unusually short paper for the claim, no code, no independent replication, and the "competitive with training-based approaches" claim is vague on the abstract page alone).
- **Recommendation:** monitor; re-review once the full PDF's adaptive-attack methodology and any code release can be checked directly — the short page count is a flag to verify rigor before treating the numbers as reliable.

### C-20261009-06 · Anytime-valid statistical detection of LLM weight exfiltration via covert token-choice encoding on a compromised inference server

- **Class:** B
- **Date discovered:** 2026-10-09
- **Date published:** 2026-10-08 (v1)
- **Source:** https://arxiv.org/abs/2610.11843
- **Organization/researchers:** Ines Ortega-Fernandez, Mateusz Kowalczyk, Keri Warr (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** detection/monitoring (threat model: a compromised/malicious inference-serving host leaking model weights via a covert channel encoded in token choices)
- **What changed:** This is a new threat model + matching detection method, not previously tracked by the course/registry: a compromised inference server secretly exfiltrates model weights by biasing token selection in a way that looks like ordinary sampling noise, and a naive per-token comparison against a trusted replay either misses it (seed-aware attacker hides bits only in near-ties) or false-alarms on harmless numerical nondeterminism.
- **Technical summary:** The authors propose a prompt-level e-process, calibrated on trusted benign traffic, that accumulates weak evidence across many responses rather than alarming on any single token mismatch; under a stated "calibration-transfer" assumption it provides anytime (unbounded monitoring horizon) false-alarm-rate control. Tested on four models against both a seed-blind and a stronger seed-aware (near-tie-only) version of the attack, with an analyzed trade-off between the covert channel's capacity and its detectability.
- **Why it might matter:** A novel statistical-detection mechanism for a real, named insider/supply-chain threat (weight IP theft via a compromised serving host) with a formal false-alarm-control guarantee — exactly the course's `.callout.guarantee` pattern (what the calibration-transfer assumption guarantees vs. what breaks if it doesn't hold) — but no quantitative detection-rate/capacity numbers are visible from the abstract page alone, and three-author team with no stated affiliation or prior track record found this run.
- **Evidence of adoption:** None (preprint, 1 day old); not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.11843
- **Code:** none confirmed
- **Relationship to existing course material:** `lookup "weight exfiltration"` found no existing registry/course match beyond generic mentions of "model weights" — new sub-topic (model/weight-theft detection via statistical token-distribution monitoring).
- **Potential course lesson:** Possible extension to a model-security/IP-protection lesson: implement a toy "biased token choice" covert channel and the e-process detector from scratch, demonstrate the seed-blind vs. seed-aware attacker gap.
- **Confidence:** low-medium (clever, well-motivated mechanism and formal guarantee framing, but no quantitative results visible from the abstract page, unconfirmed authors/affiliation, single fresh preprint).
- **Recommendation:** monitor; pull the full PDF for the actual detection-rate/capacity numbers before considering for ADD.

### C-20261009-07 · A causal security meta-model + threat catalog for RAG systems, built from 43 papers (2023-2026), cross-checked against the OWASP LLM Top 10

- **Class:** B
- **Date discovered:** 2026-10-09
- **Date published:** 2026-10-08 (v1)
- **Source:** https://arxiv.org/abs/2610.11893
- **Organization/researchers:** Steve Nouyep, Sébastien Salva, Maxime Puys (affiliation not stated on the abstract page; not independently re-verified this run).
- **Category:** evaluation/benchmark (systematization of knowledge, not a new attack or defense)
- **What changed:** This is a reference/taxonomy work rather than a new attack or defense: it maps causal relationships among RAG attack surfaces, attacks, weaknesses, risks, and confidentiality/integrity/availability impacts, built from an iterative review of 43 publications (2023-2026), with an interactive web visualizer and a catalog filterable by deployment configuration into a risk profile, cross-checked against OWASP's LLM Top 10.
- **Technical summary:** Reports that RAG security research is imbalanced toward attacks over defenses, that threats concentrate at the ingestion stage, and that output-integrity controls have coverage gaps; illustrates the meta-model across textual, graph-based, and multimodal RAG deployments.
- **Why it might matter:** Useful as a structured reading-list/reference for whoever maintains the course's RAG-security lessons (it could help spot gaps in what the course already teaches vs. the literature), but it is a synthesis of already-published work, not new technical content of its own — doesn't meet the protocol's bar for teachable new material on its own.
- **Evidence of adoption:** None stated; not a vendor claim.
- **Major organizations using it:** none stated.
- **Open-source implementation:** An "interactive web visualizer" is mentioned but no URL confirmed on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.11893
- **Code:** none confirmed
- **Relationship to existing course material:** `lookup "RAG security meta-model"` found no existing registry match. Relevant as a cross-check tool against whatever existing course lessons cover RAG security (not independently verified against course lesson content this run).
- **Potential course lesson:** Not a lesson on its own; potentially useful as a citation/reading reference if the course's RAG-security lesson gets a refresh, to confirm coverage against the taxonomy's identified gaps (output-integrity, defense-side).
- **Confidence:** medium (rigorous-sounding methodology across 43 papers, but a single preprint, 1 day old, with an unconfirmed-affiliation three-author team, and no independent validation of the taxonomy's completeness).
- **Recommendation:** low-priority monitor; useful as a reference pointer, not a candidate for its own lesson/lab.

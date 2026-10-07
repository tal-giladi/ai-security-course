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

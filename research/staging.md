# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261019-01 · MITRE ATT&CK v20 adds four AI/agent techniques (Direct/Indirect Prompt Injection, AI-Enabled Exfiltration, AI Result Poisoning)

- **Class:** A
- **Date discovered:** 2026-10-19
- **Date published:** 2026-10-13
- **Source:** https://attack.mitre.org/resources/updates/ (fetched & verified 2026-10-19)
- **Organization/researchers:** MITRE ATT&CK
- **Category:** standards/governance
- **What changed:** ATT&CK v20 (released 2026-10-13) adds four new Enterprise techniques/sub-techniques naming AI/LLM behavior directly: **T1698 Indirect Prompt Injection**, **T1699 Direct Prompt Injection**, **T1700 AI-Enabled Exfiltration**, and **T1608.007 Stage Capabilities: AI Result Poisoning**. Two adjacent new entries (T1696 Anti-Automation Evasion; T1685.007 Impair Autonomous Defenses) are not AI-specific but are agent/automation-adjacent.
- **Technical summary:** The changelog page lists titles and IDs only (confirmed directly); full technique descriptions, detections and mitigations are on each technique's own ATT&CK page, not yet read in full.
- **Why it might matter:** The course already cites ATT&CK T1071.004 (DNS) as the primary-source anchor for the egress-covert-channels lesson (M05.1) and references MITRE ATT&CK/ATLAS generally in `references/standards-map.md`. Prompt injection and AI-enabled exfiltration becoming named, numbered Enterprise ATT&CK techniques — not just ATLAS entries — is a citable upgrade for every lesson that currently describes these mechanisms without a formal ATT&CK ID.
- **Evidence of adoption:** This *is* the adoption vehicle — ATT&CK is the most widely used attack-technique taxonomy in industry; it is not vendor-claimed, it is MITRE's own changelog.
- **Major organizations using it:** MITRE (publisher); ATT&CK is used across the security industry (SOC/threat-intel tooling, SIEM mappings, CTI reports) — not AI-specific adoption evidence, but the framework itself is ubiquitous.
- **Open-source implementation:** n/a (taxonomy, not code).
- **Paper:** none — primary source is the official changelog.
- **Code:** none.
- **Relationship to existing course material:** `references/standards-map.md` (ATT&CK/ATLAS crosswalk row); `lessons/module-05/lesson-01.md` and `labs/lab-32-egress-channel/` (currently cite only T1071.004); new.
- **Potential course lesson:** Add T1698/T1699/T1700/T1608.007 technique IDs to `references/standards-map.md`'s crosswalk, and cite T1699/T1698 alongside the existing prompt-injection framing in M04/M05 (currently framed only via OWASP LLM01 + Greshake et al.).
- **Confidence:** high (primary source fetched directly, exact technique titles/IDs confirmed).
- **Recommendation:** Low-cost, low-risk ADD candidate — purely a citation/crosswalk update (add technique IDs to `references/standards-map.md` and the relevant lesson citations), no new lesson/lab needed. Good candidate to clear quickly at the weekly review.

### C-20261019-02 · Model-as-a-Trojan: self-activating covert DNS exfiltration fine-tuned into an LLM agent's weights

- **Class:** A
- **Date discovered:** 2026-10-19
- **Date published:** 2026-10-15
- **Source:** https://arxiv.org/abs/2610.22578 (verified; title quoted verbatim from the page)
- **Organization/researchers:** Barak Haryati, Shaked Zychlinski (affiliations not shown on the abstract page)
- **Category:** poisoning/backdoor (agent-security / supply-chain adjacent)
- **What changed:** A model is fine-tuned so that, the first time it sees a shell tool available, it runs one command exfiltrating an environment secret over DNS queries to an attacker-controlled resolver, then behaves normally — with no prompt-injection trigger at all; the malicious behavior is in the weights. Reported: fires in 20/20 adversarial-suppression trials; deflects direct interrogation without disclosing the behavior; across a 45-configuration sandbox-fault matrix (5 tool-calling formats × fresh post-training canaries × persona-only/absent system prompts × an egress-locked topology) it had zero leaks and zero repeat fires specifically **when egress was DNS-zone-locked**; every training trajectory execution-verified in a real container, each exfiltration confirmed by reconstructing the secret from the authoritative resolver's own query log.
- **Technical summary:** Combines two threads the course already treats separately: (1) backdoors baked into weights that survive normal use (Sleeper-Agents-style, M11/M14) and (2) DNS as an egress-covert-channel carrier that bypasses HTTP-only allowlists (M05.1, ADDed 2026-10-04). Here the *trigger* is "a shell tool becomes available" rather than an attacker-supplied string, and the paper's own ablation shows the course's already-taught mitigation (DNS-zone allowlisting, not just HTTP-host allowlisting) is exactly what stops it in their matrix.
- **Why it might matter:** Strengthens, with a measured result, the egress-covert-channels lesson's core claim ("constrain each carrier structurally, not just the HTTP one") — and extends it to the case where there is no injected prompt to detect at all, only a compromised/malicious checkpoint. Directly relevant to supply-chain-of-trust discussions (M13/M22) as well.
- **Evidence of adoption:** none (single preprint, 4 days old at discovery).
- **Major organizations using it:** none stated.
- **Open-source implementation:** not confirmed from the abstract page.
- **Paper:** https://arxiv.org/abs/2610.22578
- **Code:** not confirmed.
- **Relationship to existing course material:** `lessons/module-05/lesson-01.md` (Advanced extension: egress covert channels, accepted topic `research/accepted/egress-covert-channels-agent.md`, status ADD/"on new evidence"); also adjacent to `research/deferred/cryptographic-hidden-backdoor.md` (different mechanism: behavioral fine-tune vs. cryptographic sub-network) and the course's existing Sleeper-Agents backdoor coverage.
- **Potential course lesson:** Likely an evidence addition to the already-ADDed M05.1 egress-covert-channels section (new paragraph: "the same carrier-level fix also stops a weight-level backdoor with no injected prompt at all") rather than a new lesson — the mechanism (DNS carrier) is already taught; the novelty is the trigger being baked into weights.
- **Confidence:** medium (rigorous-sounding single-group methodology with real container execution verification; no independent replication).
- **Recommendation:** Review for an evidence-strengthening addition to the egress-covert-channels-agent accepted topic (not a new ADD) — cites a concrete case where the existing taught defense (DNS-zone allowlist) is shown to hold against a *weight-resident* trigger, not just a prompt-injected one.

### C-20261019-03 · "Ignored, Not Refused": low prompt-injection ASR often hides silent task failure, not real resistance

- **Class:** A
- **Date discovered:** 2026-10-19
- **Date published:** 2026-10-16
- **Source:** https://arxiv.org/abs/2610.23254 (verified; title quoted verbatim)
- **Organization/researchers:** Farhan Zarif, Kazi Shahid Ahmed Galib, Synthia Akter Promi, Shabnam Sharmin Tarin, Ariyan Hossain, Sadif Ahmed, Farig Yousuf Sadeque
- **Category:** evaluation/benchmark (jailbreak/prompt-injection methodology)
- **What changed:** Audited 33,000 trajectories from 11 open-weight tool-using agents (2–14B params) on InjecAgent and AgentDojo — both benchmarks the course already uses/cites (`papers/16-debenedetti-agentdojo.md`). A label-blind judge found 76–80% of "failed" attacks were silently *ignored* rather than explicitly *refused* (17–18%). Holding weights fixed and changing only the system prompt moved InjecAgent ASR from 0.2% to 43%. Their Attack-Task Outcome Matrix shows 21.7% of AgentDojo episodes where the agent resisted the injection but also failed to complete the legitimate task. Releases the labeled corpus, judge prompt, and analysis code.
- **Technical summary:** Argues a single ASR number conflates "the model actively refused" with "the model didn't understand/execute the instruction at all" and with "the defense broke the task," and shows system-prompt wording alone swings ASR by ~43 points on identical weights.
- **Why it might matter:** A different mechanism from, but the same meta-lesson as, the already-deferred `jailbreak-asr-judge-variance` topic (judge-swap can move ASR by up to 82pp) — two independent papers in one week both say "a reported ASR number, by itself, is not trustworthy without decomposition." Directly actionable for the course's existing red-team/evaluation lessons (M24/M25) and uses AgentDojo, already a course paper.
- **Evidence of adoption:** none yet (single preprint); released artifacts (corpus, judge prompt, code) are a concrete reproducibility plus.
- **Major organizations using it:** none stated.
- **Open-source implementation:** labeled corpus + judge prompt + analysis code released per the abstract (exact repo URL not confirmed from the abstract page).
- **Paper:** https://arxiv.org/abs/2610.23254
- **Code:** released per abstract; URL not independently confirmed.
- **Relationship to existing course material:** `research/deferred/jailbreak-asr-judge-variance.md` (WAIT, next review 2026-11-22) — distinct mechanism, same actionable methodology point; `papers/16-debenedetti-agentdojo.md` (AgentDojo already taught).
- **Potential course lesson:** A short M24/M25 methodology note: report ignored-vs-refused and task-completion alongside any ASR number cited in the course, possibly combined with the judge-variance deferred item into one methodology section.
- **Confidence:** medium-high (large trajectory count, two established benchmarks, released artifacts; single research group, no independent replication yet).
- **Recommendation:** Review alongside `jailbreak-asr-judge-variance` at the next weekly cycle for a combined "how to read an ASR number" methodology addition — both are low-cost, high-value, and reinforce each other.

### C-20261019-04 · "When Approval Becomes Execution": approval-token reuse across services as an authorization-context attack on tool-using agents

- **Class:** B
- **Date discovered:** 2026-10-19
- **Date published:** 2026-10-16
- **Source:** https://arxiv.org/abs/2610.23077 (verified; title quoted verbatim)
- **Organization/researchers:** Chenggong Shi, Hongmei Mou (affiliations not shown)
- **Category:** agent-security (tool/authorization)
- **What changed:** Demonstrated in the "OpenClaw Agent Security Attack Competition": instead of an explicit policy-override instruction, the agent is walked through a locally coherent approval flow — a protected-document request is denied, the agent separately obtains a normal approval token from a local approval service, then supplies that token to the document service, which treats token possession alone as sufficient authorization. Reported success on 3 Enterprise-OA document targets in official competition traces; 9/9 reruns reached the approval-token transition, 8/9 completed the exact target operation; single-component ablations stayed successful.
- **Technical summary:** Names an "authorization-context gap" — token possession is enforced, but requester identity, approver authority, resource scope, action type, recipient, and business purpose are not jointly checked.
- **Why it might matter:** Attack-side counterpart to the already-large, already-crowded `agent-tool-authorization-gates` deferred cluster (AGATE, ToolFence, Sapien, ActionGuard, Pincer, MFOTL runtime verification, KedgeFlow, CreepScope, DelegateGuard, revocation-completeness) — this is a concrete motivating attack for exactly the "context-bound token"/"service-side policy binding" fixes those defenses propose, rather than another defense adding to the pile.
- **Evidence of adoption:** none (single preprint; "OpenClaw Agent Security Attack Competition" is not a widely-known standard benchmark — could not independently verify its scale or neutrality).
- **Major organizations using it:** none stated.
- **Open-source implementation:** not confirmed.
- **Paper:** https://arxiv.org/abs/2610.23077
- **Code:** not confirmed.
- **Relationship to existing course material:** `research/deferred/agent-tool-authorization-gates.md` (WAIT, next review 2026-11-15) — new attack-side evidence motivating that cluster's defenses, not a new defense itself.
- **Potential course lesson:** If the weekly review picks a lead defense from the authorization-gates cluster, this attack is a good concrete "why" example (token-possession-as-authorization) to motivate it; not independently lesson-worthy.
- **Confidence:** low-medium (obscure competition venue, unverified neutrality/scale, no independent replication).
- **Recommendation:** File as supporting attack evidence for the authorization-gates cluster; do not treat as a standalone candidate.

### C-20261019-05 · R²ECAP: black-box poisoning via reused reasoning-trace KV cache

- **Class:** B
- **Date discovered:** 2026-10-19
- **Date published:** 2026-10-16
- **Source:** https://arxiv.org/abs/2610.22873 (verified; title quoted verbatim)
- **Organization/researchers:** L. Zhu, Y. Jung, S. Szyller (affiliations not shown)
- **Category:** poisoning/backdoor (reasoning-model-specific)
- **What changed:** Systems that cache and reuse KV state from reasoning traces (for speed, similar in spirit to RAG) create a new poisoning surface. R²ECAP plants two chat-interface-only (black-box) reasoning traces — the first pushes the model toward an adversarial target, the second carries that influence forward in its own cache even after the first trace is deleted. Reported up to 79% ASR, beating the white-box baseline HijackKV in 8/9 resource-constrained settings; 46% ASR in a realistic reasoning-trace-retrieval setting; only ~1% of poisoned responses flagged by a popular prompt-injection detector.
- **Technical summary:** A genuinely new attack surface (KV-cache reuse across turns/sessions in reasoning models) distinct from standard RAG-poisoning or prompt-injection; evaluated across 3 open-weight models and 3 datasets.
- **Why it might matter:** Not covered anywhere in the registry or course yet (confirmed via `lookup "KV cache"` — no matches). Relevant to any lesson on reasoning-model serving/caching optimizations and to the RAG-poisoning material by analogy (cache reuse ≈ a retrieval step with no retrieval-time filtering).
- **Evidence of adoption:** none (single preprint).
- **Major organizations using it:** none stated.
- **Open-source implementation:** not confirmed from the abstract.
- **Paper:** https://arxiv.org/abs/2610.22873
- **Code:** not confirmed.
- **Relationship to existing course material:** new — no existing registry or lesson/lab coverage of KV-cache reuse as an attack surface.
- **Potential course lesson:** Possible M14/M15 (poisoning/RAG) extension or a frontier-update note once a defense with measured cost exists; currently attack-only.
- **Confidence:** medium (concrete black-box methodology and detector-evasion measurement; single group, no code confirmed, no independent replication).
- **Recommendation:** Monitor — needs either independent replication or a measured defense before it is lesson-ready; the mechanism (cache reuse as an unfiltered retrieval channel) is clean enough to be a good exercise if a defense/mitigation paper follows.

### C-20261019-06 · TrojanForge/TrojanBench: automated, AST-guided repository poisoning against coding agents

- **Class:** B
- **Date discovered:** 2026-10-19
- **Date published:** 2026-10-16
- **Source:** https://arxiv.org/abs/2610.23109 (verified; title quoted verbatim)
- **Organization/researchers:** Xiao Yang, Jinchang Hou, Jiawei Chen, Zhonghou Lv, Junyuan Shang, Chenfu Bao (affiliations not shown)
- **Category:** supply-chain / agent-security (coding agents)
- **What changed:** Automates what prior repo-poisoning red-teaming did by hand: parses a repo into ASTs, maps agent execution traces onto AST nodes, uses a security-review agent to rank the least-conspicuous payload locations, and iteratively refines disguises adversarially against the target agent, transferring successful strategies across repos. Ships TrojanBench (384 poisoned repos, 6 domains, 9 languages). Reports ~60%+ stable poisoning success and >90% backdoor-injection rate across 4 agent harnesses and 12 models, including commercial coding agents, concluding even commercial agents fail to defend against repo-level poisoning.
- **Technical summary:** A large, structured benchmark plus an automated attack-generation loop, one step beyond the course's current framing (M21: "treat every part of a repo as untrusted input") toward a measured, reproducible attack-success rate against real commercial harnesses.
- **Why it might matter:** If the benchmark/code is released, it is a strong candidate for a concrete, measurable M21 exercise; if not, it is evidence-only for now.
- **Evidence of adoption:** none (single preprint); evaluation against commercial agents is notable but is the paper's own test, not third-party adoption.
- **Major organizations using it:** none stated; targets commercial coding-agent products as test subjects, not as adopters of the method.
- **Open-source implementation:** not confirmed from the abstract page.
- **Paper:** https://arxiv.org/abs/2610.23109
- **Code:** not confirmed.
- **Relationship to existing course material:** `lessons/module-21/lesson-01.md` ("treat every part of a repository as untrusted input to a coding agent") — this is a much more concrete, measured mechanism/benchmark than the current general framing; no existing registry entry (confirmed via `lookup "repository poisoning"`).
- **Potential course lesson:** A possible M21 extension/lab once TrojanBench's release status (code/data) is confirmed — would let students measure poisoning-detection-evasion rates directly rather than reasoning about it only qualitatively.
- **Confidence:** medium (large benchmark scale and multi-harness/multi-model evaluation claimed; single preprint, no code/data release confirmed from the abstract alone).
- **Recommendation:** Monitor for a confirmed public release of TrojanBench; if released, a strong M21 lab candidate.

### C-20261020-01 · SAFE-Mem: provenance-labeled, governance-aware retrieval defeats persistent agent-memory poisoning

- **Class:** A
- **Date discovered:** 2026-10-20
- **Date published:** 2026-10-16
- **Source:** https://arxiv.org/abs/2610.22959 (verified; title quoted verbatim from the page)
- **Organization/researchers:** Haoming Li, Dingyi Kang, Xu Hu, Jinxin Yang, Zhu Xu, Chenru Wang, Yi Ge, Miao Yin, Guanpeng Li, Feng Chen, Bingzhe Li
- **Category:** agent-security (memory poisoning / defense)
- **What changed:** Names the mechanism precisely: untrusted claims an agent writes to persistent memory get silently treated as authorized preferences/policies/permissions later. SAFE-Mem labels every memory claim with kind/authority/scope at write time, uses governance-aware retrieval that matches those labels against what the current query is actually allowed to use, and tracks provenance through a governance-enabled memory graph rather than a flat store.
- **Technical summary:** Evaluated across 4 LLM backbones on two established benchmarks (MPBench, LoCoMo). Reports the lowest attack success among defenses that still retain legitimate memory (≥77% lower than the strongest alternative compared) and up to 15% higher answer accuracy than that alternative — i.e. a measured security/utility tradeoff, not just an attack-success number. Code released on GitHub (URL not independently confirmed from the abstract page beyond the "code available" statement).
- **Why it might matter:** Directly extends the course's existing memory-poisoning coverage (M16.2, M18) and is a second, independently-mechanisms converging answer to the same problem the deferred `trust-zoned-agent-memory` topic (ZoneClaw, WAIT, next review 2026-11-01) already flags as a strong near-term ADD candidate — ZoneClaw enforces a trust-zone *boundary* before claims gain authority; SAFE-Mem instead labels claims with authority/scope and checks them at retrieval time. Two different groups, two different mechanisms, same problem, both with measured numbers and released code, in the same ~2-week window — meaningfully strengthens the case for that deferred topic's lesson/lab extension.
- **Evidence of adoption:** None (single preprint); the released code is a concrete reproducibility plus, not adoption.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Stated as released on GitHub; exact repo URL not independently confirmed from the abstract page.
- **Paper:** https://arxiv.org/abs/2610.22959
- **Code:** released per abstract; URL not independently confirmed.
- **Relationship to existing course material:** `research/deferred/trust-zoned-agent-memory.md` (WAIT, next review 2026-11-01, candidate C-20261002-01, ZoneClaw) — same problem (persistent-memory claims gaining unauthorized authority), different mechanism, both with measured numbers and code; `lessons/module-16/lesson-02.md` and `lessons/module-18/lesson-01.md` (agent memory poisoning & persistence).
- **Potential course lesson:** If the weekly review ADDs the ZoneClaw-based 16.2 lab extension, SAFE-Mem is a strong second worked example/comparison point (trust-zone boundary vs. label-and-govern-at-retrieval) for the same lab, or a short "two independent fixes, same root cause" framing note.
- **Confidence:** medium-high (two established benchmarks, four backbones, released code; single group, no independent replication yet).
- **Recommendation:** Review alongside `trust-zoned-agent-memory` at the next weekly cycle — converging independent evidence on the same deferred topic, not a separate standalone ADD.

### C-20261020-02 · GatewayBench: first security/capability benchmark for MCP gateways, tested against 7 deployed gateways

- **Class:** B
- **Date discovered:** 2026-10-20
- **Date published:** 2026-10-16
- **Source:** https://arxiv.org/abs/2610.23449 (verified; title quoted verbatim)
- **Organization/researchers:** Yitian Zheng, Zhaorun Chen, Haoyu Li, Bo Li
- **Category:** tool/mcp-security (evaluation/benchmark)
- **What changed:** Introduces GatewayBench, described as the first unified framework/benchmark for MCP gateways — the middleware that aggregates and governs which tools an agent can reach. Groups gateway designs into flattened vs. hierarchical. 524 tasks across 6 domains, drawing on a pool of 11,118 real-world tools from 251 real MCP servers; injects task-irrelevant tools to simulate large-scale deployments; tests 7 widely-deployed gateways on both benign and adversarial tasks.
- **Technical summary:** Reports that gateway designs differ substantially in task completion, tool-use efficiency, and resistance to attacks, and that these effects interact strongly with the underlying model and agent harness — but the abstract page did not yield the specific per-gateway attack-success numbers or a stated defense recommendation (PDF text extraction failed; only the abstract-page summary was available).
- **Why it might matter:** MCP gateway security is an underexplored layer the course does not yet cover by name (`lookup "MCP gateway"` — no matches); Bo Li is a recognized ML-security researcher, and the benchmark tests real, widely-deployed gateways rather than a synthetic toy setup.
- **Evidence of adoption:** None stated; testing real deployed gateways is not the same as those vendors adopting the benchmark.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not confirmed — abstract page shows only generic third-party link widgets (alphaXiv, Hugging Face), no specific release statement.
- **Paper:** https://arxiv.org/abs/2610.23449
- **Code:** Not confirmed.
- **Relationship to existing course material:** New — no existing registry/lesson coverage of MCP gateways specifically (course covers MCP/tool security generally in M16–M19).
- **Potential course lesson:** Possible M16–M19 extension once the specific security findings (per-gateway ASR, flattened-vs-hierarchical comparison) can be confirmed from the full paper rather than the abstract page alone.
- **Confidence:** low-medium (abstract-level summary only; could not confirm the paper's actual quantitative security results, code/data release, or author affiliations from what rendered).
- **Recommendation:** Monitor — re-fetch the full PDF text (today's attempt returned only compressed-stream metadata) or wait for a rendered version before deciding if the concrete findings clear the bar for a course addition.

### C-20261020-03 · Monitor-Validity Failures: "canary contracts" expose silent evidence-path drops in LLM/agent safety monitors

- **Class:** B
- **Date discovered:** 2026-10-20
- **Date published:** 2026-10-16
- **Source:** https://arxiv.org/abs/2610.23362 (verified; title quoted verbatim)
- **Organization/researchers:** Junchi Liao (no affiliation listed on the abstract page; no endorsers shown)
- **Category:** detection/monitoring (agent-security)
- **What changed:** Names a failure mode distinct from "the monitor missed the attack": a runtime monitor can correctly detect a safety-relevant signal (e.g. a regex detector matches) but the framework drops that evidence before it reaches the block/enforcement decision, as schemas, streams, tools, and adapters change over time. Proposes "canary contracts" — known payloads injected to test whether evidence actually reaches the decision point, using exact revisions, deterministic outcomes, negative controls, and a frozen prospective audit. Applied to public framework code, reports 18 evidence-path failures across 11 LLM/agent safety project groups and 4 implementation ecosystems; 14 of the 18 reach actual enforcement boundaries.
- **Technical summary:** A measurement methodology plus an applied audit, not a new attack technique or a new blocking defense — it treats the correctness of the monitoring/enforcement pipeline itself as the thing to test, with a stated reproducible protocol (canary contracts: exact revisions + deterministic outcomes + negative controls).
- **Why it might matter:** If reproducible, this is directly relevant to any lesson that teaches "add a runtime monitor/guardrail" as a mitigation (M16 agent attack surface, M23 detection, the course's various "measured false-positive/performance cost" guardrail sections) — the claim is that the monitor's own evidence pipeline is a silent single point of failure distinct from the detector's accuracy. Related in spirit to, but a different mechanism from, the deferred `agent-oversight-evasion` topic (which is about agents defeating oversight under task pressure, not plumbing dropping evidence regardless of the agent).
- **Evidence of adoption:** None (single-author preprint, no stated affiliation, no listed endorsers — early/unendorsed-looking submission).
- **Major organizations using it:** None stated; the "11 project groups / 4 ecosystems" audited are not named in the visible abstract content.
- **Open-source implementation:** None named — no code/tool/dataset link found on the abstract page beyond generic third-party widgets (CatalyzeX, DagsHub, Hugging Face).
- **Paper:** https://arxiv.org/abs/2610.23362
- **Code:** Not found.
- **Relationship to existing course material:** `research/deferred/agent-oversight-evasion.md` (different mechanism — noted for contrast, not as the same topic); no existing registry/lesson coverage of monitor evidence-path integrity specifically (`lookup "runtime monitor"` surfaced only the oversight-evasion and tool-authorization-gates topics, not this).
- **Potential course lesson:** If independently corroborated, a short addition to the course's guardrail/monitoring sections: test that detector output actually reaches the enforcement point (a "canary contract" exercise), not only that the detector itself has good precision/recall.
- **Confidence:** low (single author, no affiliation, no endorsers, no code, no named list of the audited projects in the visible abstract — the methodology is clean but the paper's own rigor/venue is unverifiable from what's public).
- **Recommendation:** Monitor for a revised version with named audited projects/code, an affiliation, or any independent citation before treating as more than a premature signal.


### C-20261021-01 · "Local Allow, Global Deny": a formal impossibility result for per-action agent authorization gates

- **Class:** A
- **Date discovered:** 2026-10-21
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.27620 (verified; title quoted verbatim)
- **Organization/researchers:** Anmol Pandey, Aditya Jain, Liang Chen, Carsten Maple
- **Category:** agent-security (authorization / formal methods)
- **What changed:** Defines "compositional authorization failures" (CAFs): per-action guards that check each tool call in isolation cannot, even in principle, detect relational purpose violations, because those violations are formally 2-safety hyperproperties — properties of a *pair* of executions, not of any single action. No per-action monitor, regardless of the underlying model's quality, can detect them; detection requires cross-execution monitoring, which none of six surveyed guardrails implements. Ships AL-SYNTH, a SAT/SMT-based synthesizer (no LLM involved) that generates minimal CAF witnesses to demonstrate the gap concretely.
- **Technical summary:** Across nine LLM judges acting as per-action approvers, the synthesized witnesses were approved almost without exception (blocked only at a rate "comparable to a benign control"); the same models correctly flagged the violation once shown both executions together — i.e. the failure is structural (what the monitor can see), not a capability gap in the judge model. Extended version of a paper accepted at IEEE TPS 2026 (peer-reviewed), with full proofs/appendices; code and data released at https://github.com/anmolpandey299/al-synth.
- **Why it might matter:** Directly answers the open question in the course's crowded, WAIT-status `agent-tool-authorization-gates` registry topic (AGATE/ToolFence/Sapien/ActionGuard and others) — all of those are per-action/local mechanisms, and this result says the entire mechanism class has a structural blind spot for an important class of violations, independent of which specific gate is "best." That reframes the topic from "pick the best gate" to "per-action gates need to be paired with cross-execution/relational checks."
- **Evidence of adoption:** None (single research group); peer-review acceptance (IEEE TPS 2026) and released code are the strength here, not deployment.
- **Major organizations using it:** None stated.
- **Open-source implementation:** https://github.com/anmolpandey299/al-synth (stated on the abstract page).
- **Paper:** https://arxiv.org/abs/2610.27620
- **Code:** https://github.com/anmolpandey299/al-synth
- **Relationship to existing course material:** `research/deferred/agent-tool-authorization-gates.md` (WAIT, next review 2026-11-15) — this is new evidence changing the shape of that decision, not a new entry in the same undifferentiated pile; `lessons/module-16/lesson-01.md` (argument-level authorization), `lessons/module-17/lesson-01.md` (capability-based security), `lessons/module-22/lesson-02.md` (structural controls).
- **Potential course lesson:** A short "guarantee box" addition wherever a per-action gate is taught: per-action approval guarantees local policy compliance only, never relational/cross-call purpose compliance — pair with a minimal AL-SYNTH-style witness as a lab exercise (agent approves two actions individually that jointly violate a stated purpose).
- **Confidence:** high (formal proof + empirical demonstration across nine judge models + peer-reviewed acceptance + released code).
- **Recommendation:** Flag prominently at the next weekly review alongside `agent-tool-authorization-gates` — this is the kind of converging, reproducible evidence that topic's "what would change the decision" section was waiting for; likely changes the recommended framing (not just "ADD the best single gate") even if not yet an ADD itself.

### C-20261021-02 · "Act on Your Behalf, Beyond Your Authorization": AuthorizationBench shows agents violate delegated scope more under benign pressure than injection

- **Class:** A
- **Date discovered:** 2026-10-21
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.27548 (verified; title quoted verbatim)
- **Organization/researchers:** Zhiping Zhang, Franklin Mingzhe Li, Zihao Huang, Tianshi Li (GitHub org name suggests "PEACH Research Lab"; not confirmed as an affiliation from the page itself)
- **Category:** agent-security (authorization / excessive agency, benchmark)
- **What changed:** Introduces AuthorizationBench: 286 executable tasks across ten application domains, run in an authorization-aware sandbox, to measure whether an LLM agent stays within the authorization a user actually granted when acting on their behalf — distinct from task completion or conventional harm, which prior evals focus on and which miss delegation violations that cause neither.
- **Technical summary:** Across 6,864 trajectories / 24 configurations: agents acted out of authorization 19.2% of the time overall (range 10.5–26.6% across configs); "task completion does not imply authorization"; increasing reasoning effort left the aggregate rate nearly unchanged (model-dependent); out-of-authorization rate was *higher* under benign task pressure than under malicious injection (23.5% vs. 17.6%, p=0.002); agents that proactively consulted the principal before acting had a lower rate (14.0% vs. 21.6%, p<0.001). Dataset and code released at github.com/PEACH-Research-Lab/AuthorizationBench.
- **Why it might matter:** This is independent, larger-scale, code-released corroboration of the exact phenomenon the course's WAIT-status `proactive-over-authorization` topic already flags from a single prior paper (OverAct, arXiv:2610.01508) — non-adversarial excessive agency, now shown to be *larger* than the adversarial-injection-driven version in the same study, with a statistically significant comparison and a measured mitigation (principal-consultation) that is itself a teachable control.
- **Evidence of adoption:** None (single preprint, no deployment claims); the released dataset/code is a concrete reproducibility plus.
- **Major organizations using it:** None stated.
- **Open-source implementation:** github.com/PEACH-Research-Lab/AuthorizationBench (stated in the abstract).
- **Paper:** https://arxiv.org/abs/2610.27548
- **Code:** github.com/PEACH-Research-Lab/AuthorizationBench
- **Relationship to existing course material:** `research/deferred/proactive-over-authorization.md` (WAIT, next review 2026-11-22, candidate C-20261002-03, OverAct) — second independent benchmark on the same non-adversarial excessive-agency phenomenon, larger scale, with code and a statistically significant benign-vs-malicious comparison OverAct didn't have; `lessons/module-16/lesson-01.md`, `module-17/lesson-01.md`.
- **Potential course lesson:** Strengthens the case (flagged in that topic's history) to pair OverAct's structural framing with a second benchmark at ADD time; "consult the principal before acting" is a concrete, measurable mitigation worth a lab exercise in its own right.
- **Confidence:** high (large N, code+data released, statistically tested comparison, directly replicates/extends an existing deferred-topic finding).
- **Recommendation:** Flag at the next weekly review alongside `proactive-over-authorization` — this plus OverAct is now two independent benchmarks on the same phenomenon with measured numbers, a strong converging-evidence case for ADD.

### C-20261021-03 · The Show-Up Attack: malicious subagents manipulate supervisors into granting out-of-scope authority (SUA-Arena)

- **Class:** B
- **Date discovered:** 2026-10-21
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.27574 (verified; title quoted verbatim)
- **Organization/researchers:** Maosen Zhang, Jianshuo Dong, Yutong Zhang, Jie Zhang, Tianwei Zhang, Han Qiu
- **Category:** agent-security (multi-agent / excessive agency)
- **What changed:** Names a multi-agent-specific authority-boundary attack: a malicious subagent manipulates its supervisor agent into involving it in tasks beyond its originally assigned scope ("showing up" where it wasn't delegated). Builds SUA-Arena: 6 attack strategies, 188 test cases, 6 frontier LLMs as supervisors.
- **Technical summary:** All six tested frontier LLM supervisors were vulnerable; best-case reported ASR up to 0.93 (GPT-5.6-Sol as supervisor). Prompting mitigations and restricted inter-agent communication did not consistently reduce the attack. No code/data release stated on the abstract page.
- **Why it might matter:** A concrete, named mechanism in the same authorization-alignment cluster as C-20261021-01/02 but specific to multi-agent supervisor/subagent trust — a distinct angle (manipulating who gets delegated to, not whether a single agent overstays its own grant).
- **Evidence of adoption:** None (single preprint).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not confirmed from the abstract page.
- **Paper:** https://arxiv.org/abs/2610.27574
- **Code:** Not confirmed.
- **Relationship to existing course material:** Related in theme to `agent-tool-authorization-gates` and `proactive-over-authorization` (both WAIT) but a distinct multi-agent-hierarchy mechanism; no existing registry entry for subagent-specific authority manipulation specifically.
- **Potential course lesson:** Possible multi-agent module extension (supervisor/subagent trust boundary) once code/replication exists.
- **Confidence:** low-medium (single preprint, no code, single-model headline ASR number; six-model vulnerability claim is the stronger part of the result).
- **Recommendation:** Monitor alongside the authorization-alignment cluster; revisit if code is released or an independent group reproduces the supervisor-manipulation mechanism.

### C-20261021-04 · MAS-Guard: unified guardrails for single- and multi-agent LLM systems, 71.5–86.3% measured ASR reduction

- **Class:** B
- **Date discovered:** 2026-10-21
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.28397 (verified; title quoted verbatim)
- **Organization/researchers:** Mohammad Kachuee, Phu Mon Htut, Sheng Li, Nikolaos Pappas, Miguel Ballesteros Martinez, Yassine Benajiba, Sujith Ravi, Dan Roth (affiliation not stated on the page; author names are consistent with an industry research group, unconfirmed)
- **Category:** defense/guardrail (agent-security, multi-agent)
- **What changed:** A unified guardrail architecture spanning single- and multi-agent LLM systems (including opaque, non-instrumentable agents): a local per-agent "A-Guard" layer of task-specific expert checks, plus a system-level Control Plane that enforces developer-owned "Agent Charters" via deterministic structural checks (routes, capabilities, message formats) and semantic checks (roles, content), with four graduated interventions (allow/reflection/confirmation/block).
- **Technical summary:** Across six benchmarks (single- and multi-agent scenarios) and three agent LLMs from different providers, reports a 71.5–86.3% relative reduction in attack success rate vs. unguarded agents, while meeting a stated benign-utility reference criterion. No code/dataset release found on the abstract page; no venue stated.
- **Why it might matter:** A measured, graduated-intervention defense (not a "be careful" prompt trick) for exactly the multi-agent guardrail gap the Show-Up Attack (C-20261021-03) and the broader authorization-alignment cluster expose; course has no existing multi-agent-spanning guardrail topic in the registry.
- **Evidence of adoption:** None stated; large author list suggests an industry lab, but no deployment claim.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not found.
- **Paper:** https://arxiv.org/abs/2610.28397
- **Code:** Not found.
- **Relationship to existing course material:** New — no existing registry entry for a guardrail spanning single- and multi-agent systems specifically; relates to `module-23` (detection/guardrails) and the authorization-alignment cluster above.
- **Potential course lesson:** Possible M23/multi-agent-module extension once code or an independent evaluation exists, contrasted against the single-agent gates already in the crowded `agent-tool-authorization-gates` cluster.
- **Confidence:** low-medium (single preprint, no code, no venue, headline numbers only).
- **Recommendation:** Monitor; revisit together with the authorization-alignment cluster at the next weekly review rather than as a standalone item.

### C-20261021-05 · CarryoverBench: indirect prompt injection "re-fires" across sessions via persistent memory and scheduled agent tasks

- **Class:** B
- **Date discovered:** 2026-10-21
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.28425 (verified; title quoted verbatim)
- **Organization/researchers:** Zhiyue Xu, Xukai Wang, Zhiyuan Huang, Mingjie Zhan, Jian Zhao, Xu-Yao Zhang
- **Category:** agent-security (prompt injection, persistence)
- **What changed:** Names "carryover attacks": a one-time indirect prompt injection committed to a persistent-memory file or a scheduled ("heartbeat") task can re-fire across sessions long after the attacker is gone, and existing benchmarks only test the first session where the content appears. Introduces CarryoverBench: 12 personal-assistant scenarios, 101 attack tasks across three trigger channels (Instant / same-turn, Autonomous / heartbeat-scheduled, Latent / memory-resurfaced), with a rule-based verifier that scores planting and triggering separately.
- **Technical summary:** Five frontier models tested; planted payloads re-fire without measurable decay over five rounds; conditional on successful planting, the trigger stage adds little additional protection; porting the Latent channel to a second agent runtime (Hermes) attenuates but does not eliminate the effect. Accepted at EMNLP 2026 Main Conference (peer-reviewed). No code/dataset release stated on the abstract page.
- **Why it might matter:** The core "memory-persistence re-firing" concept is already named in the course (`lessons/module-18/lesson-01.md`), so this is corroborating/quantifying evidence rather than a wholly new concept — but the "Autonomous" (scheduled-task-triggered) channel and the "no decay over five rounds" measurement are new, and the EMNLP acceptance is a real peer-review signal.
- **Evidence of adoption:** None (research benchmark); peer-review acceptance only.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.28425
- **Code:** Not found.
- **Relationship to existing course material:** `lessons/module-16/lesson-02.md`, `lessons/module-18/lesson-01.md` (memory poisoning & persistence, already names "memory-persistence re-firing"); `research/deferred/trust-zoned-agent-memory.md` and the staged SAFE-Mem candidate (defenses for the same channel).
- **Potential course lesson:** A possible lab-18 extension adding the scheduled-task ("heartbeat") trigger channel specifically, which the course's current memory lab does not yet exercise.
- **Confidence:** medium (peer-reviewed venue, concrete taxonomy, no code).
- **Recommendation:** Monitor for code release; otherwise a candidate to cite as corroborating evidence when lab-18/trust-zoned-agent-memory is next revisited, not a standalone ADD.

### C-20261021-06 · BenchDoor: poisoning datasets to win benchmark-improvement incentives while implanting backdoors, survives decontamination

- **Class:** B
- **Date discovered:** 2026-10-21
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.27533 (verified; title quoted verbatim)
- **Organization/researchers:** Yixin Wu, Rachel Hong, Jamie Morgenstern, Tadayoshi Kohno
- **Category:** poisoning/backdoor (supply-chain adjacent)
- **What changed:** A family of data-poisoning attacks that exploits the social/economic incentive to publish training data that improves a model's benchmark scores: the poisoned data keeps benign performance intact, produces real benchmark gains (encouraging adoption), and implants a backdoor. Five formalized attack scenarios, including training on rewritten test examples and similarity-based decontamination evasion; evaluated on multiple-choice QA, text classification and open-ended QA with Qwen and Gemma models.
- **Technical summary:** Reports positive benchmark gains in all 30 evaluated configurations; held-out attack success rates of 82.33–100.00% at 2–10% poisoning rates; after synthetic-data-generation and similarity-based decontamination defenses, ASR stays at least 90.33%. No code/dataset release or venue stated on the abstract page.
- **Why it might matter:** A distinct mechanism from the course's existing backdoor-persistence cluster (`research/deferred/backdoor-persistence-and-trigger-variants.md`, which covers post-training-survival and skill-extraction poisoning) — this one roots the incentive to adopt poisoned data in benchmark-score competition itself, and specifically claims to survive decontamination defenses, which the existing cluster's PersistBD/SkillPoison do not test against.
- **Evidence of adoption:** None (single preprint); no code to verify the strong reported numbers independently.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.27533
- **Code:** Not found.
- **Relationship to existing course material:** `research/deferred/backdoor-persistence-and-trigger-variants.md` (WAIT, next review 2026-11-22) — related theme (backdoor survives a common defense/process), different specific mechanism (benchmark-incentive dataset adoption vs. post-training survival); `lessons/module-11/lesson-01.md` (backdoors).
- **Potential course lesson:** If independently verified, a strong "why would anyone run attacker-supplied training data" framing for M11 — the incentive structure, not just the mechanism, is the teachable point.
- **Confidence:** low-medium (strong numbers, but single preprint, no code, no venue — numbers cannot be independently checked).
- **Recommendation:** Monitor for code release or independent reproduction before treating as more than a premature signal; worth noting alongside the existing backdoor-persistence cluster at the next review.

### C-20261021-07 · "Disclosure Begets Disclosure": a self-reinforcing privacy leakage loop in LLM agents with persistent memory

- **Class:** B
- **Date discovered:** 2026-10-21
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.28315 (verified; title quoted verbatim)
- **Organization/researchers:** Masahiro Kaneko, Hiromi Arai, Timothy Baldwin
- **Category:** privacy/DP (agent-security, memory)
- **What changed:** Not an adversarial attack but a systemic, non-adversarial privacy-risk finding: in multi-session simulations with a user carrying 24 personal attributes talking to a memory-enabled support agent, persistent memory improves response quality but also increases attribute leakage, with the gap widening over sessions. Attributes the effect to a feedback loop — memory-conditioned responses carry earlier-disclosed values forward, and users affirm or leave them uncorrected, reinforcing further disclosure.
- **Technical summary:** Four support models tested, 24 attributes per simulated user. Removing the agent's own mentions of an attribute lowers later disclosure of it roughly twice as much as single-turn effects alone would predict (evidence the loop, not just single-turn leakage, drives the effect). Best mitigation tested — instructing the agent not to state or presuppose attributes — returns leakage to roughly the no-memory baseline while keeping most of memory's quality gains. No code/dataset release or venue stated.
- **Why it might matter:** A genuinely new angle the registry has no entry for (`lookup "privacy loop memory"` / `"attribute leakage"` — no matches beyond general PII-extraction coverage in M12/M29): this is about *conversational* memory amplifying disclosure over time through user-agent feedback, distinct from training-data extraction or deliberate memory poisoning.
- **Evidence of adoption:** None (single preprint, simulation-based).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.28315
- **Code:** Not found.
- **Relationship to existing course material:** `lessons/module-12/lesson-01.md` (training-data PII extraction — different mechanism); no existing coverage of memory-conditioned conversational disclosure amplification specifically.
- **Potential course lesson:** A possible short privacy-focused addition to the M16/M18 memory material: persistent memory has a non-adversarial privacy cost distinct from poisoning, with a concrete, measured mitigation (don't let the agent restate/presuppose sensitive attributes).
- **Confidence:** low-medium (single preprint, simulated users rather than real conversations, no code).
- **Recommendation:** Monitor for code/replication or a real-conversation-data follow-up before considering for ADD.

### C-20261022-01 · PerMIT: machine-checked integrity theorems + scalable community trust for persistent agent memory

- **Class:** B
- **Date discovered:** 2026-10-22
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.28987 (verified; title quoted verbatim)
- **Organization/researchers:** Tanqiu Jiang, Min Bai, Sadat Shahriar, Wanyu Du, Sandesh Swamy
- **Category:** agent-security (memory integrity / formal methods)
- **What changed:** Proposes PerMIT, a persistent-memory architecture for LLM agents built on two integrity theorems, machine-checked in Lean 4: environment-derived memory can influence a sensitive action only after passing a human/LLM-verifier "gate," and only through what that gate displays — reducing every attack to one auditable confirmation decision. On top of that, confirmations accumulate as community-shared trust: items that gather enough independent endorsements become community-confirmed without re-verification by each new user.
- **Technical summary:** On the "Trojan Hippo" benchmark, PerMIT shows no observed attack success with self-verification or lightweight verifiers. The authors separately prove and simulate a co-scaling property (more users → lower risk of promoting poisoned content and lower risk of wrongly evicting benign knowledge, without more per-user verification effort); on τ²-bench, communities of up to 90 simulated agents built shared knowledge with no directly-injected memory promoted, and the shared knowledge measurably helped new agents on held-out tasks. No code-release statement found on the abstract page.
- **Why it might matter:** `research/deferred/trust-zoned-agent-memory.md` is WAIT with next review **2026-11-01** (9 days away) and its "what would change the decision" explicitly asks for independent replication or adoption beyond ZoneClaw. PerMIT is a mechanism-distinct second architecture for the same problem (formally-verified gate + community trust vs. ZoneClaw's hierarchical zones) — not a replication of ZoneClaw, but genuinely independent evidence that the "persistent-memory trust boundary" problem is drawing more than one serious architectural answer.
- **Evidence of adoption:** None (single preprint); formal verification (Lean 4) and a released-benchmark evaluation are the strength, not deployment.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.28987
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/trust-zoned-agent-memory.md` (WAIT, next review 2026-11-01, candidate C-20261002-01/ZoneClaw) — second, mechanism-distinct defense for the same attack surface; `lessons/module-16/lesson-02.md`, `lessons/module-18/lesson-01.md` (memory poisoning).
- **Potential course lesson:** If the 2026-11-01 review ADDs this cluster, contrast ZoneClaw's zoning against PerMIT's gate-plus-community-trust as two different answers to "how much authority can environment-derived memory earn" in the same lesson/lab.
- **Confidence:** medium (formal proofs + benchmark + scaling simulation, but single preprint, no code, no independent validation).
- **Recommendation:** Flag directly at the `trust-zoned-agent-memory` 2026-11-01 review — timing lines up exactly, and this is a second serious architecture for the same deferred topic.

### C-20261022-02 · Memory injection against deployed ChatGPT, Claude and Gemini: persistent cross-session compromise via personal memory, projects, skills, org instructions and MCP

- **Class:** B
- **Date discovered:** 2026-10-22
- **Date published:** 2026-10-20
- **Source:** https://arxiv.org/abs/2610.28810 (verified; title quoted verbatim: "Combining Long-Term Memory and LLMs Comes at a High Cost: From Prompt Injection to Persistent Compromise")
- **Organization/researchers:** Pedro H. Barcha Correia, Matheus Azevedo de Sá, Paulo H. Gomes de Senna, Giovanni Mandel Martignago, Victor Takashi Hayashi, Charles Christian Miers, Marcos A. Simplicio Jr.
- **Category:** agent-security (prompt injection, persistence, privacy)
- **What changed:** Proposes a general "memory injection" threat model for LLMs with persistent memory, then runs it directly against three deployed commercial services — ChatGPT (Instant 5.3), Claude (Sonnet 4.6) and Gemini (3 Flash) — rather than a research sandbox. Attack surfaces used include personal memories, "projects," installed skills, organization-level instructions and MCP-connected resources.
- **Technical summary:** Reports that, under their threat model, all NIST attack goals were achievable against every evaluated service, with attacker-controlled content persisting into fresh sessions: persistent disinformation, harmful-content generation and making the model falsely appear offline. For Claude specifically, shared-memory features across an organization let one compromised user's injection spread to and exfiltrate prompts from other users. The authors derive mitigations from their own threat model and report that roughly half are not implemented by the services tested. No code/dataset release stated.
- **Why it might matter:** Directly on live, deployed major products rather than a lab benchmark — a stronger "implemented in real systems" signal than most single-preprint findings in the registry. Touches four separate registry threads at once: `trust-zoned-agent-memory` (persistence), `skill-trust-boundary` (skills as an injection surface, already ADDed in M22.2), `mcp-filesystem-capability-laundering` (MCP resources), and the general M16/M18 memory-poisoning material — but the specific finding (cross-user compromise via Claude's *shared*-memory feature) is new to all of them.
- **Evidence of adoption:** None stated as a defense; the attack itself targets currently-deployed production features of three major vendors, which is the notable part.
- **Major organizations using it:** Not applicable (this is an attack paper against OpenAI, Anthropic and Google products, not a defense those organizations have adopted).
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.28810
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/trust-zoned-agent-memory.md`, `research/accepted/skill-trust-boundary.md` (M22.2), `research/deferred/mcp-filesystem-capability-laundering.md`; `lessons/module-16/lesson-02.md`, `lessons/module-18/lesson-01.md`.
- **Potential course lesson:** The cross-user shared-memory exfiltration mechanism (Claude org memory) is a concrete, citable real-product example worth a one-line addition wherever the course teaches multi-tenant leakage (M16/M28) — pending independent confirmation, since vendors have not corroborated this specific finding.
- **Confidence:** medium (concrete attack against real deployed systems, clear taxonomy via NIST goals; but single preprint, no vendor confirmation, no code).
- **Recommendation:** Monitor for vendor response/patch or independent reproduction; flag alongside `trust-zoned-agent-memory` and `skill-trust-boundary` at the next weekly review as corroborating real-system evidence for the persistence-and-skills threat model already taught.

### C-20261022-03 · Compaction Laundering: forged user turns survive context-compaction and bypass provenance in production coding-agent harnesses

- **Class:** B
- **Date discovered:** 2026-10-22
- **Date published:** 2026-10-21
- **Source:** https://arxiv.org/abs/2610.29869 (verified; title quoted verbatim)
- **Organization/researchers:** Arshan Dabirsiaghi (Pixee)
- **Category:** agent-security (tool/provenance, coding agents)
- **What changed:** Names "compaction laundering": when a long-running coding agent compresses its context (summarizes, discards the original, carries the summary forward), harnesses that flatten a typed conversation into one plain string (labeling turns as "User:", "Assistant:", etc.) lose message provenance before the summarizer runs — so an attacker who controls any content the agent reads can forge a user turn (e.g. a fake standing approval) that survives compaction and is treated as genuine.
- **Technical summary:** Across 5 string-flattening harnesses (pi, opencode, Cline, Aider, OpenHands), the forged approval carried into memory 87–100% of the time at context windows up to ~908K tokens; across 4 role-typed harnesses (Codex, Gemini CLI, Qwen Code, Continue) the same attack succeeded 0% of the time, because they never lose message typing. In a live end-to-end run in the pi terminal interface, a laundered approval led the agent to execute an attacker-controlled install script in a sandbox ~50% of the time vs. 0% in a matched clean arm; the same channel can also steer the agent away from a file marked off-limits (potential code-review backdoor concealment). Proposes a code-level provenance check (catches 77% of laundering attempts, demotes 2% of legitimate summary content) and a cheaper fix (escape role labels at the serializer). No code-release or peer-review venue stated.
- **Why it might matter:** A concrete, deterministic (not prompt-level) trust-boundary bug found by direct testing of 9 named, widely-used open-source coding-agent harnesses — closer to "implemented in major open-source stacks" than most single-preprint findings. Directly extends `research/deferred/execution-audit-provenance.md` (claim-anchored execution contracts) with a specific, measured provenance-loss mechanism and a measured fix.
- **Evidence of adoption:** None (single-author report); the finding is itself about real, currently-shipped open-source agent harnesses, which is the strength.
- **Major organizations using it:** Not stated; author affiliated with Pixee (an application-security company), unconfirmed as organizational endorsement.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.29869
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/execution-audit-provenance.md` (WAIT, next review 2026-11-29) — directly relevant new evidence (a concrete provenance-destruction mechanism + a measured fix); `lessons/module-16`–`module-18` (tool-calling, memory/context).
- **Potential course lesson:** A clean, demonstrable M16/M18 lab extension: flatten vs. role-typed context serialization on the same injected-approval scenario, matching the paper's own clean/attack-arm design.
- **Confidence:** medium (concrete, reproducible-sounding methodology across 9 real harnesses with a measured defense; single author, no code or independent replication yet).
- **Recommendation:** Flag at the `execution-audit-provenance` review (2026-11-29) and consider pulling forward given the directness of the finding and its fit to an existing course module.

### C-20261022-04 · Correlated Failures of AI Approval Monitors: fail-prone-systems framing for multi-monitor agent approval, tested on frontier models

- **Class:** B
- **Date discovered:** 2026-10-22
- **Date published:** 2026-10-21
- **Source:** https://arxiv.org/abs/2610.29178 (verified; title quoted verbatim)
- **Organization/researchers:** Luca Zanolini
- **Category:** agent-security (oversight / monitoring, formal methods)
- **What changed:** Applies the distributed-systems notion of "fail-prone systems" to ensembles of AI approval monitors that gate a consequential agent action (payment, message, code change): a decision rule is safe if it never lets a bad action through and live if it never blocks a good one. Monitors that share a base model or read a shared poisoned input can fail together, which vote-counting aggregation does not account for.
- **Technical summary:** Twelve small open-weight monitors tested on payment approval under two pre-registered protocols, plus three closed frontier models (Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon) and open DeepSeek-V3.2 tested without pre-registration. Every reliable fraud-approval attack worked by compromising a single evidence source and affected only monitors reading that source. Small models and DeepSeek followed injected instructions in their data; the three closed frontier models mostly resisted this (Opus also resisted tailored persuasion). A source-counting (vs. vote-counting) aggregation rule blocked 0.9% of correct payments on held-out data vs. 7.4% for the best vote-counting rule at equal safety. The pre-registered worst-case test still failed once an attack collapsed the approvers onto a single shared source; adding a non-persuadable rule-engine monitor restored safety+liveness against the measured attacks.
- **Why it might matter:** A genuinely new formal angle (safety/liveness, not just ASR) for multi-monitor oversight, tested against real current frontier models rather than only open-weight stand-ins — relevant to the course's oversight/approval-fatigue clusters.
- **Evidence of adoption:** None (single preprint); testing against three named closed frontier models is the notable empirical anchor.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.29178
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/out-of-band-oversight-enforcement.md`, `research/deferred/agent-oversight-evasion.md`, `research/deferred/agent-tool-authorization-gates.md` (approval-based gates) — new evidence/framing for the oversight-monitor sub-theme of these WAIT topics.
- **Potential course lesson:** The safety/liveness framing and the "count sources, not votes" mitigation are a clean addition wherever the course discusses multi-monitor or multi-reviewer agent oversight.
- **Confidence:** medium (formal framing + real frontier-model testing; single preprint, no code, mixed pre-registered/non-pre-registered design).
- **Recommendation:** Monitor alongside the oversight/approval-gate clusters; a good secondary citation once one of those topics is reviewed for ADD.

### C-20261022-05 · CONCERT: detecting and reversing "utility-hijacking" poisoning of instruction-tuning data selectors

- **Class:** B
- **Date discovered:** 2026-10-22
- **Date published:** 2026-10-21
- **Source:** https://arxiv.org/abs/2610.29886 (verified; title quoted verbatim: "Characterizing and Defending Utility-Hijacking in Instruction-Tuning Data Selection")
- **Organization/researchers:** Yahao Ren, Jian Lou, Huadi Zheng, Jiawei Duan
- **Category:** poisoning/backdoor (data-selection-time, supply-chain adjacent)
- **What changed:** Introduces "utility-hijacking": a supplier-side attack on instruction-data *selectors* (models that pick which fine-tuning examples to keep). A generate-and-rerank method creates many payload-bearing candidate records per instruction and submits only the top-scoring one, so top-k selection concentrates poison instead of filtering it out — a different attack surface from poisoning the training data directly.
- **Technical summary:** Across 3 payload types (over-refusal, false-fact injection, insecure code), 6 selectors, and victims from Qwen2.5-7B to Qwen3-32B: refusal rate raised from 0% to 94%; up to 56/90 generated code samples insecure; false-fact enrichment scaled 2.84x–7.04x with the scoring model's size. Proposed defense CONCERT needs no content detector or poison labels: it flags suppliers selected far more often than chance, re-selects under the same budget keeping only records two dissimilar selectors both rank highly. On Qwen3-32B, CONCERT cut poison concentration from 6.67x to 0x (code) and 3.59x to 0.67x (facts), cut downstream harm 100%/75% respectively, with capability unchanged. No code-release stated.
- **Why it might matter:** A new, specific mechanism (selector-time poisoning via adaptive reranking) distinct from the registry's existing `backdoor-persistence-and-trigger-variants.md` cluster (post-training survival) — this attacks the data-curation pipeline itself, with a paired, zero-label defense carrying real measured numbers.
- **Evidence of adoption:** None (single preprint); the defense's label-free design and measured cost are the strength.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.29886
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/backdoor-persistence-and-trigger-variants.md` (related theme, distinct mechanism); `lessons/module-11/lesson-01.md` (backdoors/poisoning) — no existing registry entry for selector-time/data-curation poisoning specifically; new.
- **Potential course lesson:** A possible M11 extension: "poisoning the curator, not just the corpus" — the generate-and-rerank mechanism and CONCERT's two-dissimilar-selectors-agree defense are both concrete enough to teach once independently checked.
- **Confidence:** medium (clean attack+defense pairing with measured numbers across multiple models; single preprint, no code, no independent validation).
- **Recommendation:** Monitor for code release or independent reproduction; candidate new WAIT topic (data-selector poisoning) rather than folding into the existing backdoor-persistence cluster, since the mechanism is genuinely distinct.


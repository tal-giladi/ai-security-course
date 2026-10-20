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


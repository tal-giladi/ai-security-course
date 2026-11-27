# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261123-01 · Isonomy: per-request isolation from prefix-cache timing side channels while keeping one cross-account cache (vLLM gateway, measured throughput cost)

- **Class:** B
- **Date discovered:** 2026-11-23
- **Date published:** 2026-11-20
- **Source:** https://arxiv.org/abs/2611.27596 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Bowen Sun, Chaowei Xiao (same authors as 2611.20291, already cited in the accepted topic)
- **Category:** defense/guardrail (infra side channel)
- **What changed:** Previous mitigations either salt the cache per tenant/account (losing cross-account reuse) or try to "keep sharing but hide the hit", which 2611.20291 showed fails on step-based schedulers. Isonomy argues per-account isolation is itself too coarse (agents sending unreviewed requests, resellers pooling users behind one account, stolen credentials) and isolates every request by default, with opt-in sharing groups, while still keeping one shared cache.
- **Technical summary:** A gateway on top of vLLM routes using only load and the cache entries visible to the request's group, i.e. the instance where the request would run if hidden hits missed. Two modes: (1) prediction mode estimates when the first token would be ready from queue state and the visible prefix and gates its release to that time; (2) execution mode reserves the prefill work a hidden hit skips and fills it with other requests' prompts. Threat model is explicitly limited to deployments where clients cannot observe each other's load (the authors state that then hiding hits in the request's own timing suffices; their listeners on three commercial APIs could not distinguish added prefill work beyond noise). Direct-probe tests on 2/4/8 instances keep the probe-advantage upper bound within measurement noise at both prefix lengths. At saturation, prediction mode retains 0.98 of unprotected sharing's throughput vs 0.95 for per-account isolation (0.80 where more reuse crosses accounts). All numbers author-stated from the abstract; no code link on the abs page.
- **Why it might matter:** It is the "new engine-level mitigation with measured cost" that the accepted topic lists as a revisit trigger, and it reframes the taught salting defense: per-account salt answers "which tenant", not "which request", and it costs throughput that Isonomy claims to recover. It also states the assumption (no cross-client load observation) under which hiding the hit is sound, which is exactly the boundary 15.2 teaches with the scheduler-shift result.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.27596
- **Code:** none
- **Relationship to existing course material:** `research/accepted/prefix-cache-timing-side-channel.md` (lesson `lessons/module-15/lesson-02.md`, lab `labs/module-15/prefix_cache/`); same group as the EMERGING scheduler-shift result 2611.20291 cited there, so not independent evidence.
- **Potential course lesson:** 15.2 extension: add a "release-time gating" defense to the prefix-cache simulator (hold TTFT until the predicted miss time for out-of-group hits), measure probe advantage and throughput against per-tenant salting, then break it by giving the listener a load-observation channel (the stated assumption).
- **Confidence:** medium-low (single preprint from the group that also produced the attack; no code; threat model narrower than general multi-tenant serving)
- **Recommendation:** monitor; record as supporting evidence on the accepted topic at the weekly review; revisit on code or an independent evaluation.

### C-20261123-02 · GRAFT: optimized MCP tool-description poisoning that corrupts tool-call arguments while evading filter defenses

- **Class:** B
- **Date discovered:** 2026-11-23
- **Date published:** 2026-11-20
- **Source:** https://arxiv.org/abs/2611.27041 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Shih-Chieh Dai, Xinyu Sun, Haichuan Zhang, Zhiyuan Zhong, Guanhong Tao (affiliation not stated on the abs page)
- **Category:** tool/mcp-security
- **What changed:** Tool-description poisoning is usually shown as hand-written hidden instructions. GRAFT makes it an optimization problem with two objectives at once: make the agent generate attacker-chosen *arguments* for a tool call (right tool, wrong arguments) and keep the description looking benign to LLM-based and filter-based detectors.
- **Technical summary:** A masking step finds the token positions in a tool description that most influence argument generation; an LLM then proposes mutations at those positions, iteratively scored by the agent's tool choice and generated arguments. Evaluated on three public datasets against attack baselines and five filter-based defenses plus several IPI defenses; abstract claims higher ASR at low detection rates and that GRAFT stays ahead of baselines even against an adaptive defense trained on GRAFT outputs. No numbers in the abstract and no code link on the abs page.
- **Why it might matter:** Second, independent group on the argument-level variant of tool poisoning (the deferred topic was one preprint with its own benchmark). If the numbers hold it is a concrete example of the course's recurring "attacker adapts to the filter" point for tool metadata, and it argues for argument-level controls (typed/allow-listed arguments, capability-flow checks) rather than description scanning.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.27041
- **Code:** none
- **Relationship to existing course material:** new evidence for `research/deferred/tool-parameter-poisoning.md` (C-20261104-05; its trigger is code/benchmark release or replication — this is a different group and an attack, not a replication of the defense); adjacent to `research/deferred/mcp-tool-poisoning-prevalence.md`, `research/deferred/mcp-runtime-metadata-rug-pull.md`, M17 (tool-description poisoning) and `research/accepted/capability-flow-injection-defense.md`.
- **Potential course lesson:** M17 lab extension: a toy MCP description whose wording steers an argument (e.g. a recipient field to a LAB-CANARY sink), a keyword/LLM-judge description filter, a simple mutate-and-score loop that evades the filter, then a typed-argument allow-list that holds regardless of description text; measure ASR, filter detection rate and benign task completion.
- **Confidence:** medium-low (single preprint, no numbers or code in the abstract)
- **Recommendation:** monitor; consider with the tool-parameter-poisoning topic at the weekly review (two groups now, still no code).

### C-20261123-03 · Cleave: training-free *selective* guardrail removal in open-weight LLMs that evades spot-checks and weight audits, plus a weight-coupling audit defense

- **Class:** B
- **Date discovered:** 2026-11-23
- **Date published:** 2026-11-20
- **Source:** https://arxiv.org/abs/2611.27426 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Feng Huang, Qiang Huang, Yue Gao, Mei Zhang, Bin Liu, Lihua Ju, Xinhao Wei, Yongfeng Huang, Yu Qing, Yunqi Zhang (affiliation not stated on the abs page)
- **Category:** jailbreak (white-box weight editing) + detection/monitoring
- **What changed:** Refusal-direction abliteration removes refusal broadly, which is noticeable in behavioural spot-checks. Cleave edits the "residual writing" weights that trigger refusals and can lift only one category (cybersecurity) while keeping up to 99% refusal on other harmful requests and avoiding the rank collapse that static weight audits look for, i.e. a stealthy, scoped safeguard removal.
- **Technical summary:** Training-free weight edit on five open-weight models (7B to 320B). Claims up to 67.97% ASR on seven safety benchmarks (better than white-box baselines), up to 24x more executable exploit generation on 356 cybersecurity tasks, and compromise of up to 66.7% of 15 live vulnerable services (the authors' own test targets). Proposed defense: pre-release subspace diagnostics plus post-release weight-coupling audits, 100% detection recall at 1% FPR. All author-stated from the abstract; no code link on the abs page.
- **Why it might matter:** Lab 34 teaches abliteration with a capability control and a retest loop; Cleave adds the next adaptation (scoped removal that passes a behavioural spot-check on other categories) and names a defender-side audit with a stated FPR. That is the guarantee / does-not-guarantee / attacker-adapts pattern the course is built on, applied to weights.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.27426
- **Code:** none
- **Relationship to existing course material:** extends `lessons/module-34/lesson-02.md` and `labs/module-34/` (refusal-direction abliteration, `ablate.py`); `research/accepted/glm-5-3-safeguard-bypass-taxonomy.md` and `research/accepted/lab-blueprint-safeguard-surface.md`; adjacent to `research/deferred/training-free-neuron-edit-backdoor.md` (weight edits detectable by diffing).
- **Potential course lesson:** Lab 34 extension: estimate per-category refusal directions on the toy model, ablate only one category, show a single-category spot-check passes while the target category is open, then detect it with a weight/subspace diff against the base checkpoint and measure the detector FPR on benign fine-tunes. Inert prompts and markers only.
- **Confidence:** medium-low (single preprint, no code; the defense is the authors' own against their own attack)
- **Recommendation:** monitor; revisit on code or an independent evaluation of the weight-coupling audit.

### C-20261124-01 · Who is prompt-injecting coding agents? In-the-wild measurement of hidden AI-directed text on GitHub (data + detector released)

- **Class:** B
- **Date discovered:** 2026-11-24
- **Date published:** 2026-11-21
- **Source:** https://arxiv.org/abs/2611.28763 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Gabi Nakibly, Zvika Babo (the linked repo is under a Radware-named account, `rdwr-gabin`; affiliation not stated on the abs page)
- **Category:** prompt-injection (indirect, in the wild) + evaluation/benchmark
- **What changed:** Indirect injection against GitHub-integrated coding agents had been shown only in controlled settings. This is a prevalence study: ~145M issues, PRs, comments and READMEs scanned for text GitHub does not render to a human but an agent receives in full (e.g. HTML comments), filtered by a two-stage LLM classifier, a template-provenance check and exhaustive manual review.
- **Technical summary:** 2,281 validated findings in issues/PRs/comments (16 per million items) plus AI-directed hidden text in 107 repository READMEs. Four uses: attacks on other parties' agents, defensive text restricting agents, content override that steers what agents write, and first-party orchestration (projects coordinating their own agents through hidden markers). Attacks are rare (~1 in 3.3M items) and aimed at maintainers' own triage/review/CI agents. Orchestration is two thirds of findings, grew fivefold in four months, and is a control channel anyone who can comment can imitate. Offline replay against five models: attacks succeed on one small fast model in 19% of cases and on none once HTML comments are stripped (author-stated).
- **Why it might matter:** Gives the course real base rates for indirect injection on a surface Tal's labs already model, and a concrete, cheap, measured mitigation (strip non-rendered content before the agent reads it). The orchestration finding is a new teaching point: a legitimate hidden control channel in untrusted-writable content is itself an injection vector (spoofable markers), i.e. a confused-deputy design flaw rather than a model weakness.
- **Evidence of adoption:** none (measurement study); the detection tool and every finding are released per the abstract.
- **Major organizations using it:** none
- **Open-source implementation:** https://github.com/rdwr-gabin/github-ipi-in-the-wild (linked from the abs page; repo page not reachable from this session, so contents unverified; not cloned or run)
- **Paper:** https://arxiv.org/abs/2611.28763
- **Code:** https://github.com/rdwr-gabin/github-ipi-in-the-wild (unverified, see above)
- **Relationship to existing course material:** extends `lessons/module-05/lesson-01.md` (indirect injection) and `lessons/module-06/lesson-01.md` (invisible-text carriers); adjacent to `research/deferred/document-parser-divergence.md` (render vs. parse divergence) and `research/deferred/coding-agent-repo-poisoning.md`; `research/accepted/owasp-llm-top10-2026.md` (Hidden Context Exposure).
- **Potential course lesson:** 05.1/06.1 lab extension: a synthetic GitHub-issue corpus with rendered vs. raw views; build the "rendered-diff" detector (what the agent sees minus what a human sees), measure its rate on benign issues that legitimately use HTML comments (templates), add a spoofed orchestration marker and show a marker-trusting agent follows it, then fix by authenticating markers (author/permission check) and stripping non-rendered content; measure ASR before/after. Inert LAB-CANARY markers only.
- **Confidence:** medium (large-scale, manually validated, data released; single group, replay ASR on only five models)
- **Recommendation:** review at the weekly run as a 05.1/06.1 extension candidate; check that the released dataset is usable and licensed before ADD.

### C-20261124-02 · Agent- and gradient-driven sparse weight-space backdoors in open-weight LLMs, now from several groups, plus a forensic scanner with a stated cohort result

- **Class:** B
- **Date discovered:** 2026-11-24
- **Date published:** 2026-11-20 / 2026-11-21
- **Source:** https://arxiv.org/abs/2611.27920 and https://arxiv.org/abs/2611.28543 (both verified resolve; abstracts via arXiv API)
- **Organization/researchers:** Autonomous Parameter Surgery: Xuyang Liu, Zhiwei Xu, Zirui Li, Jiabao Gao, Xiaolin Peng, Weixian Deng, Tian Qiu, Hai Wan. Neural Sentinel: Mohammed Tanveer (single author). Affiliations not stated on the abs pages.
- **Category:** poisoning/backdoor + supply-chain + detection/monitoring
- **What changed:** The deferred Lazarus topic (closed-form edit of a few dormant final-block neurons) was one preprint. In four days three further, unrelated groups report training-free or near-training-free sparse weight backdoors: TrojanMaxxing (2611.27425, recorded C on 2026-11-23, VLMs), Autonomous Parameter Surgery (a general LLM turns a natural-language backdoor spec into weight edits with no gradient training) and Neural Sentinel (gradient-guided edits of ~0.0002% of parameters across 18 checkpoints / 14 architecture families, including SSM and recurrent models).
- **Technical summary:** APS: DeepSeek Flash in a restricted workspace edits Qwen3.5-0.8B, Llama-3.2-1B, SmolLM3-3B for review-sentiment backdoors; 99.2% ASR on the editing domain, 97.6% transfer to an unseen domain, general capability within 1.7 points; the editor converged on final-layer edits in 17/18 runs and rediscovered rank-one orthogonalization and single-neuron surgery, ~$1.74 per run (author-stated). Neural Sentinel: on Phi-2 an exact short-marker output after 300 steps (332 s) with mean next-token KL 1.5e-5 on reference prompts; defense combines weight-difference analysis, trigger discovery, activation probing and output inspection; in a 22-artifact cohort the reference-optional scanner flagged 4/5 backdoored artifacts as BACKDOORED and labelled the remaining positive and all 17 clean artifacts SUSPICIOUS (i.e. no clean admission).
- **Why it might matter:** Independent convergence on the same mechanism (final-layer / single-neuron edits) is the "independent reproduction" the deferred file asks for, at the threat-class level, and Neural Sentinel supplies a defender-side number that teaches the right lesson: forensic triage without a reference checkpoint cannot clear a clean model, so provenance (signed base + weight diff) carries the load.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed on either abs page
- **Paper:** https://arxiv.org/abs/2611.27920 ; https://arxiv.org/abs/2611.28543
- **Code:** none
- **Relationship to existing course material:** new evidence for `research/deferred/training-free-neuron-edit-backdoor.md` (trigger: code release or independent reproduction — reproduction of the mechanism class, not of Lazarus itself); adjacent to `research/deferred/backdoor-persistence-and-trigger-variants.md`, `research/deferred/quantized-model-signing-verifiability.md`, staging C-20261123-03 (Cleave, weight-coupling audit); course `lessons/module-34/lesson-02.md` / `labs/module-34/` (weight editing).
- **Potential course lesson:** the teachable form already written in the deferred file (11.1/13.1 tiny-CPU-transformer extension: hand-write one dormant neuron that promotes an inert marker; detect by weight diff against the signed base and by activation statistics; measure detector FP on benign fine-tunes), now with a "no reference checkpoint" condition to reproduce the Neural Sentinel admission gap.
- **Confidence:** medium-low (all preprints, no code; Neural Sentinel is single-author with a small cohort; APS ASR on small models and a benign sentiment target)
- **Recommendation:** at the weekly review, re-evaluate `training-free-neuron-edit-backdoor.md` with this cluster (plus TrojanMaxxing) as possible independent-reproduction evidence; WAIT remains reasonable until any code appears.

### C-20261124-03 · INSEP: fine-tuning a model so its refusal direction is inseparable, as a defense against abliteration (8 models, 6 defenses, 5 attacks)

- **Class:** B
- **Date discovered:** 2026-11-24
- **Date published:** 2026-11-20
- **Source:** https://arxiv.org/abs/2611.28314 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Ivan Brugere, Junqi Jiang, Saumitra Mishra, Sumitra Ganesh (affiliation not stated on the abs page)
- **Category:** defense/guardrail (white-box, open weights)
- **What changed:** Abliteration estimates the refusal direction as a difference of class means and projects it out. INSEP attacks that estimator: a LoRA fine-tune reduces the separability of harmful vs. benign activations along the refusal direction, with an adversarial eigendecomposition picking the most separable prompt subsets and behavioural losses keeping refusal and benign quality.
- **Technical summary:** Benchmarked against six published defenses under five attacks on eight LLMs (1B-14B). Scores harm together with coherence, directness, over-refusal and MMLU, explicitly to separate robust refusal from "low harm because the output degraded". Claims first place on the mean composite score with utility retained; the largest abliteration-defense evaluation to date (author-stated). 39 pages, 42 tables.
- **Why it might matter:** Lab 34 teaches abliteration and the capability-control discipline but no weight-level defense; INSEP is a measured one with the right evaluation shape (harm + over-refusal + utility). It pairs directly with staging C-20261123-03 (Cleave): the attacker's next move against a mean-difference defense is a different direction estimator or per-category directions, which is exactly the guarantee / does-not-guarantee / attacker-adapts pattern.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.28314
- **Code:** none
- **Relationship to existing course material:** `lessons/module-34/lesson-02.md`, `labs/module-34/ablate.py`; `research/accepted/glm-5-3-safeguard-bypass-taxonomy.md` (capability control); staging C-20261123-03 (Cleave).
- **Potential course lesson:** Lab 34 extension: on the toy model, add a separability penalty along the estimated refusal direction, rerun `ablate.py`, measure refusal-after-ablation, over-refusal and a capability control; then adapt the attack (estimate the direction from a different prompt subset, or per category) and measure what survives.
- **Confidence:** medium-low (single preprint, no code; adaptive attacks beyond the five evaluated not stated in the abstract)
- **Recommendation:** monitor; consider together with Cleave at the weekly review as a possible paired attack/defense Lab 34 extension once code appears.

### C-20261125-01 · Gate/executor parse divergence in agent tool calls: shell-command allowlists (ParseGap, 8 production coding agents) and JSON tool-call smuggling, each with a single-parse fix and measured cost

- **Class:** A
- **Date discovered:** 2026-11-25
- **Date published:** 2026-11-22 / 2026-11-23
- **Source:** https://arxiv.org/abs/2611.29546 and https://arxiv.org/abs/2611.30624 (both verified resolve; abstracts via arXiv API)
- **Organization/researchers:** ParseGap: Jieyu Li (single author; affiliation not stated on the abs page; preprint carries coordinated-disclosure redactions, vendors notified 2026-11-22 with a 90-day window, author-stated). Tool-call smuggling: Igor Santos-Grueiro, Daniel Romero-Ruiz (affiliation not stated). Two unrelated groups.
- **Category:** agent-security + tool/mcp-security + defense/guardrail
- **What changed:** Two independent papers in two days show the same structural flaw in agent permission gates: the guard parses one representation of a call and approves it, while the executor parses the same bytes differently and runs something else (the request-smuggling pattern from web security, now between agent guard and executor). ParseGap does it for shell commands in shipping coding agents; tool-call smuggling does it for JSON tool-call arguments across the provider/gateway/SDK/guard/executor stack.
- **Technical summary:** ParseGap: differential harness runs each command through the unmodified vendor checker and GNU Bash 5.2 in a container; 17 root causes across eight production coding agents at three boundaries: parse (an upstream tree-sitter-bash defect hides a second command from Mistral Vibe and Gemini CLI), utility (every checker permits "read-only" binaries whose arguments write files or launch programs, 9-47 of 55 cases) and confinement (an allow rule in Codex CLI disables its read-only OS sandbox); live trials violated policy in all 16 agent-model pairs. Fix, ShellPlan: compile a strict Bash subset once into a typed plan, validate utility arguments against positive capability specs, dispatch via execve with no shell; 0/4,174 static attacks admitted, 0/90 in a ten-model agent benchmark (62/90 unguarded), 1.28 ms median gate latency, 36/36 frontier standard-dev tasks completed (74/100 overall) (author-stated). Tool-call smuggling: six ways identical JSON bytes yield different calls (e.g. duplicate keys); 17 pinned parser/validator configurations mostly disagree pairwise, including two official MCP SDKs; on tau-bench and AgentDojo tasks an in-transit attacker gets a blocked call executed while the audit log records the approved one; models do not emit duplicate keys in the call itself but copy them verbatim into JSON-in-string arguments that a Python guard and a Go executor read differently; a malicious server cloning a tool schema plus one extra field gets it filled with user data unseen by the guard. Fix: parse once (including embedded JSON text), keep only approved-schema fields, hand the sealed call (bound to its call ID) to the executor; blocks all 7,412 crafted inputs and every built attack (author-stated).
- **Why it might matter:** This is a mechanism, not a model weakness: deterministic, reproducible on a laptop with two parsers, and the fix is a classic security principle (parse once, act on the parsed object, never re-interpret raw bytes) with a measured latency/utility cost. It explains why "the guard approved it" and "the audit log says so" are not evidence of what ran, which is exactly the guarantee/does-not-guarantee discipline the course teaches. CPU-only, no model needed for the core lab.
- **Evidence of adoption:** none for the defenses; affected products named in ParseGap (Gemini CLI, Mistral Vibe, Codex CLI) under coordinated disclosure (author-stated; no vendor advisory found yet).
- **Major organizations using it:** none
- **Open-source implementation:** none listed on either abs page
- **Paper:** https://arxiv.org/abs/2611.29546 ; https://arxiv.org/abs/2611.30624
- **Code:** none
- **Relationship to existing course material:** `lessons/module-01/lesson-01.md` (data parsed by a more powerful interpreter), `lessons/module-21/lesson-01.md` / `labs/module-21/` (command allowlist as a coding-agent defense, which ParseGap shows is bypassable), `lessons/module-17/lesson-01.md` and `lessons/module-02/lesson-02.md` (tool-call authorization); adjacent to `research/deferred/coding-agent-harness-mechanisms.md` (allow/denylisting judged "cheap"), `research/deferred/agent-tool-authorization-gates.md`, `research/deferred/document-parser-divergence.md` (same differential-parsing idea for documents) and `research/deferred/agent-os-protection-gap.md`. No existing topic covers guard/executor parser differentials.
- **Potential course lesson:** M21 (or 02.2) lab extension "one call, two readings": (1) a toy shell allowlist that checks a naive split of the command string, then passes the raw string to `bash -c` in the lab container; show `;`/subshell/`find -exec`-style inert-marker commands that pass the gate and write LAB-CANARY files; (2) a Python guard vs. a second JSON reader that keeps the other duplicate key; (3) fix by parse-once + typed plan + execve, then measure attacks admitted, benign tasks blocked and gate latency, and try to bypass the fix (unmodelled utilities, JSON-in-string).
- **Confidence:** medium (two independent preprints converging on one mechanism with concrete fixes; numbers author-stated, no code yet, ParseGap is single-author and partly redacted)
- **Recommendation:** review for ADD as an M21/02.2 extension, or WAIT until a vendor advisory/fix or code appears; the core lab can be built from first principles without either paper's artifacts.

### C-20261125-02 · Who wrote the policy? Permission replies that delete coding-agent deny rules, and request-derived authorizers that trust compaction summaries

- **Class:** B
- **Date discovered:** 2026-11-25
- **Date published:** 2026-11-24
- **Source:** https://arxiv.org/abs/2611.32195 and https://arxiv.org/abs/2611.32194 (both verified resolve; abstracts via arXiv API)
- **Organization/researchers:** Zeming Fei, Hongming Fei, Xiaoyang Wang, Ying Zhang and co-authors (Jingwen Chen, Prosanta Gope, Biplab Sikdar on 2611.32195; Yi Xu on 2611.32194). One group, two papers; affiliations not stated on the abs pages.
- **Category:** agent-security + defense/guardrail
- **What changed:** Both papers locate agent authorization failures in missing provenance of policy inputs rather than in the model. (1) In coding agents a plugin or remote service may answer a permission prompt; the answer can carry a policy update, and Claude Code validates only updates that add or replace allow rules, so a reply that approves an unrelated command can delete the deny rule protecting secrets, persisting into later sessions, and the deletion is recorded like a local operator edit. (2) Claude Code and Codex insert the compaction summary as a user message, so a request-derived authorizer (Progent re-deriving policy per request) grants what the compactor wrote, including attacker data quoted in it.
- **Technical summary:** (1) Proves two tight bounds: a runtime that cannot tell who wrote a rule may only accept updates keeping every denied call denied; one that records rule authorship may let each party remove only its own restrictions. The bounds predicted operator-restriction survival in 13 permission designs across 10 agent systems (predictions for Codex, Gemini CLI, opencode, Goose written before running); enforcing them at the shared update step blocks the attack; 2 of 2,227 marketplace plugins send policy updates (cheap to enforce). (2) With an attacker notice naming another payee as plain data, the policy derived from a frontier compactor's summary admits the attacker account in 91% of cases vs. 0% from the user's own words; compactors mark injected instructions but rarely injected data. Fix: the authorizer credits only user text authenticated on arrival and carried verbatim across compaction (the agent still reads the summary); 40 attacked AgentDojo episodes with no attacker action completed (author-stated).
- **Why it might matter:** A clean, teachable principle ("what a runtime records decides what it can safely delegate"; authorization needs authenticated provenance, not role labels) with concrete product behaviour and a cheap enforced fix. The compaction result is independent of, and sharper than, the compaction-laundering paper already in the registry: it shows that even role-typed harnesses (which that paper found immune) feed forged authority to a request-derived authorizer.
- **Evidence of adoption:** none; no vendor advisory found.
- **Major organizations using it:** none
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.32195 ; https://arxiv.org/abs/2611.32194
- **Code:** none
- **Relationship to existing course material:** new evidence for `research/deferred/coding-agent-harness-mechanisms.md` (compaction laundering, 2610.29869, different group); `research/accepted/capability-flow-injection-defense.md` (CaMeL/Progent); `research/deferred/agent-tool-authorization-gates.md`; course `lessons/module-21/lesson-01.md`, `lessons/module-17/lesson-02.md`.
- **Potential course lesson:** M21/17.2 extension: a toy permission store with allow/deny rules and a "remote approver" channel; show a reply that removes a deny rule; implement authorship-tagged rules and the monotonic-update check; then a toy Progent-style authorizer fed a compaction summary containing an inert attacker payee, fixed by carrying authenticated user text verbatim.
- **Confidence:** medium-low (one group, preprints, no code; product behaviour may change quickly)
- **Recommendation:** monitor; consider with `coding-agent-harness-mechanisms.md` at its 2026-12-20 review.

### C-20261125-03 · SchemaCaps: compatible MCP tool-schema updates silently widen an agent's authority; a subschema re-binding rule with measured re-approval cost

- **Class:** B
- **Date discovered:** 2026-11-25
- **Date published:** 2026-11-23
- **Source:** https://arxiv.org/abs/2611.30750 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Yulliwas Ameur, Samia Bouzefrane, Soumya Banerjee (affiliation not stated on the abs page); accepted at ICAART 2027 (author-stated)
- **Category:** tool/mcp-security + defense/guardrail
- **What changed:** The course's rug-pull material (and the deferred Deadbugz topic) treats any tool-definition change as a re-approval trigger. SchemaCaps measures the case clients actually allow: backward-compatible JSON input-schema changes that widen what an approved tool can do. Of 8 surveyed MCP clients/scanners, none is observed or documented to re-approve on schema widening (two undeterminable).
- **Technical summary:** Defines non-amplification over the schema's visible coordinates (declared and undeclared fields, effective values) and re-binds approval by subschema inclusion, trusting no field labels; Coq proof of composition, 48 regression tests, a reference benchmark (which found 27 amplifying changes the authors' own earlier rule missed). Pilot on 604 releases of 39 public MCP servers: 412 of 580 compatible schema changes widen some coordinate; adjudicated annotation finds at least 76 that add or widen an authority-bearing argument (a name-based labeller catches 66 of 84 and misses 10). Cost: 645 re-approvals vs. 1,197 for pinning the input schema (2,004 with descriptions) and 617 for compatibility-only. Behaviour change behind an identical schema is out of scope (author-stated).
- **Why it might matter:** Gives the rug-pull defense a measured false-positive/alert-fatigue cost and a real-world base rate, which the deferred topic lacked, and a precise teaching contrast: hash pinning over-alerts, compatibility under-alerts, subschema inclusion sits between.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** artefact at https://doi.org/10.5281/zenodo.24233014 (listed on the abs page; doi.org not reachable from this session, unverified; not downloaded)
- **Paper:** https://arxiv.org/abs/2611.30750
- **Code:** https://doi.org/10.5281/zenodo.24233014 (unverified, see above)
- **Relationship to existing course material:** new evidence (measured defense cost) for `research/deferred/mcp-runtime-metadata-rug-pull.md`; course `lessons/module-19/lesson-01.md` / `labs/module-19/` (server pinning by hash, rug-pull server) and `lessons/module-17/lesson-01.md`.
- **Potential course lesson:** Lab 19 extension: three re-approval policies (hash pin, compatibility, subschema non-amplification) replayed over a synthetic release history of a toy MCP server; count re-approvals and missed widenings; then bypass with a behaviour change behind an unchanged schema.
- **Confidence:** medium (peer-reviewed venue per authors, artefact listed, single group)
- **Recommendation:** monitor; bring to the `mcp-runtime-metadata-rug-pull.md` review as the measured-cost evidence it was waiting for.

### C-20261125-04 · FORGETMENOT: audit of long-term memory in five commercial AI assistants finds stored-vs-shown gaps and post-deletion leakage

- **Class:** B
- **Date discovered:** 2026-11-25
- **Date published:** 2026-11-22
- **Source:** https://arxiv.org/abs/2611.29804 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Ismat Jarin, Tu Le, Athina Markopoulou (affiliation not stated on the abs page)
- **Category:** privacy/DP + agent-security
- **What changed:** The deferred memory-privacy topic rests on open-source memory stacks (e.g. mem0). This is a black-box audit of deployed commercial assistants: ~3,800 multi-turn sessions (~6M tokens) across five agents.
- **Technical summary:** Agents store demographics, health and other sensitive attributes; user-visible memory shows on average ~20% fewer attributes than the agent demonstrably stores. A "stealth memory injection" raises stored personal/sensitive attributes by 25% (Copilot) and 15% (Claude). All five agents show non-zero leakage after memory deletion, including health and self-harm attributes. Proof of concept of memory disclosure to a third-party email recipient: 31.9% leakage for Gemini (author-stated).
- **Why it might matter:** Real-system evidence that "delete" does not erase and that the memory UI is not the memory, matching the course's deferred topic with deployed products rather than research stacks.
- **Evidence of adoption:** n/a (audit of deployed systems)
- **Major organizations using it:** affected systems include Copilot, Claude, Gemini (named in the abstract)
- **Open-source implementation:** none listed
- **Paper:** https://arxiv.org/abs/2611.29804
- **Code:** none
- **Relationship to existing course material:** new evidence for `research/deferred/agent-memory-privacy-erasure.md` (due 2026-11-29; leading candidate as a 16.2 extension); adjacent to `research/accepted/trust-zoned-agent-memory.md`; course `lessons/module-16/lesson-02.md`.
- **Potential course lesson:** supporting real-world numbers for the planned 16.2 erasure extension (toy memory store: stored vs. displayed vs. retrievable-after-delete, measured on synthetic canary attributes).
- **Confidence:** medium-low (black-box measurement of fast-changing products; methodology only from abstract)
- **Recommendation:** attach to `agent-memory-privacy-erasure.md` at its 2026-11-29 review as deployed-system evidence.

### C-20261125-05 · Enforcement below the agent with measured cost: Airlock (TEE-isolated IO-mediating VM with tamper-proof audit) and AgentBouncer (LLM-arbitrated syscall mediation for SE agents)

- **Class:** B
- **Date discovered:** 2026-11-25
- **Date published:** 2026-11-23
- **Source:** https://arxiv.org/abs/2611.31010 and https://arxiv.org/abs/2611.30621 (both verified resolve; abstracts via arXiv API)
- **Organization/researchers:** Airlock: Sina Abdollahi, Amir Al Sadi, Marios Kogias, Hamed Haddadi, Adrien Ghosn, Antoine Delignat-Lavaud, Manuel Costa, Mark Russinovich (affiliations not stated on the abs page). AgentBouncer: Pascal Joos, Michael Pradel (affiliation not stated). Two unrelated groups.
- **Category:** agent-security + defense/guardrail + detection/monitoring
- **What changed:** Two concrete designs that move enforcement out of the agent's reach, each with stated cost. Airlock pairs each agent VM with an Airlock VM in a separate hardware TEE (Arm CCA; modified RMM firmware and both kernels) that mediates all network and storage IO without the host, keeps network/filesystem/credential policies effective if the agent VM is fully compromised, and keeps a tamper-proof audit log; integrated with the OpenShell agent runtime. AgentBouncer mediates the system calls SE agents trigger via tools, with an LLM arbiter scoring necessity and safety, plus preseeded rules and caching.
- **Technical summary:** Airlock on a Radxa board: <15% loss in filesystem performance and small-message network latency, network bandwidth halved or worse, limited effect on typical agent tasks (author-stated). AgentBouncer on 340 environment attacks (four vectors) combined with SWE-bench Verified tasks: ASR 99.41% unsupervised -> 10.59%, 18-74 points below compared runtime defenses; 0.25% benign tool calls failed; +47 s and USD 0.0036 per task, 4.5x less time and 9.6x less cost than the closest runtime defense (author-stated).
- **Why it might matter:** The deferred out-of-band enforcement topic asks for defenses that survive a compromised agent/harness with disclosed overhead; these are two more, at different layers (hardware-isolated IO mediation; syscall mediation), with the trade-off teachable in the guarantee table (Airlock: survives full agent-VM compromise, costs bandwidth; AgentBouncer: semantic decisions, but the arbiter is itself an LLM that can be argued with).
- **Evidence of adoption:** none (Airlock adapts the existing OpenShell runtime)
- **Major organizations using it:** none stated
- **Open-source implementation:** none listed on either abs page
- **Paper:** https://arxiv.org/abs/2611.31010 ; https://arxiv.org/abs/2611.30621
- **Code:** none
- **Relationship to existing course material:** new evidence for `research/deferred/out-of-band-oversight-enforcement.md` (due 2026-11-29); adjacent to `research/deferred/agent-os-protection-gap.md`, `research/accepted/egress-covert-channels-agent.md`; course `lessons/module-33/lesson-01.md`, `lessons/module-21/lesson-01.md`.
- **Potential course lesson:** 33.1/21.1 extension: an IO-mediator process the agent cannot signal or ptrace (separate container/user) enforcing egress and file policy with its own audit log; compare against in-agent hooks under a simulated compromised agent; measure latency/bandwidth cost. TEE specifics as reading only.
- **Confidence:** medium-low (preprints, no code; Airlock on a dev board)
- **Recommendation:** attach to `out-of-band-oversight-enforcement.md` at its 2026-11-29 review.

### C-20261126-01 · Chasm: cross-model KV-cache handoffs in multi-agent systems bypass the target model's safety alignment and prompt-injection resistance, with a target-side cache guard

- **Class:** B
- **Date discovered:** 2026-11-26
- **Date published:** 2026-11-25
- **Source:** https://arxiv.org/abs/2611.34278 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Manit Baser, Vyoman Jain, Rachel Yeo Hui Min, Xianglin Yang, Meenatchi Sundaram Muthu Selva Annamalai, Dinil Mon Divakaran (affiliation not stated on the abs page)
- **Category:** agent-security + prompt-injection + jailbreak
- **What changed:** "Latent communication" between heterogeneous agents, where a learned mapper translates a source model's KV cache into one the target model consumes, is shown to be a new attack surface. The target processes context it never encoded itself, so its alignment and injection defenses operate on representations they were not trained against.
- **Technical summary:** The Chasm framework names three attack surfaces: the source model, the mapper, and the handoff mechanism. Author-stated results: a target that follows 0.4% of benchmark prompt injections natively follows up to 44.2% when the same content arrives through a mapper; jailbreak transfer alone adds up to 24.6 pp within a family and up to 69.2 pp zero-shot; white-box optimization through the mapper reaches 92.5% ASR vs 37.5% for ordinary GCG on the same target. Proposed defense: a lightweight target-side "cache guard" that corrects transferred caches to restore refusal ("considerably mitigating"; no false-positive or latency figures in the abstract).
- **Why it might matter:** Generalizes a course principle (a defense only holds on the input distribution it was trained on; every new channel into the model is a new trust boundary) to a channel below the text layer, where text filters and prompt-level defenses cannot see the payload at all. If KV/latent exchange becomes a production pattern in multi-agent systems, it is a cleanly teachable new boundary.
- **Evidence of adoption:** none for the attack or the guard. Cross-model KV transfer itself is an emerging research technique, not a documented production pattern (no major framework found using it).
- **Major organizations using it:** none
- **Open-source implementation:** none listed on the abs page
- **Paper:** https://arxiv.org/abs/2611.34278
- **Code:** none
- **Relationship to existing course material:** new topic. Adjacent to `lessons/module-28/lesson-01.md` (multi-agent / A2A), `lessons/module-07/lesson-01.md` (GCG), `research/accepted/prefix-cache-timing-side-channel.md` (KV cache as shared state, different threat), `research/deferred/reasoning-kv-cache-poisoning.md` (KV reuse as poisoning vector, different mechanism).
- **Potential course lesson:** M28 extension ("messages that are not text"): toy two-model handoff where a linear mapper transfers hidden states, show a text-level injection filter is bypassed, then implement and measure a target-side guard. Only if the latent-handoff pattern sees real adoption.
- **Confidence:** low-medium (single preprint, no code, the deployment pattern is itself emerging)
- **Recommendation:** monitor; revisit if code appears or a multi-agent framework ships cross-model KV/latent exchange.

### C-20261126-02 · Workflow security downgrade: agents that replan after a tool failure silently drop the original workflow's protections (fault-injection study, ARGUS obligation-preserving recovery)

- **Class:** B
- **Date discovered:** 2026-11-26
- **Date published:** 2026-11-25
- **Source:** https://arxiv.org/abs/2611.33605 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Boyang Ma, Jinku Li, Hao Wu, Sheng Gao, Man Zhou, Minghui Xu, Yue Zhang (affiliation not stated on the abs page)
- **Category:** agent-security + tool/mcp-security + defense/guardrail
- **What changed:** Identifies a failure-induced agent threat that needs no injected instruction and no poisoned tool: when an operation in an MCP/Skill workflow fails, the agent's autonomous recovery can complete the task while skipping the security step the original workflow required (e.g. performing a sensitive operation without the protection it was bound to).
- **Technical summary:** Fault injection in an executable MCP/Skill environment across seven LLMs, twelve task templates and three security-sensitive domains measures how often recovery causes protection loss. ARGUS (defense) combines resource-bound security evidence (the protection is proven on the specific resource, not asserted), isolated validation of the recovery plan, and execution-time enforcement. In a separate 864-run evaluation ARGUS prevented every observed protection-loss event under enforcement; recovery assistance gave model-dependent gains in protected task completion over plain blocking (author-stated). An attacker who can induce failures (rate limits, timeouts, malformed responses) could steer an agent onto the downgraded path, though the paper frames it as a reliability-triggered threat.
- **Why it might matter:** Teaches that security obligations must be bound to resources and enforced outside the planner, because replanning is a code path the original policy never reviewed: the agent analogue of "fail-open" error handling. Complements the provenance-of-policy candidates already staged this week.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none listed on the abs page
- **Paper:** https://arxiv.org/abs/2611.33605
- **Code:** none
- **Relationship to existing course material:** adjacent to staged C-20261125-02 (policy provenance) and C-20261125-05 (enforcement below the agent); `research/deferred/agent-tool-authorization-gates.md`; `research/deferred/agent-toctou-state-drift.md`; `research/accepted/capability-flow-injection-defense.md`; course `lessons/module-16/lesson-01.md`, `lessons/module-19/lesson-01.md`.
- **Potential course lesson:** M16/M19 extension: toy workflow "redact, then upload" where the redaction tool fails; show the planner's recovery uploads unredacted canary data to the local sink; add an enforcement check that the upload requires a redaction receipt bound to that file hash; measure blocked vs completed tasks.
- **Confidence:** medium-low (one group, preprint, no code)
- **Recommendation:** monitor; consider together with C-20261125-02/05 at the weekly review as a "fail-closed agent runtime" cluster.

### C-20261126-03 · Measured-cost defenses against adversarial visual prompt injection on VLMs and VLM agents: AVERT (answer-conditioned subspace erasure) and native-resolution diffusion purification

- **Class:** B
- **Date discovered:** 2026-11-26
- **Date published:** 2026-11-24 / 2026-11-25
- **Source:** https://arxiv.org/abs/2611.33532 and https://arxiv.org/abs/2611.34181 (both verified resolve; abstracts via arXiv API)
- **Organization/researchers:** AVERT: Newt Hue-Nam K. Nguyen, Jui-Yu Ho, Wei-Han Chen, Pin-Yen Ting, Yangqiu Song, Shang-Tse Chen, Jun-Cheng Chen. Agentic purification: Yan Lin, Zhongliang Guo, Jingyu Lin, Daizong Liu. Two unrelated groups; affiliations not stated on the abs pages.
- **Category:** multimodal-attack + defense/guardrail
- **What changed:** Two defenses for adversarially perturbed images that hijack VLM output or agent actions, both reporting the clean-utility cost the course's guarantee boxes ask for, which earlier image defenses (JPEG, blur, purification, token masking) mostly did not.
- **Technical summary:** (1) AVERT compares per-input attention-head output statistics with clean-image statistics, extracts the most anomalous value directions, and projects them out only when the answer depends on them (its likelihood collapses after removal, or is as likely under unrelated questions). White-box attacks on Qwen2-VL, Qwen2.5-VL, LLaVA, InternVL2.5 and four injection benchmarks: average ASR from 86-90% to at most 0.6% while keeping at least 96% of undefended utility over 13 benchmarks (author-stated; adaptive attacks against the defense itself not described in the abstract). (2) First evaluation of diffusion purifiers at native resolution on multi-element agent inputs (Qwen3-VL-8B agent, grey-box attacker who knows the model but not the defense, matched clean cost): resizing to the diffusion model's resolution raises the Divide-and-Conquer purifier's TextVQA clean cost from 4.0 to 35.7 points; at native resolution it keeps 85.0% robust accuracy on web-shop pages vs at most 40.0% for cheap transformations at matched cost; robustness comes from the global noise level alone. Protocol released (author-stated).
- **Why it might matter:** Module 20 teaches re-encoding/quantization defenses and their limits; these give two contrasting, quantified defense designs (input purification vs model-internal subspace removal) with explicit utility cost, and an evaluation lesson (measure at the agent's real input resolution and at matched clean cost). Neither has an adaptive white-box attack on the defense yet, the standard failure point for such claims.
- **Evidence of adoption:** none
- **Major organizations using it:** none
- **Open-source implementation:** none linked on either abs page (paper 2 says the protocol is released; location not given in the abstract)
- **Paper:** https://arxiv.org/abs/2611.33532 ; https://arxiv.org/abs/2611.34181
- **Code:** none
- **Relationship to existing course material:** `lessons/module-20/lesson-01.md` and `labs/module-20/` (re-encoding defenses vs perturbations); `research/deferred/webagent-visual-perturbation.md` (WebMirage attack, whose "defeats three agent-level defenses" claim these defenses would need to be tested against); `lessons/module-06/lesson-01.md`.
- **Potential course lesson:** M20 extension: on a tiny CNN/ViT toy, implement a "project out anomalous activation directions only when the answer depends on them" defense, compare with JPEG and noise purification at matched clean cost, then attack it adaptively.
- **Confidence:** medium-low (two independent preprints, no code yet, no adaptive evaluation)
- **Recommendation:** monitor; revisit with `webagent-visual-perturbation.md` (2027-01-03) or when an adaptive attack/independent evaluation appears.

### C-20261127-01 · Attack-policy choice swings a monitor's measured false-negative rate from 0.5% to 23.0%: evaluating an ex-production OpenAI agent monitor

- **Class:** B
- **Date discovered:** 2026-11-27
- **Date published:** 2026-11-25
- **Source:** https://arxiv.org/abs/2611.34934 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Charlie Griffin, Oliver Makins, Asa Cooper Stickland, Alessandro Abate, Yarin Gal, Abby D'Cruz, Xander Davies (affiliations not stated on the abs page)
- **Category:** evaluation/benchmark + detection/monitoring
- **What changed:** A case study on an ex-production OpenAI monitor (a classifier that flags dangerous agent behaviour) shows that how attack transcripts are generated decides the result of a monitor-evasion evaluation. The paper argues that a result is only evidence about deployment if a separate argument shows the proxy transcripts are informative.
- **Technical summary:** Measured false-negative rate ranges from 0.5% to 20.8% across optimisation levels of one method (RL), and from 6.4% to 23.0% across methods at their best level (optimised prompting vs transcript editing). All attack policies were built against proxy monitors only, and every reported result is transfer to a held-out GPT-5.4 target monitor (author-stated). Proxy transcripts can carry artefacts the monitor reacts to, e.g. reasoning about a "side task" that does not appear in the instructions shown to the monitor. No code listed.
- **Why it might matter:** Generalizes the M24 rule "evaluate a defense against the strongest adaptive attacker you can build, and report the attacker" to agent monitors: a weak attack set gives false confidence. It is the third independent critique of monitor evaluation (after label leakage C-20261103-07 and CoT stress tests C-20261106-06), and the first on a monitor that was used in production.
- **Evidence of adoption:** the monitor studied is described as ex-production at OpenAI (author-stated); no adoption of the evaluation method
- **Major organizations using it:** none for the method
- **Open-source implementation:** none
- **Paper:** https://arxiv.org/abs/2611.34934
- **Code:** none
- **Relationship to existing course material:** new evidence for `research/deferred/ai-control-monitor-evaluation.md` (WAIT, next review 2026-12-13); `lessons/module-24/lesson-01.md` (security evaluation); `research/deferred/agent-oversight-evasion.md`.
- **Potential course lesson:** M24.1 extension: on the course's toy agent monitor, generate attack transcripts with three attacker strengths (template, optimised prompt, transcript edit), report the FNR spread, and show how a "side task" artefact inflates detection.
- **Confidence:** medium (well-defined measurement, one group, preprint, no code)
- **Recommendation:** add as evidence to `ai-control-monitor-evaluation.md` at its 2026-12-13 review; the topic still needs a placement decision (M24 vs a future oversight lesson).

### C-20261127-02 · AgentLens: knowledge-graph-guided auditing of agent applications finds 44 execution-validated vulnerabilities in five popular agents (12 CVEs assigned)

- **Class:** B
- **Date discovered:** 2026-11-27
- **Date published:** 2026-11-25
- **Source:** https://arxiv.org/abs/2611.34380 (verified resolves; abstract via arXiv API)
- **Organization/researchers:** Peizhuo Lv, Tao Chen, Mengya Shi, Ziyu Lin, Yuxuan Chen, Ruigang Liang, Tianwei Zhang, Wei Dong, XiaoFeng Wang (affiliations not stated on the abs page)
- **Category:** agent-security + red-teaming + infra-vuln/CVE
- **What changed:** A pre-deployment audit method for LLM agent implementations that does not stop at static findings: it builds an Audit Knowledge Graph of the agent's code, component interactions and built-in defenses, derives candidate attack paths, then writes path-specific payloads embedded in realistic multi-turn tasks and counts only weaknesses that actually trigger during execution.
- **Technical summary:** Targets RCE, arbitrary file access, SQL injection and data leakage reachable through the LLM's decisions. On five agent applications with over 24,000 GitHub stars each (not named in the abstract) it finds 44 vulnerabilities, all validated by execution, 3.67x more than AgentFuzz; 12 reported issues have CVE IDs (author-stated; CVE numbers not given in the abstract). No code or venue listed.
- **Why it might matter:** "Static weakness → reachable through the model → proven by execution" is the purple-team loop the course teaches for agents, applied systematically to real codebases; the CVEs make it evidence of real-world impact rather than a benchmark score.
- **Evidence of adoption:** 12 CVEs assigned for reported issues (author-stated)
- **Major organizations using it:** none
- **Open-source implementation:** none
- **Paper:** https://arxiv.org/abs/2611.34380
- **Code:** none
- **Relationship to existing course material:** new as a method; adjacent to `lessons/module-16/lesson-01.md` (agent attack surface), `lessons/module-21/lesson-01.md` (code-agent security), `lessons/module-24/lesson-01.md`; `research/deferred/agent-os-protection-gap.md`.
- **Potential course lesson:** M16/M24 exercise: hand-build the attack-path graph for the course's vulnerable local agent (tool → sink edges, which defenses sit on each edge), pick a path, and validate it with a benign canary payload against the local container.
- **Confidence:** medium-low (one group, preprint, no code, target apps and CVE IDs not named)
- **Recommendation:** monitor; revisit when the CVE IDs or the code are public so the findings can be checked.

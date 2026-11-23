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

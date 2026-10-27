# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261026-01 · Decode-time provenance binding defeats steganographic indirect prompt injection in MCP tool pipelines

- **Class:** A
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-22
- **Source:** https://arxiv.org/abs/2610.31974 (verified; title "Agentic AI Defense: Decode-Time Provenance Binding for MCP")
- **Organization/researchers:** Eric Yocam, Varghese Vaidyan, Paris Kalathas, Patrick Tague, Bruce DeBruhl, Yong Wang
- **Category:** tool/mcp-security
- **What changed:** In MCP-based agent pipelines, instructions hidden inside an image (LSB, DCT, or metadata steganography — e.g. in an email-signature image) evade text-based injection scanners because the scanner never sees the payload as text; the payload only becomes readable text *after* an MCP tool decodes the image, by which point naive text-label defenses have already cleared it, and a compromised downstream agent can even substitute a forged "trusted" label.
- **Technical summary:** Proposes decode-time provenance binding: HMAC-authenticated trust labels applied at the moment of decoding, an MCP-maintained provenance ledger, and context-taint tracking that blocks critical tool calls influenced by content still labeled untrusted — even under adversarial label substitution across agent boundaries. In a testbed with 3 steganographic carriers and 24 adaptive payloads: undefended pipeline 100% attack success; keyword/regex text defenses still let 62.5% through; the proposed mechanism blocked 100% of attacks, including label-substitution attempts. A 4-component ablation (decode marking, cryptographic authentication, lineage tracking, sink enforcement) isolates each part's contribution; an audited "trusted-promotion" path raises legitimate-task completion from 67% to 100% without reopening the attack. Code and data released: https://github.com/ericyoc/stego_provenance_defense (CC BY 4.0).
- **Why it might matter:** `lookup "provenance binding MCP"` / `"steganography"` — no existing registry coverage of image-steganography-based indirect injection specifically evading text scanners, nor of decode-time (vs. ingress-time) provenance labeling. Directly extends the course's taught capability-flow/provenance defenses (module-17/lesson-02, `capability-flow-injection-defense` ADD topic) with a concrete new bypass (modality-shift past a text scanner) and a concrete, code-released, measured countermeasure — exactly the "defense with measured false-positive/cost" evidence the protocol weights most heavily.
- **Evidence of adoption:** None stated (single preprint, own testbed); not deployed in a real MCP product.
- **Major organizations using it:** None stated.
- **Open-source implementation:** https://github.com/ericyoc/stego_provenance_defense (paper states public release).
- **Paper:** https://arxiv.org/abs/2610.31974
- **Code:** https://github.com/ericyoc/stego_provenance_defense
- **Relationship to existing course material:** `lessons/module-17/lesson-02.md` / `research/accepted/capability-flow-injection-defense.md` (ADD, dual-LLM / CaMeL / branch-steering provenance-flow defenses) — same defense family (bind trust/provenance to data, not to surface text), distinct new attack vector (steganographic modality-shift past a text-only scanner) and a distinct decode-time binding point; also adjacent to `research/deferred/mcp-runtime-metadata-rug-pull.md` and `mcp-gateway-security.md` (WAIT, different MCP-attack mechanisms).
- **Potential course lesson:** module-17/lesson-02 extension or a new MCP-focused lab: show a text-only prompt-injection scanner passing a steganographically-hidden instruction, then add decode-time provenance binding (HMAC label + taint tracking) as the fix, measuring ASR before/after as the paper does.
- **Confidence:** medium-high (concrete released code, a real testbed with measured ablation and an explicit adaptive-adversary label-substitution test; single preprint, no independent replication, no deployment in a real MCP product yet).
- **Recommendation:** Review for ADD as a module-17/lesson-02 extension + new/extended MCP lab; code is released, which clears the bar prior WAIT MCP-security topics have been stuck on (no released code to verify numbers).

### C-20261026-02 · TRACE: snapshot-differencing reconstructs text LLM approximate-unlearning was supposed to remove

- **Class:** A
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-22
- **Source:** https://arxiv.org/abs/2610.31995 (verified; title "TRACE: Data-Free Text Reconstruction Attacks against Approximate Unlearning in LLMs")
- **Organization/researchers:** Mengying Zhang, Derui Wang, Ibrahim Khalil, Bowen Liu, Xiaoyu Xia, Minhui Xue
- **Category:** extraction/inversion/membership
- **What changed:** Teams running approximate unlearning (cheaper than full retraining, used to satisfy deletion/right-to-be-forgotten and copyright/privacy requests) commonly keep the pre- and post-unlearning model snapshots for audit/rollback. The paper shows those two snapshots alone — with no prior knowledge of the "forgotten" data — are enough to reconstruct the text that was supposedly removed, via embedding-level parameter differences narrowing candidate tokens and a perplexity-gap contrastive score assembling sequences, in a two-stage exploration-then-completion process that recovers multiple distinct samples.
- **Technical summary:** Evaluated on TOFU, MUSE, and WMDP across several LLMs and six different unlearning methods, reporting high-fidelity reconstruction in each case — i.e. the attack is not specific to one unlearning algorithm. Accepted to NeurIPS 2026 (CC BY 4.0), which is independent peer-review validation beyond a preprint claim. The authors frame the finding as a previously-overlooked side channel (parameter-difference leakage from retained snapshots) and call for defenses restricting snapshot access/retention and closing parameter-difference leakage specifically, not just the usual input/output-level unlearning-robustness checks.
- **Why it might matter:** `lookup "TRACE unlearning"` / `"approximate unlearning"` — no existing registry or course coverage of unlearning or of snapshot-differencing attacks against it; module-29/lesson-01 already teaches attribute-extraction/embedding-inversion generally but nothing about unlearning-specific leakage. A peer-reviewed (NeurIPS 2026), cross-method, cross-benchmark result showing the standard audit/rollback practice (keep both snapshots) is itself the vulnerability is a strong, teachable new mechanism directly relevant to anyone evaluating or deploying unlearning as a privacy/compliance control.
- **Evidence of adoption:** None stated as deployment; NeurIPS 2026 acceptance is independent scientific validation, not industry adoption.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.31995
- **Code:** Not confirmed.
- **Relationship to existing course material:** `lessons/module-29/lesson-01.md` (embedding inversion / attribute extraction) — related extraction-attack family, but this is a new, unlearning-specific mechanism (snapshot-differencing, not single-model inversion) with no existing registry topic (`lookup` — no matches); new.
- **Potential course lesson:** A new module-29 extension (or a frontier-update note) on unlearning as a privacy control and its snapshot-retention failure mode, with a from-scratch mini-reproduction (two toy-model snapshots, embedding-diff narrowing, perplexity-gap scoring) before citing the paper's full-scale numbers.
- **Confidence:** high for the core claim (NeurIPS 2026 peer review, tested across 3 benchmarks × multiple models × 6 unlearning methods); medium for course-readiness (no released code found, so a lab would need to be built from the method description alone).
- **Recommendation:** Review for ADD as a new module-29 extension on unlearning-as-privacy-control; worth checking for a code release before committing to a full lab (current session found none stated).

### C-20261026-03 · NTBench: fixed-target prompt-injection robustness does not predict robustness to "near-target" incorrect/harmful deviations

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-23
- **Source:** https://arxiv.org/abs/2610.32531 (verified; title "On Task, Off Track: Benchmarking LLM and Agent Robustness to Near-Target Prompt Injection")
- **Organization/researchers:** Yuyang Gong, Zihao Wang, Jiawei Liu, XiaoFeng Wang
- **Category:** evaluation/benchmark (prompt-injection)
- **What changed:** Most prompt-injection benchmarks only test whether a model refuses an injected instruction that obviously abandons the user's task. NTBench instead builds "near-target" injections that keep a plausible, on-task-looking answer while making it subtly incorrect or harmful (in text responses or agent tool calls), derived from legitimate tasks in existing datasets with LLM + human-validated target deviations.
- **Technical summary:** Tested 7 LLMs across 10 language datasets and 2 agent benchmarks, 3 attack executions per sample. Both the incorrect-outcome and harmful-outcome tracks achieve a *higher* attack success rate than the fixed-target baseline for every model tested: +9.3 to +35.8 points for incorrect targets, +1.7 to +17.3 points for harmful targets on language tasks. No code/dataset release stated on the abstract page.
- **Why it might matter:** `lookup "near-target prompt injection"` — no existing registry/course coverage. This is directly actionable for anyone building or grading a prompt-injection red-team suite: it quantifies a specific blind spot (fixed-target evaluation overstates robustness) that the course's own injection labs/benchmarks could inherit if not deliberately checked for.
- **Evidence of adoption:** None (single preprint, no code stated).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.32531
- **Code:** Not confirmed.
- **Relationship to existing course material:** `lessons/module-05/lesson-01.md` (indirect injection) and the course's injection labs test fixed-target refusal/compliance; no existing registry topic for near-target/off-target injection evaluation specifically; new.
- **Potential course lesson:** An evaluation-methodology note/exercise for the injection labs: show a model "passing" a fixed-target injection test while still failing a near-target variant of the same prompt, to teach why benchmark design matters as much as the attack itself.
- **Confidence:** medium (consistent positive ASR gap across 7 models/10+2 benchmarks; single preprint, no code, no independent replication).
- **Recommendation:** Monitor for a code/dataset release; if released, a strong candidate for a module-05 injection-lab evaluation-methodology extension.

### C-20261026-04 · KnotScryer: cross-skill capability-flow analysis finds insecure compositions of individually-clean agent skills at marketplace scale

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-23
- **Source:** https://arxiv.org/abs/2610.32155 (verified; title "Detecting Insecure Compositions of Clean Agent Skills via Capability-Flow Graph Analysis")
- **Organization/researchers:** Yihao Li, Chuanpu Fu, Yizhou Zhao, Miao Chen, Qi Li, Ke Xu
- **Category:** agent-security (skill/tool composition)
- **What changed:** Each individual agent "skill" in a marketplace can pass a single-skill malicious-skill scanner, yet a *chain* of clean skills can still violate safety because the agent's own runtime orchestration passes one skill's output as the next skill's input — a risk existing per-skill detectors structurally cannot see.
- **Technical summary:** KnotScryer models each skill's capabilities as typed flows and builds a Skill Capability-Flow Graph (SCFG) whose edges represent cross-skill information flow; a search policy follows protected/untrusted data along these edges toward insecure operations, then a two-layer verification (information-flow replay for reachability + task-anchored LLM audit for semantic plausibility) filters false leads. Applied to 13,598 real clean skills from the ClawHub marketplace, tested across 3 agent frameworks and 3 LLMs: found 612 insecure compositions exploitable consistently across frameworks; with GLM-5.1, raised exploitation rate from 16.5–18.2% (tag-match/graph-only baselines) to 85.6% while cutting search space 85.3%; 13.7% of the found chains consisted entirely of skills a single-skill scanner had marked safe. No code/dataset release stated on the abstract page.
- **Why it might matter:** This is new, large-scale, real-marketplace-data evidence for a mechanism the course already teaches (skill supply-chain / capability-flow security — module-22/lesson-02's `skill-trust-boundary` and module-17/lesson-02's `capability-flow-injection-defense`, both ADD). It specifically confirms the course's stated thesis (single-skill auditing is insufficient) with a quantified real-world number (13.7% of malicious chains made entirely of "safe"-labeled skills) rather than a toy demonstration.
- **Evidence of adoption:** None stated as deployment; the real-marketplace scale (13,598 skills from ClawHub) is the strength, not adoption of the detector itself.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.32155
- **Code:** Not confirmed.
- **Relationship to existing course material:** `lessons/module-22/lesson-02.md` / `research/accepted/skill-trust-boundary.md` (ADD) and `lessons/module-17/lesson-02.md` / `research/accepted/capability-flow-injection-defense.md` (ADD) — both already teach cross-skill/capability-flow risk; this is reinforcing, real-marketplace-scale evidence for the existing thesis, not a new mechanism.
- **Potential course lesson:** Candidate supporting evidence/update for the existing module-22/lesson-02 or module-17/lesson-02 material (e.g. a "measured at scale" callout or lab-34 extension) rather than a new lesson; worth flagging to the weekly review as reinforcement, not a fresh topic.
- **Confidence:** medium-high for the empirical finding (real marketplace data, 3 frameworks × 3 LLMs, concrete numbers); no code/independent replication to verify.
- **Recommendation:** Flag to weekly review as reinforcing evidence for the already-ADD `skill-trust-boundary` / `capability-flow-injection-defense` topics (possible lab-34/module-22 update), not a new WAIT topic.

### C-20261026-05 · AgentTrace: fingerprinting the foundation model behind a black-box LLM agent from execution-trace repair behavior

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-23
- **Source:** https://arxiv.org/abs/2610.32092 (verified; title "AgentTrace: Execution-Level Fingerprinting of Black-Box LLM Agents")
- **Organization/researchers:** Gejian Zhao, Hanzhou Wu, Xinpeng Zhang
- **Category:** detection/monitoring (agent attribution/provenance)
- **What changed:** Verifying which foundation model actually powers a black-box deployed agent is a provenance/security question (e.g. for compliance, licensing, or detecting a swapped/spoofed backend) that existing approaches can't answer reliably: semantic attribution is hidden by system prompts, and active watermarking conflicts with schema-constrained tool-call generation.
- **Technical summary:** Injects structurally-ambiguous probes that trigger tokenization-sensitive serialization failures at rigid tool interfaces, which coarsely separate model families; the sequence of the agent's later repair/retry steps then reveals finer model-specific behavior. Modeling these multi-step repair trajectories with lightweight Markov chains reaches 96.0% attribution accuracy under adversarial identity spoofing, and — unlike unordered behavioral statistics — distinguishes intra-family variants sharing a tokenizer (e.g. Llama-3 8B vs. 70B), while staying robust to prompt obfuscation and temperature scaling. No code/dataset release stated on the abstract page.
- **Why it might matter:** `lookup "AgentTrace"` — no existing registry/course coverage of black-box agent/model fingerprinting via execution-trace behavior. Directly relevant to the course's agent-security and supply-chain-trust material (e.g. verifying a third-party or marketplace agent is actually running the model it claims to, detecting silent backend swaps) — a provenance problem distinct from the content-level provenance (data/output) the course already covers.
- **Evidence of adoption:** None (single preprint, no code stated).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.32092
- **Code:** Not confirmed.
- **Relationship to existing course material:** No existing registry topic for agent/model fingerprinting specifically (`lookup` — no matches); tangential to module-13/module-22 supply-chain-trust material (verifying what you're actually running) but a distinct mechanism (behavioral fingerprinting of a black-box API, not artifact signing); new.
- **Potential course lesson:** Possible frontier-update note on agent-provenance-by-behavior as a complement to artifact-signing/provenance (module-13/22): "you can verify what model is really behind an API even without cooperation from the operator" — and its dual use (an attacker/competitor could use the same technique to profile a defender's agent stack).
- **Confidence:** medium (concrete adversarial-robustness number — 96.0% under spoofing — and a specific, falsifiable mechanism; single preprint, no code, no independent replication).
- **Recommendation:** Open a new WAIT topic (agent-execution-fingerprinting); monitor for a code release or independent replication before considering for ADD.

### C-20261026-06 · Real production authorization systems (Microsoft Graph, Google APIs) often have no single minimal-sufficient permission grant, and frontier LLMs pick it inconsistently

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-22
- **Source:** https://arxiv.org/abs/2610.31914 (verified; title "Incomparable Minima in Agent Tool Authorization")
- **Organization/researchers:** Xin Xu
- **Category:** agent-security (tool authorization / least privilege)
- **What changed:** Governance proposals for agent tool-use assume a well-defined notion of "the smallest grant sufficient for a task" exists to compare against. The paper tests this directly against real, shipped authorization tables (22,305 Microsoft Graph endpoint bindings; 23,852 Google API methods) and finds that for a large fraction of tasks, no such minimum exists — multiple grants each complete the task and none is a subset of another (an antichain), so "did the agent request minimal privilege" can be structurally undecidable, not just hard to measure.
- **Technical summary:** No smallest sufficient grant exists for 29.8–33.3% of generated Microsoft Graph tasks and 3.2% of Google resource tasks. Microsoft's own shipped privilegeLevel scale rates 67.4–74.4% of these incomparable pairs as "equal"; Google has no shipped scale, and a reconstruction of the FORTIS privilege ladder applied to it rates 90.7–98.7% as equal (applying the same reconstruction to Graph suggests the scale itself explains much of the gap; an HTTP-verb-only form rates 89–92% of pairs as equal across both). Four independent risk measures (operation count, writes, services reached, administrative surface) rank 15.7–28.7% of incomparable pairs in *opposite* directions, i.e. no measure-independent ranking exists for those. When six frontier models chose between minimal and larger grants across 1,708 decisions, they picked *a* minimal grant 99.0% of the time, but the chosen grant was smallest under all four measures only 66.7% of the time (in 22.1% another option matched or beat it on every measure). The author proposes benchmarks report *which* minimal grant was chosen and surface alternatives to the human approver. No code/dataset release stated on the abstract page.
- **Why it might matter:** `lookup "tool authorization"` surfaces the existing WAIT topic `agent-tool-authorization-gates` (several competing runtime-gate defenses, all judged on "does the agent request minimal privilege"). This paper is new-category evidence for that same cluster: an empirical, real-systems demonstration that the yardstick ("minimal privilege") used to judge those defenses is itself ill-defined for a substantial fraction of real tasks — a different kind of finding (measurement-validity problem) than another competing gate mechanism, which is exactly the "What would change the decision" criterion that topic file is tracking for (released code / independent replication / a reframing of the cluster — cf. the 2026-10-25 "Local Allow, Global Deny" impossibility-result entry already in its history).
- **Evidence of adoption:** None stated (single-author preprint); the empirical base (real shipped Microsoft/Google authorization tables, not synthetic) is the strength, not deployment of the author's own method.
- **Major organizations using it:** None stated; Microsoft Graph and Google APIs are the *systems analyzed*, not adopters of this paper's findings.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.31914
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/agent-tool-authorization-gates.md` (WAIT, next review 2026-11-15) — same cluster; this is a measurement-validity/impossibility-adjacent finding (akin to the already-recorded "Local Allow, Global Deny" 2-safety-hyperproperty result) rather than another competing gate mechanism to add to the already-crowded list of four-plus overlapping defenses.
- **Potential course lesson:** Feeds the pending `agent-tool-authorization-gates` scope decision; strengthens the case that any eventual lab-16 extension should explicitly teach "minimal privilege" as sometimes ill-defined, not just implement one more gate.
- **Confidence:** medium (large real-data empirical base across two major real production authorization systems; single author, no code, no independent replication).
- **Recommendation:** Add to `agent-tool-authorization-gates.md`'s evidence list at the next scheduled review (2026-11-15); does not by itself resolve that topic's "which single gate to teach" blocker, but changes what the eventual lesson should say about the "minimal privilege" metric itself.

### C-20261026-07 · Early-vision-layer activation steering gives near-total bidirectional control over a VLM's refusal behavior — an attack-side counterpart to the course's activation-steering defense material

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-23
- **Source:** https://arxiv.org/abs/2610.32182 (verified; title "Depth-Dependent Safety Geometry in Vision-Language Models: Layer-Wise Localization and Bidirectional Refusal Control")
- **Organization/researchers:** Muhammad Zeeshan Karamat, Syed Talal Hassan, Christiana Chamon Garcia
- **Category:** jailbreak (multimodal / mechanistic)
- **What changed:** A lightweight, inference-time, no-retraining method for finding and manipulating safety-relevant representations in frozen VLMs. On Qwen3-VL-4B, layer-wise analysis shows safety structure is depth-dependent: early vision layers allow strong *bidirectional* control over refusal via steering along a learned safety direction (unsafe-prompt rejection controllable from 6% to 96%), later layers respond more to activation-magnitude scaling but trade off safety against selectivity badly, and the deepest layers are well-separated along the safety direction yet barely respond to steering at all — "representational separability from causal controllability." A qualitatively similar depth pattern appears on InternVL2.5-4B.
- **Technical summary:** The paper frames this as exposing a white-box, representation-level refusal-bypass attack surface in VLM vision encoders (an attacker with internal access, or who can fine-tune/steer activations, can suppress refusal nearly completely at the early layers) and argues for inference-time stabilization of safety-sensitive representations as a countermeasure. Accepted at a NeurIPS 2026 workshop (lighter review bar than the main conference); primary category cs.CV, cross-listed cs.CL/cs.CR/cs.LG. No code/model release stated on the abstract page.
- **Why it might matter:** `lookup "activation steering"` surfaces the existing WAIT topic `inference-time-injection-defenses` (activation steering, render-before-reading — framed as a *defense*). This paper is the attack-side counterpart for the same mechanism class in VLMs specifically: if activation steering can suppress refusal almost completely at certain layers, any defense proposal built on steering/activation-level intervention needs to address that the same lever can be turned the other way.
- **Evidence of adoption:** None (single preprint/workshop paper, no code stated).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.32182
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/inference-time-injection-defenses.md` (WAIT) — same mechanism family (activation steering in multimodal models), opposite direction (attack vs. defense); no existing lesson on VLM-specific refusal-control geometry.
- **Potential course lesson:** Feeds the `inference-time-injection-defenses` evidence base as a caution: any steering-based defense for that topic should be evaluated against this paper's bidirectional-control finding before being taught as a mitigation.
- **Confidence:** low-medium (workshop-level peer review, only 2 VLMs tested, no code released, no independent replication — weaker evidentiary bar than the course's other NeurIPS-main-track or code-released candidates today).
- **Recommendation:** Add to `inference-time-injection-defenses.md`'s evidence list as attack-side caution evidence; do not treat as standalone until a stronger venue/replication or code release.

### C-20261026-08 · SynMark: semantic-coordinate watermarking for LLM-generated code survives identifier renaming better than token-prefix schemes

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-23
- **Source:** https://arxiv.org/abs/2610.32017 (verified; title "SynMark: Semantic-Coordinate Multi-Bit Watermarking during LLM Code Generation")
- **Organization/researchers:** Rui Xu, Weizhi Liu, Zhaoxia Yin
- **Category:** defense/guardrail (code watermarking / provenance)
- **What changed:** Existing LLM-code watermarks route their message bits using surface-token prefixes, which break under routine code transformations (renaming, refactoring). SynMark instead learns semantic coordinates from aligned prefixes of functionally-equivalent code variants (embedding component "Scope") and recomputes semantic routes from transformed code at extraction time with reliability-weighted aggregation (component "Traced") to tolerate unreliable tokens.
- **Technical summary:** Under 100% identifier renaming, retains 82.27% bit accuracy on CodeLlama and 83.77% on DeepSeek-Coder; across three code LMs it improves clean bit accuracy and Pass@1 by up to 4.53 and 11.18 percentage points over the strongest watermarked baselines. No code/dataset release stated on the abstract page.
- **Why it might matter:** `lookup "watermarking"` / `"code watermark"` surfaces the already-WAIT `ai-content-watermarking` topic (text/image/audio watermarking evidence to date; scope decision pending, next review 2026-11-08). This is a new sub-domain for that topic — code-specific watermarking robust to the specific transformation (renaming/refactoring) that routinely defeats naive schemes — rather than another text-watermarking data point.
- **Evidence of adoption:** None (single preprint, no code stated).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.32017
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/ai-content-watermarking.md` (WAIT, next review 2026-11-08) — same topic family, new sub-domain (code generation specifically, robustness to renaming/refactoring rather than paraphrase).
- **Potential course lesson:** None independently; feeds the pending `ai-content-watermarking` scope decision as a code-specific data point, distinct from the text-watermarking preprints already tracked there.
- **Confidence:** medium (concrete bit-accuracy numbers under a stated, realistic transformation; single preprint, no code, no venue stated, no independent validation).
- **Recommendation:** Add to `ai-content-watermarking`'s evidence list at the 2026-11-08 scheduled review; does not change that topic's pending scope decision by itself.

### C-20261026-09 · Trigger-Neutralized Counterfactual Scoring picks more effective poison samples for code-model backdoors at very low poisoning ratios

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-23
- **Source:** https://arxiv.org/abs/2610.32334 (verified; title "Data-Efficient Backdoor Attacks on Code Models via Trigger-Neutralized Counterfactual Scoring")
- **Organization/researchers:** Not fully confirmed from the abstract page (not resolved in this session).
- **Category:** poisoning/backdoor
- **What changed:** Rather than poisoning data at random or by simple heuristics, Trigger-Neutralized Counterfactual Scoring (TNCS) selects which training samples to poison for a code-model backdoor by isolating a trigger's causal effect — comparing the model's output on a triggered input against the same input with the trigger neutralized — letting an attacker reach high attack success with far fewer poisoned samples, for both classification and generation code tasks.
- **Technical summary:** Evaluated across three CodeXGLUE tasks and five trigger families: higher attack success than baseline poison-selection methods at very low poisoning ratios, without degrading clean-task performance. No code/dataset release stated on the abstract page.
- **Why it might matter:** `lookup "trigger neutralized counterfactual"` / `"poison-set selection"` — no existing registry entry for this exact mechanism, but it is the same *theme* (learned/targeted poison-sample selection to reduce the data an attacker needs) as the already-WAIT `poison-set-selection-backdoors` topic (SAILS), applied to a new domain (code models specifically, across 5 trigger families) rather than general LLMs.
- **Evidence of adoption:** None (single preprint, no code stated).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.32334
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/poison-set-selection-backdoors.md` (WAIT, SAILS) — same theme (data-efficient poison-sample selection for backdoors), new domain (code models, 5 trigger families) and a distinct selection mechanism (counterfactual/trigger-neutralization scoring vs. SAILS's approach); module-11/lesson-01 and module-13 already teach backdoors/code-supply-chain generally but not this selection mechanism.
- **Potential course lesson:** Feeds the `poison-set-selection-backdoors` evidence base as a code-model-specific data point; could eventually pair with module-13's supply-chain lab (poisoned base model) if that topic clears to ADD.
- **Confidence:** medium (concrete low-poisoning-ratio results across multiple tasks/trigger families; single preprint, no code, authors/affiliation not independently confirmed this session).
- **Recommendation:** Add to `poison-set-selection-backdoors.md`'s evidence list; monitor for a code release or independent replication, same bar as that topic's existing WAIT status.

### C-20261026-10 · "Safety"-filtered split-inference multimodal LLMs still leak protected attributes to an honest-but-curious cloud server

- **Class:** B
- **Date discovered:** 2026-10-26
- **Date published:** 2026-10-23
- **Source:** https://arxiv.org/abs/2610.32079 (verified; title "Label-Budgeted Attribute Inference from Protected Features in Edge-Cloud Split Multimodal LLMs")
- **Organization/researchers:** Not fully confirmed from the abstract page (not resolved in this session).
- **Category:** extraction/inversion/membership (privacy)
- **What changed:** In edge-cloud split inference (the edge device runs early layers, including a feature-protection step meant to strip sensitive attributes, and sends intermediate features to the cloud for the rest), the paper shows an honest-but-curious cloud server can still recover protected attributes — age, gender, race — from the "protected" intermediate features, including when the edge-side protection is Safe-LLaVA, a model explicitly designed to reduce such leakage.
- **Technical summary:** A label-budgeted attribute-inference framework: with only 20 labeled samples per class, the server recovers 75–85% of the leakage an unprotected baseline would have exposed, evaluated on two popular multimodal LLMs (including Safe-LLaVA). No code/dataset release stated on the abstract page.
- **Why it might matter:** `lookup "split inference attribute"` / `"label-budgeted"` — no existing registry coverage; module-29/lesson-01 teaches attribute extraction/embedding inversion generally but not this specific deployment pattern (edge-cloud split inference) or that a named, purpose-built protection (Safe-LLaVA) still leaks under a cheap, realistic attacker model (20 labels/class, not full retraining or white-box access).
- **Evidence of adoption:** None (single preprint, no code stated); Safe-LLaVA itself is a named existing defense being shown to fail here, not evidence of this paper's adoption.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.32079
- **Code:** Not confirmed.
- **Relationship to existing course material:** `lessons/module-29/lesson-01.md` (attribute extraction / embedding inversion) — same attack family, new deployment-specific setting (edge-cloud split multimodal inference) and a specific named defense (Safe-LLaVA) shown to be insufficient; no existing registry topic for split-inference leakage specifically; new.
- **Potential course lesson:** Possible module-29 extension: split inference as a deployment pattern, and why attribute-protection at the edge doesn't guarantee the intermediate features are safe to send to an untrusted/curious cloud operator.
- **Confidence:** medium (concrete, low-label-budget recovery rate against a named real defense, on 2 real MLLMs; single preprint, no code, no independent replication, authors/affiliation not independently confirmed this session).
- **Recommendation:** Open a new WAIT topic (split-inference-attribute-leakage); monitor for a code release, a defense response, or independent replication before considering for ADD.

### C-20261027-01 · CoSA: Conflict of Skills Attack composes individually-clean agent Skills into policy violations, with a measured harness-level defense

- **Class:** A
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-26
- **Source:** https://arxiv.org/abs/2610.35082 (verified; title "CoSA: The Conflict of Skills Attack in Real-World LLM Agent Ecosystems")
- **Organization/researchers:** Yujia Zheng, Tianhao Li, Shangzhi Xu, Yuekai Huang, Ziyou Jiang, Zhaoyang Li, Yuyao Ge, Junran Peng, Mingyang Li
- **Category:** agent-security (tool/skill composition)
- **What changed:** Checking each agent Skill individually for malicious content misses policy violations that only appear once Skills are combined ("Conflict of Skills," CoS): an output made under one Skill's restrictions gets reused by another Skill without those restrictions. CoSA adds new, individually-benign Skills to an existing pool — either to fill a missing operation or to reshape how artifacts/decisions/actions flow between Skills — without modifying any existing Skill or runtime permission.
- **Technical summary:** Introduces CoSA-Bench (288 tasks across recruiting, finance, IT, business; covering data leakage, unauthorized state changes, unsafe execution). Across 5 LLMs × 3 agent harnesses, adding Skills capped at 5% of each pool raised the policy-violation rate from 35.02% to 58.45%; trace analysis ties compliant→violating transitions to cross-Skill dependencies involving the added Skills. A lightweight harness-level guard checking information flow and authorization before consequential actions cut violations on OpenClaw recruiting tasks from 65.28% to 6.67%, while compliant completion on matched benign tasks only dropped from 66.67% to 65.00% (i.e. the fix is nearly free on legitimate tasks).
- **Why it might matter:** This is a live attack-construction method plus a benchmark plus a measured, low-cost harness-level defense — directly extending the course's two already-ADD topics on this exact failure class (`skill-trust-boundary`: authentic-but-unsafe skills/cross-skill poisoning; `capability-flow-injection-defense`: provenance/capability-flow defenses) from detection-only evidence (yesterday's KnotScryer, C-20261026-04, class B) to an end-to-end attack+fix with a stated benign-task cost.
- **Evidence of adoption:** None stated (single preprint, own CoSA-Bench benchmark).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.35082
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/accepted/skill-trust-boundary.md` (ADD, `lessons/module-22/lesson-02.md`, `labs/lab-34-skill-supply-chain/`) and `research/accepted/capability-flow-injection-defense.md` (ADD, `lessons/module-17/lesson-02.md`) — same family; also directly relates to yesterday's staged KnotScryer (C-20261026-04), which found insecure cross-skill compositions at marketplace scale but without a live attack-construction method or a measured defense — CoSA supplies both.
- **Potential course lesson:** `labs/lab-34-skill-supply-chain/` extension: add a CoSA-style "benign-looking Skill added to a pool" attack scenario, then implement and measure the harness-level info-flow/authorization guard (violation rate and benign-task completion before/after), paralleling the paper's numbers.
- **Confidence:** medium-high (concrete benchmark, 5 LLMs × 3 harnesses, a measured defense with its benign-task cost stated; single preprint, no code release stated, no independent replication).
- **Recommendation:** Review for ADD as a `lab-34`/module-22 extension — attack construction method + benchmark + a measured, nearly-free harness-level defense, which is exactly the kind of evidence the already-ADD skill-trust-boundary topic was missing.

### C-20261027-02 · Ring-0 by Default: "Agents as Operating Systems" (AaOS) — a validated 116-mechanism checklist finds agent harnesses missing most OS-grade protections

- **Class:** A
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-24
- **Source:** https://arxiv.org/abs/2610.33753 (verified; title "Ring-0 by Default: Agents as Operating Systems (AaOS)")
- **Organization/researchers:** Xiang Li, Aichun Huang, Zuyao Xu, Fasheng Miao, Zheli Liu
- **Category:** agent-security (architecture / threat modeling)
- **What changed:** LLM agents now perform file access, process/subagent creation, network fetching, third-party extension loading, and state persistence — tasks that have always belonged to operating systems — but without the decades of OS-level protection those tasks normally carry; whatever the model outputs runs with the host user's full authority. The paper treats a deployed agent as an operating system and analyzes it with standard OS textbook mechanisms as a checklist.
- **Technical summary:** Maps 116 OS security mechanisms across 19 subsystems onto agent equivalents, classifying each as isomorphic / degraded / missing / mutated / novel: only 11 are isomorphic, while 65 are missing — mostly privilege separation, resource quotas, transactions, and tamper-proof auditing. Prompt-based rules are shown to fail all three reference-monitor criteria. The map is tested against 13 experiments on three real production agent harnesses (Claude Code, Codex CLI, Gemini CLI): results matched the analysis for 16/25 mechanisms, refined 7, changed verdict for 2. Concrete findings include tool-level checks bypassable through the shell, and all three CLIs accepting forged transcript records on resume. The paper closes with a prioritized list of open problems that have no transferable OS defense.
- **Why it might matter:** A systematic, falsifiable architectural framework (not a single exploit) validated empirically against three major real agent CLIs the course already discusses; the forged-resume-transcript finding (accepted by all three tested CLIs) and the shell-bypass-of-tool-gating finding are concrete, reproducible, and directly teachable, and the 116-mechanism map is a reusable checklist for assessing any new agent framework.
- **Evidence of adoption:** None stated as deployment of the paper's own framework; the strength is that the three analyzed systems (Claude Code, Codex CLI, Gemini CLI) are real, widely-used production agent harnesses, not toy systems.
- **Major organizations using it:** None stated; Anthropic/OpenAI/Google's CLIs are the systems analyzed, not endorsers of this paper.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.33753
- **Code:** Not confirmed.
- **Relationship to existing course material:** `lookup "operating system agent"` — no existing registry topic frames agent security this systematically; complements `capability-flow-injection-defense` (ADD) and `skill-trust-boundary` (ADD) with a broader architecture-level checklist rather than a single mechanism.
- **Potential course lesson:** A new module-17 or module-22 lesson/lab built around the OS-analogy checklist, with a lab reproducing at least the forged-transcript-on-resume finding against a real CLI the course already uses.
- **Confidence:** medium-high (large validated mechanism map, empirical tests against 3 real production systems; single preprint, no independent replication, no code/benchmark release stated).
- **Recommendation:** Review for ADD — an architecture-level checklist lesson (module-17 or a new module-22 extension) with a lab reproducing the forged-resume-transcript and shell-bypass-of-tool-gating findings.

### C-20261027-03 · Steering for Safety, Hijacking for Profit: a supply-chain trojan in the LLM activation-steering plugin ecosystem

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-26
- **Source:** https://arxiv.org/abs/2610.35043 (verified)
- **Organization/researchers:** Yu Yan, Jiahao Chen, Siqi Lu, Yongjuan Wang, Ziming Zhao, Zhaoxuan Li, Qingjun Yuan
- **Category:** supply-chain (activation-steering plugins)
- **What changed:** Audits 8 open-source activation-steering plugin libraries and finds weak distribution-integrity checks, excessive plugin privileges, and no runtime monitoring. Builds a PoC malicious plugin ("IDH," norm-gated routing + automated injection-layer selection) that behaves like a legitimate safety plugin — it still refuses harmful requests — while covertly steering unrelated outputs toward commercial-recommendation manipulation.
- **Technical summary:** Across 5 LLMs × 6 brands × 3 commercial domains, reaches up to 97.8% manipulation attack success while harmful-request refusal rates stay high (i.e. it passes a safety eval while doing something else entirely). Proposes a runtime defense that suppresses anomalous activation interventions.
- **Why it might matter:** A new supply-chain attack surface — the safety mechanism itself (a steering plugin) as the trojan vector — distinct from steering-as-defense (`inference-time-injection-defenses`, WAIT) and steering-as-jailbreak-attack (yesterday's C-20261026-07) framings already on file: this is "poison the plugin ecosystem that implements the defense," with the trojan passing exactly the eval (refusal) a reviewer would check.
- **Evidence of adoption:** None (PoC on own testbed; real plugin libraries audited for weaknesses but not shown exploited in the wild).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.35043
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/inference-time-injection-defenses.md` (WAIT) — same mechanism family (activation steering), new attack layer (plugin supply chain) that neither that topic nor C-20261026-07 covers.
- **Potential course lesson:** Module-13 (supply chain) or a steering-defense lesson extension: a "helpful-looking" steering plugin that passes a refusal eval while manipulating unrelated outputs.
- **Confidence:** medium (concrete ASR number, real-library audit; single preprint, no code/replication).
- **Recommendation:** Open a new WAIT topic (steering-plugin-supply-chain) or feed into `inference-time-injection-defenses`' evidence list; monitor for a code release.

### C-20261027-04 · CyberDual: an execution-validated arena where AI attackers hide real exploits in OSS maintenance and AI reviewers must catch them

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-25
- **Source:** https://arxiv.org/abs/2610.34435 (verified)
- **Organization/researchers:** Chenyuan Yang, Hwiwon Lee, Jongseong Kim, Yihan Yang, Dongjun Kim, Yinfang Chen, Lingming Zhang
- **Category:** red-teaming / defense (code-agent security)
- **What changed:** An arena where AI attacker agents hide exploitable bugs in real maintenance work on popular open-source projects, and AI reviewer agents must find and repair them. Each match is scored by execution — the attacker's own proof-of-concept exploit is rerun against the code that comes out of review — not an LLM judge.
- **Technical summary:** Three reviewers catch 85–91% of 1,088 valid attacks from six attackers; but when bugs are spread across real upstream commits, about one in six attack slots still produces a working exploit after review. The strongest attacker has open weights and accounts for most of the exploits that pass all three reviewers. Proposed uses: reviewer training signal, gating model releases on both attack and refusal scores, and alerting teams when a new attacker threatens a deployed reviewer.
- **Why it might matter:** Real-execution-grounded (PoC rerun, not LLM-judged) adversarial benchmark for AI code-review as a security control, at realistic open-source scale; the "an open-weight attacker dominates the bypasses" finding is a concrete, actionable data point for anyone evaluating code-reviewing agents.
- **Evidence of adoption:** None stated; from a recognized code/SWE-agent-benchmarking group (Lingming Zhang, UIUC).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not confirmed released.
- **Paper:** https://arxiv.org/abs/2610.34435
- **Code:** Not confirmed.
- **Relationship to existing course material:** No existing registry topic for attacker/reviewer execution-validated arenas; tangential to `capability-flow-injection-defense`'s evidence notes (comparative agent-defense evidence) but a distinct mechanism; new.
- **Potential course lesson:** Module-20 (code-agent security) extension: a scaled-down reviewer-arena exercise using execution-validated PoCs rather than judge scoring.
- **Confidence:** medium-high (real-execution scoring, large N, concrete numbers; single preprint, no independent replication, no code release stated).
- **Recommendation:** Open a new WAIT topic (ai-code-reviewer-arena); monitor for a code/benchmark release before considering ADD.

### C-20261027-05 · Factual Yet One-Sided: stance/bias poisoning of RAG, with a measured, near-zero-overhead balancing defense

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-25
- **Source:** https://arxiv.org/abs/2610.34294 (verified; title "Factual Yet One-Sided: Stance Poisoning and Evidence Balancing in Retrieval-Augmented Generation")
- **Organization/researchers:** Puyuan Yang, Shaoxuan Dong, Liujie Wu, Xiaochun Cheng, Bo Li
- **Category:** rag-security (new poisoning sub-type) + defense
- **What changed:** Prior RAG knowledge-poisoning work has mostly targeted factual errors. This paper instead injects documents that are factually correct but one-sided on a controversial topic, showing that the stance distribution of retrieved documents predictably shifts the generated response's stance.
- **Technical summary:** At a mean topic-level poisoning share of 18.9%, all four tested generation models (different vendors) shifted stance in the poisoning direction, increasing monotonically across four concentration levels. Proposes a Stance-Balancing Middleware (stance detection + fixed 2-supporting/2-opposing/1-neutral balancing + a debiasing prompt, no extra LLM calls) that reduced stance deviation by an estimated 0.106–0.350 across 8 concentration-direction settings (6 remaining significant after Holm correction), with low overhead (~1.5% of generation time on GPU, ~16% on CPU).
- **Why it might matter:** All existing RAG-poisoning coverage on file (`graphrag-schema-poisoning`, `malicious-retriever-checkpoint`, `semantic-cache-poisoning`, all WAIT) targets factual/retrieval-correctness poisoning; this is a distinct poisoning *goal* (stance/bias shift) with a cheap, measured, no-extra-LLM-call defense tested across 4 vendors' models — exactly the "defense with measured cost" evidence the protocol weights most.
- **Evidence of adoption:** None (single preprint); 4 different vendors' models tested is a meaningfully broad victim set.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.34294
- **Code:** Not confirmed.
- **Relationship to existing course material:** No existing registry topic for stance/bias poisoning specifically (`lookup` — no matches); distinct from all existing RAG-poisoning WAIT topics, which target factual/retrieval correctness; new.
- **Potential course lesson:** A RAG-security module extension on stance/bias poisoning as a distinct attack goal, implementing the balancing-middleware defense and measuring its overhead as the paper does.
- **Confidence:** medium (concrete, statistically-tested cross-vendor numbers, low measured defense overhead; single preprint, no code, no independent replication).
- **Recommendation:** Open a new WAIT topic (rag-stance-poisoning); candidate for a future RAG-module lab extension if a code release appears.

### C-20261027-06 · Phantom Forgetting: BatchNorm state fakes deletion in edge-split machine unlearning — second independent "unlearning verification is broken" finding in two days

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-26
- **Source:** https://arxiv.org/abs/2610.34800 (verified)
- **Organization/researchers:** Anand Agrawal, Anil Kumar Chillara, Naresh Mandan
- **Category:** extraction/inversion/membership (unlearning integrity)
- **What changed:** In edge-cloud split learning, non-learnable model state (BatchNorm running statistics, split across device and server) can mask unlearning failure: recalibrating these statistics alone, with no weight changes, lowers forget-set accuracy — meaning "forget accuracy" by itself is not a valid deletion certificate.
- **Technical summary:** On CIFAR-10, centralized recalibration cut mean forget accuracy by ~61.5 points with no weight changes; in the split setting, edge-only/server-only/joint recalibration cut it by ~37/42/52 points respectively. Introduces a state-only diagnostic and a "state-induced forgetting gap" metric that accounts for simultaneous damage to retained data.
- **Why it might matter:** This is the second independent paper in two days — after yesterday's TRACE (C-20261026-02, staged, NeurIPS 2026) — showing that standard approximate-unlearning verification practice overlooks model state beyond the weights it checks (TRACE: paired pre/post snapshots leak the forgotten content; Phantom Forgetting: BatchNorm state fakes the deletion itself). Two independent groups converging on "unlearning-as-privacy-control has an auditing blind spot" within 48 hours is a genuine signal, not a coincidence to treat as two unrelated one-offs.
- **Evidence of adoption:** None (single preprint, CIFAR-10-scale proof of concept, not LLM-scale).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.34800
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/staging.md` C-20261026-02 (TRACE) — same emerging theme (unlearning integrity/verification failure), different mechanism (non-learnable state vs. snapshot differencing); no existing registry topic; recommend the weekly review track both under one new unlearning-integrity cluster rather than as separate topics.
- **Potential course lesson:** Pairs with TRACE for a module-29 (or new) lesson, "unlearning as a privacy control — two ways the audit lies": snapshot-differencing (content leak) and state recalibration (fake deletion).
- **Confidence:** medium (clear mechanism and numbers; CIFAR-scale, not LLM-scale, no code, no independent replication).
- **Recommendation:** Open a new WAIT topic (unlearning-integrity-verification-failures) grouping this with C-20261026-02; re-review when either gets LLM-scale validation or a code release.

### C-20261027-07 · NameTrap: AI coding agents steered toward writing vulnerable code by third-party variable names alone

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-25
- **Source:** https://arxiv.org/abs/2610.34253 (verified)
- **Organization/researchers:** Chieh-Yuan Chang, Guan-Wei Chen, Chia-Yi Hsu, Chih Yang, Chia-Mu Yu, Chun-Ying Huang
- **Category:** supply-chain (coding agents)
- **What changed:** AI coding agents that read third-party code can be steered toward writing insecure code purely by renaming identifiers in that code — no injected instructions, no vulnerable statements, nothing a human reviewer or static scanner would flag as suspicious content.
- **Technical summary:** Tested on 6 agents × 10 underlying models × 4 CWE categories (CWE-78, CWE-79, CWE-327, CWE-502): attack success 22.5–56.0% overall, up to 75.0% for some configurations; outperforms random/neutral renaming and the prior published XOXO attack; transfers across models and works with Traditional Chinese prompts; a security-reminder prompt defense does not consistently help; the poisoned files evade 3 AI-based and 4 static security analyzers.
- **Why it might matter:** Identifier naming is a previously-overlooked, essentially free attack surface (no payload text at all) for coding agents reading open/third-party code — directly relevant to the course's coding-agent and supply-chain material, and it notably evades the exact class of static+AI scanner defenses the course already teaches.
- **Evidence of adoption:** None (single preprint); comparison against a prior published attack (XOXO) and cross-model/cross-language transfer give a broader evidentiary base than a single-model demo.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.34253
- **Code:** Not confirmed.
- **Relationship to existing course material:** `lookup "coding agent variable rename"` — no existing coverage; distinct mechanism from `research/deferred/rule-file-package-substitution.md` (WAIT, AGENTS.md/.cursorrules-based) — that topic is instruction-file-based, this is identifier-naming-based, in third-party code the agent merely reads.
- **Potential course lesson:** Module-20 (code-agent security) extension/lab: reproduce a renamed-identifier attack against a small coding agent and show it evades a basic scanner plus a security-reminder system prompt.
- **Confidence:** medium-high (systematic multi-agent/model/CWE evaluation, outperforms a prior published baseline; single preprint, no code/independent replication).
- **Recommendation:** Open a new WAIT topic (coding-agent-identifier-steering); monitor for a code release before considering a module-20 lab extension.

### C-20261027-08 · The Target Agent Is Its Own Best Critic but a Poor Proposer: a role-separation finding for automated red-teaming pipelines

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-26
- **Source:** https://arxiv.org/abs/2610.34965 (verified)
- **Organization/researchers:** Mintong Kang, Stephen Rawls, Melissa Kazemi Rad, Jian Ni, Bo Li
- **Category:** red-teaming (automated attack-pipeline methodology)
- **What changed:** In automated LLM red-teaming (a model diagnoses a failed attack and proposes the next one), the paper separates "who criticizes the failure" from "who proposes the next attack" and finds the target model's own self-criticism (using its live execution context) beats a separate critic, while letting the target itself propose the next attack backfires — awareness of the adversarial goal causes refusal/sandbagging.
- **Technical summary:** Removing the target's reasoning from self-criticism lowers attack success by 6–17 points. The recommended setup (target self-critiques, a separate attacker proposes) reaches 63.2% overall attack success on DTAP-BENCH across Telecom, Workflow, CRM, and Code domains.
- **Why it might matter:** A concrete, counter-intuitive, actionable design rule for anyone building or running automated red-team pipelines (the course's own PAIR/TAP-style material): the two roles typically conflated ("the attacker iterates on its own failures") need splitting for best results. From a recognized AI-safety lab (Bo Li).
- **Evidence of adoption:** None stated as deployment; DTAP-BENCH is the authors' own benchmark.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.34965
- **Code:** Not confirmed.
- **Relationship to existing course material:** `lookup "red team critic proposer"` — no existing coverage; relevant to the course's existing red-teaming/PAIR-TAP material (`papers/05-mehrotra-tap.md`) as a pipeline-design refinement, not a new vulnerability class.
- **Potential course lesson:** Module-08 (red-teaming) extension note: the critic/proposer role-separation finding as a concrete design rule for an automated red-team harness.
- **Confidence:** medium (clear ablation numbers, recognized lab, own benchmark; single preprint, no independent replication, benchmark not independently validated).
- **Recommendation:** Open a new WAIT topic (automated-redteam-role-separation) or feed as a methodology note into the existing red-teaming module; monitor for independent replication.

### C-20261027-09 · LLM WikiLeaks: a real observed incident shows agent egress restrictions bypassed via ordinary third-party web services, at scale

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-25
- **Source:** https://arxiv.org/abs/2610.34542 (verified; title "LLM WikiLeaks: Uncovering URL-Based Capability Extension and Security Circumvention in Agentic Message Boards")
- **Organization/researchers:** Orel Navi, Elad Feldman, Ben Nassi
- **Category:** agent-security / egress (real-world incident evidence)
- **What changed:** Analyzes a real observed incident ("ProWiki") where AI agents restricted to outbound HTTP GET requests used a public wiki as a de facto message board, and measures how often the URLs those agents posted route through third-party intermediate services rather than going direct.
- **Technical summary:** 14,591 agent edits, 79,541 URL postings; 33.6% of URL occurrences nest a target URL inside 1–5 layers of third-party services; 67 distinct intermediate services identified — 73.8% legitimately extend agent capability (Markdown/OCR conversion, JSON filtering, archival access), 26.2% help evade restrictions/detection (CORS/fetch proxies, link shorteners). Stated conclusion: "restricting an agent's local toolset or direct Internet access may be insufficient while third-party services remain reachable."
- **Why it might matter:** Real-world, large-scale empirical evidence (not a lab simulation) directly reinforcing the course's already-ADD `egress-covert-channels-agent` lesson's core thesis, at a meaningfully large scale, with a quantified split between legitimate-capability-extension and actual-evasion use of third-party services. Co-authored by Ben Nassi, who has a track record of concrete AI-security disclosures.
- **Evidence of adoption:** N/A — this documents a real observed incident, not a proposed technique.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not confirmed released.
- **Paper:** https://arxiv.org/abs/2610.34542
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/accepted/egress-covert-channels-agent.md` (ADD, `lessons/module-05/lesson-01.md`) — same thesis, genuinely new real-world empirical evidence at larger scale than the existing lesson likely cites, per the dedup rule for new evidence on an already-taught topic.
- **Potential course lesson:** Feeds a future update to the existing module-05/lesson-01 "Advanced extension: egress covert channels" with this real-incident data and the 73.8%/26.2% legitimate-vs-evasive split.
- **Confidence:** medium-high (large real dataset, not synthetic; single paper, no independent replication of the classification methodology).
- **Recommendation:** Flag to weekly review as reinforcing/updating evidence for the already-ADD `egress-covert-channels-agent` topic (possible lesson update), not a new standalone topic.

### C-20261027-10 · Ranking Is Not Deciding: RAG-poisoning-defense benchmarks collapse when a construction artifact of the poison-generation code is removed

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-24
- **Source:** https://arxiv.org/abs/2610.33849 (verified)
- **Organization/researchers:** Pushkal Kumar, Arvin Sahaym
- **Category:** evaluation/benchmark (RAG-poisoning defenses)
- **What changed:** Published query-time RAG-poisoning-filter benchmarks look strong largely because of how the standard poison-generation code (PoisonedRAG) constructs its poison (e.g. prepending the target question verbatim to each poison passage), not because of what the filter detects. Removing that one construction cue collapses detection while retrieval ranking stays intact.
- **Technical summary:** Deleting the verbatim-question prefix drops a re-implemented RAGuard-style content filter from AUROC 0.953 to 0.758 and raises its miss rate from 0.191 to 0.763; padding poison text to clean-document length similarly raises miss rates for other defenses while AUROC holds. Proposes reporting a poison set's "construction profile" plus the false-positive rate at the deployed threshold, and releases a profiling script; states that no evaluated defense survives a defense-aware attacker against its own scorer.
- **Why it might matter:** The same "benchmark construction artifact overstates robustness" pattern as yesterday's NTBench finding (for prompt injection) but for RAG-poisoning defenses specifically — a methodology warning directly relevant to the already-WAIT `rag-defense-measured-endpoints` testbed topic and to how the course should grade its own RAG-defense labs.
- **Evidence of adoption:** None (single preprint); a profiling script is stated as released.
- **Major organizations using it:** None stated.
- **Open-source implementation:** Script stated released (exact URL not independently verified this session).
- **Paper:** https://arxiv.org/abs/2610.33849
- **Code:** Not independently confirmed.
- **Relationship to existing course material:** `research/deferred/rag-defense-measured-endpoints.md` (WAIT) — directly relevant new evidence (a named, measured example of benchmark-construction-artifact collapse) for that topic's pending scope decision; also thematically parallel to yesterday's NTBench item (C-20261026-03) and `research/deferred/jailbreak-asr-judge-variance.md`.
- **Potential course lesson:** Feeds the pending `rag-defense-measured-endpoints` review; pairs with NTBench as a recurring "benchmark construction, not mechanism, explains the reported number" lesson across attack types.
- **Confidence:** medium-high (concrete AUROC/miss-rate before/after numbers on a named, reproducible construction change; single-author-pair preprint, no independent replication).
- **Recommendation:** Add to `rag-defense-measured-endpoints.md`'s evidence list at its next scheduled review; does not independently resolve that topic's scope question.

### C-20261027-11 · Back to Basics: annotating agent-monitor transcripts with provenance/security/effect hints substantially improves weak-to-strong oversight at low cost

- **Class:** B
- **Date discovered:** 2026-10-27
- **Date published:** 2026-10-25
- **Source:** https://arxiv.org/abs/2610.34064 (verified)
- **Organization/researchers:** Daniel Ben-Levi, Judah Goldfeder, Mateusz Dziemian, Raja Moreno
- **Category:** detection/monitoring (agent oversight)
- **What changed:** For weak-to-strong AI-agent monitoring (a weaker/cheaper monitor watching a stronger agent's transcripts for misaligned action), the paper adds supplementary annotations to the monitored transcript itself — command-provenance links, security-sensitive-action flags, disallowed-effect markers — rather than improving the monitor model.
- **Technical summary:** Identifies 4 recurring monitor failure modes (missed attacks, partial detection, accepting misleading "benign" explanations, poorly calibrated suspicion scores). The hints substantially improve weak monitors at low added compute cost and, per the paper's failure-mode analysis, nearly eliminate complete-miss failures; ablations identify which hint types matter.
- **Why it might matter:** A concrete, low-cost intervention (annotate the transcript, not the model) for agent-oversight monitoring, directly relevant to the already-WAIT `monitor-evidence-path-integrity` and `out-of-band-oversight-enforcement` topics, which track how monitors fail and how to harden them.
- **Evidence of adoption:** None (single preprint).
- **Major organizations using it:** None stated.
- **Open-source implementation:** Not stated.
- **Paper:** https://arxiv.org/abs/2610.34064
- **Code:** Not confirmed.
- **Relationship to existing course material:** `research/deferred/monitor-evidence-path-integrity.md` (WAIT) and `research/deferred/out-of-band-oversight-enforcement.md` (WAIT) — same cluster (agent-monitor reliability); this is a concrete, measured mitigation (provenance/security/effect hints) rather than another failure-mode demonstration.
- **Potential course lesson:** Feeds either pending WAIT topic's evidence list as a defense-side data point.
- **Confidence:** medium (clear failure-mode framing and ablations; single preprint, no independent replication, no code release).
- **Recommendation:** Add to `monitor-evidence-path-integrity.md`'s evidence list at its next scheduled review (2026-12-20).


# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261102-01 · Pre-Crime for Agents, at the Last Second: Probing When a Recruited Agent Gives In

- **Class:** B
- **Date discovered:** 2026-11-02
- **Date published:** 2026-10-29
- **Source:** https://arxiv.org/abs/2610.40588 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Leonidas Raghav (sole listed author; no affiliation stated on the page)
- **Category:** detection/monitoring (adjacent: agent-security)
- **What changed:** A pre-generation (not post-hoc output-filter) detector for an agent about to comply with sustained adversarial peer pressure in a multi-agent setting, probing the model's own activations before each call's output is generated rather than classifying text already produced.
- **Technical summary:** Controlled 6-scenario multi-agent setup: a peer agent pressures a target agent for up to 20 rounds to disclose a secret (e.g. a deploy token); the target typically refuses at first, then gives in. A linear probe reads the target's activations at each model call, before generation, to flag the call that will leak. On held-out Qwen3-32B episodes, at a threshold flagging 5% of benign calls the probe catches 82% of leaking calls vs. 26% for a zero-shot LLM-judge monitor; on gpt-oss-20b, a probe on the reasoning trace reaches AUROC 0.91. The authors' own ablations are candid about limits: the probe substantially confounds "about to disclose" with "violates policy" (it also fires on *permitted* disclosures); a bag-of-words classifier trained on the same labeled calls performs nearly as well, so most of the measured gain comes from the labels rather than from reading activations; and the warning is short-range — halting on every alarm would also stop many benign episodes.
- **Why it might matter:** A structurally different detection point than the course's existing output-filter/after-the-fact monitoring content (pre-generation per-call probing vs. classifying produced text), aimed specifically at multi-agent recruitment/collusion pressure — an area the course already tracks as a gap (see Relationship below) and for which it has no probe-monitoring lesson at all yet.
- **Evidence of adoption:** none — single-author preprint, no code stated, no production use.
- **Major organizations using it:** none.
- **Open-source implementation:** none stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.40588
- **Code:** none
- **Relationship to existing course material:** adjacent to three existing WAIT topics but mechanism-distinct from each — `agent-oversight-evasion` (agents defeat oversight under pressure; this is a detector, not an attack), `multi-agent-covert-collusion` (peer-agent collusion; this is single-target compliance under peer pressure, not steganographic collusion), and `safety-probe-scaling` (activation-probe monitoring, for which the course has no lesson/placement yet — this paper is a second, independent data point for that same gap). New topic in the registry; not previously logged in any daily file (checked `research.py lookup` + repo-wide grep).
- **Potential course lesson:** none yet — would need the same probe-monitoring placement decision already open on `safety-probe-scaling` (likely a module-23 extension once validated).
- **Confidence:** low — single, unaffiliated author; the authors' own ablations show the result is confounded (fires on permitted disclosures) and is barely ahead of a bag-of-words baseline on the same labels; no code; no independent replication; short-range warning limits practical use.
- **Recommendation:** monitor (WAIT if reviewed). Not mature enough to teach alone; worth citing alongside whichever of `agent-oversight-evasion` / `multi-agent-covert-collusion` / `safety-probe-scaling` next comes up for review, but the disclose-vs-violation confound and the weak margin over a bag-of-words baseline need resolving first, and it needs either released code or independent replication.

### C-20261103-01 · The Long Con on the Web: Earn-then-Exploit Fraud Attacks against Coding Agents

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-31
- **Source:** https://arxiv.org/abs/2611.00725 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Xingling Xu, Zhengwei Jiang, Zheng Zhi, Fangming Dong, LingJia Guo, Wei Dong, Chunyan Ma, Jun Jiang (affiliation not stated on the page)
- **Category:** agent-security
- **What changed:** Introduces EtE (Earn-then-Exploit), an attack on web-browsing coding agents distinct from prompt injection, malicious links, or interface deception: a malicious site first gives several rounds of verifiable, genuinely helpful responses, then issues task-related instructions that cross intended boundaries once the agent has built up trust-like reliance on that source.
- **Technical summary:** 56 environments (8 task contexts × 7 attack consequences) tested against 3 production coding agents (Codex-GPT-5.5, ZCode-GLM-5.3-Flash, QwenCode-Qwen3.7-Plus). EtE reaches 71.4% average scene-level ASR (85.7% / 67.9% / 60.7% respectively), beating all injection-based baselines tested. The proposed defense, action-authorization separation (AAS) — web content can never directly authorize a privileged action — cuts ASR to 0% while keeping 100% task completion.
- **Why it might matter:** A mechanism-distinct attack vector (multi-turn trust-building, not single-shot injection) demonstrated against real production coding-agent products, with a matched defense showing a clean 0%-ASR / 100%-utility result.
- **Evidence of adoption:** None — fresh preprint, no stated code release, no production use.
- **Major organizations using it:** None.
- **Open-source implementation:** None stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2611.00725
- **Code:** None
- **Relationship to existing course material:** New. Mechanism-distinct from `coding-agent-repo-poisoning`, `coding-agent-identifier-steering`, `coding-agent-harness-mechanisms` (checked via `research.py lookup`, no match). Nearest taught content is module-17 tool poisoning / Dual-LLM defenses, but this is a *behavioral trust* attack rather than a content-injection one.
- **Potential course lesson:** Module-17 extension (new attack subtype: trust-building before exploitation) once code/replication appears.
- **Confidence:** medium — large structured eval (56 environments × 3 real deployed-style agents) with an internally consistent attack/defense pairing, but single group, no code released, no independent replication.
- **Recommendation:** monitor; review for ADD as a module-17 extension if code or independent replication appears.

### C-20261103-02 · Kerkoporta: Injecting Structured-Output Backdoors in Reasoning Coding Agents

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-29
- **Source:** https://arxiv.org/abs/2611.00138 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Georgios Syros, Blake Bullwinkel, Alina Oprea, Cristina Nita-Rotaru, Amanda Minnich, Xiaodong Liu, Giorgio Severi. Affiliations are not stated on the arXiv page itself; the names read as a Northeastern-University-security-group / Microsoft-AI-red-team-style pairing based on prior public work, but that is unconfirmed from this page and is flagged as such, not asserted.
- **Category:** poisoning/backdoor (agent-security)
- **What changed:** Backdoors targeting *structured tool-call output* in agentic coding harnesses, not chat text: a trigger anywhere in the agent's context makes the model emit an attacker-chosen tool call that the harness then executes, so the damage is an executed action, not just bad text.
- **Technical summary:** Kerkoporta builds poison samples, injects the backdoor via SFT, and recovers lost utility with lightweight RL. Tested on modern, heavily post-trained open-weight models across proprietary and open-source harnesses. ASR up to 96.2%; the backdoor can be scoped to generalize across harnesses or target a single one; poisoned models can *outperform* the clean baseline on standard utility benchmarks, which the authors note gives a victim a reason to adopt them.
- **Why it might matter:** Extends the course's existing backdoor/supply-chain content (modules 13, 21–22) from chat-text damage to arbitrary executed tool-call actions — a higher-stakes backdoor target specific to agentic coding tools.
- **Evidence of adoption:** None — fresh preprint.
- **Major organizations using it:** None confirmed.
- **Open-source implementation:** None stated on the page.
- **Paper:** https://arxiv.org/abs/2611.00138
- **Code:** None stated
- **Relationship to existing course material:** New angle on `backdoor-persistence-and-trigger-variants` (deferred) — checked via lookup, no existing coverage of structured-output/tool-call-specific backdoors; also adjacent to module-22 (weights/adapter supply chain).
- **Potential course lesson:** Module-22 extension — "backdoors that target tool-call structure, not text."
- **Confidence:** medium — strong, clearly reported numbers and a credible-reading author list, but affiliations unconfirmed from the page, single preprint, no code stated, no independent replication.
- **Recommendation:** monitor; weekly review should verify author affiliations directly (institutional pages), which would raise confidence if the apparent pairing is confirmed.

### C-20261103-03 · SecPO: Principled Adversarial Training for Prompt Injection Security

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-30
- **Source:** https://arxiv.org/abs/2610.41998 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Sizhe Chen, Yibo Peng, Jaewon Chang, Chawin Sitawarin, David Wagner — the UC Berkeley StruQ/SecAlign research lineage the course's registry already tracks (affiliation not stated on this page, but this is a continuing, identifiable line of work).
- **Category:** defense/guardrail
- **What changed:** Shows Meta-SecAlign (the strongest defended model in their comparison) still reaches ASR near 100% under adaptive attack, traces this to its DPO training anchoring on an undefended reference model, and proposes an "injection-invariant, utility-preserving oracle" approximated via a new SecPO loss plus an adversarial-training pipeline that synthesizes stronger injections during training.
- **Technical summary:** Adversarial training alone cuts ASR 1.5–14.5x vs. Meta-SecAlign; SecPO vs. plain DPO adds a further 2.4–4.6x. In an agentic AgentDojo test, SecPO+AT Qwen3.6-27B reaches 8.8% ASR vs. 78.8% for Meta-SecAlign under the AttackerMovesSecond attack, with no measurable utility loss across nine benchmarks. Code, training data, and the fine-tuned model are all released: github.com/Sizhe-Chen/SecPO; huggingface.co/datasets/Sizhe-Chen/Qwen3.6-27B-Instruct-SecPO-trainset; huggingface.co/Sizhe-Chen/Qwen3.6-27B-Instruct-SecPO.
- **Why it might matter:** A measured, fully-released defense continuing the same learned-defense research lineage the course already tracks as WAIT (`learned-trust-delimiters`), tested against a real deployed-style baseline (Meta-SecAlign) and an agentic benchmark (AgentDojo), not just a synthetic ASR number.
- **Evidence of adoption:** None in production; the work itself builds directly on a widely-used predecessor (SecAlign/Meta-SecAlign).
- **Major organizations using it:** None stated.
- **Open-source implementation:** github.com/Sizhe-Chen/SecPO (code, data, and model all released).
- **Paper:** https://arxiv.org/abs/2610.41998
- **Code:** github.com/Sizhe-Chen/SecPO
- **Relationship to existing course material:** Extends `learned-trust-delimiters` (deferred) — same general research family as the arXiv 2610.37657 entry already tracked there (learned attention-head trust gates), but a different specific mechanism (adversarial training + a principled oracle loss). Logged as a related, distinct new candidate rather than merged into that file's existing record, since the mechanism differs.
- **Potential course lesson:** Module 17.2 (architectural prompt-injection defenses) or module 23 (defensive engineering) extension; strong lab candidate given the full code/data/model release.
- **Confidence:** medium-high — known, credible research group; full code/data/model release; measured against a real baseline and an agentic benchmark; still a single preprint with no independent reproduction yet and no stated peer-reviewed venue.
- **Recommendation:** review for ADD-track consideration once the weekly review confirms the released code/model reproduce the reported numbers — strongest candidate in today's batch given the full artifact release and its tie to an already-tracked lineage.

### C-20261103-04 · AgentShield: Fortifying Web Applications Against AI Agents and Agentic Browsers

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-30
- **Source:** https://arxiv.org/abs/2610.41181 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Moiz Ali, Nafis Karim, Rownak Islam, Jyotirmay Chauhan, Dhruv Kuchhal, Jason Polakis. "To appear in Proceedings of IEEE Symposium on Security and Privacy (IEEE S&P 2027)" per the page's comments field — a top-tier, peer-reviewed security venue, the strongest formal-review signal in today's batch.
- **Category:** agent-security / defense (inverse threat model: defending infrastructure from agents)
- **What changed:** (a) Shows modern anti-bot defenses largely fail against agentic browsers. (b) Introduces AgentShield, behavioral fingerprinting via progressively-disclosing web forms that targets an agent's perception-reasoning-action loop to distinguish it from a human. (c) Reports "Extinction-induced Policy Drift": an agent repeatedly blocked from completing a task relaxes its own safeguards. (d) Proposes defensive prompt-injection techniques against agents that scrape web content for abuse.
- **Technical summary:** Evaluates modern agentic browsers against existing anti-bot defenses and finds most such defenses fail to detect them. AgentShield's fingerprinting records fine-grained interaction data from dynamic, progressively-disclosing forms to separate agent from human behavior patterns. The Policy Drift effect is measured by repeatedly blocking an agent's task completion and observing its own safeguards relax over successive attempts. Specific quantitative figures (detection rate, drift magnitude) are not reproduced here beyond what the abstract states; the full paper should be read before any course use.
- **Why it might matter:** IEEE S&P acceptance is genuine peer-review validation, unusual among today's finds. The Policy Drift finding — external pressure degrading an agent's own safety behavior — is a new data point adjacent to the course's `agent-oversight-evasion` WAIT topic, but from the opposite direction (pressure causing self-relaxation, not an agent deliberately evading an overseer).
- **Evidence of adoption:** Accepted at IEEE S&P 2027 (peer-reviewed); no production deployment stated.
- **Major organizations using it:** None stated.
- **Open-source implementation:** None stated on the page.
- **Paper:** https://arxiv.org/abs/2610.41181
- **Code:** None stated
- **Relationship to existing course material:** New — "defending a website against AI agents" is the inverse of the course's usual threat model (an agent under attack). Nearest existing content is module-16/17 excessive-agency; the Policy Drift finding is adjacent to `agent-oversight-evasion` (deferred).
- **Potential course lesson:** Possible new angle for a defender's-seat lesson ("hardening a web app against agentic scraping/abuse"); the Policy Drift finding is a citation candidate for `agent-oversight-evasion`'s next review.
- **Confidence:** medium-high on venue strength; medium on direct course fit, since the primary contribution (anti-bot defense for websites) sits adjacent to, rather than squarely inside, the course's current scope.
- **Recommendation:** monitor; weekly review should decide whether "defending infrastructure from agents" belongs in scope, and separately consider citing the Policy Drift finding against `agent-oversight-evasion`.

### C-20261103-05 · Illusion: Safeguarding Topology Confidentiality in LLM Multi-Agent Systems via Behavior-Preserving Obfuscation

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-31
- **Source:** https://arxiv.org/abs/2611.00923 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Yiu-Fai Cheung, Hongzhi Guo, Miao Pan, Irwin King, Hao Wang (affiliation not stated on the page; Irwin King is a recognizable HK-academic ML name, unconfirmed here)
- **Category:** defense/guardrail (multi-agent)
- **What changed:** A defense against an *external observer* reconstructing a multi-agent system's communication topology from its outputs: adds fake edges/messages designed to mislead the reconstruction while preserving benign task output distribution and accuracy.
- **Technical summary:** Lowers an attacker's edge-level F1 from >0.87 to 0.62 and graph similarity from >0.94 to 0.71; fake edges resist similarity-based and LLM-judge filtering, including under adaptive pruning; largely preserves benign output distribution/accuracy.
- **Why it might matter:** The course's existing `multi-agent-topology-leakage` WAIT topic currently tracks only the *information-propagates-via-topology* disclosure problem; this paper is a related but mechanism-distinct concern — hiding the topology graph itself from an external attacker — for which the course has no entry at all. First measured defense this run has found for either framing.
- **Evidence of adoption:** None — single preprint, no stated code.
- **Major organizations using it:** None.
- **Open-source implementation:** None stated.
- **Paper:** https://arxiv.org/abs/2611.00923
- **Code:** None
- **Relationship to existing course material:** Adjacent to, but mechanism-distinct from, `multi-agent-topology-leakage` (deferred: that file is about *disclosure via* topology; this is about *confidentiality of* the topology graph itself). Logged as a new, related topic rather than folded into that file, with the distinction flagged explicitly for the weekly review.
- **Potential course lesson:** Whichever module eventually covers multi-agent topology risk (not yet taught) — this would supply a defense half for a topology-confidentiality angle distinct from the disclosure angle.
- **Confidence:** medium — single preprint, no code, no independent validation, but internally consistent numbers addressing a concrete, well-specified threat model.
- **Recommendation:** monitor; cross-reference at `multi-agent-topology-leakage`'s next scheduled review (2026-11-22) as a related-but-distinct new topic, not a direct update to that file.

### C-20261103-06 · Steering for Safety, Hijacking for Profit: Trojan Threats in the LLM Activation Steering Supply Chain

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-26
- **Source:** https://arxiv.org/abs/2610.35043 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Yu Yan, Jiahao Chen, Siqi Lu, Yongjuan Wang, Ziming Zhao, Zhaoxuan Li, Qingjun Yuan (affiliation not stated on the page)
- **Category:** supply-chain
- **What changed:** Audits 8 real open-source activation-steering plugin libraries and finds weak file-integrity verification, overly broad plugin permissions, and no runtime monitoring. Builds a proof-of-concept malicious plugin (IDH) that performs normally on its advertised task while covertly hijacking outputs (demonstrated with commercial-product-recommendation manipulation), using a routing mechanism and an injection-layer-selection method, while keeping refusal rates on harmful requests high enough to evade naive safety auditing. Proposes a runtime defense that suppresses abnormal activation interventions.
- **Technical summary:** Tested on 5 mainstream LLMs, across 6 brands in 3 commercial domains; ASR up to 97.8% for the hijack goal while the cover function (safety-refusal steering) keeps behaving normally.
- **Why it might matter:** A new supply-chain carrier — activation-steering plugins — distinct from the weights/adapter supply-chain content the course already teaches (module 13); real, audited libraries rather than a purely synthetic setup.
- **Evidence of adoption:** None — single preprint; no stated code release for IDH or the defense.
- **Major organizations using it:** None.
- **Open-source implementation:** None stated.
- **Paper:** https://arxiv.org/abs/2610.35043
- **Code:** None stated
- **Relationship to existing course material:** New. Checked via `research.py lookup`, no existing coverage of activation-steering-plugin supply chain. Module 13 covers weights/adapter supply chain but not steering-vector plugins specifically.
- **Potential course lesson:** Module 13 extension — "activation steering as a supply-chain carrier."
- **Confidence:** medium — real audited libraries and a concrete PoC, but single preprint, no code release stated, no independent validation; submitted 2026-10-26 (older than the usual ~48h window, but newly surfaced by this run only today after the Nov-1/2 API-rate-limit gap; confirmed via `lookup` and grep as not previously logged).
- **Recommendation:** monitor.

### C-20261103-07 · Simple Features Beat Most AI Control Monitors

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-30
- **Source:** https://arxiv.org/abs/2610.41713 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Shubhrangshu Debsarkar, Valmik Nahata (affiliation not stated)
- **Category:** evaluation/benchmark (detection/monitoring)
- **What changed:** On a standard AI-control backdoor-detection benchmark, simple hand-built features that never execute the code beat 20 of 24 open-weight LLM monitors. Attributes this to two label-leakage sources: human-written-honest vs. older-LLM-written-backdoor code style, and differing problem characteristics between what humans vs. LLMs can backdoor. Rebuilds the dataset with backdoors from Claude Sonnet 5 and adds validity checks (≈1 in 7 standard-dataset backdoors fail validity).
- **Technical summary:** Human-vs-backdoor separability drops from 0.95 to 0.79 when backdoors come from Claude Sonnet 5 instead of older models. A Sonnet-5 monitor's apparent catch rate falls from 77%→37% raw (78%→61% validity-filtered) once evaluated on same-generation backdoors. The authors do not claim published monitors actually rely on these shortcuts, only that a high score on the standard dataset is not by itself evidence of sabotage detection. Code and the rebuilt dataset are released: github.com/ShubsDS/authorship-not-sabotage.
- **Why it might matter:** A generalizable methodological critique of AI-control/sabotage-monitor evaluation — an area the course does not currently teach at all (checked via lookup for "AI control", "sabotage" — no match).
- **Evidence of adoption:** Accepted at the EvoRobust workshop, NeurIPS 2026; code released.
- **Major organizations using it:** None stated.
- **Open-source implementation:** github.com/ShubsDS/authorship-not-sabotage
- **Paper:** https://arxiv.org/abs/2610.41713
- **Code:** github.com/ShubsDS/authorship-not-sabotage
- **Relationship to existing course material:** New topic area (AI-control monitor evaluation) for the course. Methodologically adjacent to, but a different specific target than, `jailbreak-asr-judge-variance` and `monitor-evidence-path-integrity` (both deferred, both about evaluation rigor).
- **Potential course lesson:** Module 24 (measuring AI security) extension — "evaluation label leakage" — a second worked example alongside the existing ASR-judge-variance content.
- **Confidence:** medium-high — released code+data, workshop-accepted, a clean and directly reproducible swap-dataset experiment.
- **Recommendation:** review for ADD as a module-24 case study on evaluation-dataset leakage, given the released code and reproducible design.

### C-20261103-08 · Prevented is Not Protected: What Attack Success Rate Hides about RAG

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-29
- **Source:** https://arxiv.org/abs/2610.40742 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Chahana Dahal, Zuobin Xiong (affiliation not stated)
- **Category:** evaluation/benchmark (rag-security)
- **What changed:** Proposes "Aligned RAG Evaluation," a matched clean/poisoned, with/without-defense protocol that separates failures a RAG defense *introduces* from ones it *prevents*, and distinguishes a target merely being mentioned from the model actually endorsing it.
- **Technical summary:** On HotpotQA and Natural Questions, some RAG defenses produce new target-positive answers even while successfully blocking the specific attacks they were measured against, and defense rankings change under this broader evaluation criteria versus plain ASR. Code and evaluation artifacts released: github.com/chxhana/aligned-rag-eval.
- **Why it might matter:** A RAG-specific sibling to the course's existing ASR-measurement-rigor content — `jailbreak-asr-judge-variance` makes essentially the same methodological point on the jailbreak side; this is the RAG-defense-evaluation equivalent.
- **Evidence of adoption:** None — single preprint, no independent validation.
- **Major organizations using it:** None.
- **Open-source implementation:** github.com/chxhana/aligned-rag-eval
- **Paper:** https://arxiv.org/abs/2610.40742
- **Code:** github.com/chxhana/aligned-rag-eval
- **Relationship to existing course material:** Adjacent to module-14/15 (RAG security) and module-24 (ASR measurement rigor); checked via lookup, no existing match for this specific critique.
- **Potential course lesson:** Module-14/15 or module-24 extension — "ASR hides defense side-effects in RAG," a paired example to the existing jailbreak-ASR-variance content.
- **Confidence:** medium — released code and a clear methodology, but a small author pair, single preprint, no stated venue, no independent validation.
- **Recommendation:** monitor; a clean module-24 companion example if the weekly review wants a RAG-specific version of the ASR-rigor lesson.

### C-20261103-09 · Characterizing Recoverable Expert-Utilization Signatures in Fine-Tuned Mixture-of-Experts LLMs

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-29
- **Source:** https://arxiv.org/abs/2610.41039 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Fei Wang, Baochun Li, Bo Li (affiliation not stated on the page; Bo Li is a recognizable adversarial-ML/security name, unconfirmed here as the same person)
- **Category:** extraction/inversion/membership
- **What changed:** New evidence for the course's existing `moe-router-membership-inference` WAIT topic, via a different mechanism than the one already tracked there. Fine-tuned MoE models memorize not just training data but the expert-routing *pathway* used to process it ("structural memorization"); the memorized pathway is recoverable via unconditional generation using only routing information and output logits — no knowledge of the fine-tuning data or procedure required. Standard membership-inference methods miss this; the authors propose composite reference-tail-likelihood metrics, and note the risk compounds where routing data crosses trust boundaries (federated aggregation, multi-tenant monitoring).
- **Technical summary:** Effect appears even with a few fine-tuning samples; strength depends on which modules are trainable (full FT / frozen router / LoRA, mirroring the structure of the existing tracked evidence).
- **Why it might matter:** Strengthens the same general risk area (`moe-router-membership-inference`) the course is already monitoring, from a different specific mechanism, increasing confidence that MoE routing telemetry is a real, recurring side-channel rather than a one-off finding.
- **Evidence of adoption:** None — single preprint, no stated code.
- **Major organizations using it:** None.
- **Open-source implementation:** None stated.
- **Paper:** https://arxiv.org/abs/2610.41039
- **Code:** None stated
- **Relationship to existing course material:** Extends `moe-router-membership-inference` (deferred, status WAIT, next review 2026-11-22). That file's "what would change the decision" asks specifically for code release and independent reproduction of its tracked 2.7–9.4pp TPR@1%FPR effect; this paper does not supply that (different mechanism, different authors, no code), so it should be read as adjacent reinforcing evidence, not the specific reproduction called for.
- **Potential course lesson:** Module 12.1 extension (course already teaches LiRA-style MI), per that file.
- **Confidence:** medium — a credible-reading co-author name, single preprint, no code, not the specific reproduction the existing file's criteria call for.
- **Recommendation:** review alongside `moe-router-membership-inference` at its scheduled 2026-11-22 review as adjacent evidence, clearly distinguished from the reproduction bar that file sets.

### C-20261103-10 · Accept Changes, Reject Attacks: Robust Memory Management for LLM Agents

- **Class:** B
- **Date discovered:** 2026-11-03
- **Date published:** 2026-10-29
- **Source:** https://arxiv.org/abs/2610.41056 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Runze Zhao, Dongruo Zhou, Sumit Kumar Jha, Nathaniel D. Bastian, Ankit Shah (affiliation not stated)
- **Category:** agent-security (defense)
- **What changed:** Defines "robustness" for an agent memory manager as handling both stale-fact updates and memory-poisoning/injected-instruction attacks with a single mechanism — prior work treats these separately because they imply opposite write decisions. Introduces evidence-conditioned accuracy (ECA), a metric checking not just the final answer but whether the records used contain all needed evidence, are up to date, and are attack-free.
- **Technical summary:** Finds existing memory systems and defenses are "no more robust than an untuned manager" on their own test sets under ECA. Proposes a one-shot fine-tuning recipe (trained on episodes built around a single conversation with inserted changes and attacks) that more than doubles the untuned manager's overall ECA across three backbones, while stating "robustness remains incomplete."
- **Why it might matter:** A direct, self-critical finding relevant to the course's recently-ADDed `trust-zoned-agent-memory` lesson (module 16.2, added 2026-11-01): if existing memory defenses generally under-perform on ECA, the weekly review should check whether the taught trust-zoning mechanism was among those tested or is a genuinely different mechanism this paper doesn't speak to.
- **Evidence of adoption:** None — single preprint, no stated code.
- **Major organizations using it:** None.
- **Open-source implementation:** None stated.
- **Paper:** https://arxiv.org/abs/2610.41056
- **Code:** None stated
- **Relationship to existing course material:** Adjacent to the accepted `trust-zoned-agent-memory` topic (module-16/lesson-02) — same general problem (agent memory integrity under both drift and attack) but a different mechanism (a new metric plus unified fine-tuning, vs. trust-zone separation of persistence from authority). Not a duplicate: ECA and the one-shot recipe are new.
- **Potential course lesson:** Module 16.2 citation/extension — a second, metric-driven perspective on agent memory robustness alongside the already-taught trust-zoning defense.
- **Confidence:** medium — single preprint, no code, no independent validation, but a well-specified new metric and an honest negative finding about existing defenses rather than a hyped positive claim.
- **Recommendation:** monitor; flag for the next review touching `trust-zoned-agent-memory` to check whether ECA would also credit the course's taught defense.

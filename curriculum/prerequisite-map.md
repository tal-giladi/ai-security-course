# Prerequisite map — what the LLM Research Engineer course already gives you

This course sits **on top of** the sibling
[**LLM Research Engineer**](https://tal-giladi.github.io/llm-research-engineer-course/) course.
To avoid inferior duplication (`plan.md` §2, §40), this page records what that course already
teaches, and exactly which *security-specific* extension this course adds. When a prerequisite
is "sibling", the lesson links there instead of reteaching it.

Legend: **Have** = taught well in the sibling course, reference it. **Extend** = sibling gives
the foundation, this course adds the security depth. **New** = not in the sibling course.

| Topic | Sibling coverage | Status | Security extension in THIS course |
|---|---|---|---|
| Linear algebra, vector spaces, cosine similarity | M00–M05 | Have | used directly in embedding-space & retrieval attacks (M14) |
| Probability, expectation, distributions | M01 | Have | membership-inference likelihood-ratio test, statistical detection (M12, M24) |
| Information theory: entropy, cross-entropy, KL | M01.3 | Have | information leakage, detector design, DP accounting (M12, M23) |
| Optimization: GD/SGD/Adam, constrained optimization | M02–M03 | Have | adversarial optimization $\arg\max_x L$, PGD projection, GCG (M07, M09–M10) |
| Gradients, backprop, Jacobians/VJPs | M02 | Have | white-box gradient attacks, saliency, GCG coordinate gradients (M07, M09) |
| Tokenization / BPE | M04 | Extend | tokenization-aware injection, encoding/smuggling attacks (M04) |
| Attention, transformer internals | M05–M06 | Extend | instruction-hierarchy attacks, why injection works at the attention level (M02, M04) |
| Generation (greedy/temp/top-k/top-p) | M06.3 | Have | decoding-time attack/defense knobs, output filtering bypasses (M03, M23) |
| Training loop, checkpointing, reproducibility | M07 | Extend | training-data & fine-tuning poisoning, backdoor insertion (M11) |
| Scaling / data engineering | M10–M11 | Have | data-poisoning at scale, contamination as an attack (M11) |
| Evaluation & eval harness | M13 | Extend | security benchmarks, ASR/precision-recall/ROC-AUC, adaptive eval (M24) |
| SFT, chat templates, LoRA/QLoRA | M14 | Extend | malicious fine-tunes, malicious adapters, adapter supply chain (M11, M13) |
| RLHF: reward models, PPO, DPO | M15 | Extend | preference-data poisoning, reward hacking, safety-training limits (M02, M11) |
| Reasoning RL (GRPO/RLVR) | M16–M17 | Have | reward-spec attacks on verifiable-reward pipelines (M11, referenced) |
| Tool use / function calling | M18 | Extend | tool poisoning, malicious tool results, tool authorization (M17) |
| Agents (ReAct, mini SWE-agent) | M19 | Extend | agent hijacking, excessive agency, attack chains, MCP (M16–M19, M21) |
| Embeddings & RAG (build one) | (RAG basics) | Extend | retrieval manipulation, poisoning, ANN/HNSW attack surface, tenant leakage (M14–M15) |
| Classical AppSec (SSRF, injection class, secrets) | — | **New** | Stage 0 (M00–M01) — taught only as deep as AI security needs |
| Threat modeling / trust boundaries | — | **New** | M00 |
| Adversarial ML (FGSM/PGD/CW/AutoAttack, robustness) | — | **New** | Stage 4 (M09–M10) |
| Model extraction / inversion / membership inference | — | **New** | M12 |
| Prompt injection & jailbreaking (as research) | — | **New** | Stages 2–3 (M04–M08) |
| MCP security | — | **New** | M19 |
| Supply-chain: pickle/safetensors, model hubs, deps | — | **New** | M13, M21–M22 |
| Security evaluation methodology & red-team automation | — | **New** | M24–M25 |
| Standards: OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF | — | **New** | M26 + `references/` |

## How lessons reference the sibling course

A lesson's **Prerequisites** block links the specific sibling lesson, e.g.:

> Prerequisites: cosine similarity and ANN retrieval — see
> [LLM Research Engineer 14 · embeddings/RAG]. This lesson does **not** reteach embeddings; it
> assumes you can compute a cosine similarity and reason about nearest-neighbor retrieval, and
> builds the *attack* on top.

If you have not done the sibling course, each such block also names the minimum you must be able
to do (not a full re-teach) to proceed safely.

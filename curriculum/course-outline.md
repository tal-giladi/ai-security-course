# Curriculum map, dependency graph & competency matrix

This course is engineered, not assembled. It moves from **stable security foundations** through
**current LLM/agent attack surfaces** to **fast-moving modules** (MCP, agent frameworks) that
are deliberately isolated so they can be updated without rewriting the core. Read this page
before any lesson to answer *"what must I understand first, and why does this module exist?"*

Design influences (principles extracted, not curricula copied): CMU/Stanford/Berkeley adversarial-ML
and security-engineering courses, SANS red-team progression (recon → exploit → post-exploit →
report), MITRE ATLAS tactic/technique taxonomy, OWASP LLM Top 10 (2025) and OWASP Agentic AI,
NIST AI RMF and NIST AI 100-2 (adversarial ML taxonomy), and the primary research literature.

Layering per `plan.md` §34:

```text
FOUNDATION (stable) ─▶ CURRENT (this year's systems) ─▶ FAST-MOVING (MCP, frameworks, model APIs)
```

---

## The spine

```text
Security foundations ─▶ LLM security foundations (what boundaries actually exist)
        │
        ▼
Prompt injection (direct/indirect/multimodal) ─▶ Jailbreaking (optimization-based)
        │
        ▼
Adversarial ML (FGSM/PGD/CW, transfer) ─▶ Model-level (poisoning, backdoors, extraction, MI)
        │
        ▼
RAG security (retrieval manipulation, poisoning, tenant leakage)
        │
        ▼
Agent security (excessive agency, confused deputy, tool poisoning, attack chains)
        │
        ▼
MCP security ─▶ Multimodal ─▶ Code-agent ─▶ AI supply chain
        │
        ▼
Blue team (defenses + their limits) ─▶ Security evaluation ─▶ Automated red teaming
        │
        ▼
Purple-team synthesis ─▶ Capstones ─▶ Research project
```

Cross-cutting threads present in *every* stage: **mathematics** (optimization, information
theory, statistics), the **defense-guarantee analysis**, and the **purple-team cycle**.

---

## Stages & modules

### Stage 0 — Security foundations (FOUNDATIONAL)
Only as much classical security as AI security requires — no generic pentest course.
- **M00 Threat modeling for AI systems** — assets, trust boundaries, data flows, STRIDE/attack
  trees applied to an LLM app; the confused-deputy pattern; privilege, authn vs authz, isolation.
- **M01 AppSec primitives that AI systems inherit** — injection as a *class*, SSRF, code
  execution, secrets & data exfiltration, supply-chain/dependency attacks, sandboxing.

### Stage 1 — LLM security foundations (FOUNDATIONAL→CURRENT)
- **M02 Where the boundaries really are** — tokenization, context window, attention, the
  system/user/tool message hierarchy, instruction-following as a *statistical* not enforced
  property; training vs inference; what alignment/RLHF/safety-training guarantee and do not.
- **M03 The inference API surface** — streaming, structured output, function/tool calling,
  content filters; where each mechanism can be bypassed.

### Stage 2 — Prompt injection (CURRENT)
- **M04 Direct injection & instruction hierarchy** — delimiter, encoding, obfuscation,
  multilingual, tokenization-aware, instruction smuggling; *why* it works.
- **M05 Indirect injection** — retrieved-document, webpage, email, tool-result injection;
  delayed/persistent execution; the "data becomes instructions" root cause.
- **M06 Multimodal & cross-agent injection** — image/OCR/invisible-text injection, memory
  injection, cross-agent propagation.

### Stage 3 — Jailbreaking as research (CURRENT)
- **M07 Optimization-based jailbreaks** — GCG adversarial suffixes: the $\arg\max_x L$
  formulation, greedy coordinate gradient, transferability, cost/limitations.
- **M08 Automated & black-box jailbreaks** — search/evolutionary (PAIR/TAP-style), gradient-free,
  multi-turn/role attacks, adaptive attacks, automated red teaming.

### Stage 4 — Adversarial machine learning (FOUNDATIONAL, math-heavy)
- **M09 Adversarial examples I** — the perturbation problem, FGSM, PGD, threat models
  ($\ell_\infty/\ell_2$), from-scratch.
- **M10 Adversarial examples II** — CW, AutoAttack, transfer & black-box, robustness &
  certified robustness, adversarial training and its cost.

### Stage 5 — Model-level security (CURRENT, math-heavy)
- **M11 Poisoning & backdoors** — training/fine-tuning/preference-data poisoning, trojans,
  sleeper-agent behavior; detection.
- **M12 Extraction & inversion** — model extraction/stealing, model inversion, membership
  inference (the likelihood-ratio view), training-data memorization & extraction; differential
  privacy as mitigation and what it costs.
- **M13 Adapter & weight supply chain** — malicious LoRA/adapters, pickle/checkpoint risks,
  safetensors.

### Stage 6 — RAG security (CURRENT)
- **M14 Retrieval attack surface** — embeddings/similarity/ANN (HNSW) recap *for attackers*;
  document poisoning, embedding manipulation, ranking/citation manipulation, retrieval DoS.
- **M15 Multi-tenant retrieval** — authorization failures, cross-user/cross-tenant leakage,
  metadata attacks; the poison→retrieve→exploit→defend→retest lab.

### Stage 7 — Agent security (CURRENT, largest stage)
- **M16 The agent attack surface** — loops, planning, memory, external state, permissions,
  credentials; excessive agency & confused deputy formalized.
- **M17 Tool poisoning & abuse** — malicious tool descriptions/results, tool authorization,
  capability-based security, least privilege, approval gates.
- **M18 End-to-end attack chains** — the webpage→browser-agent→injection→tool→credential chain,
  built locally with synthetic canaries, then defended layer by layer and measured.

### Stage 8 — Fast-moving surfaces (EMERGING, modular)
- **M19 MCP security** — architecture (clients/servers/tools/resources/prompts/transports),
  trust boundaries, malicious servers/tools, tool poisoning, confused deputy, capability
  escalation, supply chain; designed to be updated independently.
- **M20 Multimodal security (deep)** — visual adversarial examples, malicious PDFs, steganography,
  audio; multimodal agent attacks.
- **M21 Code-agent security** — malicious repos/READMEs, poisoned dependencies, install/build
  scripts, CI/CD, prompt injection in source, malicious tests/issues/PRs, dependency confusion.
- **M22 AI supply chain** — model hubs, datasets, tokenizer/config files, Docker images,
  inference servers, plugins; compromise *around* the model.

### Stage 9 — Blue team, evaluation, automation (CURRENT)
- **M23 Defensive engineering** — input filtering, output validation, structured output, policy
  enforcement, isolation/sandboxing/network controls, provenance, monitoring/anomaly detection,
  rate limiting, audit logs, incident response — each with its guarantee analysis.
- **M24 Security evaluation** — attack success rate, precision/recall, ROC/AUC, robustness,
  transferability, coverage, regression testing; designing your own benchmarks; adaptive eval.
- **M25 Automated red teaming** — attack generation, mutation/fuzzing, search/optimization,
  attacker/defender models, automated exploit chains.

### Stage 10 — Synthesis
- **M26 Purple-team synthesis & standards** — OWASP LLM Top 10 / MITRE ATLAS / NIST AI RMF
  mapped onto everything built; then the capstones and the research project.

---

## Module dependency table

| Module | Depends on | Layer | Lab area |
|---|---|---|---|
| M00 Threat modeling | — | Foundation | `lab/vulnerable-apps` |
| M01 AppSec primitives | M00 | Foundation | `lab/vulnerable-apps` |
| M02 LLM boundaries | M00 (+ sibling: transformers) | Foundation→Current | `lab/models` |
| M03 Inference API surface | M02 | Current | `lab/vulnerable-apps` |
| M04 Direct injection | M02, M03 | Current | `labs/lab-04` |
| M05 Indirect injection | M04 | Current | `labs/lab-05` |
| M06 Multimodal/cross-agent injection | M05 | Current | `labs/lab-06` |
| M07 Optimization jailbreaks | M02 (+ sibling: gradients/backprop) | Current | `labs/lab-07` |
| M08 Automated/black-box jailbreaks | M07 | Current | `labs/lab-08` |
| M09 Adversarial examples I | sibling: optimization | Foundation | `labs/lab-09` |
| M10 Adversarial examples II | M09 | Foundation | `labs/lab-10` |
| M11 Poisoning & backdoors | sibling: training/SFT | Current | `labs/lab-11` |
| M12 Extraction & inversion | M09, sibling: probability | Current | `labs/lab-12` |
| M13 Adapter/weight supply chain | M11, sibling: LoRA | Current | `labs/lab-13` |
| M14 Retrieval attack surface | sibling: embeddings/RAG | Current | `labs/lab-14` |
| M15 Multi-tenant retrieval | M14, M01 | Current | `labs/lab-15` |
| M16 Agent attack surface | M05, sibling: agents/tools | Current | `labs/lab-16` |
| M17 Tool poisoning & abuse | M16 | Current | `labs/lab-17` |
| M18 End-to-end attack chains | M06, M15, M17 | Current | `labs/lab-18` |
| M19 MCP security | M17 | Emerging | `labs/lab-19` |
| M20 Multimodal (deep) | M06, M10 | Emerging | `labs/lab-20` |
| M21 Code-agent security | M17, M01 | Emerging | `labs/lab-21` |
| M22 AI supply chain | M13, M01 | Emerging | `labs/lab-22` |
| M23 Defensive engineering | M04–M18 | Current | `lab/defense-tools` |
| M24 Security evaluation | M23, sibling: evaluation | Current | `lab/attack-tools` |
| M25 Automated red teaming | M08, M24 | Current | `lab/attack-tools` |
| M26 Synthesis & standards | all | Current | `projects/` |

*"sibling"* = provided by the LLM Research Engineer course; see `prerequisite-map.md`.

---

## Capstones (`projects/`)

1. **Secure a vulnerable LLM application** end to end.
2. **Red-team a RAG application** — poison, exploit, defend, retest.
3. **Red-team an autonomous agent** — build an attack chain against a local agent with synthetic
   canaries; then defend and measure.
4. **Build an AI security evaluation framework** — reusable attack/defense/measurement harness.
5. **Research project** — hypothesis → threat model → related work → attack → experiments →
   measurements → defense → adaptive attack → results → limitations → future work.

---

## Final competency matrix

Filled in as the course is built; each capability is only "done" when every column is true.

| Capability | Theory | Math | Implementation | Attack | Defense | Research | Module/Lab |
|---|---|---|---|---|---|---|---|
| Threat-model an LLM/agent system | ● | – | ● | – | ● | ● | M00–M01 |
| Direct & indirect prompt injection | ● | ● | ● | ● | ● | ● | M04–M06 / L04–06 |
| Optimization-based jailbreaks (GCG) | ● | ● | ● | ● | ● | ● | M07 / L07 |
| Automated & black-box jailbreaks | ● | ● | ● | ● | ● | ● | M08 / L08 |
| Adversarial examples (FGSM/PGD/CW) | ● | ● | ● | ● | ● | ● | M09–M10 / L09–10 |
| Certified robustness | ● | ● | ● | – | ● | ● | M10 / L10 |
| Poisoning & backdoors / sleeper agents | ● | ● | ● | ● | ● | ● | M11 / L11 |
| Model extraction / inversion / MI + DP | ● | ● | ● | ● | ● | ● | M12 / L12 |
| Model & adapter supply chain | ● | ● | ● | ● | ● | ● | M13 / L13 |
| RAG poisoning & retrieval manipulation | ● | ● | ● | ● | ● | ● | M14 / L14 |
| Multi-tenant retrieval leakage | ● | ● | ● | ● | ● | ● | M15 / L15 |
| Agent hijacking / excessive agency | ● | ● | ● | ● | ● | ● | M16 / L16 |
| Tool poisoning & capability security | ● | ● | ● | ● | ● | ● | M17 / L17 |
| End-to-end attack chains | ● | ● | ● | ● | ● | ● | M18 / L18 |
| MCP security | ● | ● | ● | ● | ● | ● | M19 / L19 |
| Multimodal (steg / pixel-space) | ● | ● | ● | ● | ● | ● | M20 / L20 |
| Code-agent & dependency confusion | ● | ● | ● | ● | ● | ● | M21 / L21 |
| AI supply-chain verification | ● | ● | ● | ● | ● | ● | M22 / L22 |
| Defensive engineering | ● | ● | ● | – | ● | ● | M23 / L23 |
| Security evaluation & benchmarking | ● | ● | ● | – | – | ● | M24 / L24 |
| Automated red teaming | ● | ● | ● | ● | ● | ● | M25 / L25 |
| Purple-team synthesis & standards | ● | – | ● | ● | ● | ● | M26 |

Legend: ● = built (lesson + lab where applicable, tests passing). Track your own *confidence* per
capability on `progress/PROGRESS.md`; a column is "yours" only when you could do it unaided on an
unfamiliar system. The five capstones (`projects/capstones.md`) exercise the whole matrix.

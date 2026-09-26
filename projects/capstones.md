# Capstone projects

Five increasingly difficult capstones that turn the course's techniques into demonstrated
capability. Each uses the local lab (`lab/`) — synthetic canaries, local sink, no real systems — and
each must be **measured** with the evaluation harness (`lab/attack-tools/evalkit.py`) and follow the
purple-team cycle: **attack → observe → detect → mitigate → retest → adapt → measure**. A capstone is
complete only when its deliverable includes numbers with confidence intervals and a guarantee box.

Track completion in [`progress/PROGRESS.md`](../PROGRESS.md).

---

## Capstone 1 — Secure a vulnerable LLM application

**Goal.** Take the toy vulnerable app (Lab 04/05 style: a support bot with a system-prompt secret,
retrieval, and a rendering/egress side channel) and harden it end to end.

**Do.**
1. Threat-model it (M00): DFD, assets, trust boundaries, attack trees.
2. Red-team it with a suite spanning direct injection (M04), indirect injection (M05), and multimodal
   carriers (M06); report baseline ASR + CIs (M24).
3. Apply layered defenses (M23): input provenance, enforced output scrubbing, egress allowlist, least
   privilege; re-measure after each layer.
4. Attack your own defenses (M04/M05 bypasses); strengthen; re-measure.

**Deliverable.** Threat model doc; before/after ASR with CIs per attack family; per-defense guarantee
boxes; a CI regression test that fails if ASR rises.

---

## Capstone 2 — Red-team a RAG application

**Goal.** Against a RAG pipeline (Lab 14/15), demonstrate and defend retrieval attacks.

**Do.**
1. Build/extend the RAG lab with a multi-tenant knowledge base.
2. Attacks: document/embedding poisoning + ranking manipulation (M14); cross-tenant retrieval leakage
   (M15); citation manipulation. Measure retrieval-rank shift and exploit ASR.
3. Defenses: provenance allowlist, similarity threshold/reranking, dedup, pre-filter tenant authz;
   re-measure. Bypass the weaker ones (stealthy poison, metadata spoofing); strengthen.

**Deliverable.** Poison suite + rank/ASR measurements with CIs; tenant-isolation proof (a CI test
asserting no cross-tenant retrieval); guarantee boxes; a short "what still gets through" section.

---

## Capstone 3 — Red-team an autonomous agent

**Goal.** Against the agent runtime (Lab 16–19), build a full attack chain and defend it.

**Do.**
1. Configure an agent with tools, credentials (synthetic canary), and untrusted inputs (web/files/
   tools/MCP servers).
2. Build the end-to-end chain (M18): webpage/tool/MCP → injection → tool → credential → exfil to the
   sink. Include a tool-poisoning (M17) and an MCP cross-server (M19) variant.
3. Defend layer by layer (least privilege, egress allowlist, capability scoping, approval gates,
   metadata-as-data); measure **chain depth** and exfil rate at each layer; run **automated**
   exploit-chain red teaming (M25).

**Deliverable.** The chain(s) with a DFD; chain-depth/exfil measurements per defense; the minimal
control set that stops all chains while preserving the task; guarantee box; automated red-team script.

---

## Capstone 4 — Build an AI security evaluation framework

**Goal.** Produce a reusable, packaged evaluation framework (generalizing `evalkit.py` + `redteam.py`).

**Do.**
1. Define an attack-suite schema covering ≥5 families (injection, jailbreak, RAG, agent, privacy).
2. Implement runners that evaluate any target+defense and report ASR+CIs, detector ROC/AUC + base-rate
   precision, robustness curves, transferability, and per-family coverage (M24).
3. Add automated red teaming (M25) and CI regression gating.
4. Document how to add a new attack family and a new defense.

**Deliverable.** A documented framework (code + README) that another engineer can point at a system
and get an honest, covered security report; example reports for the Capstone 1–3 systems.

---

## Capstone 5 — Research project (the real goal)

**Goal.** A small academic-style security research project on a hypothesis you choose (a novel attack,
a novel defense, or a measurement of an under-studied behavior).

**Structure** (`plan.md` §27):

```text
Hypothesis → Threat model → Related work → Attack design → Implementation → Experiments →
Measurements → Defense → Adaptive attack → Results → Limitations → Future work
```

**Requirements.**
- A falsifiable hypothesis and an explicit threat model.
- Reproduce or build on ≥1 paper from `papers/index.md`; situate your work in related work.
- Implement the attack/defense **from scratch** where the mechanism matters (no hiding it behind a
  library); measure with CIs; include an **adaptive** attack against your own defense.
- Everything runs locally against synthetic targets/canaries.

**Deliverable.** A short write-up (the structure above) + runnable code + a reproducibility README.
This is the artifact that demonstrates you can *conduct* AI security research, not just perform its
techniques — the course's central objective.

---

## Grading yourself (competency)

For each capstone, self-assess against the final [competency matrix](../curriculum/course-outline.md)
columns: Theory, Math, Implementation, Attack, Defense, Research, Assessment. A capstone earns a
column only when you could do it again, unaided, on a system you haven't seen.

# Fact-check — Module 35 (iFinder / iTrue case study)

Checked 2026-11-11. Source paper supplied as extracted text; primary-source verification done where
the task required it (CVEs on NVD). Layer: CURRENT. DOCUMENTED unless marked.

## Paper identity
- Title: "Understanding Implicit Trust Errors in Core Carrier Networks through Multi-Agent Flaw
  Discovery and Analysis." Authors: Ziyu Lin, Ziting Wang, Xinfeng Li, Wei Dong, XiaoFeng Wang
  (Nanyang Technological University). Venue: USENIX Security 2026.
- arXiv 2607.10315 (v1 2026-07-11, v2 2026-09-28), CC BY 4.0. [DOCUMENTED — from supplied extract.]
- Artifacts: Zenodo zenodo.org/records/20534406; code github.com/LinZiyuu/iFinder
  (license **NOASSERTION** — NOT a standard OSS license; flagged in lesson); findings site
  linziyuu.github.io/iFinder-Website. Exploit-grade PoCs deliberately withheld by the authors.

## Method (used in lesson)
- LLM multi-agent system on the Claude Agent SDK; all agents + baseline = Claude Opus 4.5;
  known-flaw extraction used Claude Code. Each agent = an LLM session with tools (Grep/Glob/Read +
  build/execute). Grep-based caller search beat AST call-graph analysis.
- Pipeline: Preprocessing (22 known GitHub-issue flaws from Open5GS+free5GC + 3GPP specs → six
  detection patterns; human expert reviewed patterns) → Discovery Agent (backward execution-path
  analysis) → Vetting Agent (code-specification cross-check) → Exploitation Agent (protocol-compliant
  PoC, containerized testbed, refine from logs, capped at 5 iterations).
- Detection pattern = triple <information element, dangerous operation, missing validation>. Six
  families: Malformed Field, Absent Field, Invalid Value, Invalid State, Invalid Reference, Resource
  Exhaustion. Root-cause classes: missing syntactic / semantic / resource-availability validation.

## Numbers (used in lesson; vs 22 ground-truth iTrues)
- iFinder: precision 75.0%, recall 68.2%, F1 71.4% (TP15/FP12/FN7) + 21 new.
- Prompt-only baseline (already fed the patterns): precision 28.2%, F1 31.8%. Unguided LLM = severe
  hallucinations, no usable result.
- Ablation: DA only FP 62 (P 36.7%); DA+VA FP 19 (P 65.5%); DA+VA+EA FP 12 (P 75.0%). Recall 68.2%
  throughout. Valid PoCs 19/22 vs baseline 8/22.
- Cost per implementation ~710 s, ~9.8M tokens (Discovery 280s/2.1M, Vetting 230s/3.3M, Exploitation
  200s/4.4M). No dollar figure. Fuzzing / static analysis NOT compared — lesson does NOT claim
  iFinder beats them.
- Findings: 84 discovered, 83 confirmed, 81 CVEs, 58 fixed at writing. Per target: Open5GS LTE
  30/30/30, Open5GS 5G 10/9/9, free5GC 14/14/12, OAI 5G 11/11/11, OAI LTE 7/7/7, SD-Core 7/7/7,
  eUPF 5/5/5. Protocols: GTP-C 37, PFCP 47.

## CVEs — VERIFIED on NVD 2026-11-11 (WebFetch of NVD REST API)
- **CVE-2026-8233** — REAL. Dotouch XproUPF 2.0.0-release-088aa7c4, UPF component, improper access
  control. CVSS 3.1 **4.6 MEDIUM**, vector `AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L`, published
  2026-05-10. Matches task facts exactly. (Named in the paper; session-hijack fix on one commercial
  vendor.)
- **CVE-2026-8232** — REAL. Dotouch XproUPF 2.0.0-release-088aa7c4, UPF Process / libvlib.so
  vlib_worker_loop, denial of service. CVSS 3.1 **3.5 LOW**, vector
  `AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L`, published 2026-05-10. (Companion DoS; task gave no CVSS —
  now recorded.)
- **CVE-2026-36884** — NOT CITED. Task flagged as non-existent (The Hacker News misprint); not used.
- **CVE-2025-66776** — NOT CITED. Task flagged as non-existent; not used.
- The other ~79 CVEs: real but not individually numbered in the paper — stated as such in the lesson.

## Impacts (lesson describes at root cause + defence only; no attack steps)
- DoS (availability): missing syntactic validation / unbounded allocation / process-ending assert.
  Defence: syntactic validation + bounded allocation with graceful rejection.
- Session hijacking (integrity): missing uniqueness validation of a session rule identifier (PDR ID)
  lets a reused identifier override the legitimate forwarding rule. Defence: enforce the uniqueness
  invariant; reject duplicates.

## 3GPP / standards (domain knowledge; labelled "the governing specs" in lesson)
- TS 29.244 (PFCP / N4), TS 29.274 (GTPv2-C), TS 29.281 (GTP-U), TS 33.210 (NDS/IP, IPsec/mutual
  auth on internal interfaces). Defences: validate every internal-peer message (syntax/semantics/
  resource availability); uniqueness invariants on identifiers; bounded allocation; mTLS/IPsec on
  N4/S5-S8/S11; PFCP association authentication; GTP firewalls (GSMA); zero-trust segmentation;
  continuous cloud-config audit. Governance: vet/sandbox agentic security tools before granting
  testbed/code access.
- Standards-map hooks (for inbox): tool = OWASP agentic ASI02 (tool misuse) + ASI05 (unexpected code
  execution); findings = input/state validation at a trust boundary (LLM01-class discipline applied
  to an internal peer). Related: M25 automated red teaming, M24 evaluation.

## Not independently re-verified (trusted from supplied extract, acceptable as DOCUMENTED)
- arXiv ID/version dates, Zenodo record number, GitHub repo + NOASSERTION license, all count/metric
  tables. If any of these is challenged, re-fetch arxiv.org/abs/2607.10315 and the Zenodo/GitHub
  pages before publication.

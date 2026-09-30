# Standards & frameworks map

Standards are taught as **maps onto real attacks and labs**, never as memorization
(`plan.md` §37). Each row links a framework category to the module and lab where you actually
build the attack and the defense. This page is filled in as modules are built.

```text
Framework category ─▶ Threat ─▶ Concrete vulnerability ─▶ Local vulnerable app ─▶ Attack ─▶ Defense ─▶ Test
```

## OWASP Top 10 for LLM Applications (2025)

| ID | Category | Course module | Lab |
|---|---|---|---|
| LLM01 | Prompt Injection | M04–M06 | lab-04, lab-05, lab-06 |
| LLM02 | Sensitive Information Disclosure | M12, M15 | lab-12, lab-15 |
| LLM03 | Supply Chain | M13, M21–M22 | lab-13, lab-22 |
| LLM04 | Data & Model Poisoning | M11 | lab-11 |
| LLM05 | Improper Output Handling | M03, M23 | lab-04, defense-tools |
| LLM06 | Excessive Agency | M16–M18 | lab-16, lab-18 |
| LLM07 | System Prompt Leakage | M02, M04 | lab-04 |
| LLM08 | Vector & Embedding Weaknesses | M14–M15 | lab-14, lab-15 |
| LLM09 | Misinformation | M14, M24 | lab-14 |
| LLM10 | Unbounded Consumption | M23 | defense-tools |

### OWASP Top 10 for LLM Applications (2026) — crosswalk (added 2026-09-27)

Released 2026-08-03. The 2025 table above is kept as the course was written; lessons cite 2025
IDs. Read them through this crosswalk and write IDs with their year (`LLM08:2026`). Details and
the Hidden Context Exposure lab: [32.1](../lessons/module-32/lesson-01.md).

| 2026 ID | Category | 2025 ID | Course module | Lab |
|---|---|---|---|---|
| LLM01:2026 | Prompt Injection | LLM01 | M04–M06 | module-04, module-05, module-06 |
| LLM02:2026 | Sensitive Information Disclosure | LLM02 | M12, M15 | module-12, module-15 |
| LLM03:2026 | Excessive Agency | LLM06 | M16–M18 | module-16, module-18 |
| LLM04:2026 | Supply Chain | LLM03 | M13, M21–M22 | module-13, module-22 |
| LLM05:2026 | Data & Model Poisoning | LLM04 | M11 | module-11 |
| LLM06:2026 | Unbounded Consumption | LLM10 | M23 | defense-tools |
| LLM07:2026 | Misinformation | LLM09 | M14, M24 | module-14 |
| LLM08:2026 | Hidden Context Exposure (was System Prompt Leakage, broadened) | LLM07 | M02, M04, M14–M18, M32 | module-32 |
| LLM09:2026 | Vector & Embedding Weaknesses | LLM08 | M14–M15, M29 | module-14, module-15, module-29 |
| LLM10:2026 | Improper Output Handling | LLM05 | M02, M23 | module-04, defense-tools |

### OWASP Top 10 for Agentic Applications (2026) — ASI01–ASI10 (added 2026-09-30)

Published 2025-12-09 by the OWASP GenAI Security Project, peer-reviewed by 100+ practitioners. It
does **not** replace the LLM list: the LLM risks do not disappear when you add an agent, they are
amplified by everything the agent can reach. Use the LLM list for a chatbot or RAG pipeline with no
tools and no multi-agent coordination; layer this list on the moment the system starts **planning
and acting**.

The organising principle of the whole list is **least agency**: autonomy is earned, not the
default. That is the same conclusion modules 16 and 23 reach from first principles, which is the
point of reading them side by side.

| ID | Agentic risk | LLM-list analogue | Course module | Lab |
|---|---|---|---|---|
| **ASI01** | **Agent Goal Hijack** — content the agent reads alters its objectives or decision logic | LLM01:2026 | M05, M16, M28 | module-05, module-16, module-28 |
| **ASI02** | **Tool Misuse & Exploitation** — legitimate tools used unsafely: chaining a harmless tool into a sensitive API, forwarding unvalidated output into a command | LLM03:2026 | M16, M17, M18 | module-16, module-17 |
| **ASI03** | **Identity & Privilege Abuse** — the agent runs with more permission than it needs, borrowing a user session or a shared key | LLM03:2026 | M16, M28 | module-16, module-28 |
| **ASI04** | **Agentic Supply Chain Vulnerabilities** — orchestration frameworks, tool integrations and MCP servers you do not control | LLM04:2026 | M13, M19, M22 | module-13, module-19, module-22 |
| **ASI05** | **Unexpected Code Execution** — untrusted content reaches an execution path (code interpreter, shell, generated code) | LLM10:2026 | M01, M21, M30 | module-21, module-30 |
| **ASI06** | **Memory & Context Poisoning** — the agent's durable state is written with attacker-chosen content | LLM05:2026 | M16.2, M29 | module-16, module-29 |
| **ASI07** | **Insecure Inter-Agent Communication** — agents trust messages, identities and results from peers | — | M28 | module-28 |
| **ASI08** | **Excessive Agency** — more autonomy than the task requires; no least-agency boundary | LLM03:2026 | M16, M18, M23 | module-16, module-18 |
| **ASI09** | **Human-Trust Exploitation** — the agent manipulates what a human approves, by reframing or hiding the consequence | LLM03:2026 | M16, M18, M31 | module-18, module-31 |
| **ASI10** | **Rogue Agents** — the agent pursues goals outside its intended scope | LLM06:2026 | M18, M25, M31 | module-31 |

> [!NOTE]
> **Two things this list adds that the LLM list has no room for.** ASI07 is a *new surface*: in a
> multi-agent system the peer is a component you did not deploy, and trusting its output is trusting
> whoever can influence it — module 28. ASI09 is a *new defender*: a human-in-the-loop approval gate
> is only as strong as the agent's ability to describe what it is about to do, and a persuasive
> agent can get a human to approve the wrong thing. Module 16 treats approval gates as an enforced
> control; read that section again through ASI09 before you believe one.

> [!IMPORTANT]
> **What the mapping is and is not.** This crosswalk is a teaching aid: it says *where in the course
> each risk is covered*, not that a lab proves the risk is handled. ASI05, ASI07 and ASI09 in
> particular are covered as attack surface and defensive reasoning rather than as a single
> end-to-end lab — ASI07 by the A2A trust-graph work in module 28, ASI09 by the approval-gate
> guarantee analysis in modules 16 and 18. If you are reporting against the Agentic Top 10, a
> crosswalk row is a pointer to your own evidence, not the evidence.


## MITRE ATLAS

| ATLAS tactic | Course module(s) | Lab |
|---|---|---|
| Reconnaissance / Resource Development | M00 (surface mapping, threat model), M27 (recon for AI targets) | module-27 |
| ML Model Access | M02, M12 (extraction), M29 (embedding inversion) | module-12, module-29 |
| Initial Access / Execution (via prompts) | M04–M06 (injection) | module-04, module-05, module-06 |
| ML Attack Staging (evasion/optimization) | M07–M10 (jailbreak, adversarial ML) | module-07 – module-10 |
| Poison Training Data | M11 | module-11 |
| Exfiltration | M05, M12, M18 (confused-deputy chains, MI) | module-05, module-12, module-18 |
| ML Supply Chain Compromise | M13, M19, M21, M22 | module-13, module-19, module-21, module-22 |
| Persistence | M16.2 (memory poisoning), M11 (backdoors) | module-16, module-11 |
| Discovery of AI capabilities | M27 (fingerprinting, stack enumeration) | module-27 |
| Impact / Defenses | M23 (blue team), M24 (evaluation), M25 (red team) | module-23 – module-25 |

Use ATLAS technique IDs when reporting findings to a security team; each lab reproduces the
technique locally so the mapping is concrete, not nominal.

> [!NOTE]
> **Agentic gap.** ATLAS's original matrix predates tool-using agents, so several behaviours the
> course teaches have no first-class technique yet — an agent erasing its own execution trace,
> silently out-of-scope actions under ordinary task pressure, or two independently hosted agents
> agreeing on a covert channel. ATLAS keeps adding agentic techniques; the mappings above are dated
> 2026-09-30. When you report one of these, name the behaviour explicitly rather than forcing a
> poor fit onto an existing technique ID.


## NIST

- **NIST AI RMF (AI 100-1)** — govern/map/measure/manage, mapped to the course's
  understand→attack→defend→measure cycle (M26).
- **NIST AI 100-2 (Adversarial ML taxonomy)** — evasion (M04–M10), poisoning (M11), privacy
  (M12), abuse (M04–M08); measured with M24.

| NIST AI RMF function | How the course realizes it |
|---|---|
| **Govern** | policy/authorization design, least privilege, guarantee-analysis discipline (M16, M23) |
| **Map** | threat modeling, DFDs, attack surface enumeration (M00–M01) |
| **Measure** | ASR+CIs, ROC/AUC, robustness, coverage, adaptive evaluation (M24), automated red teaming (M25) |
| **Manage** | enforced controls, monitoring, audit, incident response (M23); CI regression gating (M24–M25) |

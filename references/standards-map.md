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
the Hidden Context Exposure lab: [F.1](../lessons/frontier/update-01.md).

| 2026 ID | Category | 2025 ID | Course module | Lab |
|---|---|---|---|---|
| LLM01:2026 | Prompt Injection | LLM01 | M04–M06 | lab-04, lab-05, lab-06 |
| LLM02:2026 | Sensitive Information Disclosure | LLM02 | M12, M15 | lab-12, lab-15 |
| LLM03:2026 | Excessive Agency | LLM06 | M16–M18 | lab-16, lab-18 |
| LLM04:2026 | Supply Chain | LLM03 | M13, M21–M22 | lab-13, lab-22 |
| LLM05:2026 | Data & Model Poisoning | LLM04 | M11 | lab-11 |
| LLM06:2026 | Unbounded Consumption | LLM10 | M23 | defense-tools |
| LLM07:2026 | Misinformation | LLM09 | M14, M24 | lab-14 |
| LLM08:2026 | Hidden Context Exposure (was System Prompt Leakage, broadened) | LLM07 | M02, M04, M14–M18, F.1 | lab-04 |
| LLM09:2026 | Vector & Embedding Weaknesses | LLM08 | M14–M15 | lab-14, lab-15 |
| LLM10:2026 | Improper Output Handling | LLM05 | M03, M23 | lab-04, defense-tools |

## MITRE ATLAS

| ATLAS tactic | Course module(s) | Lab |
|---|---|---|
| Reconnaissance / Resource Development | M00 (surface mapping, threat model) | — |
| ML Model Access | M02–M03, M12 (extraction) | lab-12 |
| Initial Access / Execution (via prompts) | M04–M06 (injection) | lab-04–06 |
| ML Attack Staging (evasion/optimization) | M07–M10 (jailbreak, adversarial ML) | lab-07–10 |
| Poison Training Data | M11 | lab-11 |
| Exfiltration | M05, M12, M18 (confused-deputy chains, MI) | lab-05, lab-12, lab-18 |
| ML Supply Chain Compromise | M13, M21, M22 | lab-13, lab-21, lab-22 |
| Persistence | M18 (memory poisoning), M11 (backdoors) | lab-18, lab-11 |
| Impact / Defenses | M23 (blue team), M24 (evaluation), M25 (red team) | lab-23–25 |

Use ATLAS technique IDs when reporting findings to a security team; each lab reproduces the
technique locally so the mapping is concrete, not nominal.

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

## Weekly-review additions

Rows added by the weekly curriculum review (`research/`); existing tables above are unchanged.

| Framework category | Course lesson | Lab | Added |
|---|---|---|---|
| OWASP LLM01:2026 Prompt Injection / LLM03:2026 Excessive Agency — architectural (by-design) mitigation: plan isolation, capability flow control, per-branch bounds for computer-use agents | [17.2](../lessons/module-17/lesson-02.md) | lab-33 | 2026-10-11 |
| OWASP LLM04:2026 Supply Chain / LLM03:2026 Excessive Agency — agent skills as a supply-chain trust boundary: authentic-but-unsafe skills (prose / cache≠source / under-declared capability / cross-skill artifact); scanner + checked-hash loading + capability enforcement + cross-skill provenance | [22.2](../lessons/module-22/lesson-02.md) | lab-34 | 2026-10-18 |
| MITRE ATT&CK v20 T1698/T1699 Prompt Injection → T1700 AI-Enabled Exfiltration (+ T1608.007 AI Result Poisoning) — mapping findings to ATT&CK; DET0927-style correlation analytic vs adaptive exfiltration; provenance hardening and its FP cost | [F.2](../lessons/frontier/update-02.md) | lab-35 | 2026-10-25 |

## MITRE ATT&CK v20 — AI techniques (added 2026-10-25)

ATT&CK v20 (released 2026-10-13) added Enterprise techniques that name AI behavior directly. The
ATLAS table above is unchanged; use ATT&CK IDs when a finding goes to a SOC, ATLAS IDs for the
AI-specific technique, OWASP 2026 IDs for the weakness. Details, detection lab and guarantee boxes:
[F.2](../lessons/frontier/update-02.md). IDs verified on attack.mitre.org, 2026-10-25.

| ATT&CK ID | Name | Tactic | ATLAS | OWASP 2026 | Course lesson | Lab | Detection strategy in ATT&CK |
|---|---|---|---|---|---|---|---|
| T1699 | Direct Prompt Injection | Execution | AML.T0051.000 | LLM01:2026 | 04.1 | lab-04 | none listed |
| T1698 | Indirect Prompt Injection | Execution | AML.T0051.001 | LLM01:2026 | 05.1, 06.1 | lab-05, lab-06 | none listed |
| T1700 | AI-Enabled Exfiltration | Exfiltration | — | LLM02:2026, LLM03:2026 | 05.1 (+ ext.), 18.1, F.2 | lab-05, lab-18, lab-32, lab-35 | DET0927 |
| T1608.007 | Stage Capabilities: AI Result Poisoning | Resource Development | — | LLM07:2026 | 14.1 (by analogy), F.2 | — | DET0922 (no target-side analytic) |

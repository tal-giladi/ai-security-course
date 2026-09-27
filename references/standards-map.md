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

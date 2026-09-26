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

## MITRE ATLAS

Tactics/techniques (reconnaissance, resource development, initial access, ML model access,
execution, persistence, exfiltration, impact) mapped to modules. Table added in M26.

## NIST

- **NIST AI RMF (AI 100-1)** — govern/map/measure/manage, mapped to the course's
  understand→attack→defend→measure cycle (M26).
- **NIST AI 100-2 (Adversarial ML taxonomy)** — evasion, poisoning, privacy, abuse; aligns with
  Stages 4–5 (M09–M13) and M24.

*(Verified links added alongside each module as it is written.)*

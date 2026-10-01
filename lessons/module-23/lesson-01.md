---
id: "23.1"
module: 23
minutes: 10
practice_minutes: 120
prerequisites: ["02.1", "02.2", "16.1", "18.1"]
objectives:
  - "Catalog the defensive controls and classify each as **enforced** (complete for scope) or **probabilistic** (detector with FP/FN)."
  - "Apply the **guarantee analysis** (stops / doesn't stop / adapts / FP cost / perf cost) to each."
  - "**Compose** controls in the right order and **measure** ASR, FPR, and detector precision/recall."
  - "Explain why enforced controls (scrubbing, egress allowlist, least privilege, sandboxing) carry the security weight, and detectors/monitoring provide depth and forensics."
  - "Reason about **base rates** (M02.2) when interpreting detector precision in production."
volatility: concept
sources:
  - title: "NIST AI RMF (AI 100-1) — govern, map, measure, manage"
    url: https://www.nist.gov/itl/ai-risk-management-framework
  - title: "Jain et al. — Baseline Defenses for Adversarial Attacks Against Machine Learning"
    url: https://arxiv.org/abs/1906.06070
  - title: "OWASP Top 10 for Agentic Applications 2026 — least agency"
    url: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
last_verified: "2026-09-30"
---
---
# 23.1 · Defensive engineering

This is the blue-team synthesis. Every earlier module ended with a guarantee-analysis box for one defense; here you assemble them into a pipeline and confront the recurring truth: **no defense is magic, enforced beats probabilistic, and a filter that blocks users is not a win.** Measuring the trade-offs is the job.

## Why this matters

Attackers only need one path; defenders must reason about all of them, at acceptable cost. The
temptation is to "add a filter" for each attack — but filters have false positives (blocking users)
and false negatives (missed attacks), and stacking them can degrade the product while giving a false
sense of safety. Good defensive engineering distinguishes controls that *guarantee* something (in
code, complete for their scope) from those that *reduce risk probabilistically*, composes them
deliberately, and measures the result.

## Learning objectives

1. Catalog the defensive controls and classify each as **enforced** (complete for scope) or
   **probabilistic** (detector with FP/FN).
2. Apply the **guarantee analysis** (stops / doesn't stop / adapts / FP cost / perf cost) to each.
3. **Compose** controls in the right order and **measure** ASR, FPR, and detector precision/recall.
4. Explain why enforced controls (scrubbing, egress allowlist, least privilege, sandboxing) carry the
   security weight, and detectors/monitoring provide depth and forensics.
5. Reason about **base rates** (M02.2) when interpreting detector precision in production.

## Concept

### Two kinds of control

- **Enforced** (deterministic code, complete for a defined scope): output secret-scrubbing, egress
  allowlists, tool/least-privilege policy, sandboxing/isolation, structured-output *validation* (not
  the model's JSON, your check), rate limiting, authorization. These give a *guarantee within scope*
  and hold under a fully compromised model (02.1). They have essentially **zero false positives** when
  scoped correctly (an allowlist doesn't block legitimate allowlisted traffic).
- **Probabilistic** (classifiers): input jailbreak/PII detectors, output moderation, anomaly
  detection. These have both **false negatives** (evadable — encoding/paraphrase, M07/M08) and
  **false positives** (blocking benign traffic). They *reduce* risk and provide *signal*, but are not
  boundaries.

### The catalog (map to modules)

| Control | Type | Stops (scope) | Key limit |
|---|---|---|---|
| Input filtering/detection | probabilistic | recognized attack strings | evadable + FP (M07/08) |
| Output validation/scrubbing | enforced (for the pattern) | literal secret/PII leaving | misses transformed forms (M04) |
| Structured-output validation | enforced | malformed/ill-typed values *you* check | not semantic safety (M02.2) |
| Policy/authorization | enforced | unauthorized tool/data access | over-broad scopes (M16/M15) |
| Isolation/sandboxing | enforced | code-exec blast radius, egress | within-scope abuse (M21) |
| Egress/network controls | enforced | exfil to non-allowlisted hosts | allowlisted-host abuse (M05/18) |
| Provenance/signing | enforced | tampered/untrusted artifacts | signed-but-malicious (M13/22) |
| Monitoring/anomaly detection | probabilistic | detects, doesn't prevent | FP/FN; base rate (M24) |
| Rate limiting | enforced | abuse/DoS/cost; slows automation | legit bursts (tune) |
| Audit logging | forensic | nothing (enables IR) | must be complete & tamper-resistant |

### Composition & measurement

Order: cheap **enforced** checks first (rate limit, authz, egress), **detectors** as depth, **audit**
always. Then measure on realistic traffic (attacks + benign): **ASR** (attacks that get through),
**FPR** (benign blocked), and detector **precision/recall**. Lab result: enforced scrubber+egress
drive ASR 1.0→0.0 with FPR 0; adding the keyword detector raises recall but introduces FP (0.25) and
drops precision — a concrete demonstration that "add another filter" has a cost.

## Intuition

Defending is building a house, not buying one gadget. A deadbolt (enforced: egress allowlist) either
locks or it doesn't — and it never refuses to let *you* in. A motion sensor (probabilistic detector)
catches some intruders but also trips on the cat (false positive) and misses the careful burglar
(false negative). You build the house on deadbolts and reinforced doors (enforced controls, least
privilege, sandboxing) and *add* sensors and cameras (detection, audit) for depth and forensics — you
don't replace the locks with more sensitive motion sensors and call it secure. And you check that your
sensors don't page you every time the cat moves (measure the FP cost).

## Mathematics

**Precision under base rates (from M02.2, now decisive).** A detector with recall $t$ and
false-positive rate $f$, at attack prevalence $\pi$, has precision
$$ \text{PPV} = \frac{t\pi}{t\pi + f(1-\pi)}. $$
In production, attacks are rare ($\pi$ small), so even a good detector's *alerts* are mostly false —
which is why detectors feed triage/monitoring, not hard blocking, and why enforced controls (whose
"precision" is 1 by construction within scope) carry the security weight. **Compute this for your
detector at your real $\pi$ before you let it block traffic.**

**Defense-in-depth math (M18).** Enforced control on a hop → $p_{\text{hop}}=0$ (chain broken).
Stacked probabilistic filters → residual $\prod q_i$ (shrinks, never zero). So: one enforced control
beats many filters on the same hop; use filters where no enforced control exists, and measure the
cumulative FP cost ($1-\prod(1-\text{fp}_i)$ grows as you stack).

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — the composed defense pipeline (meta-analysis).**
> - **Stops:** everything each *enforced* control covers within its scope (secret scrubbing, egress,
>   authz, sandbox, rate limit), *plus* a fraction (detector recall) of recognized attacks — with the
>   audit log enabling detection/IR of the rest.
> - **Does NOT stop:** attacks entirely within enforced scopes (allowlisted-host exfil, within-privilege
>   misuse), detector-evading variants (encoding/paraphrase), or novel attacks no control covers.
> - **Attacker adapts:** operate within allowed capabilities/hosts; evade detectors; find an uncovered
>   path — so monitoring + IR matter for the residual.
> - **FP cost:** enforced controls ~0 within scope; detectors add FP that compounds as you stack —
>   measure and bound it (user impact).
> - **Perf cost:** enforced checks are cheap; LLM-based detectors add latency/second model calls.
> - **Takeaway:** build on enforced controls (least privilege, egress, scrubbing, sandboxing, authz),
>   add detectors/monitoring for depth and forensics, log everything, and **measure ASR *and* FPR** —
>   a defense is only real if it stops attacks without blocking users, and you can only know that by
>   measuring (Module 24).

## Code

`lab/defense-tools/defenses.py` provides the toolkit; `labs/module-23/measure_defenses.py` composes a
`Pipeline` and evaluates configurations, printing ASR/FPR/precision/recall as layers are added. Read
how each control declares its scope, and how the pipeline orders enforced checks before the detector
and records every decision to the `AuditLog`.

## Practical lab

**Lab 23** ([`labs/module-23/`](../../labs/module-23/README.md)) — compose the toolkit into a pipeline and
measure each layer. Offline.

```bash
py labs/module-23/measure_defenses.py
py -m pytest labs/module-23 -q
```

## Exercise

1. **Guarantee boxes.** Write the stops/doesn't-stop/adapt/FP/perf box for each toolkit control from
   first principles; verify your claims against the lab (e.g., show the scrubber misses an
   encoded secret, the egress allowlist catches it).
2. **Detector ROC.** Sweep the detector threshold; plot FPR vs FNR (the ROC) on the traffic; pick an
   operating point and justify it. Show there is no threshold with both zero FP and zero FN.
3. **Base-rate reality.** Assume attack prevalence $\pi=0.5\%$; compute the detector's production
   precision with the PPV formula. Interpret: should it block, or only alert? 
4. **Structured-output validation.** Add a control that validates the model's tool-call arguments
   against a schema *and* your semantic rules (path scoping, URL allowlist); show it blocks a
   schema-valid-but-malicious value (M02.2) — an enforced control the detector can't provide.
5. **Anomaly detection + IR.** Add a simple anomaly detector over the audit log (e.g., a spike in
   `output_blocked` from one identity); show it surfaces an ongoing attack, and write a short incident-
   response runbook (contain → eradicate → recover → learn) for a confirmed exfiltration.
6. **Compose & measure the whole thing.** Assemble your best pipeline; report ASR, FPR, and per-control
   contribution; write the composed guarantee box. State honestly what still gets through.

<details><summary>Hint (step 3)</summary>

With $t=0.9$, $f=0.05$, $\pi=0.005$: $\text{PPV}=\frac{0.9\cdot0.005}{0.9\cdot0.005+0.05\cdot0.995}
\approx 0.083$ — over 90% of alerts are false. So this detector should *alert/triage*, not hard-block;
hard blocking at that FP rate degrades the product. Enforced controls (PPV = 1 within scope) do the
blocking.

</details>

**Deliverable.** Per-control guarantee boxes verified against the lab, the detector ROC + operating
point, the base-rate precision computation, the structured-output validator, the anomaly detector + IR
runbook, and the composed pipeline's measured ASR/FPR + guarantee box.

## Research paper

**NIST AI RMF (AI 100-1)** (govern/map/measure/manage) + **Jain et al., "Baseline Defenses" (2023)**
+ **OWASP LLM defensive guidance**. *Why:* RMF frames defense as a measured, managed process (not a
gadget); Jain evaluates concrete LLM defenses and their limits; OWASP maps controls to the Top 10.
*Read:* RMF's measure/manage functions; Jain's finding that simple defenses help but adaptive attacks
persist (M07). *Reproduce:* the lab is the measurement harness; add one Jain defense (paraphrase/
retokenize) and measure its ASR reduction and FP cost. *Limits:* defenses are evaluated against
*known* attacks — the adaptive-attack caveat (M07/M10) applies to every probabilistic control.

## Further reading

- Microsoft/Google/Anthropic production LLM-safety engineering writeups; NIST SSDF;
  [`references/standards-map.md`](../../references/standards-map.md). Bridge to M24 (evaluation).

## What you should now be able to do

- Catalog defensive controls and classify each as enforced or probabilistic with a guarantee analysis.
- Compose controls in the right order (enforced first, detectors as depth, audit always) and measure
  ASR, FPR, and precision/recall.
- Apply base-rate reasoning to decide when a detector should block vs alert.
- Explain why enforced controls carry the security weight and detectors/monitoring provide depth and
  forensics.
# Lab 23 — Defensive engineering: compose & measure defenses

**Module:** 23 (Stage 9 · blue team). **Time:** ~2 h. **Hardware:** CPU, offline. Uses the reusable
toolkit `lab/defense-tools/defenses.py`.

## Goal

Assemble a defense **pipeline** from reusable, honestly-characterized controls and **measure** each
layer on real traffic: attack success rate (ASR), false-positive rate (FPR) on benign traffic, and
the detector's precision/recall. The discipline: compose **enforced** controls (complete for their
scope, zero FP) with **probabilistic** detectors (recall, but FP cost), and *measure* — don't just
stack filters.

## Run

```bash
py labs/lab-23/measure_defenses.py    # ASR 1.0 -> 0.25 (scrubber) -> 0.0 (egress) ; detector adds recall + FPR
py -m pytest labs/lab-23 -q
```

## The toolkit (`lab/defense-tools/defenses.py`)

- **Enforced (complete for scope, no FP):** `output_secret_scrubber` (literal secret can't leave),
  `egress_allowed` (host allowlist), `RateLimiter` (abuse/DoS/cost).
- **Probabilistic (recall + FP/FN):** `jailbreak_score`/`is_flagged` (keyword detector — evadable and
  FP-prone).
- **Forensics:** `AuditLog` (doesn't stop attacks; enables detection & incident response).
- **`Pipeline`** composes them in order (cheap enforced first, detectors as depth, audit always).

## What to notice

- **Enforced controls drove ASR to 0 with FPR 0.** The scrubber blocks literal-secret leaks; the
  egress allowlist blocks exfil the scrubber missed — complete for their scope, no benign impact.
- **The detector adds recall but costs false positives** (FPR 0.25, precision 0.75): a benign message
  containing "ignore previous"/"developer mode" gets blocked. *Measure the FP cost before deploying.*
- **No defense is magic.** Each has a guarantee-analysis (stops/misses/adapt/FP/perf) — the recurring
  discipline of the whole course.

## Exercise

See [Lesson 23.1](../../lessons/module-23/lesson-01.md): add structured-output validation and a
semantic detector; sweep the detector threshold to trace its ROC (FP vs FN); add anomaly detection on
the audit log; compute the base-rate-adjusted precision (M02.2 Bayes) at a realistic attack
prevalence; write the guarantee box for each control and the composed pipeline.

## Reset / Docker

Stateless. `docker compose up` runs the measurement with no egress.

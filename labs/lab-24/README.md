# Lab 24 — Security evaluation: measure defenses honestly

**Module:** 24 (Stage 9). **Time:** ~2 h. **Hardware:** CPU, offline (shim). Uses the reusable
harness `lab/attack-tools/evalkit.py`.

## Goal

Turn "it seems secure" into a defensible measurement. Compute **attack success rate (ASR) with a
Wilson confidence interval**, **detector precision/recall/ROC-AUC**, and — the key lesson — do
**adaptive evaluation**: measure against the *strongest/adapted* attack, because reporting only a
weak suite overstates security.

## Run

```bash
py labs/lab-24/evaluate.py    # ORIGINAL suite ASR 0.00 vs ADAPTED 1.00 (CIs non-overlapping); detector ROC-AUC
py -m pytest labs/lab-24 -q
```

## The harness (`lab/attack-tools/evalkit.py`)

- `wilson_interval`/`asr` — proportions with 95% CIs (never report ASR without one).
- `roc_auc`, `precision_recall` — detector metrics (tie-averaged AUC).
- `required_n` — sample size to resolve a given ASR difference.
- `Benchmark.run/compare` — evaluate a defense against a suite; `compare` flags whether a difference
  is *established* (non-overlapping CIs) — guards against noise-driven conclusions.

## What to notice

- **Adaptive evaluation is decisive.** The same defended bot shows ASR 0.00 on weak prompts and 1.00
  on authority-framed ones — evaluating only the weak suite would certify a broken system.
- **Always report CIs.** With n=20 you can distinguish 0.0 from 1.0, but resolving a 0.1 difference
  needs ~193 samples per condition — small suites show direction, not fine differences.
- **Base rates gate detector precision** (M02.2): a great lab AUC doesn't mean great production
  precision at low attack prevalence.

## Exercise

See [Lesson 24.1](../../lessons/module-24/lesson-01.md): design your own security benchmark (coverage
across attack families); compute transferability (attack tuned on one model vs another); plot the
detector ROC and pick an operating point; add regression tests that fail if ASR rises; measure
robustness as ASR vs attack strength; write the guarantee box for your evaluation methodology.

## Reset / Docker

Stateless. `docker compose up` runs the evaluation with no egress.

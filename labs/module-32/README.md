# Lab 32 — Hidden Context Exposure (OWASP LLM08:2026)

**Lesson:** [32.1 · OWASP LLM Top 10 2026: the crosswalk & Hidden Context Exposure](../../lessons/module-32/lesson-01.md).
**Time:** ~60 min. **Hardware:** CPU-only, stdlib only, offline, runs in < 1 s. **Targets:** local
only; synthetic `LAB-CANARY-*` markers; no network.

## Goal

Measure leakage **per context slot** (system, developer, tool schema, retrieved document, memory,
credential), compare three output filters against the one architectural control that is enforced
(the credential is held by the executor and never enters the context), and relabel 2025 OWASP IDs
to 2026.

The point of the per-slot measurement is that "System Prompt Leakage" was the wrong name: once you
count slots you see that retrieved policies, tool schemas and memory leak by the same mechanism,
which is why the 2026 list renamed the category **Hidden Context Exposure**.

## Files

- `app.py` — the vulnerable `SupportApp`: five canary-tagged slots, a deterministic toy model, the
  literal / normalize / keyword filters and the `credential_in_context=False` mode.
- `attack.py` — 7 probes (dump, tools, documents, memory, dashes, backwards, ROT13), 4 benign
  queries, decode-aware scoring, the slot × config matrix with ASR (Wilson CI) and FPR.
- `crosswalk.py` — the OWASP LLM Top 10 2025 → 2026 map and `relabel()`.
- `test_lab26.py` — acceptance tests: each defense does exactly what its guarantee box says.

## Run

```bash
py labs/module-32/attack.py
py labs/module-32/crosswalk.py "found LLM07 and LLM06:2025"
py -m pytest labs/module-32 -q
```

Expected: `none` leaks every column; every filter still leaks the credential (ROT13); `keyword`
has FPR 0.25; `out_of_context` has a clean credential column with no filter at all, while every
slot left in context still leaks.

## Docker (optional)

```bash
cd labs/module-32 && docker compose up
```

## Exercise

See lesson 32.1 → **Exercise**: the base64 rung of the encoding ladder, the architectural
mitigation, and standards hygiene over the course's own lessons.

If you want to try the reporting tool under an older ID, `crosswalk.py "found LLM07"` is the
fastest way to see why quoting an ID without its year is a real failure mode rather than pedantry.

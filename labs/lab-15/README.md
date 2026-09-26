# Lab 15 — Multi-tenant retrieval: authorization failures & cross-tenant leakage

**Module:** 15 (Stage 6). **Time:** ~90 min. **Hardware:** CPU, numpy, offline. **Targets:** local;
synthetic per-tenant canaries.

## Goal

Show that the most damaging RAG bug is often not the model at all — it's **missing authorization on
retrieval**. A shared vector store returns the most-similar docs regardless of *who asks*, so one
tenant's query pulls another tenant's confidential document (and its canary) into the answer. Then
compare three retriever designs.

## Run

```bash
py labs/lab-15/tenant.py      # vuln leaks globex canary to an acme user; pre-filter is correct
py -m pytest labs/lab-15 -q
```

## The three designs

- **VULNERABLE** — no tenant check: cross-tenant leak (broken access control / IDOR in RAG clothing).
- **POST-FILTER** — rank globally, then drop unauthorized docs: blocks the leak but (a) crowds out
  the caller's real results (availability) and (b) trusts the doc's own tenant field (spoofable).
- **PRE-FILTER (correct)** — restrict candidates to the caller's tenant *before* ranking, using a
  trusted principal→tenant mapping in code. Authorization lives outside the model.

## What to notice

- **The model is irrelevant to this bug.** No prompt defense fixes broken retrieval authz; the check
  must be deterministic code keyed on the authenticated caller (00.1: "the model decides" ≠ authz).
- **Where you filter matters.** Post-filtering leaks availability and can be bypassed by metadata
  spoofing; pre-filtering by a trusted principal is the only correct design.

## Exercise

See [Lesson 15.1](../../lessons/module-15/lesson-01.md): demonstrate a **metadata-spoofing** bypass
of post-filter (a doc that claims the victim's tenant); show pre-filter with a *trusted* principal→
tenant map resists it; add row-level security semantics; measure the availability cost of post-filter;
combine with poisoning (Lab 14); write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs `tenant.py` with no egress.

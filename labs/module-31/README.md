# Lab 31 — Capstone AI red-team engagement range

**Module:** 31. **Time:** ~2.5 h (rehearsal for a timed engagement). **Hardware:** CPU, offline, no Docker.
**Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> **In-process and synthetic.** The entire "enterprise AI environment" is plain Python — **nothing
> binds to a socket, nothing leaves the process, there is no real code execution, and no real system
> is contacted.** The two objectives are synthetic `LAB-CANARY-...` markers. Only ever run these
> techniques against systems you are authorised to test.

## Rules of engagement (stay in scope)

- **In scope:** the `Range` object and everything it exposes (`range.py`). **Out of scope:** anything
  else on your machine or network — do not scan, connect to, or touch it.
- **Allowed:** reading OSINT, probing the mock registry and agent pipeline, chaining findings.
- **Objectives:** make `Range.objectives()` return both `infra_secret_read: True` and
  `data_exfiltrated: True`, using only the range.
- **Safety:** synthetic canaries only; no destructive actions; no real data.

## Goal

Run a full engagement end to end — recon → foothold → lateral movement → objective → report — then
break the chain with the single highest-leverage fix and retest.

## Files

- `range.py` — the mock enterprise AI environment: OSINT, a path-traversable artifact registry holding
  an infra secret, and a planner/research/exec agent pipeline with memory. Scoring via `objectives()`.
- `solution/walkthrough.py` — one valid reference kill chain (try the range yourself first).

## Run

```bash
py -m pytest labs/module-31 -q          # verifies the intended chain is solvable
py labs/module-31/solution/walkthrough.py   # the reference kill chain + findings summary
```

## The engagement

1. **Recon** — `range.OSINT` names the registry and the agent pipeline.
2. **Foothold** — `registry.get("../config/agents.env")` path-traverses to the infra secret
   (**objective 1**); recover the `EXEC_WEBHOOK_TOKEN` from it.
3. **Lateral** — influence `pipeline.web_content` so `research()` writes a poisoned memory; then
   `exec_task(task, presented_token=<recovered token>)` exfiltrates the data canary (**objective 2**).
4. **Report** — fill [`../../templates/engagement-report.md`](../../templates/engagement-report.md):
   findings ranked, chain narrative, remediation by leverage (with a guarantee box each), standards
   crosswalk.
5. **Retest** — apply your highest-leverage fix (e.g. quarantine untrusted memory, or a safe path
   join) and show an objective is now denied.

## What to notice

- No single bug is game over — the **chain** is the finding. The traversal only yields a token; the
  pipeline only exfiltrates if both poisoned and shown that token.
- Prioritise fixes by leverage (which link breaks the most chains most cheaply), not by count.
- The capstone is done when you have captured the objective, named the highest-leverage fix, and
  shown a retest where it denies the objective.

## Reset

`range.reset()` clears the sink and scoring. Re-run any command to start fresh.

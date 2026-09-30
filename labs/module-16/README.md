# Lab 16 (memory) — Agent memory poisoning & persistence

**Module:** 16 (lesson 16.2). **Time:** ~10 min to run, ~60 min with exercises. **Hardware:** CPU,
offline, no Docker. **Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> **In-process and synthetic.** The agent, its memory store, and the "privileged action" are plain
> Python — **nothing binds to a socket, nothing leaves the process.** The action appends a synthetic
> `LAB-CANARY-...` marker to an in-memory sink. Only ever run these techniques against agents you are
> authorised to test.

> [!NOTE]
> This is the **memory** lab for module 16. The original module-16 agent-surface lab lives separately
> under `labs/lab-16/`; this folder (`labs/module-16/`) is the one packaged for the module download.

## Goal

Turn a one-shot injection into persistence: poison an agent's long-term memory from untrusted
content, watch it fire in a later clean session, measure the persistence curve, then defend with
trust tags, read-time re-validation, and quarantine — and see a stealthy delayed payload evade a
sampling detector but not a source-based control.

## Files

- `memory.py` — a mock `Agent` with a memory store, trust-tag and quarantine toggles, a LOUD and a
  STEALTH (delayed-trigger) payload, and a sampling detector.
- `mem_lab.py` — the driver: persistence measurement, the `1-(1-pq)^n` curve, and the stealth adaptation.

## Run

```bash
py labs/module-16/mem_lab.py
py -m pytest labs/module-16 -q
```

## Purple cycle

1. **Poison** — the agent summarises attacker web content and stores the directive.
2. **Persist** — a later clean task retrieves it and fires the privileged action (canary → sink).
3. **Measure** — `P_fire(n) = 1-(1-pq)^n` climbs toward 1 as the agent is used.
4. **Defend** — trust tags make untrusted memories data-only; quarantine drops them entirely (q→0).
5. **Adapt** — a stealthy, delayed-trigger payload evades the sampling detector (buried out of its
   window, dormant until the invoice trigger) but is still stopped by quarantining untrusted sources.

## What to notice

- Persistence is what makes memory poisoning worse than single-turn injection: success approaches
  certainty over the agent's lifetime.
- Trust tags cut the per-retrieval effect; quarantine cuts retrieval itself — the stronger lever.
- A payload written via a *trusted* path is not caught by source tags alone (the guarantee limit).
- Stealth beats sampling detectors, not source-based controls.

## Exercise

See [Lesson 16.2 · Exercise](../../lessons/module-16/lesson-02.md): the persistence curve, the
stealth/detector knee, a delayed trigger vs a sampling detector, a trusted-path laundering attempt,
and the TTL trade-off.

## Reset

Stateless in-memory `SINK`; helpers clear it. Re-run any command to start fresh.

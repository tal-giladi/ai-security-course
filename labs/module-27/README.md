# Lab 27 — Reconnaissance for AI targets

**Module:** 27. **Time:** ~5–10 min to run, ~60 min with the exercises. **Hardware:** CPU, offline,
no Docker required. **Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> Everything here is **in-process and synthetic**. `mock_target.py` models a small organization's AI
> footprint as plain Python objects — **nothing binds to a socket and nothing leaves the process**.
> The recon engine only ever talks to these mocks. Secrets are synthetic `LAB-CANARY-...` markers;
> leaking one is a benign success marker. Only ever run recon techniques against systems you are
> authorised to test.

## Goal

Build a four-layer asset map (applications, ML components, model infrastructure, dependencies) of a
mock AI target at the lowest detection cost, harden the target, and run the attacker/defender purple
cycle: recon → observe → detect → mitigate → retest → adapt → measure.

## Files

- `mock_target.py` — the target, in **vulnerable** and **hardened** configurations, plus published
  OSINT fixtures (passive, detection-free). Its `TRUTH_ASSETS` set is what completeness is measured against.
- `recon.py` — `passive_collect()` (OSINT only) and a `Prober` (active infra scan, behavioural
  fingerprint, system-prompt leak attempt) + `completeness()`.
- `detector.py` — a **rate** detector (volume per window) and a **coverage** detector (endpoint fan-out).
- `recon_lab.py` — the five-stage driver.

## Run

```bash
py labs/module-27/recon_lab.py
py -m pytest labs/module-27 -q
```

## Purple cycle (the five stages)

1. Noisy recon vs the **vulnerable** target → completeness 1.0 but the rate detector fires.
2. Same recon vs the **hardened** target (auth, disabled metadata, scrubbed banners, generic errors)
   → active completeness collapses; **passive completeness is unchanged** (you cannot un-publish OSINT).
3. **Low-and-slow** recon (lower probe rate) → evades the rate detector while staying complete.
4. The **coverage detector** catches low-and-slow anyway — slowing down changes *when* probes arrive,
   not *how many distinct endpoints* one source touches.
5. The attacker **adapts** by distributing probes across sources → measure how many sources are needed
   to push per-source fan-out below the coverage threshold.

## What to notice

- Passive OSINT gets you apps and dependencies for free; infra ports and the exact model version each
  cost about one active probe.
- Hardening the target's own systems cannot retract already-published information.
- A reachable model can always be behaviourally fingerprinted, even when hardened.
- Every defence has an adaptation; the lab makes you pay the cost of each adaptation in probes/sources.

## Exercise

See [Lesson 27.1 · Exercise](../../lessons/module-27/lesson-01.md): passive-only inventory, the
probes-vs-detection knee, the hardened re-measurement with both guarantee boxes, the low-and-slow
trade, and the adaptive-detector table with your verdict on the highest-leverage defence.

## Reset

Stateless — nothing is written to disk. Re-run any command to start fresh.

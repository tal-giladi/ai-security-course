# Lab 28 — Multi-agent systems & A2A attacks

**Module:** 28. **Time:** ~10 min to run, ~75 min with exercises. **Hardware:** CPU, offline, no Docker.
**Deps:** Python 3.11+, stdlib only (`hmac`, `hashlib`).

> [!WARNING]
> **In-process and synthetic.** The "agents" are plain Python objects and the "bus" is a function
> call — **nothing binds to a socket and nothing leaves the process.** The privileged action appends
> to an in-memory `SINK` list. The only secret is a synthetic `LAB-CANARY-...` marker. Only ever run
> these techniques against systems you are authorised to test.

## Goal

Attack the *edges* of a planner → researcher → executor workflow (impersonation, tampering, and an
injection that rides transitive trust to a privileged action), then defend the edges with message
authentication, per-edge capability scoping, and task provenance — measuring risk at each step.

## Files

- `mas.py` — the mock multi-agent system: agents, an in-memory `Bus` with `require_auth` and
  `scope_caps` toggles, HMAC signing/verification, and provenance-based authorization.
- `mas_lab.py` — the driver: three attacks, the transitive-trust risk model (`rho`, `R`), and the
  four defense stages.

## Run

```bash
py labs/module-28/mas_lab.py
py -m pytest labs/module-28 -q
```

## Purple cycle

1. **Baseline** (no auth, no scoping): injection, impersonation, and tampering all succeed; the
   synthetic canary reaches the sink.
2. **Measure**: transitive-trust risk `R = max_v eps(v)*rho(v)` on the open graph = **9.0**, dominated
   by the exposed researcher whose trust path reaches the executor's `send_email`.
3. **Authenticate**: HMAC signing kills impersonation and tampering — but a *signed-but-malicious*
   message from the injected (legitimate) researcher still reaches the executor.
4. **Scope + provenance**: the executor refuses a privileged task whose provenance is tainted by the
   untrusted researcher; the injection path closes and `R` drops to **0.9**. Benign workflows still run.
5. **Adapt** (exercise): move the attacker to a capability-over-claiming agent card and re-measure.

## What to notice

- Signing proves *who sent* and *that it was not altered* — it does **not** make content trustworthy.
  A correctly-signed message from an injected agent is authentic and still malicious (the guarantee box).
- The injection is closed only by an *edge* control (scoping + provenance), not by any single node's
  least privilege.
- Risk is dominated by the node that is both easy to inject and can reach a powerful action.

## Exercise

See [Lesson 28.1 · Exercise](../../lessons/module-28/lesson-01.md): audit the trust graph by hand,
find and fix the unsigned edge, add a capability-over-claiming fourth agent, attempt a provenance
forgery, and produce the `attack-success × R × capability-lost` table.

## Reset

Stateless in-memory `SINK`; each attack helper clears it. Re-run any command to start fresh.

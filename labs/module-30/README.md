# Lab 30 — AI infrastructure & deployment exploits

**Module:** 30. **Time:** ~5 min to run, ~70 min with exercises. **Hardware:** CPU, offline, no Docker.
**Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> **In-process and synthetic.** The "services" are plain Python objects with a virtual filesystem —
> **nothing binds to a socket, there is no real code execution, and no real service is contacted.**
> The only secret is a synthetic `LAB-CANARY-...` value in the mock VFS. Only ever run these
> techniques against infrastructure you are authorised to test.

## Goal

Exploit the two dominant AI-infrastructure flaws — an unauthenticated admin/management surface and a
path-traversal artifact fetch — then harden and measure which control is load-bearing.

## Files

- `infra.py` — a mock `Service` (model server + artifact registry) with `bind`, `require_auth`, and
  `block_traversal` toggles, and a virtual filesystem holding a canary outside the artifact root.
- `infra_lab.py` — the driver: exploit, harden, adapt, and the single-control gate comparison.

## Run

```bash
py labs/module-30/infra_lab.py
py -m pytest labs/module-30 -q
```

## Purple cycle

1. **Exploit** the vulnerable public service: unauth admin model-load and `../etc/ai-secrets.env`
   traversal both reach the synthetic canary.
2. **Harden** (auth + block traversal + bind localhost): both attacks fail; legitimate authenticated
   reads still work.
3. **Adapt**: an attacker who gains a localhost foothold defeats the network control but is still
   stopped by auth + validation.
4. **Measure**: toggle one control at a time to verify the multiplicative gate model
   `P(success) = r · f · a` and confirm network exposure (`bind`) is the highest-leverage control —
   it zeroes every exploit at once.

## What to notice

- An unauthenticated management surface is effectively code execution; a naive `join(root, input)` is
  path traversal. Both are classic AppSec bugs on AI services.
- Network exposure is shared across all exploits, so making a service unreachable is the cheapest,
  broadest win — the guarantee box in [30.1](../../lessons/module-30/lesson-01.md).
- Auth and input validation are still needed for attackers already inside the boundary.

## Exercise

See [Lesson 30.1 · Exercise](../../lessons/module-30/lesson-01.md): the gate table, an SSRF variant
with a URL allowlist, traversal-bypass attempts against the safe join, container blast-radius, and a
management-endpoint detector.

## Reset

Stateless — nothing is written. Re-run any command to start fresh.

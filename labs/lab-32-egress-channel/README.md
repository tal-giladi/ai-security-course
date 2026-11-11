# Lab 32 — Egress covert channels (DNS & legitimate-tool carriers)

**For:** lesson [05.1 · Indirect prompt injection](../../lessons/module-05/lesson-01.md),
section *Advanced extension: egress covert channels*. **Time:** ~5 min to run, ~45 min with
exercises. **Hardware:** CPU, offline, no Docker required. **Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> **In-process and synthetic.** The deputy, the HTTP egress gateway, and the DNS resolver are
> plain Python objects — **nothing binds to a socket, nothing leaves the process.** The "secret"
> is a synthetic `LAB-CANARY-...` marker and the "attacker's authoritative server" is an in-memory
> log. Only ever run these techniques against systems you are authorised to test.

## Goal

You built an **HTTP egress allowlist** in Lab 05 and proved it caps the confused-deputy
exfiltration chain. This lab shows the allowlist's blind spot: it guards **one carrier (HTTP
host)**. A deputy that obeys an injection can route the same secret out through a *different*
legitimate capability the allowlist never inspects —

1. **DNS** — the secret is base32-encoded into the query's labels and sent to an
   attacker-controlled zone. The HTTP gateway sees nothing; the attacker's authoritative resolver
   sees everything (MITRE ATT&CK **T1071.004**; the OpenAI 2026 sandbox incident; Zenity
   *SalesBleed* against Agentforce).
2. **A legitimate web-fetch to an allowlisted host** — the secret rides in the URL of a benign
   "fetch this doc" call to a host that *is* on the allowlist (LLMLeak / *The Innocent Courier*,
   arXiv:2610.01768).

Then you close each carrier and measure what the fix does and does not guarantee.

## Run

```bash
py labs/lab-32-egress-channel/attack.py
py -m pytest labs/lab-32-egress-channel -q
```

## Purple cycle

1. **Attack** — direct HTTP exfil to `evil.test` (Lab 05's carrier).
2. **Observe** — the HTTP allowlist blocks it. Good — but it is only one carrier.
3. **Attack again** — DNS carrier and allowlisted-host ride-along both reach the attacker while
   the HTTP log reports "nothing exfiltrated."
4. **Mitigate** — a resolver-side **zone allowlist** (DNS egress control) closes the DNS carrier
   structurally; a query-anomaly **detector** adds depth with a measured FPR/recall.
5. **Adapt** — the attacker shrinks the per-query payload below the detector's entropy/length
   threshold and slips past it; only the structural zone allowlist still holds.
6. **Measure** — carrier success, detector recall and false-positive rate are printed as numbers.

## What to notice

- An egress *host* allowlist is not an egress *boundary*: it is complete only for the channel it
  guards. Enumerate every outward capability (DNS, each tool, each renderer), not just HTTP.
- Structural controls (resolver zone allowlist) give the carrier `p=0`; the anomaly detector is
  defense-in-depth with a cost and an adaptive bypass — exactly the guarantee-box distinction.
- The allowlisted-host ride-along shows that even a perfect DNS fix leaves exfil through any
  allowlisted destination the attacker can read — minimise secrets in context, too.

## Exercise

See lesson 05.1, *Advanced extension: egress covert channels*. In brief: (1) measure the DNS
carrier's capacity in bytes/query; (2) sweep the detector threshold and plot the recall/FPR
trade-off; (3) implement the LLMLeak carrier against a tighter allowlist and find the residual;
(4) write the guarantee box for your combined DNS-egress + detector defense.

## Reset

Stateless, in-memory logs rebuilt on each run. Re-run any command to start fresh.

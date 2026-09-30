# Lab 16 — Agent security: excessive agency, confused deputy & memory poisoning

**Module:** 16 (Stage 7 · agent security). **Time:** ~2 h. **Hardware:** CPU, offline.
Synthetic canary; egress -> local sink.

This folder holds both module-16 labs: the original agent-surface lab (lesson 16.1) and the memory
lab added for lesson 16.2. They share the agent runtime, so run them in either order.

---

# Part A — The agent attack surface (lesson 16.1)

> [!NOTE]
> **Shared runtime.** Uses `agent.py` from `labs/common/` (also at `lab/agents/agent.py` in the repo).

## Goal

Turn the confused deputy (00.1) into running code. A benign task ("summarize this file") makes the
agent read attacker-controlled content containing a tool DIRECTIVE; because the agent has broad
capabilities (egress), it emails its own synthetic secret to the attacker. Then measure **excessive
agency** (reachable-action set size) and show three independent defenses each break the chain.

## Files

- `excessive_agency.py` — the vulnerable agent, the injection, the reachable-action-set measurement
  and the three enforced defenses.
- `test_lab16.py` — acceptance tests for the attack and each defense.

## Run

```bash
py labs/module-16/excessive_agency.py    # vulnerable exfiltrates; least-priv / approval / egress-allowlist block it
py -m pytest labs/module-16 -q
```

## What to notice

- **Capabilities are the asset.** The attacker never had egress or the secret; the *agent* did.
  Excessive agency = a large reachable-action set an injection can drive.
- **Three orthogonal enforced defenses:** least privilege (remove the tool), approval gates (human
  in the loop for side effects), egress allowlist (constrain destinations). Each is code, not prompt.
- **The brain is irrelevant to the fix.** No system prompt makes an over-privileged agent safe; the
  policy layer authorizes each tool call regardless of what the model was convinced to do.

## Exercise

See [Lesson 16.1](../../lessons/module-16/lesson-01.md): measure reachable actions as tools/args
grow (multiplicative surface, 00.1); add a multi-step plan the injection hijacks mid-loop; implement
argument-level validation (not just tool allowlist); build an approval gate that a clever directive
tries to social-engineer; write the guarantee box.

---

# Part B — Memory poisoning & persistence (lesson 16.2)

**Time:** ~10 min to run, ~60 min with exercises. **Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> **In-process and synthetic.** The agent, its memory store, and the "privileged action" are plain
> Python — **nothing binds to a socket, nothing leaves the process.** The action appends a synthetic
> `LAB-CANARY-...` marker to an in-memory sink. Only ever run these techniques against agents you are
> authorised to test.

## Goal

Turn a one-shot injection into persistence: poison an agent's long-term memory from untrusted
content, watch it fire in a later clean session, measure the persistence curve, then defend with
trust tags, read-time re-validation, and quarantine — and see a stealthy delayed payload evade a
sampling detector but not a source-based control.

## Files

- `memory.py` — a mock `Agent` with a memory store, trust-tag and quarantine toggles, a LOUD and a
  STEALTH (delayed-trigger) payload, and a sampling detector.
- `mem_lab.py` — the driver: persistence measurement, the `1-(1-pq)^n` curve, and the stealth adaptation.
- `test_lab16_memory.py` — acceptance tests.

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

---

## Reset

Both parts are stateless: Part A is a pure function of its inputs, Part B keeps its sink in memory.
Re-run any command to start fresh. `docker compose up` also runs Part A's demo with no egress.

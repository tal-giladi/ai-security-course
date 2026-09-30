# Lab 33 — Oversight the agent cannot edit

**Module:** 33 (Stage 11 · oversight, scope and evidence). **Time:** ~45 min to run, ~90 min with
exercises. **Hardware:** CPU, offline, stdlib only.

> [!WARNING]
> **In-process and synthetic.** The agent, the monitor and the "secret" are plain Python — **nothing
> binds a socket, nothing leaves the process.** The secret is a synthetic `LAB-CANARY-...` marker
> appended to an in-memory list. Run these only against agents you are authorised to test.

## Goal

Test the assumption the whole industry runs on: that the thing watching the agent can be trusted
to notice when the agent misbehaves. This lab attacks that assumption from inside the harness —
first by making the agent route around an in-harness monitor, then by making it delete its own
record, and finally by showing the one property that actually helps: evidence the agent has no
handle on. Then measure scope adherence separately from capability, because that is a different
property and stating the scope is not the same as getting it.

## Files

- `oversight.py` — the monitor, the agent's four strategies, the trace, the out-of-band recorder,
  the audit-coverage measurement and the scope-adherence model.
- `test_lab33.py` — 14 acceptance tests.

## Run

```bash
py labs/module-33/oversight.py
py -m pytest labs/module-33 -q
```

## What the output shows

| Experiment | Result |
|---|---|
| 1. Monitor evasion | The complying agent is blocked. All three evasions reach the secret: encoding the name, using a second tool with the same effect, and simply waiting out the guardrail's window. |
| 2. Trace tampering | The agent erases the steps recording its own attempt, and the harness shows nothing wrong. |
| 3. Out-of-band capture | The same evasions still succeed — nothing is prevented — but every step is recorded somewhere the agent cannot reach. |
| 4. Audit coverage | What the in-harness log shows versus what actually happened: 0% to 100% coverage depending on the strategy. |
| 5. Scope adherence | An explicit out-of-scope statement raises adherence substantially and still does not reach 1.0. |

## What to notice

- **The monitor is not the weak point by accident.** A guardrail that expires is advice the agent
  can outlive, and the agent controls the clock. The fix is not a longer window.
- **Trace tampering is not "the agent misbehaved".** Anyone who can influence the conversation can
  ask for the deletion, which is why "our agent would never do that" is not a control.
- **Out-of-band capture makes behaviour observable; it does not prevent it.** Read the guarantee box
  in the lesson before you claim otherwise — the lab asserts the attack still succeeds.
- **Adherence and capability are separate.** A more capable model is not automatically a more
  obedient one, so scope adherence has to be measured on its own.

## Exercise

1. **Harden the guardrail.** Replace the time-boxed deny with an unconditional one in code (an
   enforced control, module 23's vocabulary). Which strategies still succeed, and why? Write down
   the one that survives and the control that would actually stop it.
2. **Model the attacker as external.** The trace deletion is currently a function you call. Make it
   something an injected instruction in a tool result can trigger, and show that the guardrail
   against "the agent won't tamper" is no guardrail at all.
3. **Break your own evidence.** Given the out-of-band recorder, write an evasion that produces the
   same *effect* without ever calling the recorded API — batch it through another process, or route
   it over a channel the recorder does not watch. What now has to be watched, and why is each layer
   necessary? This is the module 33 research question.
4. **Scope adherence with a real model.** Replace the toy drift model with a local model and measure
   adherence across dead-end tasks, with and without an explicit scope statement, reporting a
   confidence interval. Does the gap close with a better prompt, or does it plateau?
5. **Write the guarantee box.** For "out-of-band logging", state what it stops, what it does not,
   how the attacker adapts (exercise 3 is the adaptation), the false-positive cost and the
   performance cost.

## Reset

Stateless. Re-run any command to start fresh.

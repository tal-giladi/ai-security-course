# Lab 33 — Prompt-injection defense by design (plan isolation, capabilities, branch steering)

**For:** lesson [17.2 · Prompt-injection defense by design](../../lessons/module-17/lesson-02.md).
**Time:** ~5 min to run, ~60 min with exercises. **Hardware:** CPU, offline, no Docker required.
**Deps:** Python 3.11+, stdlib only (reuses the shared agent runtime `lab/agents/agent.py` unchanged
as the naive baseline).

> [!WARNING]
> **In-process and synthetic.** The planner, the quarantined extractor, the interpreter, the
> "screens" and the outbox are plain Python objects — **nothing binds to a socket, nothing leaves
> the process, no browser is driven.** The confidential report and the credential carry synthetic
> `LAB-CANARY-...` markers; every attacker destination is a reserved `*.test` name recorded in an
> in-memory list. Only ever run these techniques against systems you are authorised to test.

## Goal

Lab 17 made tool authority structural (capabilities). This lab applies the same idea to the
*whole prompt-injection problem*:

1. **Plan isolation (Dual LLM).** The planner sees only the trusted query; untrusted data is read
   by a quarantined extractor with no tools. An injected `CALL send_email(...)` can no longer add a
   tool call — but the extractor's *values* still flow into arguments.
2. **Capability flow control (CaMeL-style).** Every value carries provenance (`sources`) and
   allowed `readers`; an interpreter checks a policy at each tool call. The data-flow hijack is
   denied — and you measure what it does *not* guarantee and what it costs.
3. **Branch steering (computer-use agents).** GUI plans must branch on what the screen shows and
   ground every click on screen content. The attacker steers the agent into an approved-but-
   hazardous branch. You compare no defense, taint-everything, and per-branch capability
   constraints (a simplified illustration in the spirit of COBRA, not a reproduction of it).

## Run

```bash
py labs/lab-33-capability-flow/attack.py
py -m pytest labs/lab-33-capability-flow -q
```

Files: `capflow.py` (part A: tags, Q-LLM, interpreter, policy, plans), `steer.py` (part B: CUA
branches, grounding, constraints, evaluation), `attack.py` (driver), `test_lab33.py`.

## Purple cycle

1. **Attack** — injected `CALL` in the meeting notes: the naive shared agent leaks its canary.
2. **Mitigate** — Dual-LLM plan isolation: the call never exists. **Adapt** — the attacker
   switches to a *data-flow* hijack ("reviewer: audit-desk@evil.test"): plan isolation alone
   sends the report there.
3. **Mitigate** — capability flow control denies it (the body's readers exclude `evil.test`, and
   the recipient derives from untrusted notes). **Measure** the residue: a wrong *internal*
   reviewer still gets the report; a legitimate external reviewer is a false positive.
4. **Adapt** — steer a branch on untrusted data. NORMAL mode runs it; STRICT mode (control-flow
   dependencies) blocks it — and also blocks the legitimate flagged case.
5. **GUI** — branch steering: ASR 0.67 with no defense; taint-everything gives ASR 0 but utility
   0.20; per-branch constraints give ASR 0 at utility 1.00.
6. **Adapt again** — same-origin user-generated content satisfies an origin-only bound; a
   path-prefix bound closes it with no utility loss on the benign set.

## What to notice

- Plan isolation buys **control-flow integrity**, not data-flow integrity. Capabilities buy a
  **confidentiality bound**, not correct choices.
- Every defense here is a structural check in code: it holds even though the Q-LLM and the
  perception model are fully fooled (they are modelled as maximally injectable).
- The utility cost is the honest part of the story: the stricter the flow rule, the more legitimate
  work needs a human. The benign-set numbers are deliberately printed next to the ASR.

## Exercise

See lesson 17.2, *Exercise*. In brief: (1) add a `forward_email` tool and write its policy;
(2) add a side channel (an exception that leaks one bit) and show the policy does not see it;
(3) write a branch constraint for a `pay(amount, iban)` branch; (4) find an attack page that passes
your constraints; (5) measure the FP rate of STRICT mode on a benign task set you design.

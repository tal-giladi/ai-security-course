# Lab 35 — Defensive validation at an internal-peer trust boundary

**Module:** 35 (Stage 13). **Time:** ~90 min. **Hardware:** CPU, offline, stdlib only. No network,
no sockets, no packets. Case study: the iFinder / implicit-trust-error (iTrue) study (USENIX
Security 2026).

## Goal

Build the *defensive* side of what the iFinder Discovery and Vetting agents reason about: given a
stated spec rule and a toy internal-peer message handler, decide whether the required validation is
present before the dangerous operation, and write the missing check. You work only on parsed message
*records* (static fixtures) — you never send anything or run an exploit.

## Run

```bash
py labs/module-35/audit.py          # prints the code-vs-spec audit table + safe/unsafe contrast
py -m pytest labs/module-35 -q      # the pass condition for the exercise
```

## Files

- `validator.py` — reference solution. The six-family validator
  (`<information element, dangerous operation, missing validation>`) plus a safe vs unsafe handler.
- `fixtures.py` — benign and malformed/duplicate Session Establishment / Modification records.
- `audit.py` — runnable audit; shows which iTrue family each record trips and how the uniqueness
  check changes the handler's outcome.
- `exercise.py` — student starting point: a vulnerable handler to fix (R1 uniqueness, R2 bounded
  allocation).
- `test_lab35.py` — tests encoding the pass condition.

## What to notice

- **One missing check is the whole class.** The difference between the unsafe and safe handler is a
  single uniqueness test. Missing it is the root cause of the session-hijack class (a reused rule
  identifier overrides the legitimate forwarding rule); the fix is to **reject the duplicate**, not
  to sort by precedence.
- **Three validation classes close iTrue.** Syntactic (mandatory-field presence, length/bounds),
  semantic (range, uniqueness, state), and resource-availability (bounded allocation with graceful
  rejection instead of assert-and-die).
- **The validator is a detector, so it has a false-positive cost.** Every benign fixture must stay
  clean; that is the M24 discipline applied to your own check.

## Exercise

See [Lesson 35.1](../../lessons/module-35/lesson-01.md) — audit each handler as a triple, write the
missing checks so the fixed handler rejects every malformed/duplicate record and accepts every benign
one, and write the ablation reflection (why the code-specification cross-check cut false positives
62 → 19 while leaving recall unchanged).

## Reset / Docker

Stateless; nothing is written. `docker compose up` runs the audit with no egress.

# Lab 36 — Trust-zoned agent memory (persistence ≠ authority)

**For:** lesson [16.2 · Agent memory poisoning & stealth](../../lessons/module-16/lesson-02.md),
section *Advanced extension: trust-zoned memory*. **Time:** ~2 min to run, ~60 min with exercises.
**Hardware:** CPU, offline, no Docker required. **Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> **In-process and synthetic.** The runtime, the memory store and the "sensitive actions" are plain
> Python objects. **Nothing binds to a socket and nothing leaves the process.** A fired `send_email`
> appends the synthetic marker `LAB-CANARY-3c1f9a2e-…` and a reserved `*.test` address to an
> in-memory `SINK`. The "attacker tool" is a string ending in `-evil`. Only ever use these
> techniques against systems you are authorised to test.

## Goal

In the Module 16 lab you labelled every memory write with a **source** and refused to let
untrusted-source memories act as instructions. That stops the direct poison. This lab shows three
ways the attacker gets a poisoned memory **labelled trusted**, and then builds the defense that the
2026 memory-security literature converged on: the runtime puts each write in a **zone** chosen by
the *channel it arrived on*, and only HIGH-zone, in-scope claims may authorise a sensitive action.

| Attack | Why source tags miss it | Source |
|---|---|---|
| Misattributed preference | a post *quotes* `User: I prefer …`, so a content-based labeler says "user" | Role Grounding Attack, arXiv:2610.38209 |
| Self-note laundering | the agent writes its own "reminder" after reading attacker text; agent notes are trusted | ZoneClaw arXiv:2610.00450; CarryoverBench arXiv:2610.28425 |
| Shared org memory | a hostile peer writes through *their own* real user channel; tags have no scope | arXiv:2610.28810 (shared memory on deployed assistants) |

## Run

```bash
py labs/lab-36-trust-zoned-memory/attack.py
py -m pytest labs/lab-36-trust-zoned-memory -q
```

## Files

- `zones.py`: the runtime, the three policies (`flat`, `source_tags`, `zoned`), promotion, the
  noninterference property check and the persistence formula.
- `attack.py`: attack scenarios, utility tasks, adaptive attacks, and the printed purple cycle.
- `test_lab36.py`: acceptance tests that pin each policy to its guarantee box.

## Purple cycle

1. **Attack.** Four scenarios against a flat memory. All four fire: ASR 1.00.
2. **Observe.** Turn on 16.2 source tags. The direct poison is stopped, but the other three still
   fire (ASR 0.75), because each one gets a *trusted* label.
3. **Mitigate.** Turn on zoning. The zone is set by the runtime from channel + taint, never from
   content; authority also requires scope (owner or org admin) and an authority-bearing kind.
   ASR 0.00.
4. **Measure utility.** The user's own preferences and web facts used as data still work. Two costs
   are measured. A legitimate note written in a tainted session is filed LOW (the taint
   over-approximation is a false positive). A legitimate preference learned from email needs one
   promotion confirmation.
5. **Property.** Differential noninterference check over 200 random attacker spans: zoned has 0
   violations, flat and source tags have many.
6. **Adapt.** The attacker goes after what zoning does not promise: a compromised HIGH channel
   fires; a LOW fact still steers the *answer*; a user who rubber-stamps promotion requests at rate
   $c$ gives an ASR of about $c$.

## What to notice

- A label computed **from the claim** (who it says spoke, who wrote the bytes) is
  attacker-controllable. A zone assigned **by the runtime from the ingestion channel** is not.
- Zoning separates *remembering* from *being obeyed*. Attacker text still persists and is still
  readable as data, so the agent keeps learning from its environment. That is why zoning costs so
  little utility, and it is also why it gives no guarantee that the data is true.
- The promotion gate moves the residual risk onto a human. Measure the confirmation rate. Do not
  assume it is zero.

## Exercise

See lesson 16.2, *Advanced extension: trust-zoned memory*. In short: (1) make taint finer (per
derived-from lineage instead of per session) and re-measure the tainted-note false positive;
(2) add a `kind` check so a LOW `fact` can never be promoted into a `policy`; (3) give the
promotion request a diff of what will change and model a lower rubber-stamp rate; (4) write the
guarantee box for your finer-taint variant, including how an attacker abuses lineage gaps.

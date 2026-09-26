# Lab 05 — Indirect prompt injection & the confused-deputy chain

**Module:** 05 (Stage 2). **Time:** ~2 h. **Hardware:** CPU-only, offline. **Targets:** local
only; synthetic canary; exfiltration goes to the **local sink** (`lab/sink/sink.py`).

## Goal

Reproduce the attack class that matters most in real deployments: the attacker **never messages
the bot**. They plant an instruction in a document the bot retrieves, and the bot — holding a
secret and able to render links (its privilege) — becomes a **confused deputy** (Lesson 00.1)
that carries the secret out.

```text
poisoned doc → retrieved into context → bot obeys injected instruction
             → emits image URL carrying the canary → renderer fetches it → LOCAL sink
```

## Run

```bash
py labs/lab-05/attack.py            # in-process fake sink; no server needed
# or, to see it hit the real local sink:
py lab/sink/sink.py                 # terminal 1
py labs/lab-05/attack.py --sink     # terminal 2
py -m pytest labs/lab-05 -q         # acceptance tests
```

Expected: **VULNERABLE** exfiltrates the canary (True); **DEFENDED** does not (False).

## The three defenses (in `app.py`, `defended=True`)

1. **Provenance / segregation (input, weak):** wrap retrieved text as
   `<retrieved_untrusted>…</retrieved_untrusted>` so it is framed as data, not instructions.
   Prior-shaping only — a stronger payload can still win (02.1).
2. **Egress allowlist (enforced):** the renderer only fetches allowlisted hosts; the sink host is
   not on the list, so the outbound request is dropped. This is the confused-deputy fix — remove
   the deputy's ability to act on the attacker's chosen destination.
3. **Output scrub (enforced):** block any response still containing the literal canary.

## What to notice

- Indirect injection is **direct injection through a lower-priority channel** (`retrieved` role,
  more negative bias). That is why the payload needs *more* strength `s(I)` than a direct one —
  authority framing + "ignore previous" — to clear the threshold. The shim models this exactly.
- The decisive defense is #2: even a fully obeyed injection cannot exfiltrate if the deputy has
  no egress to the attacker's destination. Least privilege beats persuasion.

## Exercise (in the lesson)

[Lesson 05.1](../../lessons/module-05/lesson-01.md) → **Exercise**:
1. Show the attack works; measure over several poisoned-doc variants (ASR).
2. Defeat defense #3 alone (encode the canary so the literal-match scrub misses it) — then show
   defense #2 still blocks it. Argue why #2 is the real boundary.
3. **Bypass #2 (purple team):** find an exfil path that uses an *allowlisted* host, or a channel
   the renderer doesn't guard (link text the user copies, a citation the app resolves server-side).
   Then strengthen and re-measure.
4. Write the guarantee-analysis box for your final layered defense.

## Reset

```bash
py labs/lab-05/reset.py
```

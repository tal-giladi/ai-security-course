# Lab 08 — Automated black-box jailbreaks (PAIR/TAP-style)

**Module:** 08 (Stage 3). **Time:** ~2 h. **Hardware:** CPU-only, offline (shim). **Targets:**
local; inert "disallowed-content" marker; nothing harmful produced.

## Goal

Jailbreak with **no gradients — only queries**, like PAIR (Chao et al., 2023) and TAP (Mehrotra
et al., 2023): an attacker loop proposes jailbreak wrappers, a **judge** scores each target reply,
and a **beam search** refines the best composition. Then add an input-classifier defense and show
the search **rediscovers an evasive paraphrase** — classifier defenses are evadable by novel framing.

## Run

```bash
py labs/lab-08/pair.py        # vulnerable: PAIR ASR ~1.0; defended: PAIR rediscovers 'story' evasion ~0.6
py -m pytest labs/lab-08 -q
```

## What to notice

- **Query-only search works.** The attacker never sees weights or gradients (contrast Lab 07);
  it composes wrappers that push the target out-of-distribution, lowering refusal (02.1 coverage).
- **Judges are the engine.** Automated red teaming needs an automatic success signal (`judge`);
  its quality bounds the search (a weak judge = a weak attacker). This is the seed of Module 25.
- **Marker classifiers are brittle.** Blocking known wrapper words (`roleplay`, `DAN`, `base64`)
  stops the obvious attacks, but the search finds a paraphrase (`story`) with none of those words
  that still works. Real PAIR uses an attacker *LLM* to generate unlimited novel framings.

## Exercise

See [Lesson 08.1](../../lessons/module-08/lesson-01.md): add a multi-turn variant; replace the
fixed strategy library with an attacker that mutates prompts (a crude "attacker model"); measure
queries-to-success vs random with CIs; build a semantic (not keyword) jailbreak detector and then
evade it; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs `pair.py` with no egress.

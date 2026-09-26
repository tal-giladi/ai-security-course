# Lab 04 — Direct prompt injection & system-prompt leakage

**Module:** 04 (Stage 2 · prompt injection). **Time:** ~90 min. **Hardware:** CPU-only, offline
(uses the deterministic lab model shim; swap in a small local model for higher fidelity).
**Targets:** local only; synthetic `LAB-CANARY-*` secret; no network.

## Goal

Experience the purple-team cycle on the simplest LLM attack: talk a support bot into revealing a
secret it was told to keep, **measure** the attack success rate (ASR), add defenses, **re-measure**,
then try to defeat your own defense.

```text
attack (suite) → measure ASR → defend (input wrap + enforced output scrubber) → re-measure → adapt
```

## Files

- `app.py` — the vulnerable `SupportBot` (and a `defended=True` mode you extend).
- `attack.py` — a suite of direct-injection payloads + `asr()` measurement.
- `test_lab04.py` — acceptance tests: attack works on the vulnerable bot, defense blocks the leak.
- `reset.py` — clears the local sink log (used when the exfil bypass exercise points at the sink).

## Run

```bash
py labs/lab-04/attack.py            # see ASR on vulnerable vs defended bot
py -m pytest labs/lab-04 -q         # acceptance tests
```

Expected: vulnerable ASR well above zero (authority-framed / ignore-previous / debug payloads
leak); defended ASR = 0.00 for the literal canary.

## What to notice

- **Why some payloads leak and others don't:** the leaking ones raise the instruction "strength"
  `s(I)` (authority framing, "ignore previous", shouting) enough to overcome the finite system
  guard bias — exactly the log-odds model from Lesson 02.1. This is a *rate*, not a rule.
- **Why the defense is different in kind:** the output scrubber is an **enforced** control in
  code (02.1) — it stops the canary from leaving *even when the model is fully jailbroken*. The
  input-wrapping is only behavior-shaping (a prior) and is not, by itself, trustworthy.

## Docker (optional)

`docker compose up` runs the attack suite in a pinned container so the lab is reproducible if
your local Python changes. The lab is identical either way; Docker is for isolation/repro, not
because anything here needs the network (it doesn't — the container runs with no egress).

```bash
cd labs/lab-04 && docker compose up
```

## Exercise (in the lesson)

See [Lesson 04.1](../../lessons/module-04/lesson-01.md) → **Exercise**. Summary:
1. Extend the payload suite with two encoding/obfuscation variants; report the new ASR + a Wilson CI.
2. **Bypass the scrubber (purple team):** make the secret *leave* without the literal canary in
   the output (hint: the scrubber only matches the literal string — think about what the model
   could emit instead, and what a downstream renderer/tool would do with it). Point the exfil at
   the local sink and confirm with `SinkLog`.
3. Strengthen the defense to stop your bypass; write the guarantee-analysis box for your final
   defense (stops / doesn't stop / adapt / FP cost / perf cost).

## Reset

```bash
py labs/lab-04/reset.py      # clears lab/sink/sink_log.jsonl
```

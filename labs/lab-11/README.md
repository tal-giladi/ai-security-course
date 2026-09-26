# Lab 11 — Data-poisoning backdoors (sleeper agents) & detection

**Module:** 11 (Stage 5 · model-level security). **Time:** ~2.5 h. **Hardware:** CPU torch, no
download. **Targets:** local toy model; inert target label; synthetic data.

## Goal

Reproduce the **sleeper-agent** pattern: poison a fraction of training data so the model learns a
hidden rule — *"if the TRIGGER is present, output the attacker's target class"* — while keeping
**high clean accuracy** (it passes normal evaluation). Then attempt **detection** with a spectral
signature, and confront how hard detection is.

## Run

```bash
py labs/lab-11/backdoor.py    # clean model ASR 0.00; poisoned model clean 0.98 + backdoor ASR 0.98
py -m pytest labs/lab-11 -q
```

## What to notice

- **Clean eval is blind to backdoors.** The poisoned model's clean accuracy (0.98) is
  indistinguishable from the clean model's — the danger only appears when the trigger does.
- **Small poison fraction, large effect.** ~10% poisoned data yields ~98% ASR — poisoning is
  cheap and potent.
- **Detection is hard.** The spectral signature surfaces poisoned samples *above* the base rate
  but with imperfect precision/recall — a realistic picture, not a solved problem. Defenses are
  probabilistic (guarantee analysis in the lesson).

## Exercise

See [Lesson 11.1](../../lessons/module-11/lesson-01.md): sweep poison fraction vs ASR and clean
accuracy; make the trigger stealthier (fewer/smaller features) and show detection degrades;
improve detection (activation clustering, or fine-tuning/pruning defenses) and measure
precision/recall + the clean-accuracy cost; craft an adaptive trigger that evades your detector;
write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs `backdoor.py` (torch image), no egress.

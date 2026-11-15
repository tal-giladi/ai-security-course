# Lab 23.2 — Text watermarking: detect, remove, forge

**Module:** 23 (Stage 9 · blue team), lesson 23.2. **Time:** about 1.5 h. **Hardware:** CPU, offline,
Python 3.10+ standard library only. **Runtime:** about 15 s for the full evaluation, about 10 s for
the tests.

## Goal

Build a green-list text watermark (Kirchenbauer et al., ICML 2023) from scratch on a toy language
model, measure what its detector promises, and then run the purple cycle against it:

1. **Defend:** watermarked generation plus a one-sided z-test detector.
2. **Measure:** true-positive rate against text length and entropy; empirical false-positive rate on
   unwatermarked text.
3. **Attack:** removal by random edits (a stand-in for paraphrasing) and **forgery** by watermark
   stealing (Jovanović, Staab, Vechev, ICML 2024): estimate the green lists from watermarked outputs
   alone, with no key.
4. **Adapt:** informed scrubbing with the stolen lists; the defender widens the context window `h`.
5. **Retest:** at the same query budget `h=3` defeats this stealing attack, and the same edits now
   remove the watermark more easily. That is the trade-off you will write up.

Tokens are integers from a 64-token synthetic vocabulary. There is no real model, no network and
no payload. The key in `wm_core.py` is a lab constant, not a secret.

## Run

```bash
python labs/module-23/watermark/wm_evaluate.py
python -m pytest labs/module-23/watermark -q
```

## Files

| File | What it is |
|---|---|
| `wm_core.py` | `ToyLM` (seeded bigram model with adjustable entropy), `Watermark` (keyed green lists, biased sampling, z-test), `one_sided_p` |
| `wm_attacks.py` | `random_edit` (removal), `StolenWatermark` (frequency-ratio green-list estimate), `spoof` (forgery), `informed_scrub` (removal using the stolen lists) |
| `wm_evaluate.py` | The whole purple cycle, printed as tables |
| `test_lab23_watermark.py` | Acceptance tests: every claim in lesson 23.2 that the lab demonstrates |

## What to notice

- **The z-test threshold sets the false-positive rate, not the true-positive rate.** At z ≥ 4 the
  normal tail promises about 3×10⁻⁵, and the empirical rate on unwatermarked text is 0. Recall
  depends on length and entropy: short or low-entropy text (the `sharpness=4` model) is detected
  less often at the same length.
- **Edits wear the signal down; they do not flip a switch.** With `h=1`, 30% random edits still
  leave a detectable watermark at T=200, and 50% mostly remove it.
- **A watermark that can be learned can be forged.** With `h=1` the attacker covers every context
  after 200 outputs, and text it generates *without the key* is detected as watermarked. This is the
  failure that matters for attribution ("the model wrote this").
- **Widening the context is a trade, not a fix.** `h=3` has about 262,000 contexts in this toy
  vocabulary, so the same budget covers almost none of them and forgery fails. But each edit now
  disturbs up to `h+1` scored positions, so the watermark breaks at a lower edit rate. A
  better-funded attacker buys coverage back with more queries.

## Exercise

See [lesson 23.2](../../../lessons/module-23/lesson-02.md), section *Exercise*.

## Reset / Docker

The lab is stateless. `docker compose up` (from this folder) runs the evaluation with no network.

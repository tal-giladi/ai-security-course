# Lab 37 — Evaluating prompt-injection detectors (over-defense & distribution shift)

**For:** lesson [24.1 · Security evaluation](../../lessons/module-24/lesson-01.md), section
*Advanced extension: evaluating prompt-injection detectors*. **Time:** under 1 s to run, ~60 min with
exercises. **Hardware:** CPU, offline, no Docker required. **Deps:** Python 3.11+, stdlib only.

> [!WARNING]
> **In-process and inert.** The detectors only classify strings. Nothing is sent, fetched or
> executed. The "attack" strings ask for the synthetic marker `LAB-CANARY-5b0e9c41-…` or the
> inert word `PINEAPPLE-OK`, or name a reserved `*.test` address that never resolves. A test
> (`test_payloads_are_inert`) fails if any other address appears in the corpus.

## Goal

In Lab 24 you scored a detector with ROC-AUC and a base-rate PPV, on one test set drawn from the
same distribution as its training data. That is the number most detector papers report. This lab
keeps the threshold fixed and moves the *data*. It measures the four things that number hides:

| Axis | What changes | Source |
|---|---|---|
| Over-defense | benign text full of trigger words ("ignore the typos", "override the CSS font") | InjecGuard / NotInject (arXiv:2410.22770); PIDS-Bench (arXiv:2609.15017, IEEE Access 2026) |
| External benign source | trigger-word benign text written differently from anything you trained on | PIDS-Bench's "externally sourced" subset |
| Format shift | an injection inside a JSON tool output instead of a chat turn | Liu, arXiv:2610.03448 (AgentDojo / tau-bench replay; code released) |
| Obfuscation | leetspeak, letter spacing, paraphrase | PIDS-Bench obfuscation split |
| No imperative at all | a fabricated hazard in a review that steers the agent's choice | "Voluntary Servitude", arXiv:2611.04393 (NeurIPS 2026; single paper, EMERGING) |

## Run

```bash
py labs/lab-37-injection-detector-eval/evaluate.py
py -m pytest labs/lab-37-injection-detector-eval -q
```

## Files

- `corpus.py`: every split, generated from templates (deterministic, seed 37).
- `detectors.py`: the 23.1 keyword detector (imported unchanged from `lab/defense-tools/defenses.py`),
  a multinomial naive-Bayes detector written from scratch, and the evaluation primitives
  (`calibrate_threshold`, `rates_at` with Wilson CIs from `lab/attack-tools/evalkit.py`,
  `recall_at_fpr`, `f1`, `ppv`).
- `evaluate.py`: the printed purple cycle and `evaluate_all()`, which the tests use.
- `test_lab37.py`: acceptance tests that pin each finding below.

## Purple cycle (what you should see)

1. **Measure.** The naive-Bayes detector trained on chat-style injections scores F1 1.00 on its
   held-out test split, at the shipped threshold (posterior 0.5).
2. **Observe.** At the same threshold it flags 35% of the curated hard-benign set and 75% of the
   external one. That is over-defense.
3. **Mitigate.** Add hard negatives to training. The curated FPR goes to 0.00, but the external FPR
   is still 0.25, above the 0.10 deployability bar. You fixed your home turf.
4. **Shift.** On injections inside tool outputs, recall falls to 0.60 for the original detector and
   0.36 after the hard-negative fix. Look at the CIs: at n=25 they overlap, so this is a direction,
   not an established cost. Leetspeak and letter spacing also cut recall.
5. **Mitigate.** Add agent-style training data, using templates that differ from the eval split.
   Recall@5%FPR on the agent split reaches 1.00, but at the shipped threshold the agent-benign FPR is
   0.20. The ranking is fixed; the calibration is not.
6. **Adapt.** The attacker drops the imperative. A fabricated hazard ("the venue was cited for a gas
   leak") contains no instruction, so every hardened detector scores 0.00 recall on it.
7. **Report.** One row per detector, with in-distribution F1, both hard-benign FPRs, agent recall at
   the fixed threshold and at 5% FPR, obfuscation recall, PPV at a 1% base rate, and whether the
   detector meets the joint bar. None does.

## What to notice

- A detector has an operating threshold. Report every split **at that one threshold**. Recall@1%FPR
  re-chosen per split measures ranking quality only, and it is optimistic: nobody re-calibrates per
  incoming distribution.
- Hard-negative augmentation works on the distribution it was drawn from. Measure it on a benign
  source you did not write.
- The splits are small on purpose, so the Wilson CIs are wide. Exercise 1 asks you to grow them.
- Detection is a probabilistic control that sees *text shape*. Steering that has no command shape
  needs a different kind of control (17.2 capability flow; a corroboration rule).

## Exercise

See lesson 24.1, *Advanced extension: evaluating prompt-injection detectors*. In short: (1) grow the
agent and external splits until the recall cost of hard negatives is established or refuted;
(2) write your own external benign set from a source you did not template and re-measure; (3) add a
de-obfuscation pre-pass and attack it; (4) write the guarantee box for your best detector.

# Lab 29 — Embedding inversion & attribute extraction

**Module:** 29. **Time:** ~5 min to run, ~75 min with exercises. **Hardware:** CPU, offline, no Docker.
**Deps:** Python 3.11+, numpy (see `requirements.txt`).

> [!WARNING]
> **Offline and synthetic.** A deterministic toy encoder stands in for a sentence-embedding model —
> **no weights are downloaded, no network, no real data.** The only "secret" is a synthetic
> `LAB-CANARY-...` token. Only ever run these techniques against data you are authorised to test.

## Goal

Show that stored embeddings are recoverable data: invert them to their tokens, read a private
attribute off them with a linear probe, then measure how much the noise defense actually helps and
what it costs in retrieval utility.

## Setup

```bash
py -m pip install -r labs/module-29/requirements.txt
```

## Files

- `emb.py` — the toy encoder (`encode`), inversion (`invert`), a from-scratch logistic attribute
  probe, the noise defense (`add_noise`), retrieval utility, and a synthetic corpus builder.
- `emb_lab.py` — the driver: attacks on clean embeddings, the noise trade-off table, and the
  surrogate-encoder adaptation.

## Run

```bash
py labs/module-29/emb_lab.py
py -m pytest labs/module-29 -q
```

## Purple cycle

1. **Invert** clean stored embeddings → token-F1 ≈ 0.94; the canary is recovered when present.
2. **Extract** the private attribute with a linear probe → well above the majority-class baseline,
   *without* full inversion.
3. **Defend** with Gaussian noise → trace inversion F1, extraction accuracy, and retrieval top-1
   across σ. Both recovery and utility fall together — a Pareto curve, not a free lunch.
4. **Adapt** → invert with an imperfect *surrogate* encoder (weights not exact) and confirm recovery
   stays well above chance: the attacker does not need the exact model.

## What to notice

- An embedding is not a one-way hash; similarity-preservation is exactly what makes it invertible.
- A coarse attribute (extraction) survives more noise than full inversion does.
- Access control and minimisation (don't embed/store secrets) are load-bearing; noise only raises the
  bar and costs utility — the guarantee box in [29.1](../../lessons/module-29/lesson-01.md).

## Exercise

See [Lesson 29.1 · Exercise](../../lessons/module-29/lesson-01.md): the recovery curve, attribute
robustness to noise, minimisation-beats-noise with both guarantee boxes, surrogate-strength sweep,
and a scikit-learn cross-check of the from-scratch probe.

## Reset

Stateless — nothing is written. Re-run any command to start fresh.

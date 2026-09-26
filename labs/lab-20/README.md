# Lab 20 — Multimodal security (deep): steganography & pixel-space attacks

**Module:** 20 (Stage 8). **Time:** ~2 h. **Hardware:** CPU, numpy, offline. Inert payload +
synthetic canary.

## Goal

Show an **image** carrying an attack that no text filter can see:
1. **LSB steganography** — hide an injected directive in the least-significant bits of pixels; the
   image is visually ~identical (MSE ~0.05, max pixel delta 1) yet a pipeline that extracts hidden
   data recovers and acts on the instruction. Defense: **strip the LSB plane** (destroys the payload
   at negligible visual cost).
2. **Pixel-space perturbation** — the FGSM/PGD math (Labs 09/10) on image pixels flips a vision
   classifier imperceptibly (the visual adversarial-example half of multimodal attacks).

## Run

```bash
py labs/lab-20/stego.py       # payload hidden & recovered; LSB-strip removes it
py -m pytest labs/lab-20 -q
```

## What to notice

- **Images bypass text filters entirely.** The steg payload is invisible to humans *and* to
  content filters that only see the prompt text (M06's carrier, now bit-level).
- **Cheap, near-lossless defense for steg:** re-quantizing (stripping LSBs) destroys hidden bits
  with imperceptible visual change — but only defends the LSB channel, not pixel-space adversarial
  perturbations (different threat model, M09/M10) or semantic image injections (M06 OCR/alt).
- **Durable defenses:** provenance on uploaded media + *not acting on extracted image content as
  instructions* (M06) + re-encoding on ingest.

## Exercise

See [Lesson 20.1](../../lessons/module-20/lesson-01.md): measure payload capacity vs image size and
detectability (LSB histogram / chi-square); build a pixel-space PGD attack on a toy vision classifier
(reuse Lab 09) and show LSB-strip does NOT defend it; combine steg with a multimodal agent (M06/M16);
compare re-encoding defenses (JPEG/quantization) vs perturbation robustness; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs the demo with no egress.

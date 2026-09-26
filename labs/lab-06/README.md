# Lab 06 — Multimodal & cross-agent injection

**Module:** 06 (Stage 2). **Time:** ~90 min. **Hardware:** CPU-only, offline. **Targets:** local
only; synthetic canary.

## Goal

Show that injection needs neither a text prompt from the attacker nor a document: it rides in via
an **image's extracted text** (alt / EXIF / OCR) or **across an agent-to-agent boundary**. Same
root cause as M04/M05 (untrusted text → the one instruction stream), new carriers that text-only
input filters never see.

## Run

```bash
py labs/lab-06/attack.py          # multimodal ASR + cross-agent leak, vulnerable vs defended
py -m pytest labs/lab-06 -q
```

Expected: vulnerable multimodal ASR = 1.00 (alt/exif/OCR all leak), cross-agent leak = True;
defended = 0.00 / False.

## What to notice

- **No real vision model is needed to learn the bug.** The security fact is that a preprocessing
  step (OCR/alt/metadata) turns image bytes into *text in context*. Whoever controls that text
  controls an injection channel — and it is invisible to the user and to prompt-text filters.
- **Cross-agent:** agent A's output is untrusted input to agent B. Designers routinely trust
  downstream links they never drew as a boundary (00.1). One injected agent poisons the pipeline.
- The defended path pairs provenance labels (prior) with an enforced output scrub (the control
  that actually guarantees the canary can't leave). The scrub is doing the guaranteeing.

## Exercise

See [Lesson 06.1](../../lessons/module-06/lesson-01.md). Summary: add an invisible-text /
zero-width variant and a base64-in-OCR variant; defeat the literal scrub; then show why the real
fixes are (a) treating all extracted/upstream text as untrusted data with least privilege, and
(b) not carrying secrets the pipeline can emit. Write the guarantee box.

## Reset

Stateless (no sink). `docker compose up` runs the attack in a no-egress container.

# Lab 13 — Model & adapter supply chain: pickle RCE, safetensors, malicious LoRA

**Module:** 13 (Stage 5). **Time:** ~2 h. **Hardware:** CPU torch + safetensors, no download.
**Safety:** the pickle payload is an **inert marker** (writes a local file), not malware; no
network, no harm.

## Goal

Show that **loading a model can run someone else's code**, and that a shipped **adapter** can
backdoor a trusted base model:
1. **Pickle RCE** — a `.pt`/`.bin` checkpoint (torch.save uses pickle) can execute arbitrary code
   on load via `__reduce__`. Demonstrated with a harmless marker.
2. **safetensors** — stores tensors only; loading cannot execute code.
3. **Malicious LoRA** — an adapter delta that preserves clean accuracy (0.99→0.98) while installing
   a trigger→target backdoor (ASR 1.00), without altering the base weights file.

## Run

```bash
py labs/lab-13/supply_chain.py    # pickle executes (marker=True); safetensors doesn't; stealthy adapter
py -m pytest labs/lab-13 -q
```

## What to notice

- **`torch.load` historically unpickled by default** — downloading a `.pt` from a model hub was
  running untrusted code. Use `weights_only=True` (newer torch) or **safetensors**.
- **safetensors is safe *because* it can't express code** — a format-level guarantee, not a filter.
- **Adapters are supply-chain artifacts too.** A stealthy backdoor can ride in a LoRA you merge
  into a model you trust; clean-eval won't reveal it (Lab 11). Verify provenance and signatures.

## Exercise

See [Lesson 13.1](../../lessons/module-13/lesson-01.md): enumerate every load-time code path in a
real model repo (pickle, custom `code`/`trust_remote_code`, tokenizer files); convert a checkpoint
to safetensors and verify round-trip; build a signature/hash-verification gate for adapters and try
to bypass it; detect the malicious adapter by its trigger-response; write the guarantee box.

## Reset / Docker

Marker file is auto-cleared. `docker compose up` runs the demo (torch image) with no egress.

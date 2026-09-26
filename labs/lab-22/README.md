# Lab 22 — AI supply chain: verifying the whole artifact graph

**Module:** 22 (Stage 8). **Time:** ~90 min. **Hardware:** CPU, offline (hashlib). Ties together
M13 (weights/adapters) and M21 (deps).

## Goal

An AI system is a *graph* of externally-sourced artifacts — model weights, tokenizer/config,
datasets, LoRA adapters, Docker images, inference servers, plugins. Build a **verification gate**
that checks each on four axes and turns "we downloaded it" into "we verified exactly what we
approved."

## Run

```bash
py labs/lab-22/supply_chain_graph.py   # clean chain passes; tampered/untrusted/unsafe/unpinned caught
py -m pytest labs/lab-22 -q
```

## The four checks

1. **Integrity** — sha256 matches a trusted manifest (catches tampering/substitution).
2. **Provenance** — source allowlisted + signature from a trusted publisher.
3. **Format** — reject code-executing formats (pickle `.pt`/`.bin`); require safetensors (M13).
4. **Pinning** — no floating `latest` versions (dependency-confusion, M21).

## What to notice

- **Compromise around the model is the norm.** You can vet the model's behavior perfectly and still
  be owned by a poisoned dataset, a pickle tokenizer, an unpinned dependency, or a backdoored image.
- **Verification beats detection.** Hashes/signatures/allowlists/safe-formats are structural — they
  don't rely on spotting "bad" content, they enforce "exactly the approved artifact from the approved
  source in a safe format at a pinned version."

## Exercise

See [Lesson 22.1](../../lessons/module-22/lesson-01.md): extend to transitive artifacts (a plugin that
pulls its own deps); add signature *verification* (not just presence) with a key store; model a
compromised-but-signed publisher (residual risk); integrate M13's pickle scan and M21's lockfile;
map to SLSA levels; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs the demo with no egress.

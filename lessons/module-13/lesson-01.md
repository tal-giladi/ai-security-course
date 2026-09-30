---
id: "13.1"
module: 13
minutes: 10
practice_minutes: 120
prerequisites: ["11.1", "01.1"]
objectives:
  - Explain pickle deserialization remote code execution and why .pt and .bin checkpoints are executable code.
  - Explain what safetensors guarantees, and why that guarantee is stronger than any scanner.
  - Enumerate load-time code paths, including trust_remote_code and tokenizer or config code.
  - Build a malicious adapter that preserves clean accuracy while installing a backdoor.
  - Design a layered load-time defense of safe format, provenance, behavioral vetting, and least privilege.
volatility: implementation
sources:
  - title: "safetensors — a simple, fast, and safe format for storing tensors"
    url: https://github.com/huggingface/safetensors
  - title: "CWE-502: Deserialization of Untrusted Data"
    url: https://cwe.mitre.org/data/definitions/502.html
  - title: "PyTorch documentation — torch.load and weights_only"
    url: https://docs.pytorch.org/docs/stable/generated/torch.load.html
  - title: "Hugging Face Hub security documentation — pickle, safetensors, trust_remote_code"
    url: https://huggingface.co/docs/hub/security
last_verified: "2026-09-30"
---

# 13.1 · Adapter & weight supply chain

Loading a model is a trust decision, not a download. This lesson covers the load-time code paths that make a checkpoint dangerous, the guarantee safetensors gives that a scanner cannot, and the malicious adapter that backdoors a trusted base model without touching its weights file.

## Why this matters

You would not `curl | sh` a random script — but `torch.load("model.bin")` from a hub historically
did essentially that, because the checkpoint format is *pickle*, and pickle can run code on load.
And even with safe weights, a LoRA adapter you merge can carry a sleeper backdoor. Loading a model
is a trust decision; this lesson makes the mechanisms concrete so you treat model artifacts like the
untrusted code they are.

## Learning objectives

1. Explain **pickle deserialization RCE** (`__reduce__`) and why `.pt`/`.bin` checkpoints are code.
2. Explain what **safetensors** guarantees and *why* (a format that cannot express code).
3. Enumerate other load-time code paths: **`trust_remote_code`**, custom tokenizer/processor code,
   config-driven imports.
4. Build a **malicious adapter** that preserves clean accuracy while installing a backdoor; explain
   why clean-eval misses it.
5. Design provenance/verification defenses (hashes, signatures, safe formats, sandboned loading) and
   know their limits.

## Concept

### Pickle is code

Python's `pickle` serializes objects by recording how to *reconstruct* them — including, via
`__reduce__`, a callable and its arguments to invoke on load. So a pickle stream can say "on load,
call `os.system` with this string" (or anything). `torch.save`/`torch.load` use pickle, so a
`.pt`/`.bin` checkpoint is an executable payload. **Loading an untrusted checkpoint = running
untrusted code**, before you ever run inference. (CWE-502, M01.) The lab demonstrates this with an
inert marker: unpickling the malicious checkpoint calls a benign function that writes a local file —
proving code ran, with zero harm.

### safetensors: safe by construction

**safetensors** stores a JSON header (shapes/dtypes/offsets) plus raw tensor bytes — *and nothing
executable*. There is no `__reduce__`, no callable, no code path; loading only memory-maps tensors.
Its safety is a **format-level guarantee**, not a scanner that might miss something: the format
literally cannot express code. This is why the ecosystem moved to it and why `torch.load` added
`weights_only=True` (restrict unpickling to tensors/plain data). The lab shows loading the same
weights via safetensors runs no code.

### Other load-time code paths

Pickle is not the only door:
- **`trust_remote_code=True`** (Hugging Face) executes model/tokenizer *code* shipped in the repo —
  arbitrary Python by design. A repo you don't control is arbitrary code execution.
- **Custom tokenizers/processors/configs** can import and run code; some formats allow references
  that trigger imports.
- **Build/convert scripts** shipped alongside weights.

Each is the same trust decision: *whose code am I about to run?*

### Malicious adapters (LoRA)

A LoRA/adapter is a small weight delta merged into a base model. An attacker can train an adapter
that (a) **keeps clean accuracy** (so it passes evaluation and looks like a normal fine-tune) and
(b) **installs a trigger⇒target backdoor** (Lab 11). It ships as an innocuous "improved adapter,"
merges into a base *you* trust, and the base's own weights file is never modified — the backdoor
lives in the adapter's supply chain. Lab: adapter keeps clean acc 0.99→0.98 while trigger ASR = 1.00.

## Intuition

A model file is a shipping container. safetensors is a container with a glass front: you can see
it's just weights. A pickle checkpoint is a sealed container that, when you open it, might run
whatever machine the sender welded inside — and `trust_remote_code` is you handing the sender the
keys to your forklift. A malicious adapter is a small, official-looking add-on part that fits your
trusted machine perfectly and quietly rewires it to misbehave only when a specific rare button is
pressed. In every case the question is the same and rarely asked: *do I trust who made this, and can
I verify it's what they claim?*

## Technical explanation

## Mathematics

Little equation here — this is a systems/trust lesson — but two quantitative points:
- **Detection base rates (M02.2/M11).** Scanning downloaded artifacts for "malicious" content is a
  classifier with false negatives; a novel pickle payload or a stealthy adapter evades it. Format
  guarantees (safetensors) and provenance (signatures) sidestep the base-rate problem entirely by
  not relying on detection.
- **Stealth objective.** The adapter attacker solves
  $\min_\Delta\ \mathbb E_{\text{clean}}[\ell(f_{\theta+\Delta}(x),y)] + \lambda\,\mathbb E[\ell(f_{\theta+\Delta}(x_{\text{trig}}),t)]$,
  choosing $\lambda$ to trade stealth (clean accuracy) against ASR — the same clean/backdoor balance
  as M11, now delivered through the supply chain.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — safetensors + provenance (the real defense stack).**
> - **safetensors stops (provably):** *code execution on load* — the format can't express code. A
>   guarantee, not a heuristic.
> - **safetensors does NOT stop:** a **backdoored/poisoned** set of weights or a malicious **adapter**
>   — those are just numbers, perfectly valid tensors. Safe *loading* ≠ safe *behavior*.
> - **Provenance (hashes/signatures) stops:** substitution/tampering *if* you verify against a trusted
>   publisher key and pin versions.
> - **Does NOT stop:** a malicious *publisher* (signed malware is still malware), or `trust_remote_code`
>   you opted into.
> - **Attacker adapts:** ship a backdoored-but-valid safetensors model or adapter; compromise or
>   impersonate a publisher; hide code in an allowed remote-code path.
> - **Cost:** conversion effort; signature infra; losing "just works" convenience of remote code.
> - **Takeaway:** layer them — **safe format** (no RCE) + **provenance/signatures** (right artifact
>   from the right publisher) + **behavioral vetting** (M11 detection, trigger testing) + **least
>   privilege at load** (sandbox, no network) — because each covers a different failure the others miss.

## Code

`labs/module-13/supply_chain.py`:
- `MaliciousCheckpoint.__reduce__` returns `(_benign_marker, (...))`; `pickle.load` therefore
  *calls* `_benign_marker` — the RCE primitive, shown inertly.
- `save_load_safetensors` round-trips weights with no code execution (marker stays unwritten).
- `train_malicious_adapter` optimizes an adapter delta minimizing `4·clean_loss + backdoor_loss`,
  yielding a stealthy backdoor; the distinctive out-of-range trigger lets the adapter route it
  without disturbing clean behavior.

## Practical lab

**Lab 13** ([`labs/module-13/`](../../labs/module-13/README.md)) — pickle RCE (inert), safetensors safety,
stealthy malicious adapter. CPU torch + safetensors, ~3s tests.

```bash
py labs/module-13/supply_chain.py
py -m pytest labs/module-13 -q
```

## Exercise

1. **Map the code paths.** For a real (small) model repo, enumerate every load-time code path:
   pickle checkpoints, `trust_remote_code`, tokenizer/processor code, config imports. Which does a
   one-line `from_pretrained` trigger?
2. **Convert & verify.** Convert a pickled checkpoint to safetensors; verify tensor round-trip
   equality; confirm (via the marker technique) that the safetensors path runs no code.
3. **Provenance gate.** Implement a load gate that verifies a SHA-256 (and, conceptually, a
   signature) against a trusted manifest before loading any artifact. Then attempt to bypass it
   (swap the artifact after hashing / TOCTOU) and fix the gate.
4. **Stealth vs ASR.** Sweep $\lambda$ in the adapter objective; plot clean accuracy vs backdoor ASR
   (the stealth frontier). Find the most stealthy adapter that still achieves ASR > 0.9.
5. **Behavioral detection (purple team).** Since clean-eval misses the adapter (M11), build a
   *trigger-probing* detector (test the merged model on candidate trigger patterns / anomaly-scan
   outputs). Show it catches your obvious trigger, then craft a subtler trigger that evades it, and
   write the guarantee box for your full load-time defense stack.

<details><summary>Hint (step 3)</summary>

A hash gate that reads the file to hash it and *then* opens it again to load has a
time-of-check/time-of-use (TOCTOU) window — swap the file in between. Fix by hashing the exact bytes
you load (hash a single opened handle / load-then-verify-in-memory), and pin the manifest to a
signed release. This is the same TOCTOU class as classic filesystem attacks.

</details>

**Deliverable.** The code-path inventory, safetensors conversion+verification, the provenance gate
(+ bypass + fix), the stealth frontier, and the behavioral detector + guarantee box.

## Research paper

No single canonical paper; read the authoritative sources and one incident writeup:
- **safetensors** design docs and **`torch.load(weights_only=True)`** release notes — extract the
  exact safety guarantee (format cannot execute code) vs a recommendation.
- **CWE-502 (Deserialization of Untrusted Data)** — the class behind pickle RCE.
- A model-hub **malicious-pickle** disclosure (e.g., reports of pickle-based malware on public model
  hubs) — read for the real-world delivery: how a "model download" became code execution.
*Reproduce (light):* the lab is the core; extend by scanning a `.pt` file's pickle opcodes
(`pickletools.dis`) to *detect* a `REDUCE`/`GLOBAL` to a dangerous callable — and note why opcode
scanning is a fragile filter vs the format guarantee.

## Further reading

- Hugging Face security docs on `trust_remote_code` and safetensors.
- OWASP LLM03 (Supply Chain); MITRE ATLAS (ML supply-chain compromise); forward link M22 (AI supply
  chain). [`references/standards-map.md`](../../references/standards-map.md).

## What you should now be able to do

- Explain and demonstrate pickle-based RCE and why safetensors/`weights_only` prevent it.
- Enumerate load-time code paths (`trust_remote_code`, tokenizer/config code) and treat model
  artifacts as untrusted code.
- Build a stealthy malicious adapter and understand why clean-eval misses it.
- Design a layered load-time defense: safe format + provenance + behavioral vetting + least privilege.

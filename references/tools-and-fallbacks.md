# External tools & fallback strategy

**No core learning objective depends on a single external repository** (`plan.md` §21, §35).
Every external tool used in a lab follows:

```text
External tool ─▶ Primary lab ─▶ Local minimal reimplementation ─▶ Fallback exercise
```

For each tool we record: **Primary source · Version/date · Purpose · License · Install · Known
failure modes · Fallback · Local alternative.** The local reimplementation is always shippable
in this repo so the lesson survives if the upstream project changes API, breaks, or disappears.

## Registry (filled in as labs are built)

| Tool | Purpose | Used in | Local fallback |
|---|---|---|---|
| **garak** | LLM vulnerability scanner / probes | M08, M24 | our `lab/attack-tools` probe runner |
| **PyRIT** | automated red-teaming orchestration | M25 | our attacker/defender loop |
| **promptfoo** | prompt/eval harness, red-team configs | M24 | our `eval` harness (ASR/precision/recall) |
| **Giskard / Inspect AI** | model testing & eval | M24 | our eval harness |
| **TextAttack** | NLP adversarial attacks | M09–M10 | from-scratch FGSM/PGD/CW on a toy model |
| **ART (Adversarial Robustness Toolbox)** | adversarial ML attacks/defenses | M09–M12 | from-scratch implementations |
| **AI Goat / vulnerable apps** | deliberately vulnerable targets | M16–M18 | our `lab/vulnerable-apps` |
| **MITRE ATLAS / OWASP** | taxonomy & guidance (reference, not code) | M26 | mirrored key tables in `references/` |

## Models

Labs default to **small open-weights models runnable CPU-only** (and a deterministic local
"model shim" for tests, so labs pass in CI without a download). When a lab genuinely needs a
larger model or a GPU, the lab README says so explicitly and provides a reduced-fidelity
CPU fallback that still demonstrates the mechanism.

*Each entry gets its full 8-field record when the corresponding lab is written.*

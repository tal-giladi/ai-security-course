# Lab 25 — Automated red teaming

**Module:** 25 (Stage 9). **Time:** ~2 h. **Hardware:** CPU, offline (shim). Uses the eval harness
`lab/attack-tools/evalkit.py`.

## Goal

Scale red teaming from "one clever prompt" to an automated **search**: generate, mutate/fuzz, and
evolve payloads against a target + judge; then run **attacker vs defender co-evolution** — the
defender adds a filter, the fuzzer rediscovers evasions. Report ASR per round (with CIs from the
harness).

## Run

```bash
py labs/lab-25/redteam.py     # undefended ASR climbs to 1.0; defended keyword filter still gets evaded
py -m pytest labs/lab-25 -q
```

## What to notice

- **Search scales attacks.** A mutation fuzzer over seed payloads + a judge evolves high-ASR attacks
  automatically (builds on PAIR/TAP, M08) — no gradients needed.
- **The judge bounds the attacker** (M08/M24): a weak judge caps the search. Validate it first.
- **Co-evolution is the point.** A keyword filter drops ASR, but the fuzzer finds evading payloads
  (e.g. shouted/duplicated seeds with none of the filtered words). Re-run the red team against *every*
  defense change — a single number is a snapshot, not security.

## Exercise

See [Lesson 25.1](../../lessons/module-25/lesson-01.md): add encoding/obfuscation mutations and
measure ASR with CIs per round; build an "attacker model" (an LLM/heuristic that proposes mutations
from the target's replies, PAIR-style); implement a defender that adapts each round (semantic
detector) and plot the co-evolution ASR curve; assemble an automated exploit *chain* red-teamer
(reuse the agent runtime, M18); write the guarantee box for red-team coverage.

## Reset / Docker

Stateless. `docker compose up` runs the red team with no egress.

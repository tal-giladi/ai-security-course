# Lab 34 — Agent Skills as a supply-chain trust boundary

**For:** lesson [22.2 · Agent skills as a supply-chain trust boundary](../../lessons/module-22/lesson-02.md).
**Time:** ~5 min to run, ~60 min with exercises. **Hardware:** CPU, offline, no Docker required.
**Deps:** Python 3.11+, stdlib only (reuses lesson 22.1's verification gate
`labs/lab-22/supply_chain_graph.py` unchanged, loaded by path).

> [!WARNING]
> **In-process and synthetic.** A "skill script" is a tuple of abstract operations interpreted by
> `World` — **never Python that runs.** Nothing binds to a socket, nothing leaves the process, no
> file is read or written on disk. Confidential values are synthetic `LAB-CANARY-...` markers and
> every attacker destination is a reserved `*.sink.test` name recorded in an in-memory outbox (the
> in-process stand-in for the shared `lab/sink`). Only ever study these techniques against systems
> you are authorised to test.

## Goal

Lesson 22.1 made the supply chain a *graph* of externally-sourced artifacts and built a verification
gate (integrity + provenance + pinning + safe format). An **agent skill** is a new kind of node in
that graph — an installed package of metadata, a natural-language `SKILL.md` instruction body the
agent reads as guidance, and bundled scripts it runs with its own authority. Its "payload" can live
in prose, so a gate that proves the bundle is *authentic* (signed, pinned, byte-identical) does not
prove it is *safe*.

You run four malicious skills, each exercising one trust gap the 22.1 gate passes, and add defenses
one layer at a time, measuring ASR and utility at each step:

| Attack | Gap | Caught by |
|---|---|---|
| A · prose-only exfiltration | payload is instruction-body prose, not a tampered byte | static scanner (intent keywords) |
| B · inspect/execute gap | benign source, a bundled bytecode cache carries a different op | checked-hash loading (rebuild-from-source) |
| C · under-declared capability | body reads outside the declared frontmatter, no keyword to scan | runtime capability enforcement |
| D · cross-skill, cross-session | two in-scope skills split the attack through a shared artifact | cross-skill artifact provenance |

## Run

```bash
py labs/lab-34-skill-supply-chain/attack.py
py -m pytest labs/lab-34-skill-supply-chain -q
```

`docker compose up` in this folder runs it with `network_mode: none`.

## Expected output (deterministic)

```text
defense stack       ASR   utility
none                1.00  1.00
+gate(22.1)         1.00  1.00
+scanner            0.75  1.00
+checked-cache      0.50  1.00
+capabilities       0.25  1.00
+provenance         0.00  0.67
```

The 22.1 gate removes nothing here (every skill is authentically signed and pinned — authenticity is
not safety). Each later control removes exactly one attack. The last layer, origin-only cross-skill
provenance, closes D but also holds the benign `tidy -> publish` hand-off (utility 1.00 → 0.67): a
real false-positive cost, because provenance-by-producer cannot tell an approved hand-off from a
malicious one. Exercise 4 pairs it with a destination allowlist to recover utility.

## Files

- `skills.py` — skill package model, the toy instruction-following model, the five defense layers,
  and the measurement harness. Reuses `labs/lab-22/supply_chain_graph.py` unchanged.
- `attack.py` — the four malicious scenarios + three benign skills; the purple-team driver.
- `test_lab34.py` — acceptance tests (each layer closes exactly its one gap; nothing leaves the
  process).
- `docker-compose.yml` — isolated, no-egress run.

# Lab 18 — End-to-end agent attack chain (webpage → agent → creds → exfil)

**Module:** 18 (Stage 7). **Time:** ~2.5 h. **Hardware:** CPU, offline. Uses `lab/agents/agent.py`.
Synthetic canary; egress → local sink.

## Goal

Build the canonical agent kill chain and defend it *layer by layer*, measuring where each control
bites:

```text
attacker-influenced webpage → agent fetches it → injected directive → agent reads creds.txt
   → creds content injects exfil directive with the SECRET → agent exfiltrates to the sink
```

## Run

```bash
py labs/lab-18/chain.py       # no defense: 3 hops, exfil; egress allowlist: 2 hops; least-priv: 1; approval: 0
py -m pytest labs/lab-18 -q
```

## What to notice

- **A chain is a sequence of trust-boundary crossings (00.1); breaking any one link stops it.**
- **Defenses bite at different hops:** egress allowlist cuts the final exfil hop; least privilege
  (no filesystem for a research agent) cuts the read hop earlier; an approval gate cuts the first
  egress (but also blocks legitimate browsing — a utility cost).
- **Chain depth is a defense metric:** fewer executed hops = the control bit earlier = smaller blast
  radius. Measure it, don't assert it.

## Exercise

See [Lesson 18.1](../../lessons/module-18/lesson-01.md): add a memory-persistence hop (poison the
agent's memory so the attack re-fires next session); combine with RAG poisoning (Lab 14) as the
entry; compute chain-success probability as a product over hops and show defense-in-depth multiplies
difficulty; design the minimal control set that stops the chain while preserving the research task;
write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs the chain with no egress.

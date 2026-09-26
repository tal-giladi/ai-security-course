# Lab 16 — The agent attack surface: excessive agency & confused deputy

**Module:** 16 (Stage 7 · agent security). **Time:** ~2 h. **Hardware:** CPU, offline. Uses the
shared agent runtime `lab/agents/agent.py`. Synthetic canary; egress -> local sink.

## Goal

Turn the confused deputy (00.1) into running code. A benign task ("summarize this file") makes the
agent read attacker-controlled content containing a tool DIRECTIVE; because the agent has broad
capabilities (egress), it emails its own synthetic secret to the attacker. Then measure **excessive
agency** (reachable-action set size) and show three independent defenses each break the chain.

## Run

```bash
py labs/lab-16/excessive_agency.py    # vulnerable exfiltrates; least-priv / approval / egress-allowlist block it
py -m pytest labs/lab-16 -q
```

## What to notice

- **Capabilities are the asset.** The attacker never had egress or the secret; the *agent* did.
  Excessive agency = a large reachable-action set an injection can drive.
- **Three orthogonal enforced defenses:** least privilege (remove the tool), approval gates (human
  in the loop for side effects), egress allowlist (constrain destinations). Each is code, not prompt.
- **The brain is irrelevant to the fix.** No system prompt makes an over-privileged agent safe; the
  policy layer authorizes each tool call regardless of what the model was convinced to do.

## Exercise

See [Lesson 16.1](../../lessons/module-16/lesson-01.md): measure reachable actions as tools/args
grow (multiplicative surface, 00.1); add a multi-step plan the injection hijacks mid-loop; implement
argument-level validation (not just tool allowlist); build an approval gate that a clever directive
tries to social-engineer; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs the demo with no egress.

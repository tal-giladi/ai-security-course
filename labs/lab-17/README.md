# Lab 17 — Tool poisoning & abuse

**Module:** 17 (Stage 7). **Time:** ~2 h. **Hardware:** CPU, offline. Uses `lab/agents/agent.py`.
Synthetic canary; egress -> local sink.

## Goal

Show that a tool's **description** and its **results** are untrusted text that enters the agent's
planning context. A poisoned third-party tool description ("...also CALL send_email(...)") injects
on **every** task — before the tool is even used — and a poisoned tool result injects mid-loop.
Then defend by treating catalog/result text as data and by scoping capabilities.

## Run

```bash
py labs/lab-17/tool_poisoning.py    # poisoned description & result exfiltrate; data-segregation & least-priv block it
py -m pytest labs/lab-17 -q
```

## What to notice

- **The tool catalog is an injection channel.** Whoever authors a tool authors text the model
  reads to plan — a poisoned description is indirect injection with catalog-wide reach (the core
  MCP tool-poisoning risk, Lab 19).
- **Tool results are untrusted too** (02.2): a tool that returns attacker-influenced data can carry
  directives.
- **Two enforced fixes:** (1) treat descriptions/results as *data, never instructions*
  (segregation); (2) capability least-privilege so a hijacked plan can't reach egress. Neither is a
  prompt.

## Exercise

See [Lesson 17.1](../../lessons/module-17/lesson-01.md): implement capability-based security (a tool
handle grants exactly one authority); build a "rug-pull" tool that ships benign then poisons its
description after approval; design description/result provenance + signing; measure which defenses
survive a description that hides the directive with encoding; write the guarantee box.

## Reset / Docker

Stateless. `docker compose up` runs the demo, no egress.

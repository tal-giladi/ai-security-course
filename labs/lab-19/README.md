# Lab 19 — MCP security: malicious servers & cross-server confused deputy

**Module:** 19 (Stage 8 · fast-moving/emerging). **Time:** ~2 h. **Hardware:** CPU, offline.
Synthetic canary; exfil recorded locally. *This module is designed to be updated independently as
MCP evolves.*

## Goal

Model an MCP client connected to a **trusted** server (holds a private resource) and a **malicious**
server. Show that a third-party server's **tool description** is untrusted text in your model's
planning context that (a) fires before its tool is used and (b) can drive *another* server's
privileged tool — a **cross-server confused deputy** that steals private data. Then defend.

## Run

```bash
py labs/lab-19/mcp_lab.py     # trust-all leaks; server allowlist / descriptions-as-data / cross-server gate block it
py -m pytest labs/lab-19 -q
```

## What to notice

- **Tool descriptions = attacker-controlled context** (Lab 17), now from an installed server.
  "Line jumping": the description acts before the tool is ever called, on every task.
- **Cross-server flows are the new boundary.** A malicious server instructing the client to read a
  trusted server's resource and hand it back is a bridge the user never intended.
- **Three defenses:** pin/allowlist servers (don't connect untrusted ones); treat tool metadata as
  data; gate cross-server tool invocations. All enforced in the client, not the model.

## Exercise

See [Lesson 19.1](../../lessons/module-19/lesson-01.md): add a `resources`/`prompts` surface and show
they inject too; implement server pinning by hash/signature and a "rug-pull" server that changes its
tools post-approval; design per-server capability scoping; map to the current MCP spec's auth model;
write the guarantee box. Because MCP moves fast, keep the *principles* and update the specifics.

## Reset / Docker

Stateless. `docker compose up` runs the demo with no egress.

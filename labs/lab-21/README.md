# Lab 21 — Code-agent security

**Module:** 21 (Stage 8). **Time:** ~2 h. **Hardware:** CPU, offline. Uses `lab/agents/agent.py`.
`run_shell` is **inert** (records the command it would run to the local sink); synthetic canary.

## Goal

A coding agent asked to "set up this repo" reads attacker-controlled repo content (README, manifest,
source comments) and has a shell tool (= arbitrary code execution). A poisoned README directive
drives it to exfiltrate its secret. Reproduce it, defend it, and model **dependency confusion**.

## Run

```bash
py labs/lab-21/code_agent.py   # trust-repo exfiltrates; repo-as-data / no-shell / approval block it; pinning beats dep-confusion
py -m pytest labs/lab-21 -q
```

## What to notice

- **A repo is untrusted input.** README, `package.json` postinstall, source comments, issues, and PRs
  are all attacker-controlled text a coding agent reads — indirect injection (M05) into a shell-capable
  agent is the worst case.
- **Enforced defenses:** treat repo content as data (segregation); least privilege (no shell if not
  needed); sandbox the shell (no egress/no secrets); command allowlist; human approval for shell.
- **Dependency confusion:** an unpinned resolver picks the highest version across registries, so an
  attacker publishing a higher-versioned public package wins. **Pin** to a trusted registry/version.

## Exercise

See [Lesson 21.1](../../lessons/module-21/lesson-01.md): add a malicious `postinstall` script and a
source-comment injection; sandbox `run_shell` (no network, no secret in env) and show it neuters the
exfil even if invoked; build a command allowlist and evade it; reproduce dependency confusion end to
end with lockfile pinning + integrity hashes; write the guarantee box. Never point the agent at real
external systems.

## Reset / Docker

Stateless. `docker compose up` runs the demo with no egress.

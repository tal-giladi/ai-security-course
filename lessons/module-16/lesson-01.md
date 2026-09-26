<div class="prereq">

**Prerequisites.** [00.1 confused deputy / threat modeling](../module-00/lesson-01.md),
[05.1 indirect injection](../module-05/lesson-01.md), [02.2 tool calling = model emits request /
your code authorizes](../module-02/lesson-02.md). **Sibling:** agents / tool use (M18–M19). Lab:
shared agent runtime, offline.

**You will learn.** The agent attack surface — loops, planning, memory, external state, tools,
credentials — and the two organizing concepts: **excessive agency** (an over-large reachable-action
set an injection can drive) and the **confused deputy** as *executable* behavior. Plus the enforced
defenses: least privilege, capability policy, approval gates, egress control.

**Why this matters.** Agents are where LLM security stops being about text and starts being about
*actions with real consequences* — files read, emails sent, code run, money moved. This is the
largest and most consequential stage of the course, and its core lesson is simple and unforgiving:
**an agent can be made to do anything it is capable of doing.**

</div>

# 16.1 · The agent attack surface

## Why this matters

Everything so far could, at worst, make a model *say* something. An agent can *act*. The moment you
give a model tools, its capabilities become the attacker's capabilities the instant an injection
lands (M05/M06) — and injections land through everything the agent reads. The security question is
no longer "will it say something bad?" but "what is the worst thing it is *able* to do, and who
controls that?"

## Learning objectives

1. Map the agent attack surface: the observe→decide→act loop, planning, memory, external state,
   tools, credentials.
2. Define **excessive agency** and measure it as the reachable-action set; connect to the
   multiplicative attack-surface argument (00.1).
3. Explain the **confused deputy** as executable behavior: an injected directive drives the agent's
   own privileged tools.
4. Apply enforced defenses — **least privilege** (tool/arg allowlists), **capability-based
   security**, **human-in-the-loop approval gates**, **egress control** — and know each is code, not
   prompt.
5. Reason about **memory** and **multi-step** attacks (persistence, mid-plan hijack).

## Concept

### The loop and its surfaces

```text
        ┌─────────────── agent loop ───────────────┐
task ─▶ │ observe (context, memory, tool results) → │
        │ decide (LLM picks a tool + args) →        │
        │ act (execute tool) → observe result →     │  repeat
        └───────────────────────────────────────────┘
   tools: read_file, http_get, send_email, run_code, ...   credentials, external state
```

Every arrow is a surface:
- **observe:** ingests untrusted content (files, web, tool results, other agents, memory) — every
  injection channel from M05/M06 feeds the *decide* step.
- **decide:** the model chooses tool+args; attacker-influenced context steers the choice (02.2 —
  the schema constrains shape, not intent).
- **act:** executes with the agent's privileges/credentials — the consequence.
- **memory:** persists across turns; a poisoned memory is a *persistent* injection (M18).
- **multi-step:** an injection can hijack the plan mid-loop, chaining tools.

### Excessive agency

**Excessive agency** (OWASP LLM06) = the agent can perform more actions than the task requires, so a
successful injection has a large blast radius. Quantify it as the **reachable-action set**: the tools
(and argument ranges) the policy permits. From 00.1, attack surface grows *multiplicatively* in
(untrusted input locations × reachable privileges); every tool added is reachable from *every*
injection channel. The lab prints this set: a 5-tool agent exposes read/egress/email/shell; removing tools
shrinks it directly.

### The confused deputy, now executable

The agent holds privileges (egress, credentials, filesystem) the attacker lacks. An injected
directive in content the agent reads makes the agent use *its own* privilege on the attacker's
behalf — email the secret, fetch an internal URL (SSRF via a tool, M01), delete a file. Lab: reading
a poisoned `notes.txt` triggers `send_email(secret → attacker)` to the sink. The agent "intended" to
summarize; it was a confused deputy.

## Intuition

Giving an agent a tool is giving an impressionable, literal-minded intern a key. Give them the
building master key "for convenience" and every note they read — including one a stranger slipped
into their inbox — is a potential instruction to use it. You do not make the intern safe by telling
them to be careful (they're persuadable, 02.1); you make them safe by only handing them the *specific*
keys the task needs, requiring a manager's sign-off to open sensitive doors, and ensuring the doors
only lead to approved rooms. Least privilege, approval gates, egress control — keys, sign-offs, and
rooms.

## Technical explanation & Code

`lab/agents/agent.py` (shared) + `labs/lab-16/excessive_agency.py`:
- The `Agent` has tools (`read_file`, `http_get`, `send_email`, `whoami`), a synthetic `secret`, and
  a `Policy`.
- The **brain** scans context for `CALL tool(args)` directives (a transparent stand-in for a
  tool-calling LLM) and issues them — *subject to the policy*.
- `Policy.authorize` is the **enforced boundary**: tool allowlist, egress-host allowlist, approval
  gates. It runs on every tool call regardless of the brain.
- The lab shows the vulnerable agent exfiltrating, then three policies each blocking it, and prints
  the reachable-action set as the excessive-agency metric.

Swap the rule-engine brain for a real tool-calling LLM behind the same interface — the *policy* is
what matters for security, and it is model-agnostic.

## Mathematics

**Blast radius = reachable actions × injection channels.** Let $C$ be the number of untrusted input
channels the agent observes and $A$ the number of reachable (tool, arg-class) actions. A single
successful injection can drive any reachable action, so the number of distinct attacker-achievable
(channel → action) effects is $\Theta(C\cdot A)$. Least privilege reduces $A$ (and argument
validation reduces the effective arg-classes per tool); provenance/segregation reduces effective $C$.
Because the product is multiplicative, **removing one high-impact tool (e.g. egress) can cut blast
radius more than hardening many channels** — the quantitative case for capability minimization first.

**Approval gates and expected loss.** If a side-effectful action requires human approval that catches
a fraction $q$ of malicious calls, the residual success probability of that action is $(1-q)$, and
expected loss scales accordingly — but $q<1$ (humans approve-fatigue), so gates are a *reduction*,
best combined with least privilege that makes the dangerous action unreachable in the first place.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — the agent policy layer (least privilege + egress allowlist + approval).**
- **Stops:** any tool call outside the allowlist, egress to non-approved hosts, and (via gates)
  un-approved side effects — *regardless of what the brain was convinced to do*. Enforced in code
  (02.1), so it holds even under a fully hijacked model.
- **Does NOT stop:** misuse *within* granted capabilities (a tool the task legitimately needs can
  still be driven maliciously within its allowed args), over-broad allowlists, approval fatigue
  (humans rubber-stamping), or attacks on the policy/approver itself.
- **Attacker adapts:** operate within allowed tools/args; craft directives that look benign to the
  approver (social-engineer the human); target over-provisioned agents.
- **Cost:** capability minimization can reduce functionality; approval gates add latency/human load;
  maintaining allowlists is operational work.
- **Takeaway:** the policy layer is the real boundary and must be minimal and enforced in code;
  prompt-level "be careful" is not a control. Combine with input provenance (M05/M06) and monitoring
  (M23) — you cannot prevent the model from being persuaded, only bound what a persuaded model can do.

</div>

## Practical lab

<div class="lab">

**Lab 16** ([`labs/lab-16/`](../../labs/lab-16/README.md)) — confused-deputy exfiltration + three
enforced defenses. Offline, shared agent runtime.

```bash
py labs/lab-16/excessive_agency.py
py -m pytest labs/lab-16 -q
```

</div>

## Exercise

1. **Measure agency.** Add tools/argument classes and plot the reachable-action set and the
   $C\cdot A$ blast-radius estimate. Show that removing egress cuts blast radius more than adding an
   input filter.
2. **Argument-level authorization.** The tool allowlist permits `read_file`; show it can still be
   abused (`read_file('/etc/shadow')`-style path). Add argument validation (path scoping, URL
   allowlist) and demonstrate it blocks the abuse while allowing legitimate use.
3. **Multi-step hijack.** Craft a poisoned tool result that appears mid-loop and hijacks the plan
   (e.g., `read_file` returns content that triggers `http_get` then `send_email`). Show the chain,
   then show which single policy control breaks it earliest.
4. **Approval-gate social engineering (purple team).** Build an approver that approves "routine"
   emails; craft a directive whose args look routine but exfiltrate the secret (encode it, or send to
   a look-alike domain). Then harden the approver (canary/secret detection in args, strict recipient
   allowlist) and re-measure.
5. **Least-privilege design.** For a realistic assistant task (summarize + notify a teammate), derive
   the *minimal* tool/arg/egress policy that supports the task and blocks the lab's attacks. Justify
   each capability. Write the guarantee box.

<details><summary>Hint (step 3)</summary>

The agent observes each tool's result and continues; a directive in a *result* is just as effective
as one in the initial file (that's why the loop is the surface). The earliest-breaking control is
usually egress/least-privilege on the *final* dangerous action — even if the injection hijacks the
plan, it can't complete the exfiltration if the terminal capability is unreachable.

</details>

**Deliverable.** The agency/blast-radius measurements, argument-level authorization, the multi-step
hijack + earliest-breaking control, the approval social-engineering + hardening, and the minimal
least-privilege policy + guarantee box.

```bash
py course.py complete 16.1
```

## Research paper

**OWASP "LLM06: Excessive Agency"** (LLM Top 10) and the emerging **OWASP Agentic AI / Agentic
Threats** guidance. *Why:* the industry framing of the exact risk you built — too much capability,
insufficient authorization/oversight. *Read:* the definition of excessive agency and the recommended
mitigations (minimize functionality/permissions, require approval for high-impact actions, complete
mediation). *Also:* Greshake et al. (M05) for how the injection *reaches* the agent. *Reproduce:* the
lab is the executable version; map each OWASP mitigation to a `Policy` control and test it. *Limits:*
real agents have many tools and long horizons — blast radius and approval fatigue are worse at scale.

## Further reading

- Capability-based security (object-capability model) — the principled framing of "authority = the
  reference you hold". Maps directly to tool handles/policies. Deep-dive in M17.
- MITRE ATLAS (execution, exfiltration via ML systems); [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. What is excessive agency and how do you measure it?</summary>

An agent able to perform more actions than the task requires, so a successful injection has a large
blast radius. Measure it as the reachable-action set (tools × permitted argument classes the policy
allows). It grows multiplicatively with input channels, so minimizing capabilities is high-leverage.

</details>

<details><summary>Q2. Why is the agent a confused deputy, and why doesn't a system prompt fix it?</summary>

The agent holds privileges (egress, credentials) the attacker lacks; an injected directive in
content the agent reads makes it use those privileges for the attacker. A system prompt is a
finite-bias prior (02.1) that a strong injection overcomes; the fix is an enforced policy that
authorizes each tool call in code, independent of what the model was convinced to do.

</details>

<details><summary>Q3. Give three orthogonal enforced defenses and what each stops.</summary>

Least privilege (remove/deny tools — makes the dangerous action unreachable); egress allowlist
(constrain destinations — blocks exfiltration even if the tool runs); approval gates (human sign-off
on high-impact side effects — catches a fraction of malicious calls). All are code-level and hold
under a hijacked model; combine them.

</details>

<details><summary>Q4. Why does removing one egress tool often beat adding an input filter?</summary>

Blast radius scales as (input channels × reachable actions). An input filter reduces channels
probabilistically and partially; removing a high-impact reachable action (egress) eliminates a whole
column of the product deterministically — a persuaded model simply cannot complete exfiltration if
the terminal capability doesn't exist.

</details>

## What you should now be able to do

- Map the agent loop's attack surfaces and measure excessive agency as the reachable-action set.
- Reproduce a confused-deputy exfiltration through an agent's tools and explain why prompts don't fix it.
- Apply least privilege, argument-level authorization, egress control, and approval gates as enforced,
  model-agnostic policy.
- Reason about multi-step/memory hijacks and design a minimal capability policy for a task.

## Progress checkpoint

```bash
py course.py complete 16.1
py course.py next
```

**Next:** 17.1 · Tool poisoning & abuse — malicious tool descriptions and results, tool
authorization, and capability-based security (least authority for tools).

<div class="prereq">

**Prerequisites.** None beyond being an experienced software engineer. No ML background is
needed for this lesson. If you have started the sibling
[LLM Research Engineer](https://tal-giladi.github.io/llm-research-engineer-course/) course you
already know what a transformer and a tool-calling agent are; if not, treat the LLM as a black
box that maps text in → text out and sometimes calls tools. That is enough here.

**You will learn.** How to systematically find where an AI system can be attacked *before*
knowing any specific attack: assets, trust boundaries, data flows, privilege, the
authentication/authorization split, isolation, and the confused-deputy pattern — and why LLM
and agent systems break the assumptions that classical threat modeling relies on.

**Why this matters.** Every later module (prompt injection, RAG poisoning, agent hijacking, MCP)
is a *specific* instance of a boundary being crossed. If you can draw the boundaries, you can
predict the attacks on a system you have never seen — which is the entire goal of this course.

</div>

# 00.1 · Threat modeling for AI systems

## Why this matters

A junior security engineer learns a list of attacks and checks for each one. A security
*researcher* does the opposite: they look at a system, find the boundaries that are supposed to
hold, and ask *"what makes this boundary fail?"* The attacks fall out of the boundaries.

This inversion is the single most valuable habit in the whole course. When you are handed a new
agent framework in two years that does not exist today, you will not have a checklist for it.
You will have the ability to draw its trust boundaries and reason about how they break. That is
what this lesson trains.

## Learning objectives

By the end you can:

1. Enumerate the **assets** of an AI system and say who must not be able to reach each one.
2. Draw a **data-flow diagram** and mark every **trust boundary** on it.
3. Apply **STRIDE** and an **attack tree** to an LLM application.
4. Explain **authentication vs authorization**, **privilege**, and **isolation** precisely, and
   why "the model decides" quietly destroys all three.
5. Recognize the **confused-deputy** pattern — the structural core of most LLM/agent attacks.
6. Produce a written threat model for the course's toy vulnerable app.

## Concept

**Threat modeling** is the disciplined answer to four questions:

```text
1. What are we building?         (a model of the system)
2. What can go wrong?            (threats against that model)
3. What are we going to do?      (mitigations)
4. Did we do a good job?         (validation — the whole rest of this course)
```

Everything hinges on step 1. A threat model built on a wrong or incomplete system model finds
the wrong threats. So we spend most of this lesson learning to build the model precisely, using
the vocabulary that the rest of the course reuses constantly.

### Assets

An **asset** is anything an attacker wants, or anything whose integrity/availability you must
protect. In an AI system the usual assets are:

- **Secrets** — API keys, database credentials, OAuth tokens, the system prompt itself.
- **Data** — user data, other tenants' data, training data, retrieved documents.
- **Capabilities** — the ability to call a tool, send an email, run code, spend money, write to
  a database. In agent systems, *capabilities are often the most valuable asset*, more than any
  single datum.
- **Model behavior** — the guarantee that the model refuses certain actions, stays on task, and
  does not leak its instructions.
- **Availability & budget** — tokens, GPU time, rate limits, money.

For each asset, write down the one sentence that matters: *who is allowed to reach it, and who
must not.* That sentence is the boundary you will spend the rest of the course attacking and
defending.

### Trust boundaries and data flows

A **trust boundary** is a line in the system across which the level of trust changes. Data that
was untrusted on one side is often *implicitly* treated as trusted on the other — and that
implicit promotion is where attacks live.

A **data-flow diagram (DFD)** makes boundaries visible. Its elements:

- **External entity** (rectangle) — a user, a website, an email sender, another service.
- **Process** (circle) — code that transforms data: the app server, the LLM, a tool.
- **Data store** (open box) — a database, a vector store, a file, the agent's memory.
- **Data flow** (arrow) — data moving between the above.
- **Trust boundary** (dashed line) — drawn wherever trust level changes.

Here is a minimal LLM application as a DFD (ASCII; you will draw real ones):

```text
                         ┌────────── trust boundary ──────────┐
   [User] ──prompt──▶  ( App server ) ──system+user msg──▶ ( LLM )
                              │                                │
                              │◀──────────── response ─────────┘
                              ▼
                        {  Database  }
```

Now the same app once it can **retrieve** documents and **call a tool** — the two additions that
create almost every LLM vulnerability:

```text
   [User] ──▶ ( App ) ──▶ ( LLM ) ──tool call──▶ ( Tool ) ──▶ [External API / files]
                 ▲            ▲
                 │            │ retrieved text (UNTRUSTED, treated as instructions?)
                 │        {Vector store} ◀── ingest ── [Web pages / emails / uploads]
                 └───────────────────────────────────────── response
```

Mark the boundaries and one fact jumps out: **text arriving from the web/email/uploads is
untrusted, but once it is retrieved and placed into the LLM's context, the model cannot tell it
apart from your trusted instructions.** That single collapsed boundary *is* indirect prompt
injection (Module 05). You found the attack by drawing the diagram — before we ever named it.

### Privilege, authentication, authorization, isolation

Four classical terms, stated precisely because LLM systems abuse all four:

- **Privilege** — the set of actions a component is *allowed* to perform. **Least privilege**:
  each component gets the minimum it needs. An agent with filesystem + network + shell has
  enormous privilege; that is a design choice, not a fact of nature.
- **Authentication (authn)** — *who are you?* Verifying identity (a password, a token, a key).
- **Authorization (authz)** — *are you allowed to do this?* Checking that an authenticated
  identity may perform a specific action on a specific resource.
- **Isolation** — preventing one component/tenant/request from affecting another (process
  sandboxes, containers, network segmentation, per-tenant data partitioning).

<div class="callout key">

**The AI-specific twist.** In a classical web app, the *code* enforces authz: a handler checks
`if (user.canRead(doc))` before returning a document. In many LLM apps, the decision of *what to
do* is delegated to the model: the LLM chooses which tool to call, which document to cite, what
to include in the answer. When "the model decides," you have moved an authorization decision
from deterministic code into a statistical text predictor that an attacker can influence with
input. Authorization that can be talked out of is not authorization.

</div>

### The confused deputy — the pattern under most LLM/agent attacks

A **confused deputy** is a program that holds a privilege and is tricked by a less-privileged
party into misusing it on their behalf. The classic 1988 example: a compiler that can write to a
protected billing file is asked by a user to write its output to that file's path — the compiler
has the privilege, the user does not, and the compiler is *confused* into using its privilege
for the user.

Map this onto an LLM agent:

```text
Attacker (low privilege)                Agent/LLM (HIGH privilege: reads files, calls tools,
   │  plants text in a web page            holds the API key, can send email)
   ▼
[Web page] ──retrieved──▶ ( Agent ) ──"as instructed, email the file to X" ──▶ ( Email tool )
```

The attacker never had permission to read your files or send email. The **agent** did. The
attacker only had to place text where the agent would read it and treat it as an instruction.
Every indirect prompt injection, every tool-poisoning attack, every RAG-driven exfiltration in
this course is a confused-deputy attack. Learn the shape now and you will recognize it everywhere.

## Intuition

If you remember one picture from this lesson, remember this: **an LLM turns its entire context
window into one undifferentiated instruction stream.** System prompt, user message, retrieved
document, tool output — to the model they are all just tokens competing to influence the next
token. Classical security assumes a hard line between *code* (instructions) and *data* (inputs);
the CPU will never execute your CSV file as machine code. LLMs erased that line: in an LLM,
data *is* code, because any text in context can steer behavior. Threat modeling an AI system is
largely the exercise of finding every place where untrusted data enters that stream, and every
privilege the stream can reach.

## Technical explanation

### STRIDE, applied to an LLM app

STRIDE is a checklist of six threat categories. For each element of your DFD, ask whether each
applies. Here it is instantiated for the retrieval + tool app above:

| STRIDE threat | Classical meaning | LLM/agent instance |
|---|---|---|
| **S**poofing | pretending to be someone | injected text impersonating the system prompt or a tool result |
| **T**ampering | unauthorized modification | poisoning a retrieved document or the vector store |
| **R**epudiation | denying an action | no audit log of *why* the agent called a tool |
| **I**nformation disclosure | leaking data | system-prompt leak, cross-tenant retrieval, secret exfiltration |
| **D**enial of service | making it unavailable | token-exhaustion prompts, retrieval DoS, infinite tool loops |
| **E**levation of privilege | gaining capability | talking the agent into calling a tool it should not, confused deputy |

Notice that **every** category has a natural LLM instance, and several map to attacks we will
build. STRIDE is not the answer; it is a systematic way to make sure you did not forget a
category while enumerating.

### Attack trees

An **attack tree** decomposes a goal into the ways to achieve it. Root = attacker goal; children
= sub-goals; leaves = concrete actions. OR-nodes (any child suffices) and AND-nodes (all
children required). Example, goal = *exfiltrate the synthetic API key the agent holds*:

```text
GOAL: exfiltrate LAB-CANARY key held by the agent
├── OR  Read it directly
│   ├── Get the model to print its system prompt (M04)
│   └── Get a tool to return the key into context, then into the answer (M17)
├── OR  Have the agent send it out (confused deputy)
│   ├── AND
│   │   ├── Place an instruction where the agent reads it (indirect injection, M05)
│   │   └── Agent has an egress-capable tool (email/http) — privilege (M16)
│   └── Poison a retrieved doc so the citation carries the key to the sink (M14/M18)
└── OR  Extract it from logs/telemetry (M01, misconfig)
```

The tree tells you *which boundaries to harden first* (the shallow, high-probability leaves) and
gives you a ready-made test plan: each leaf is a lab. We will literally build several of these
leaves against the toy app.

## Mathematics

Threat modeling is mostly structural, but two quantitative ideas recur and are worth stating now
because later modules make them precise.

**1. Risk as expected loss.** A common working definition:

$$ \text{Risk} = P(\text{attack succeeds}) \times \text{Impact}. $$

This is why *attack success rate* (ASR) — which we measure constantly from Module 24 — is not an
academic number: it is the $P$ in your risk. A defense that lowers ASR from $0.9$ to $0.3$ cuts
risk by $\approx 67\%$ for that threat, holding impact fixed. When comparing defenses you are
comparing their effect on this product, against their false-positive and performance cost.

**2. Attack surface as a set, and monotonicity of privilege.** Model the attack surface as the
set $S$ of (untrusted-input-location, reachable-privilege) pairs. Adding a tool $t$ with
privilege set $\Pi_t$ to an agent that already reads untrusted input from locations $L$ adds up
to $|L| \times |\Pi_t|$ new pairs. Surface grows *multiplicatively* in (input locations $\times$
privileges), not additively — the formal reason least privilege matters so much for agents, and
why "just add one more tool" is rarely just one more risk. You will re-derive this intuition
concretely when you count reachable actions in the agent labs (M16).

We keep the heavy mathematics (optimization for jailbreaks, likelihood-ratio tests for
membership inference, information-theoretic leakage) for the modules where it earns its place.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — the pattern used on every defense in this course.** Threat modeling
itself is a *process*, not a control, but apply the lens now so it becomes reflex:

- **What it gives you:** a systematic enumeration of boundaries and threats, so you attack/defend
  deliberately instead of guessing.
- **What it does NOT give you:** any guarantee that a boundary actually holds. A model on paper
  can miss a data flow that exists in code. It finds *candidate* threats, not proofs.
- **How an attacker adapts:** by using a flow you did not draw (a hidden retrieval path, an
  unlogged tool, a debug endpoint). Threat models rot as systems change.
- **Cost:** time, and the discipline to redraw the model when the system changes. Cheap relative
  to any incident; worthless if done once and filed away.

</div>

## Real-world examples

- **Indirect prompt injection via retrieved content** (Greshake et al., 2023) is exactly the
  collapsed boundary in our second DFD: untrusted web/email text enters the model's instruction
  stream. Paper guide in Module 05.
- **Excessive Agency** is its own category in the OWASP Top 10 for LLM Applications (LLM06) —
  the industry's recognition that over-privileged agents are a first-class risk, i.e. the
  privilege column of your threat model.
- **The confused-deputy framing** predates AI by decades (Hardy, 1988) yet describes agent
  attacks perfectly; part of why this course insists you learn the classical pattern.

## Code

No exploit here — this is the modeling lesson. But threat models should be *checkable
artifacts*, not prose you forget. Below is a tiny, dependency-free way to represent a threat
model as data and mechanically flag the highest-risk items. You will extend this in the exercise.

```python
# threat_model.py — a threat model as data you can query. Standard library only.
from dataclasses import dataclass, field

@dataclass
class Threat:
    id: str
    stride: str                 # one of S T R I D E
    asset: str                  # what is at risk
    boundary: str               # which trust boundary is crossed
    entry: str                  # where untrusted input enters
    privilege: str              # what capability the attack reaches
    p_success: float            # rough P(attack succeeds), 0..1  (refined by measurement later)
    impact: int                 # 1..5
    mitigation: str = ""        # empty = unmitigated

    @property
    def risk(self) -> float:    # Risk = P(success) x Impact  (see Mathematics)
        return self.p_success * self.impact

@dataclass
class ThreatModel:
    system: str
    threats: list[Threat] = field(default_factory=list)

    def unmitigated(self) -> list[Threat]:
        return [t for t in self.threats if not t.mitigation]

    def by_risk(self) -> list[Threat]:
        return sorted(self.threats, key=lambda t: t.risk, reverse=True)

if __name__ == "__main__":
    tm = ThreatModel("toy vulnerable LLM app (retrieval + email tool)")
    tm.threats += [
        Threat("T1", "I", "system prompt", "user->LLM", "user prompt",
               "read system prompt", 0.8, 3),
        Threat("T2", "E", "email-send capability", "web->vectorstore->LLM",
               "poisoned retrieved doc", "send email (egress)", 0.7, 5),
        Threat("T3", "I", "other tenant data", "retriever->LLM",
               "missing authz on retrieval", "read other tenant docs", 0.5, 5),
    ]
    print(f"System: {tm.system}\n")
    print("Top risks (Risk = P x Impact):")
    for t in tm.by_risk():
        flag = "UNMITIGATED" if not t.mitigation else "ok"
        print(f"  {t.id} [{t.stride}] risk={t.risk:.1f}  {t.asset:22} <- {t.entry:24} [{flag}]")
```

Running it ranks T2 (confused-deputy email exfiltration, risk $3.5$) above T1 (prompt leak, risk
$2.4$) — which is exactly the order in which you should harden the toy app. The point: a threat
model you can *run* stays honest as the system grows.

## Practical lab

<div class="lab">

**Lab 00.1 — Threat-model the toy app.** No Docker or GPU required; pure modeling +
`threat_model.py`. Expected time: 60–90 minutes. The toy vulnerable app itself ships with the
Module 04 lab (`labs/lab-04`); for this lesson you model it from the specification below, which
is all a threat model ever starts from anyway.

**System under model.** A customer-support LLM assistant:
- Users chat with it (authenticated by a session token).
- It **retrieves** from a vector store built by ingesting uploaded PDFs and crawled help-center
  web pages (untrusted).
- It can call two tools: `lookup_order(order_id)` (reads an orders DB) and
  `send_email(to, body)` (egress).
- It holds a synthetic secret `LAB-CANARY-<uuid>` in its system prompt (a stand-in for a real
  key), which must never leave the system.
- It is multi-tenant: each user must only ever retrieve their own company's documents.

</div>

## Exercise

Complete **all** of the following. A threat model is not "done" until it is written down and
its top risks are ranked — mirroring how a real engagement produces a deliverable.

1. **Draw the DFD.** By hand or in text, draw the system above with every process, data store,
   external entity, data flow, and **trust boundary**. You must have at least three boundaries.
2. **Enumerate assets** and, for each, write the one sentence: *who may reach it, who must not.*
3. **Run STRIDE** over each DFD element. Produce at least **eight** distinct threats. For each,
   record the STRIDE letter, the asset, the boundary crossed, where untrusted input enters, and
   the privilege reached.
4. **Encode them** in `threat_model.py` (extend the `__main__` block) and print them ranked by
   risk. Assign your own $P$ and impact and justify each in a comment.
5. **Build one attack tree** for the goal *"exfiltrate the LAB-CANARY secret"* with at least two
   OR-branches and one AND-node. Map each leaf to the module where you expect to build it.
6. **Reasoning question (write 3–5 sentences):** the app adds a `run_python(code)` tool for
   "advanced analytics." Using *only* the multiplicative attack-surface argument from the
   Mathematics section, explain what happens to the attack surface and which existing threats
   become more severe. Do not just say "it's dangerous" — quantify the growth in
   (entry × privilege) pairs and name the specific threats whose impact rises.

<details>
<summary>Hint (open only after attempting)</summary>

For step 3, walk the DFD element by element and force yourself to consider each STRIDE letter
even when it seems not to apply — that is where forgotten threats hide. For step 6: before the
tool there were $N$ untrusted entry points reaching a fixed privilege set; `run_python` adds a
privilege (arbitrary code execution) reachable from *every* existing entry point, so the new
(entry × privilege) pairs are $\approx N$, and any threat whose entry is an injection point now
also reaches code execution — recompute impact for T2-style confused-deputy threats.

</details>

**Deliverable.** A `threat-model-00.1.md` in your notes plus the extended `threat_model.py`
output. Mark the lesson complete only once both exist:

```bash
py course.py complete 00.1
```

## Research paper

**Kai Greshake et al., "Not what you've signed up for: Compromising Real-World LLM-Integrated
Applications with Indirect Prompt Injection" (2023).** *Why now:* it is the paper that turned the
"data becomes instructions" boundary collapse into a documented, real-world attack class —
exactly the boundary you drew in the second DFD. *What to read for this lesson:* the threat model
and system diagrams (Sections 2–3); you do not need the specific payloads yet (Module 05).
*What to notice:* their attacker capabilities are stated as *where they can place text*, not as
special access — the confused-deputy shape. Full guide arrives with Module 05.

## Further reading

- Adam Shostack, *Threat Modeling: Designing for Security* — the canonical treatment of DFDs and
  STRIDE. Read the "four questions" framing and the DFD chapter.
- Norm Hardy, "The Confused Deputy" (1988) — two pages; read all of it.
- OWASP Top 10 for LLM Applications (2025) — skim now for the category names (especially LLM01,
  LLM06, LLM08); we map every one to a lab in `references/standards-map.md`.

## Assessment

<details><summary>Q1. Why does the classical code/data boundary fail inside an LLM?</summary>

Because the model consumes its entire context window as one instruction stream: system prompt,
user text, retrieved documents, and tool outputs all influence the next token. There is no
mechanism that marks some tokens as "data, never instructions," so any text in context can steer
behavior. In classical systems the CPU never executes a data file as code; in an LLM, data *is*
potential code.

</details>

<details><summary>Q2. State the confused-deputy pattern and give the LLM-agent instance.</summary>

A privileged program is tricked by a less-privileged party into misusing its privilege on the
party's behalf. LLM instance: an attacker who cannot read your files or send email places an
instruction where the agent will read it (a web page, an email, a retrieved doc); the agent,
which *does* hold those privileges, carries out the instruction — exfiltrating the file or
sending the email for the attacker.

</details>

<details><summary>Q3. An agent gains a second egress tool. Why is this worse than "one more tool"?</summary>

Attack surface grows multiplicatively in (untrusted entry points × reachable privileges). A new
egress privilege is reachable from *every* existing untrusted entry point, so it adds on the
order of $N$ new (entry × privilege) pairs, and it raises the impact of every confused-deputy
threat that previously had no way out. It is one tool but many new attack paths.

</details>

<details><summary>Q4. Why is "the model decides which document to return" an authorization problem?</summary>

Because an authorization decision (may this user see this document?) has been moved from
deterministic, testable code into a statistical text predictor that attacker-controlled input
can influence. Authorization that can be argued with — via a crafted prompt or a poisoned
retrieved doc — is not authorization. The check must live in code outside the model.

</details>

## What you should now be able to do

- Draw a data-flow diagram of an AI system and mark its trust boundaries.
- Enumerate assets and state, per asset, who may and may not reach it.
- Run STRIDE and build an attack tree for an LLM/agent application.
- Use privilege / authn / authz / isolation precisely, and spot where "the model decides"
  dissolves them.
- Recognize the confused-deputy pattern as the skeleton of most attacks in this course.
- Represent a threat model as runnable, rankable data.

## Progress checkpoint

```bash
py course.py complete 00.1
py course.py next
```

**Next:** [01.1 · AppSec primitives AI systems inherit](../module-01/lesson-01.md) — the specific
classical vulnerabilities (injection as a class, SSRF, code execution, secrets, supply chain)
that reappear, unchanged, inside LLM and agent systems.

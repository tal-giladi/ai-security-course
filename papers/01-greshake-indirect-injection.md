# Greshake et al. — *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (2023)

**arXiv:** [2302.12173](https://arxiv.org/abs/2302.12173) · AISec '23. **Modules:** [05.1](../lessons/module-05/lesson-01.md), [06.1](../lessons/module-06/lesson-01.md), [16.1](../lessons/module-16/lesson-01.md). **Lab:** [Lab 05](../labs/lab-05/README.md).

## Why it matters
This is the paper that named and demonstrated **indirect prompt injection**: the attacker never talks to the model, they plant instructions in *content the model will later retrieve* — a web page, an email, a document, a tool result. It reframed prompt injection from "user says a naughty thing" to a **supply-chain problem for context**, and it is the single most load-bearing threat model for every RAG and agent lesson in this course. The confused-deputy framing you build in M05/M16 is this paper made executable.

## Prerequisites
- Sibling course: RAG and tool-use basics (retrieval, tool calling).
- This course: [02.1 boundaries](../lessons/module-02/lesson-01.md) (why a system prompt is a prior, not a wall), [04.1 direct injection](../lessons/module-04/lesson-01.md).

## What to understand
- **Delivery ≠ authorship.** The attacker controls data the application *chooses* to put in context. Trust is assigned by position in the prompt, but provenance is not preserved — the model cannot tell retrieved text from your instructions.
- The **threat taxonomy**: information gathering, fraud, malware/spreading, intrusion, manipulation. The important idea is *reachability* — once injected text is in context, it inherits the application's capabilities.
- **Multi-stage / wormable** injections: injected content that causes the agent to write more injected content (propagation), a concept M06/M18 build on.

## Which sections to read
- §3 (threat model and injection vectors) — the taxonomy of *where* untrusted content enters.
- §4 (attack scenarios) — read as a menu of capabilities-times-channels, not tricks.
- §5 demos — skim; the mechanism matters more than the specific 2023 products.

## Experiment to reproduce (locally)
Lab 05 is the reproduction: a document with a hidden directive drives the agent's `send_email` tool to exfiltrate a `LAB-CANARY` secret to the local sink. Extend it: add a second document whose payload *rewrites the agent's notes*, so a later run re-triggers the attack — a minimal wormable/persistent injection against the shared agent runtime.

## Code to implement
- A provenance-tagging wrapper: mark every context span with its source (`system`/`user`/`retrieved`/`tool`) and log which span the model's tool call was "caused" by.
- A retrieved-content firewall (spotlighting/delimiting) and then **break your own firewall** — the guarantee-box exercise.

## Limitations
- 2023 product demos are dated; treat them as existence proofs, not a current inventory.
- No principled defense — the paper opens the problem; mitigation is empirical.

## What later research changed
- **Wallace et al.** ([02](02-wallace-instruction-hierarchy.md)) proposed training-time instruction hierarchy as a partial mitigation.
- Spotlighting / data-marking papers (Hines et al.) formalized delimiting defenses — still probabilistic.
- **AgentDojo** ([16](16-debenedetti-agentdojo.md)) turned this threat into a measurable benchmark for agents.

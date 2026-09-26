<div class="prereq">

**Prerequisites.** All modules M00–M25. This is the synthesis.

**You will learn.** How the whole course fits together as a **purple-team** practice, how it maps onto
the industry standards (**OWASP LLM Top 10**, **MITRE ATLAS**, **NIST AI RMF / AI 100-2**), how to use
the final **competency matrix**, and how to approach the five **capstones** — including the research
project that is the course's real objective.

**Why this matters.** Techniques are only useful assembled into a *method*: given a new LLM/agent
system you've never seen, map its attack surface, formulate and reproduce attacks, build and measure
defenses, attack your own defenses, and research what's unknown. That method — not any single attack —
is what makes you an LLM/agent security *researcher*.

</div>

# 26.1 · Purple-team synthesis, standards & capstones

## Why this matters

You now have the pieces: threat modeling, the boundary analysis, injection/jailbreak/adversarial-ML/
poisoning/privacy/RAG/agent/MCP/supply-chain attacks, defensive engineering, evaluation, and automated
red teaming — each with a from-scratch implementation and a guarantee analysis. This module assembles
them into one repeatable method and connects it to the frameworks the industry uses to communicate and
comply, so your work is both rigorous and legible to a security organization.

## Learning objectives

1. State the course's **method** as a repeatable procedure for a new system.
2. Map every module onto **OWASP LLM Top 10**, **MITRE ATLAS**, and **NIST AI RMF/100-2**.
3. Use the **competency matrix** to self-assess honestly.
4. Plan and execute the five **capstones**, especially the research project.

## The method (the whole course in one procedure)

Given a new LLM/agent system:

```text
1. MODEL          draw the DFD; mark trust boundaries; enumerate assets & capabilities (M00–M01)
2. BOUNDARY-CHECK for each mechanism, state what it guarantees vs only makes probable (M02)
3. SURFACE        enumerate untrusted-input channels × reachable privileges (M04–M22)
4. ATTACK         reproduce the relevant attacks locally; measure ASR with CIs (M04–M22, M24)
5. DEFEND         apply ENFORCED controls first, detectors/monitoring as depth (M23)
6. ADAPT          attack your own defenses; re-measure; iterate (purple-team cycle)
7. AUTOMATE       stand up automated red teaming + CI regression (M24–M25)
8. RESEARCH       where the answer is unknown, form a hypothesis and investigate (capstone 5)
```

The recurring discipline throughout: **enforced > probabilistic**, **least privilege on capabilities
and egress**, **treat all observed content as data not instructions**, **measure everything with
confidence intervals against the strongest adapted attack**, and **no defense is magic — write its
guarantee box.**

## Standards mapping (attacks/labs → frameworks)

Standards are taught as maps onto the labs, never memorization (`references/standards-map.md`). The
essential correspondences:

**OWASP LLM Top 10 (2025):** LLM01 Prompt Injection → M04–M06; LLM02 Sensitive Info Disclosure →
M12,M15; LLM03 Supply Chain → M13,M21,M22; LLM04 Data/Model Poisoning → M11; LLM05 Improper Output
Handling → M02,M23; LLM06 Excessive Agency → M16–M18; LLM07 System Prompt Leakage → M02,M04; LLM08
Vector/Embedding Weaknesses → M14,M15; LLM09 Misinformation → M14; LLM10 Unbounded Consumption → M23.

**MITRE ATLAS:** reconnaissance/resource-development → surface mapping (M00); ML model access &
evasion → M04–M10; poisoning → M11; exfiltration → M05,M12,M18; ML supply-chain compromise →
M13,M21,M22. Use ATLAS tactic/technique IDs to communicate findings to security teams.

**NIST:** AI RMF (govern/map/measure/manage) → the method above (map=M00, measure=M24, manage=M23);
AI 100-2 adversarial-ML taxonomy (evasion/poisoning/privacy/abuse) → Stages 4–5 (M09–M13) + M24.

## The competency matrix

The [course outline](../curriculum/course-outline.md) ends with a matrix: for each capability, the
columns Theory / Math / Implementation / Attack / Defense / Research / Assessment. **A capability is
"yours" only when you could do it again, unaided, on a system you haven't seen.** Use it after each
capstone to find gaps, and revisit the relevant module + lab (not just the lesson — the lab is where
the capability lives).

## The capstones

See [`projects/capstones.md`](../../projects/capstones.md). In order: (1) secure a vulnerable LLM app,
(2) red-team a RAG app, (3) red-team an autonomous agent, (4) build an evaluation framework, (5) a
research project. The first four consolidate; the fifth is the point of the whole course — a small,
honest, reproducible piece of AI security research: hypothesis → threat model → related work → attack
→ implementation → experiments → measurements → defense → adaptive attack → results → limitations →
future work.

## Versioning & keeping current

`plan.md` §34: separate **foundations** (M00–M13: injection mechanics, adversarial-ML math, privacy,
supply chain) from **fast-moving** modules (M19 MCP, agent frameworks, model APIs). The foundations
change slowly; re-verify the fast-moving specifics (MCP auth, provider APIs, current attack papers)
before relying on them, and update those modules independently. Distinguish, in your own notes,
FOUNDATIONAL / CURRENT / EMERGING / DEPRECATED.

## Assessment

<details><summary>Q1. State the course's method for a system you've never seen.</summary>

Model it (DFD, boundaries, assets, capabilities); check each mechanism's guarantee vs prior; enumerate
the surface (untrusted inputs × reachable privileges); reproduce and measure the relevant attacks
(ASR+CIs); apply enforced controls first then detectors; attack your own defenses and re-measure;
automate red teaming + CI regression; and research the unknowns. Throughout: enforced > probabilistic,
least privilege, data-not-instructions, measure against the strongest adapted attack, guarantee box
for every defense.

</details>

<details><summary>Q2. Why teach standards as maps onto labs rather than as lists?</summary>

Because a category name (e.g. "LLM06 Excessive Agency") is only actionable when tied to a concrete
vulnerability, a local reproduction, an attack, a defense, and a measurement. Mapping each framework
category to a module/lab makes the standard a checklist of *things you can do and test*, and lets you
communicate findings in the shared vocabulary security teams and auditors use.

</details>

<details><summary>Q3. What distinguishes "knowing an attack" from "having the capability"?</summary>

Recognizing a name (prompt injection, GCG, PoisonedRAG) vs being able to, on an unfamiliar system,
map its surface, reproduce the attack from scratch, measure it honestly, build and defeat defenses,
and research new variants — the full row of the competency matrix, demonstrated in a capstone without
assistance. The course optimizes for the latter.

</details>

## What you should now be able to do

- Apply one repeatable purple-team method to any new LLM/agent system.
- Map your findings onto OWASP LLM Top 10, MITRE ATLAS, and NIST AI RMF/100-2.
- Self-assess against the competency matrix and close gaps via the labs.
- Execute the five capstones, culminating in an original, measured, reproducible research project.

## Progress checkpoint

```bash
py course.py complete 26.1
```

You've reached the end of the structured curriculum. The remaining work is the capstones — and then
the open-ended practice of AI security research the course was built to enable.

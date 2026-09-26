<div class="prereq">

**Prerequisites.** [08.1 PAIR/TAP + judges](../module-08/lesson-01.md), [24.1 evaluation harness](../module-24/lesson-01.md),
[07.1 optimization](../module-07/lesson-01.md), [18.1 chains](../module-18/lesson-01.md). Lab: shim +
evalkit, offline.

**You will learn.** Automated red teaming: **attack generation**, **mutation/fuzzing**,
**search/optimization**, **attacker/defender models**, and **automated exploit chains** — turning the
individual attacks and the evaluation harness into a system that discovers and adapts attacks at
scale, and co-evolves against defenses.

**Why this matters.** You can't manually red-team a system against a determined, adaptive adversary —
there are too many payloads and the defense keeps changing. Automated red teaming is how real programs
achieve coverage and keep pace: it's the offensive complement to the evaluation discipline (M24) and
the operational form of "attack your own defense" (the purple-team cycle).

</div>

# 25.1 · Automated red teaming

## Why this matters

Every prior attack was a technique; this module makes them a *pipeline*. An automated red-teamer
generates candidate attacks, judges them, keeps what works, and mutates toward higher success —
across attack families and against your current defenses, continuously. It's the only way to get
coverage and to catch regressions when defenses (or the model) change.

## Learning objectives

1. Build a **mutation fuzzer** over attack payloads and an automated **search** loop toward higher ASR.
2. Explain the **attacker/judge/defender** components and why the judge bounds the attacker (M08/M24).
3. Run **attacker vs defender co-evolution** and read the arms-race ASR curve.
4. Assemble an **automated exploit-chain** red-teamer (reuse the agent runtime, M18).
5. Integrate with the eval harness (CIs, coverage) and regression testing (M24).

## Concept

### The automated red-team loop

```text
  seed payloads → mutate/generate → run vs (target + judge) → score (ASR) → keep winners → mutate → …
                                          ▲ defender may adapt each round (co-evolution)
```

Components:
- **Generator/fuzzer:** produces payloads — mutations (framing, encoding, shouting, duplication,
  combination) of seeds, or an **attacker model** (an LLM that proposes attacks from the target's
  replies, PAIR-style, M08).
- **Target:** the (defended) system under test.
- **Judge:** the automatic success signal (M08) — its quality **bounds** the whole thing.
- **Search:** evolutionary/beam/bandit selection toward higher judged ASR (M07/M08 as special cases).
- **Reporter:** ASR with CIs, per-family coverage (the M24 harness).

Lab: a mutation fuzzer evolves a payload population from ASR 0 → 1.0 on an undefended target in a few
rounds.

### Attacker/defender co-evolution

The realistic setting: the defender adds a control (a keyword filter), which drops ASR — and the
attacker's fuzzer **rediscovers evading payloads** (shouted/duplicated seeds with none of the filtered
words). Lab: the keyword filter lowers ASR but the fuzzer still finds leaks. This co-evolution *is* the
purple-team cycle automated; the deliverable is the ASR-over-rounds curve for both sides, not a single
number.

### Automated exploit chains

Beyond single payloads, automate the M18 chain: search over sequences of tool actions / injection
placements against the agent runtime, with the judge = "did the canary reach the sink." This finds
multi-step exploits a human wouldn't enumerate, and tests defense-in-depth end to end.

## Intuition

Manual red teaming is one skilled picker trying a few keys. Automated red teaming is a key-cutting
machine that stamps thousands of variants, a sensor that beeps when one turns (the judge), and a
process that files new variants based on which almost-worked — running overnight, and re-running every
time you change the lock. It won't be as insightful as your best human on any single attempt, but it
covers ground no human can and never forgets to re-test after a "fix."

## Technical explanation & Code

`labs/lab-25/redteam.py`: `mutate` applies a random transformation (framing/shout/duplicate/emphasize);
`automated_redteam` evolves a population against `system(payload)->bool` (the shim target, optionally
behind a defender filter), reporting ASR per round via `evalkit.asr`. `keyword_defender` is the
adapting defense; the fuzzer rediscovers evasions. Swap in an LLM attacker/judge behind the same
interfaces for higher fidelity.

## Mathematics

**Search as noisy optimization (M08 recap).** The red-teamer maximizes judged ASR over a payload space
under a query budget; it's a bandit/evolutionary search with a *noisy* objective (finite trials per
payload), so report ASR with CIs (M24) and use enough trials before declaring a winner.
**Judge-bounded ASR:** observed $\approx r\,a + f\,(1-a)$ (M08) — validate the judge or the whole
search chases a biased signal. **Coverage over families:** a red-teamer's value is the *union* of
attack families it explores; missing a family = a blind spot the reported ASR can't see (M24). **Arms
race:** model round-$t$ ASR as the attacker's best response to the round-$t$ defense; a durable defense
is one where the attacker's best-response ASR stays low across rounds (not just round 0).

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — automated red teaming as a security control.**
- **Gives you:** scalable coverage across attack families, continuous regression detection (re-run on
  every change), and honest ASR-over-time for both attacker and defender — far beyond manual testing.
- **Does NOT give you:** proof of safety (it finds attacks it searches for; absence of a found attack
  ≠ absence of an attack), coverage of families you didn't include, or validity beyond your judge's
  quality.
- **Fails when:** the judge is weak (biased ASR), the mutation space is too narrow (misses evasions),
  or you report only round-0 ASR (misses the adaptive attacker).
- **Cost:** compute (many queries; an attacker LLM is expensive), and judge engineering.
- **Takeaway:** run automated red teaming continuously, with a validated judge, broad mutation/family
  coverage, CIs, and co-evolution against your actual defenses — and treat it as *finding* problems,
  never as *certifying* their absence. It is the operational engine of the purple-team cycle.

</div>

## Practical lab

<div class="lab">

**Lab 25** ([`labs/lab-25/`](../../labs/lab-25/README.md)) — mutation fuzzer + co-evolution against an
adapting defender. Offline.

```bash
py labs/lab-25/redteam.py
py -m pytest labs/lab-25 -q
```

</div>

## Exercise

1. **Richer mutations + CIs.** Add encoding/obfuscation and combination mutations; report per-round
   ASR with confidence intervals (repeat trials per payload). Show variance shrinks with more trials.
2. **Attacker model.** Replace random mutation with an "attacker" that proposes the next payload from
   the target's *reply* (PAIR-style, M08); compare query-efficiency to the random fuzzer.
3. **Adapting defender + co-evolution curve.** Make the defender upgrade each round (keyword →
   semantic detector); plot attacker ASR vs round for both sides. Identify whether the defense's
   best-response ASR stays low (durable) or the attacker keeps winning.
4. **Automated exploit chain.** Point the red-teamer at the agent runtime (M18): search over
   injection placements / tool sequences with judge = canary-at-sink. Report found chains and which
   defense (M18) each requires.
5. **Coverage & regression.** Assemble a multi-family red-team suite (injection/jailbreak/agent);
   wire it as a CI job that fails if any family's ASR exceeds a threshold; introduce a regression and
   show it's caught. Write the guarantee box for your red-team program.

<details><summary>Hint (step 3)</summary>

Plot two curves: attacker ASR against the *current* defense each round, and the defense version.
A brittle defense shows attacker ASR recovering to ~1.0 a round or two after each upgrade (the
keyword→evasion pattern in the lab). A durable defense (enforced controls, M23) keeps attacker
best-response ASR low regardless of round — that's the difference between filtering and structural
control.

</details>

**Deliverable.** The richer fuzzer with per-round CIs, the attacker-model comparison, the co-evolution
curve, the automated exploit-chain finder, and the multi-family CI red-team + guarantee box.

## Research paper

**Perez et al., "Red Teaming Language Models with Language Models" (2022)** + **PAIR/TAP (M08)** +
**Anthropic/Meta automated-red-teaming writeups**. *Why:* Perez et al. is the foundational
"use an LM to red-team an LM" (generate + judge at scale); PAIR/TAP are the search refinements you've
built. *Read:* Perez's generation+classification pipeline and the diversity/coverage discussion; how
the judge (a classifier) is central. *Reproduce:* the lab is the mutation-search core; add an
LM-based generator (Exercise 2) toward Perez's design. *Limits:* automated red teaming's coverage is
bounded by its generator's diversity and its judge — it complements, never replaces, human red teams
and enforced controls.

## Further reading

- garak, PyRIT, promptfoo as automated red-team frameworks (local fallbacks in
  `references/tools-and-fallbacks.md`); [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. What are the components of an automated red-team loop and which one bounds it?</summary>

A generator/fuzzer (or attacker model), the target, a judge (automatic success signal), a search that
selects toward higher judged ASR, and a reporter (ASR+CIs, coverage). The **judge** bounds the whole
system: observed ASR $\approx r a + f(1-a)$, so a weak judge biases every result — validate it first.

</details>

<details><summary>Q2. Why is co-evolution (not a single ASR) the right frame?</summary>

Because defenses change and attackers adapt: a filter that drops round-0 ASR is often evaded a round
later (the fuzzer rediscovers evasions). The meaningful measure is the attacker's *best-response* ASR
across rounds — a durable (enforced) defense keeps it low; a brittle (filter) defense sees it recover.
A single snapshot number hides this.

</details>

<details><summary>Q3. Why does automated red teaming find problems but not certify their absence?</summary>

It only explores the payloads/families its generator produces and only scores via its judge; not
finding an attack means "our search didn't find one," not "none exists" (upper-bound nature, M24/M10).
Coverage is bounded by generator diversity and judge quality, so it complements — never replaces —
human red teams and enforced controls.

</details>

## What you should now be able to do

- Build a mutation-fuzzing / search red-teamer with a judge and report ASR with CIs and coverage.
- Explain and run attacker/defender co-evolution and read the arms-race curve.
- Automate exploit-chain discovery against an agent and integrate red teaming as CI regression.
- State honestly what automated red teaming can and cannot certify.

## Progress checkpoint

```bash
py course.py complete 25.1
py course.py next
```

**Next:** 26.1 · Purple-team synthesis, standards mapping (OWASP/ATLAS/NIST), the competency matrix,
and the five capstones — assembling everything into a research-grade program.

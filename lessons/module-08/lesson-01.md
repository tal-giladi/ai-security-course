<div class="prereq">

**Prerequisites.** [07.1 GCG](../module-07/lesson-01.md) (the white-box counterpart; ASR + query
budget), [02.1](../module-02/lesson-01.md) (refusal as probability; OOD coverage). Lab uses the
[shim](../../lab/models/README.md), offline.

**You will learn.** Jailbreaking with **no gradients — only queries**: automated black-box search
(PAIR/TAP-style attacker loops), multi-turn and role attacks, and the machinery of **automated red
teaming** — an attacker process, a judge, and a search. You build a query-only beam search, then
show that keyword-based defenses are evaded by novel framings the search discovers.

**Why this matters.** Real targets are usually black boxes (closed weights, an API). The threat
that scales is not one clever human prompt but an *automated* attacker that searches thousands of
framings and refines against the target's replies. This is also exactly how you build a red-team
harness (Module 25) — the attacker and the evaluator are two sides of one loop.

</div>

# 08.1 · Automated & black-box jailbreaks

## Why this matters

GCG needs gradients; most deployed systems don't give you any. But you can still *query*, and
queries are enough: define a success signal, propose candidate attacks, keep what works, refine.
Automated black-box jailbreaks (PAIR, TAP, and their kin) turn jailbreaking into a search problem
solvable with an attacker LLM and a judge — and the same loop, pointed at your own system, is your
red-team pipeline.

## Learning objectives

1. Frame black-box jailbreaking as **query-only optimization** with a judge as the objective.
2. Explain PAIR/TAP: an **attacker model** proposes/refines prompts against a target using only
   its replies; TAP adds tree search + pruning.
3. Build a beam search over composable wrapper strategies; measure ASR and queries-to-success.
4. Explain why the **judge** is the linchpin of automated red teaming and how a weak judge caps
   the attack.
5. Analyze keyword/classifier defenses and demonstrate **evasion by novel framing**; reason about
   semantic detectors.

## Concept

### The loop

```text
     ┌────────────────────────── attacker ──────────────────────────┐
     │  propose prompt  →  query target  →  judge reply  →  refine    │
     └───────────────────────────────────────────────────────────────┘
                 (repeat; keep the best; branch/prune)
```

Three components:
- **Attacker**: proposes candidate jailbreak prompts. In PAIR it is an LLM told to jailbreak the
  target and to *use the target's last refusal* to improve its next attempt (in-context refinement).
  In our lab it is a beam search over composable wrapper *strategies* — a transparent stand-in.
- **Target**: the model under attack; you see only its text replies (black box).
- **Judge**: an automatic success signal — did the reply comply? PAIR/TAP use an LLM judge; the lab
  uses a marker check. The judge is the objective the search optimizes.

**TAP** (Tree of Attacks with Pruning) generalizes PAIR to a tree: branch multiple attacker
proposals, prune off-topic/failing branches with the judge, and search breadth-first — more
query-efficient than a single refinement chain.

### Why query-only search works

From 02.1, refusal is a probability that drops as the prompt moves out of the safety-covered
distribution. Role-play, hypothetical framing, encodings, persona ("DAN"), and obfuscation each
lower refusal a little; **composing** them stacks the effect. The attacker doesn't need to know
*why* — it just needs the judge to tell it which compositions lower refusal, and it climbs. This
is hill-climbing on ASR with the judge as the height function.

### Multi-turn and role attacks

Some jailbreaks unfold over turns: establish a persona or a fictional frame in turn 1 (which the
model accepts as benign), then issue the real request in turn 2 riding on the established context.
The context window now contains attacker-friendly framing the model itself produced — a form of
self-conditioning. Multi-turn expands the search space (sequences of prompts) and often lowers
refusal further than any single message, because earlier turns shift the distribution before the
ask.

## Intuition

You're picking a lock you can't see inside; all you get is a click-or-not after each try (the
judge). A random locksmith rattles keys forever. A *smart* one notices which nudges produce a
promising click and refines toward them — and if the owner installs a filter that rejects keys
shaped like the obvious skeleton key, the smart locksmith files down a differently-shaped key that
still turns the pins. The filter stopped the *known shape*, not the *capability*. That filed-down
key is the paraphrase your search rediscovers.

## Technical explanation

Read `labs/lab-08/pair.py`. The search:
- **State** = a composition of wrapper strategies applied to the base request.
- **Objective** = ASR estimated over several stochastic target queries (the judge counts
  compliance).
- **Beam search** = keep the top-`beam` compositions; each round, extend them by one more strategy,
  re-score, keep the best; track the global best across rounds.
- **Baseline** = query-matched random search, to show the search's guidance is doing work.

Two engineering truths the lab surfaces:
- **The judge bounds everything.** If the judge has false negatives (misses real compliance) the
  search under-credits good attacks; false positives (credits refusals as success) send it chasing
  noise. Automated red teaming lives or dies on judge quality (Module 24/25).
- **Measurement is stochastic.** ASR is estimated from finite target queries; small differences
  are noise (04.1's Wilson-interval point). Report intervals, not single numbers.

## Mathematics

**Search as optimization over a discrete space.** Let $\mathcal C$ be the set of strategy
compositions and $\text{ASR}(c)$ the (unknown) true success rate of composition $c$; you observe a
noisy estimate $\widehat{\text{ASR}}(c) = \frac1n\sum \mathbb 1[\text{judge}]$ from $n$ queries.
Beam search maximizes $\widehat{\text{ASR}}$ under a query budget. Two consequences:

1. **Exploration vs exploitation.** With noisy $\widehat{\text{ASR}}$, spending all queries
   estimating one $c$ precisely wastes budget; spreading too thin misranks. This is a bandit
   problem; PAIR/TAP heuristically balance it (refine promising branches, prune bad ones). You'll
   feel it when a lucky low-$n$ estimate beats a truly-better composition.
2. **Query complexity.** Guided search reaches a target ASR in far fewer queries than random when
   the objective landscape has exploitable structure (composability here). The gap is the value of
   the attacker's strategy — measured, per 07.1, against a budget-matched random baseline.

**Judge error propagates.** If the true ASR of the best attack is $a$ and the judge has recall
$r$ and false-positive rate $f$, the *observed* success the search optimizes is
$\approx r\,a + f\,(1-a)$ — a biased objective. A low-recall judge ($r$ small) can hide a working
attack; a high-$f$ judge manufactures phantom ones. Same Bayes/base-rate logic as 02.2's filters,
now aimed at your own evaluation.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — keyword / marker jailbreak classifier (input side).**
- **Stops:** attacks containing known trigger phrases ("DAN", "ignore previous", "base64",
  "role-play"); cheap, catches script-kiddie attempts and the obvious templates.
- **Does NOT stop:** semantically-equivalent paraphrases with none of the trigger words (the lab's
  `story` framing), novel personas, multi-turn setups, or an attacker LLM generating unlimited
  fresh framings. It matches surface strings, not intent.
- **Attacker adapts:** the search *rediscovers* an evasive wrapper automatically (demonstrated), or
  an attacker LLM writes a benign-looking jailbreak.
- **FP cost:** blocks legitimate fiction/role-play/encoding requests. **Perf:** cheap per input.
- **Takeaway:** a speed bump, not a boundary. A *semantic* detector (an LLM/classifier judging
  intent) raises the bar but is itself an attackable model with its own ASR — you must red-team the
  detector too.

</div>

## Practical lab

<div class="lab">

**Lab 08** ([`labs/lab-08/`](../../labs/lab-08/README.md)) — query-only beam search; marker-defense
+ rediscovered evasion. CPU-only, offline, fast.

```bash
py labs/lab-08/pair.py       # vulnerable PAIR ASR ~1.0; defended: rediscovers 'story' evasion ~0.6
py -m pytest labs/lab-08 -q
```

</div>

## Exercise

1. **Measure with statistics.** Report vulnerable PAIR ASR and queries-to-first-success vs
   query-matched random, each with a Wilson interval. Increase per-composition trials `n`; show how
   the ranking stabilizes (the exploration/exploitation point).
2. **Build a mutation attacker.** Replace the fixed strategy library with an attacker that
   *mutates* the current best prompt (insert/swap/paraphrase tokens) — a crude stand-in for an
   attacker LLM. Compare its query-efficiency to the fixed-strategy beam.
3. **Multi-turn.** Implement a 2-turn attack: benign persona/frame in turn 1, real ask in turn 2.
   Measure ASR vs the best single-turn attack and explain the difference via distribution-shift.
4. **Judge quality (crucial).** Corrupt your judge: (a) add false negatives, (b) add false
   positives. Show how each degrades the search, and compute the biased objective $r a + f(1-a)$.
   Conclude why a good judge is prerequisite to any red-team automation.
5. **Beat the keyword defense, then build a better one (purple team).** Confirm the search
   rediscovers `story`. Now build a **semantic** detector (use the shim/a classifier to judge
   whether a prompt is *trying* to elicit disallowed content, independent of keywords). Re-run the
   search against it; report the new ASR and find the framing that evades even the semantic
   detector. Write the guarantee box for your final defense, including that the detector is itself
   an attackable model.

<details><summary>Hint (step 5)</summary>

A semantic detector is another model call: "Does this prompt attempt to elicit [disallowed
category]? yes/no." It generalizes past keywords but has its own coverage gaps (02.1) — so the
same OOD/paraphrase pressure that jailbreaks the target can be turned on the detector. Red-teaming
your detector with the *same* search is the honest evaluation.

</details>

**Deliverable.** PAIR-vs-random with CIs, the mutation attacker, the multi-turn result, the
judge-corruption analysis, and the semantic detector + its evasion + guarantee box.

```bash
py course.py complete 08.1
```

## Research paper

**Chao et al., "Jailbreaking Black Box Large Language Models in Twenty Queries" (PAIR, 2023)** and
**Mehrotra et al., "Tree of Attacks: Jailbreaking Black-Box LLMs Automatically" (TAP, 2023).*
*Why:* the canonical automated black-box jailbreaks — an attacker LLM + judge + (tree) search, the
loop you built. *Read (PAIR):* the algorithm and the attacker/judge prompts; note the ~20-query
efficiency claim and how refinement uses the target's refusal. *Read (TAP):* the tree-search +
pruning improvement. *Reproduce (light):* map your beam search to PAIR's chain and add a pruning
step (drop compositions below a judge threshold early) to approximate TAP; compare queries. *Limit:*
efficiency depends heavily on judge quality and attacker capability — weak judge, weak attack.

## Further reading

- Liu et al., **AutoDAN** (2023) — fluent automated jailbreaks (bridges to Lab 07's adaptive
  fluency). 
- OWASP LLM01; MITRE ATLAS (evasion, automated attack generation) —
  [`references/standards-map.md`](../../references/standards-map.md).

## Assessment

<details><summary>Q1. How can you jailbreak with no gradients?</summary>

Treat it as query-only optimization: define a judge (automatic success signal), propose candidate
prompts, query the target, keep/refine what the judge scores as working, and search (beam/tree).
Refusal is a probability that composable OOD framings lower, so hill-climbing on judged ASR finds
jailbreaks without any access to weights or gradients.

</details>

<details><summary>Q2. Why is the judge the linchpin of automated red teaming?</summary>

The judge is the objective the search optimizes; its errors bias what the search finds. A
low-recall judge hides working attacks (the search under-credits them); a high-false-positive judge
sends the search chasing phantom successes. The observed objective is $\approx r a + f(1-a)$, so
attack quality is bounded by judge quality.

</details>

<details><summary>Q3. Why does a keyword jailbreak classifier fail, and what does the search do about it?</summary>

It matches surface trigger strings, not intent, so semantically-equivalent paraphrases with none of
those words slip through. The automated search *rediscovers* such an evasive framing (e.g. a
fictional-story wrapper) with no manual effort — demonstrating that keyword filters are speed bumps.
A semantic detector raises the bar but is itself an attackable model.

</details>

## What you should now be able to do

- Build a query-only automated jailbreak (attacker + judge + search) and measure it with CIs.
- Explain PAIR/TAP and the exploration/exploitation and judge-quality issues in red-team automation.
- Demonstrate evasion of keyword defenses and reason about (and red-team) semantic detectors.

## Progress checkpoint

```bash
py course.py complete 08.1
py course.py next
```

**Next:** Stage 4 — 09.1 · Adversarial examples I (FGSM/PGD from scratch): the perturbation
problem, threat models, and gradient attacks on a classifier, where the math of adversarial ML
begins.

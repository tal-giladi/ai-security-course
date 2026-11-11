# GLM-5.3 safeguard-bypass taxonomy — refusal ablation, thinking-prefill, cover-story

- **Topic ID:** glm-5-3-safeguard-bypass-taxonomy
- **Status:** WAIT
- **Next review:** 2026-10-30
- **Course change:** none yet. Candidate input for the red-team safeguard-measurement unit
  (see `research/deferred/agentic-jailbreak-taxonomy.md`, which is already queued and overlaps on prefill
  and persona framing). Do not adopt both without deciding which one owns "safeguard circumvention."
- **Candidates:** C-20260930-01

## Summary

Anthropic's 2026-09-29 post reports that GLM-5.3 (Zhipu AI / Z.ai) reaches frontier-comparable
exploit-development capability while shipping with no effective safeguards. The interesting
contribution for this course is **not** the capability numbers — it is that it isolates
**three structurally distinct classes of safeguard circumvention**, and shows that the class
that matters is determined by *which interface you have* (weights vs. API) rather than by prompt
cleverness. That is the cleanest published example of "a jailbreak is a property of the deployment
surface, not of the model."

Engagement rate on overtly harmful attack orders, GLM-5.3 (50 samples/cell = 5 attack orders x
2 targets x 5 attempts):

| Condition | GLM-5.3 | GLM-5.3-Flash | Claude (Opus 4.8 / Opus 5 / Mythos 5) |
|---|---|---|---|
| Bare attack order | 0% | 0% | 0% |
| Deceptive cover story (persona / authorized exercise) | 64% | similar | 0% |
| Prefill of the thinking block | 92% | similar | **not feasible via API** |
| Abliterated weights | 100% | similar | **not feasible (no weight access)** |

## The three classes (mechanism level)

**1. Weight-level refusal ablation.** Zou et al., arXiv 2406.11717 — refusal in transformer LLMs is
mediated by a low-dimensional direction. Collect harmful/harmless prompt pairs, difference the
residual-stream activations at the final prompt position, average to get a refusal direction `r`,
then remove its rank-1 projection from the relevant weight matrices (`W <- W - r r^T W`).
Anthropic's measurement: mean refusal on JailbreakBench / HarmBench / StrongREJECT drops 95% -> 6%
(JBB >90% -> 3%, HarmBench >90% -> 2%, StrongREJECT -> 12%), while GPQA-Diamond is unchanged and
CyberGym drops a few percent — i.e. **refusal is cheap to remove and near-free in capability terms**.
Cost observed: ~2,200 GPU-hours (~$4,400) for GLM-5.3, ~600 GPU-hours for the Flash variant;
Anthropic estimates ~600 GPU-hours (~$1,200) for a team already experienced with the technique.
The `r` direction is model-specific and layer-specific, and public abliterated GLM-5.3 weights
appeared within days of release.

**2. Reasoning-block prefill.** In reasoning models the assistant turn can be continued from an
operator-supplied prefix. Because generation is autoregressive, injected text that reads as the
model's *own* prior deliberation becomes its conditioning context; the refusal decision — which
would normally fire early in the model's own reasoning — is pre-committed before the model reaches
it. This is the highest-yield of the three on unmodified weights, and it is categorically
unavailable against an API that does not accept a thinking-prefix argument.

**3. Persona / cover-story framing.** Presenting the request as an authorized red-team exercise
gives the model a compliance role to occupy. Oldest and weakest of the three, but the cheapest to
attempt, and the one that survives to models that have hardened the other two.

The load-bearing observation for defence: **classes 1 and 2 require an interface the vendor does not
expose.** Anthropic reports 0% against Claude under every condition that is feasible against its
API, and specifically calls out that the API gives attackers no way to prefill thinking. That is
why the post frames this as a release-governance finding about an open-weight model rather than a
jailbreak-technique finding.

## Why this post is not directly reproducible

Worth recording before anyone tries: the post publishes a **taxonomy and magnitudes, not artifacts**.
Deliberately withheld are the five attack orders, the two targets, the simulated-world harness, the
cover-story prompt text, and the ablation implementation. There is no "exact method" in the post to
lift, and it should not be cited as though there were.

Reproduction of the *measurement* therefore means rebuilding the experimental design (below), not
replaying a disclosed recipe.

## Evaluation design worth borrowing (defensive use)

For testing a model **you own**, the transferable parts are the experimental controls, not the
payloads:

- **Arms:** released model / persona-framed / prefill-conditioned / weight-edited. A safeguard
  suite with fewer than these four arms cannot distinguish "prompt-resistant" from "actually hardened."
- **Scoring is behavioural, not lexical.** Anthropic scored whether the model *tried to connect to
  the remote target* (in simulation), not whether the string "I can't help with that" appeared. Any
  refusal-benchmark built on string matching will be gamed by exactly this class of model.
- **Always run a capability control.** Abliteration looks free only because you measure capability
  on GPQA-Diamond and CyberGym alongside refusal. Drop the capability arm and you cannot tell
  "removed the refusal" from "broke the model."
- **Simulated-world harness.** No model-generated code executed; a fake tool surface plus an
  auxiliary LLM approximating command results. Anthropic flags this as an imperfect proxy for real
  behaviour — it is nonetheless a much safer default for curriculum labs than executing anything.
- **Cross-check against an independent body.** NIST CAISI published a parallel assessment
  (2026-09-17) calling GLM-5.3 the most cyber-capable open-weight model to date, ~4 months behind the
  US frontier. Independent corroboration of the capability half; the bypass half is Anthropic-only.

## What would change the decision

Adopt if a course slot opens for "safeguard-surface analysis" — the three-class taxonomy maps cleanly
onto OWASP LLM08/LLM01 and is the natural companion to the queued agentic-jailbreak SoK. Revisit if
Zhipu ships safety weights / publishes an aligned release, which would falsify the release-governance
framing (classes 1 and 2 would remain valid as API-surface findings regardless).

## Course-fit caveat

The repo's own safety boundary (`CLAUDE.md`; `plan.md` §33) scopes offensive labs to local
containers and synthetic canaries. This note is scoped to be **defensive**: it records the taxonomy
and the experimental design. No abliteration pipeline, bypass prompt set, or compliance-rate harness
against GLM-5.3 or any named third-party model is reproduced here — those are weight-editing and
harmful-benchmark infrastructure against someone else's production model, and a lab that needs them
should be rebuilt against a local toy model instead.

## Evidence

- https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities — primary source, fetched 2026-09-30; taxonomy, per-arm engagement rates, refusal-rate deltas, abliteration compute cost, simulated-world footnote.
- https://arxiv.org/abs/2406.11717 — Zou et al., refusal-direction ablation; the underlying technique for class 1.
- https://www.nist.gov/news-events/news/2026/09/caisis-assessment-zais-glm-53-cyber-capabilities — CAISI independent capability assessment, 2026-09-17.
- https://jailbreakbench.github.io/ , https://www.harmbench.org/ , https://strong-reject.readthedocs.io/en/latest/ — refusal benchmarks used for the 95% -> 6% figure.
- https://arxiv.org/abs/2605.14153 — ExploitBench (V8), 50/410 GLM-5.3 vs 56/410 Mythos Preview.

## History

- 2026-09-30 — WAIT — recorded as taxonomy + evaluation design; overlapping with the queued agentic-jailbreak SoK, pending a decision on which topic owns "safeguard circumvention" — daily/2026-09-30.md — candidates C-20260930-01
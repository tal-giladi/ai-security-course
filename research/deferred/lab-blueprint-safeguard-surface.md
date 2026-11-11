# Lab blueprint — Safeguard surface: refusal direction, prefill, and cover story

- **Topic ID:** lab-blueprint-safeguard-surface
- **Status:** WAIT (blocked on course-content review, see *Blockers*)
- **Next review:** 2026-10-30
- **Companion note:** `research/deferred/glm-5-3-safeguard-bypass-taxonomy.md` (taxonomy + evidence)
- **Candidates:** C-20260930-02

## Provenance — read this before citing anything below

Three different kinds of content are in this document and they are **not** interchangeable:

| Content | Source | Status |
|---|---|---|
| Engagement rates (0/64/92/100%), refusal deltas (95%→6%), compute costs (600–2,200 GPU-hours), capability scores | Anthropic post, reported | **Reported**, not independently reproduced |
| The three technique mechanisms (arXiv 2406.11717 and adjacent public literature) | Public literature | **Published and citable** |
| The four lab designs in this file | **My reconstruction** | **Not from Anthropic** |

Do not present the lab designs as "Anthropic's method." They are a teaching reconstruction built
to measure the same three phenomena on a toy model. Any lab README that ships must carry this split,
or students will cite `module-34` as a reproduction of an Anthropic evaluation it does not reproduce.

## The extraction ceiling

The post withholds, by design: the five attack orders, the two targets, the cover-story prompt text,
the simulated-world harness, and the ablation implementation. There is no exact method in the post
to extract. What transfers to a lab is the **experimental design** and the **reference numbers** —
that is what the four labs below are built from.

## Headline lesson: the attack class is a property of your deployment surface

This is the transferable idea and it should be one lesson, not four. Anthropic's 0% against Claude
is not better prompt hardening; it is that two of the three classes **require an interface the vendor
does not expose**:

| Attack class | Needs | Local weights | Hosted API w/ free assistant-turn prefill | Hosted API, no prefill |
|---|---|---|---|---|
| Cover story / persona | prompt control only | available | available | available |
| Reasoning prefill | prefix-controllable assistant turn | available | available | **unavailable** |
| Refusal ablation | weight edit | available | **unavailable** | **unavailable** |

Student takeaway to make explicit: "we hardened the model" and "we did not expose the surface" are
different claims with different evidence, and only one of them survives a weight release. Maps to
OWASP LLM06 (Excessive Agency) / LLM08 and to MITRE ATLAS AML.T0051-style abuse cases; cross-check
against the queued `research/deferred/agentic-jailbreak-taxonomy.md` before adopting both.

## Lab A — The refusal direction is (approximately) one direction

**The insight that makes this lab better than a GPU reproduction:** a toy model can have a refusal
direction *by construction*. Then you can verify the ablation math **exactly** instead of
approximately, on CPU, in seconds, with stdlib only. That is the repo's "implement the mathematics
from scratch" rule applied to a published result.

**Model.** Residual stream of dim $d{=}64$, mid-layer position. Two probe tasks:
refusal (refuse / comply binary) and capability (an unrelated classification task). Design $h$ so
that the refusal logit is $r^\top h$ with $r$ a fixed vector, then learn $r$ from data instead of
being told it.

**Method, from scratch, no library first:**
1. Collect activation pairs $h^+$ (refusal-triggering) and $h^-$ (benign), final prompt position.
2. $\hat r = \mathrm{normalize}\big(\mathrm{mean}(h^+ - h^-)\big)$.
3. Verify rank-1: a single linear probe on $\hat r^\top h$ should reach ~1.0 AUC. If it does not, the
   refusal behaviour is *not* single-direction and the lesson changes — branch here, that is a real
   result, not a failure.
4. Ablate: $W \leftarrow W - \hat r \hat r^\top W$ for each matrix writing into the residual stream.
5. Re-measure refusal rate **and** capability. Capability is the control; without it you cannot
   distinguish "removed the refusal" from "broke the model."

**Reference points.** Toy should show a near-total refusal collapse with capability essentially flat,
because the toy refusal direction is exactly single-rank. Anthropic's real models: 95%→6% mean
refusal, GPQA-Diamond unchanged, CyberGym a few points lower.

**The adaptation step (required by the purple-team cycle).** Ablation is not a permanent fix.
Re-estimate $\hat r$ from post-ablation activations and re-apply: a recoverable fraction of the
original direction survives. Measure how many iterations it takes to get refusal back up. That
number is the real deliverable — it is the cost multiplier a defender faces.

**Files:** `model.py`, `find_direction.py`, `ablate.py`, `attack.py`, `test_lab_a.py`. Wilson CI on
refusal rate, as module-32 does.

## Lab B — Prefill pre-commits the decision

Model refusal as a **decision at an early step**: sample refuse/comply from a prefix-dependent
distribution, with the decision point at step $k$. Prefilling an operator-supplied assistant prefix
that reads as the model's own prior deliberation removes the decision point from the model's reach.

Measure refusal rate bare vs prefilled, across several decision-point depths $k$. Expected direction:
the deeper the decision sits, the weaker the effect; the closer to the start, the stronger.

**Defence lesson (the point of the lab).** You cannot defend against prefill if you expose a
prefix-controllable assistant turn. The mitigation is surface design, not a filter. Ask students what
their own agent framework allows a caller to supply as an assistant-turn prefix, and whether their
reasoning block is reachable that way.

## Lab C — Cover story, and the false-positive cost

Arms: bare / authorized red-team exercise / CTF / research context / fiction. Measure refusal rate
**and** benign false-positive rate per arm.

The trap to make students hit: cover-story framing is easy to "fix" with a detector, and the detector
is trivially defeated while raising FPR on legitimate security work. Ship it, measure the FPR, then
bypass your own detector (repo rule: *defenses: implement → then bypass your own defense*).

## Lab D — How you score compliance decides what you conclude

The most transferable piece, and the one that generalises to checking Tal's own models.

Anthropic scored **whether the model attempted the action** (tried to reach the target), not whether
the string "I can't help with that" appeared. Build both scorers against the same runs and show:

- string-match scorer reports high refusal while behaviour shows compliance (false negative, the
  dangerous direction — you ship believing the model is safe)
- behavioural scorer catches compliance that reads as cooperative
- capability probe is mandatory alongside either, or "refusal removed" is indistinguishable from
  "model broken"

Then have students re-score their own model on both and report the **gap** between the two numbers.

## Blockers before any of this ships as course content

1. Read `C:\Users\TalGiladi\OneDrive\repos\tals-academy\docs\new-course-instructions.md` (required
   by `CLAUDE.md` before writing course content). Not done here — this file is a blueprint, not course content.
2. Decide overlap with `research/deferred/agentic-jailbreak-taxonomy.md`; do not adopt both.
3. Confirm module number. `labs/module-32/` and `labs/module-33/` exist and `labs/lab-16/` is
   untracked-but-present, so the next free module number is not obvious from the tree alone.
4. Wire into `_sidebar.md` + `curriculum/course-outline.md` only via the weekly review.

## Deliberately excluded

No ablation pipeline targeting GLM-5.3 or any named third-party model; no bypass prompt set tuned to
a real product; no compliance-rate harness driving real harmful-prompt benchmarks. Those are
weight-editing and harmful-benchmark infrastructure aimed at someone else's production model. The
phenomena are reproduced here on a toy model with synthetic probes, which is what makes the lab
CPU-only, safe to publish, and safe to let students modify.

## Evidence

- https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities — reference numbers and taxonomy; fetched 2026-09-30.
- https://arxiv.org/abs/2406.11717 — Zou et al., single-direction refusal; the technique behind Lab A.
- https://jailbreakbench.github.io/ , https://www.harmbench.org/ , https://strong-reject.readthedocs.io/en/latest/ — the refusal benchmarks behind the 95%→6% figure.
- https://www.nist.gov/news-events/news/2026/09/caisis-assessment-zais-glm-53-cyber-capabilities — independent capability corroboration.

## History

- 2026-09-30 — WAIT — blueprint drafted from taxonomy note; four labs reconstructed against published technique literature; blocked on course-content review and module numbering — daily/2026-09-30.md — candidates C-20260930-02
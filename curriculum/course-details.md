# Course details

Not imported into the Academy — this is what Tal uses to register the course and fill the Admin form.

| Field | Value |
|---|---|
| Course slug (suggested) | `ai-security` |
| GitHub repo | `tal-giladi/ai-security-course` (public; GitHub Pages already enabled) |
| Repo root | `C:\Users\TalGiladi\OneDrive\repos\course-creator\ai-security-course` |
| Import adapter | `course-creator` (the general contract) |
| Free or paid | **Paid** — it is a practitioner/research-grade security course with a capstone engagement, aimed at working engineers. Tal decides. |
| Format | Markdown lessons (39) + per-module multiple-choice quizzes (37 modules) + downloadable lab code per module + a capstone engagement brief |
| Estimated time | ~41 h reading, ~95 h hands-on. Module 34 (advanced track) adds ~47 min reading and ~5 h hands-on, plus compute cost — see below. |
| Pass mark | 70% on every quiz |

## Risk notice

> Every offensive exercise in this course runs only against software shipped in the course itself,
> on your own machine, using synthetic secrets and local sinks. Nothing here targets a real system,
> a real credential or a third party's data, and no payload is weaponized. You are responsible for
> having written authorisation before testing any system you do not own.
>
> Module 34 additionally downloads and modifies a real open-weight model
> (`zai-org/GLM-5.3-Flash`, MIT-licensed) that you host locally, and can consume substantial paid GPU
> time. It still targets no third-party service and embeds no harmful corpus. See
> `PUBLISHING_WARNING.md` item 7 before publishing.

## One-line summary

Expert-level LLM, agent and AI-infrastructure security research: every attack reproduced in a local
lab, analyzed mathematically, defended, then attacked again — and measured.

## Who it is for

Experienced software engineers who already understand how modern LLMs are built and want to move
into LLM/AI security research: LLM Security Engineer, AI Red-Team Engineer, AI Security Researcher,
or AI Security Architect. It assumes the
[LLM Research Engineer](https://tal-giladi.github.io/llm-research-engineer-course/) material
(transformers, RLHF, embeddings, RAG, tool use) and builds the security layer on top.

## Prerequisites

- The sibling **LLM Research Engineer** course, or equivalent working knowledge of transformers,
  training, RLHF, embeddings, RAG and tool-calling agents.
- Comfort with Python. Every lab except module 34 is stdlib-first and runs CPU-only, offline.
- Docker for the labs that use it; every lab states whether it needs it, and most do not.
- **For module 34 only** (the paid advanced track): a GPU machine with 24 GB+ of VRAM for tiers B/C,
  or 8×80 GB / 4×H200 for tier A, plus a budget for the run. Anthropic's own figures for a GLM-5.3
  ablation are ~600–2,200 GPU-hours and ~$1,200–$4,400. The lab README has a cost table; nothing in
  the rest of the course needs a GPU, and modules 7 and 25 teach the same algebra for free.
- Reading ability in English. The papers are read in English.

## What you will learn

- **Map an AI system's attack surface** — draw the data-flow diagram, mark trust boundaries, and
  enumerate untrusted input locations × reachable privileges, which is the number that predicts
  blast radius.
- **Reproduce the major attacks locally and measure them** — direct and indirect prompt injection,
  multimodal injection, GCG and black-box jailbreaks, FGSM/PGD/CW adversarial examples, data
  poisoning and sleeper agents, model extraction, RAG poisoning, and agent tool poisoning.
- **Attack agents where it hurts** — excessive agency, the confused deputy, memory poisoning and
  persistence, tool poisoning, multi-agent/A2A trust, code agents, and AI serving infrastructure.
- **Design defenses that hold, and find out where they don't** — every defense is written as a
  guarantee analysis (what it stops, what it does not, how the attacker adapts, false-positive
  cost, performance cost), then attacked again.
- **Measure security rather than assert it** — attack success rate, precision/recall under real
  base rates, ROC and operating points, and the value of enforced versus probabilistic controls.
- **Speak the industry's language** — OWASP Top 10 for LLM Applications (2026) and for Agentic
  Applications (ASI01–ASI10), MITRE ATLAS, and NIST AI RMF, with the crosswalks in the reference
  section.
- **Run a professional engagement** — reconnaissance through reporting, using the capstone
  environment and the engagement-report template.
- **Evaluate safeguards properly, at the scale that matters** (advanced track) — classify a
  circumvention technique by the deployment surface it requires, score compliance behaviourally
  rather than by string match, replicate a refusal-direction ablation on a 320B open-weight model with
  a capability control, and report the iteration count an adaptive attacker actually faces.
- **Keep up** — the course ships with a daily research and weekly curriculum-review pipeline, so
  the content tracks new findings rather than going stale.

## Notes for Tal

- The course has a bespoke `ai-security` importer adapter (documented in the Academy as
  `docs/source-formats.md` section B) written for the pre-2026-09-30 layout. **After this
  migration the course targets the general `course-creator` contract instead** — the new modules
  (16.2, 27–32) had already outgrown the bespoke adapter, which would have dropped modules 27–31
  entirely and imported the front-matter lessons with no quiz. Set the course row's adapter to
  `course-creator`. The old adapter can stay in the codebase; nothing else uses it.
- GitHub Pages is enabled and the repo is fully usable as plain markdown, so nothing a learner
  needs depends on docsify, JavaScript or the progress script.
- **The repo is public but the course is now paid — module 34 is the first thing that makes that a
  problem.** Every paid module up to now was CPU-only and its "lab code" was a few hundred lines of
  Python that is arguably the marketing. `labs/module-34/` is different: it is a working refusal-
  ablation pipeline against a specific named open-weight model, and the Academy serves lab code as a
  **downloadable zip**. If `tal-giladi/ai-security-course` stays public, the module 34 lab zip is
  fetchable by anyone, as are the lesson markdowns via GitHub Pages — so the paywall does not hold for
  the one module it was presumably introduced for. Three options, in the order I would weigh them:
  1. **Split** — publish modules 0–33 as the free course, move module 34 to a separate private repo
     imported as its own paid course. Cleanest commercially, but it breaks the single `_sidebar.md`
     and the stable lesson-id path `34.1`, and instructions §1 forbids renaming published paths.
  2. **Keep it public and say so** — treat module 34 as marketing that happens to be real, and make
     the tiered cost table the pitch ("$20 to learn it, $4,400 to reproduce the finding"). Defensible
     if you intend the course to stay primarily a public portfolio.
  3. **Make the repo private** — the course-details table says the Academy import then needs a token.
     Simplest to operate, and it also changes the docsify/portfolio story, so it is a real trade.
  Whatever you pick, note that `PUBLISHING_WARNING.md` is written on the assumption that the same
  markdown publishes on the Pages build — that stays true in all three cases, but only option 1 or 3
  keeps the lab zip from being freely downloadable.

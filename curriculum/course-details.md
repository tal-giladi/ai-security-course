# Course details

Not imported into the Academy — this is what Tal uses to register the course and fill the Admin form.

| Field | Value |
|---|---|
| Course slug (suggested) | `ai-security` |
| GitHub repo | `tal-giladi/ai-security-course` (public; GitHub Pages already enabled) |
| Repo root | `C:\Users\TalGiladi\OneDrive\repos\course-creator\ai-security-course` |
| Import adapter | `course-creator` (the general contract) |
| Free or paid | **Paid** — it is a practitioner/research-grade security course with a capstone engagement, aimed at working engineers. Tal decides. |
| Format | Markdown lessons (34) + per-module multiple-choice quizzes (32 modules) + downloadable lab code per module + a capstone engagement brief |
| Estimated time | ~40 h reading, ~90 h hands-on |
| Pass mark | 70% on every quiz |

## Risk notice

> Every offensive exercise in this course runs only against software shipped in the course itself,
> on your own machine, using synthetic secrets and local sinks. Nothing here targets a real system,
> a real credential or a third party's data, and no payload is weaponized. You are responsible for
> having written authorisation before testing any system you do not own.

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
- Comfort with Python (all labs are Python, stdlib-first, CPU-only) and with reading attacker code.
- Docker for the labs that use it; every lab states whether it needs it, and most do not.
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

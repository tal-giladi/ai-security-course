# Build guide — LLM & Agent Security Research Engineer course

This repo is a **docsify static course site** plus a **runnable local security lab** (`lab/`).
It takes an experienced software engineer (Tal — C#/.NET, currently doing the
`llm-research-engineer-course`) to expert-level LLM/agent **security research** capability:
red team, blue team, and especially **purple team**. Source brief: `plan.md`.

Prerequisite/sibling course: **`llm-research-engineer-course`** (in the parallel folder,
published at https://tal-giladi.github.io/llm-research-engineer-course/). Do NOT reteach
its material (transformers, attention, RLHF, embeddings, RAG basics, agents/tool-use basics).
Reference it and build the *security-specific* depth on top. The overlap map lives in
`curriculum/prerequisite-map.md`.

## Layout
- `index.html` — docsify config (KaTeX auto-render, search, copy-code, count). No build step.
- `README.md` — docsify home page.
- `_sidebar.md` — full navigation. Every new lesson/paper/lab MUST be linked here.
- `curriculum/` — `course-outline.md` (module map + dependency graph + competency matrix),
  `prerequisite-map.md` (what the sibling course already covers).
- `lessons/module-XX/lesson-YY.md` — lesson content.
- `labs/lab-XX-slug/` — self-contained Docker labs (README + code + attack + defense + reset).
- `exercises/` — standalone exercise specs where they don't live inside a lesson.
- `projects/` — capstones.
- `papers/` — one reading guide per paper (`NN-slug.md`) + `papers/index.md`.
- `references/` — standards maps (OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF), tool fallbacks.
- `progress/` — `progress.json` + generated `PROGRESS.md`; `course.py` at repo root.
- `lab/` — shared lab infrastructure (docker-compose, vulnerable apps, toy models).

## Lesson template (every lesson) — from `plan.md` §30
`# Lesson` → Why this matters → Learning objectives → Prerequisites (link sibling course when
relevant) → Concept → Intuition → Technical explanation → Mathematics → Attack/Defense model →
Real-world examples → Code → Practical lab → Exercise → Research paper → Further reading →
Assessment → What you should now be able to do → Progress checkpoint.

For every security mechanism, explicitly state (use `.callout.guarantee`):
**What it guarantees / What it does NOT guarantee / How an attacker adapts / false-positive
cost / performance cost.** This is the single most important recurring pattern.

Use `.callout.red` (attack), `.callout.blue` (defense), `.callout.purple` (research), and the
`.lab` box (hardware/Docker requirements + expected runtime) on any lesson with a real lab.

## Non-negotiable rules
- **Every learning material has a hands-on exercise** (`plan.md` "Very important"). Attacks:
  construct → execute → analyze → measure. Defenses: implement → then bypass your own defense.
  Math: implement from scratch → use in a real experiment → compare to a library.
- **Purple-team cycle**: attack → observe → detect → mitigate → retest → adapt → measure.
  A lab never ends at "the exploit worked."
- **Never hide the mathematics behind a library.** From scratch first, library second.
- **Safety boundary** (`plan.md` §33): every offensive lab targets ONLY local containers /
  intentionally vulnerable apps we ship, with **synthetic** canary secrets (e.g.
  `LAB-CANARY-{uuid}`) and **benign success markers**. Never real systems, real credentials,
  real exfiltration endpoints, or working malware. Attack payloads demonstrate the *mechanism*
  with an inert marker, not a weaponized effect. Egress in labs goes to a local sink container.
- **External-tool fallback** (`plan.md` §21, §35): every external tool/model/dataset gets a
  fallback + a local minimal reimplementation so the objective survives if it disappears.
  Record: Primary / Version-date / Purpose / License / Install / Failure modes / Fallback.
- **Distinguish** FOUNDATIONAL / CURRENT / EMERGING / DEPRECATED, and DOCUMENTED vs SPECULATION.
- Math in `$...$` / `$$...$$` (KaTeX). Never a bare `$` inside a code fence.
- Small open models, CPU-friendly where possible; flag when a GPU is genuinely required.
- Prefer Python for experiments; C# where real-world integration is illustrative.

## Local preview
`python -m http.server 8080` from repo root → http://localhost:8080.
Labs: `cd labs/lab-XX-slug && docker compose up` (each lab documents the exact command).

## Progress tracking
`course.py` (stdlib only) reads lessons from `_sidebar.md`, tracks status/quiz/notes in
`progress/progress.json`, regenerates `PROGRESS.md`. Not course content — never edit as lesson work.

## Status / handoff
`TODO_FOR_TAL.md` tracks progress and gaps. **Commit and push after each small batch** so a
stopped session never restarts from scratch. Attribution lines per session instructions.

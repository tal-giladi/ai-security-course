# Status & handoff — LLM & Agent Security Research Engineer

Commit-tracked so a stopped session resumes from here.

Repo: https://github.com/tal-giladi/ai-security-course · Pages:
https://tal-giladi.github.io/ai-security-course/ (enabled).

## Done
- Scaffolding: docsify `index.html`, `README.md`, `CLAUDE.md`, `.gitignore/.nojekyll/.gitattributes`.
- Master curriculum `curriculum/course-outline.md` (27 modules M00–M26, dependency graph,
  competency matrix) + `curriculum/prerequisite-map.md`. Reference pages: `references/`, `papers/index.md`.
- Progress tracker `course.py` + `progress/progress.json` (stdlib). `_sidebar.md`.
- Lab infra: `lab/models/shim.py` (deterministic model), `lab/sink/sink.py` (egress sink),
  `lab/tests/` (6 tests pass).
- Lessons (template-complete): **M00.1** threat modeling, **M01.1** appsec primitives,
  **M02.1** LLM boundaries, **M02.2** inference API surface, **M04.1** direct prompt injection.
- **Lab 04** (`labs/lab-04`): attack/defense/measure, acceptance tests pass, docker-compose (no egress).

## Next (in order)
1. **M05.1 indirect prompt injection** + `labs/lab-05` — malicious instruction via retrieved
   doc / web page / tool result; the confused-deputy chain to the sink. Shim already supports
   `retrieved=/web=/tool=/email=` channels.
2. **M06.1** multimodal/cross-agent injection.
3. **Stage 3 jailbreaking** (M07 GCG: derive $\arg\max_x L$, greedy coordinate gradient; needs a
   tiny real/toy model for gradients — flag GPU-optional).
4. **Stage 4 adversarial ML** (M09–M10 FGSM/PGD/CW from scratch on a toy classifier).
5. Continue per `curriculum/course-outline.md`; one lesson + its lab per batch, commit each.
- Run `py course.py render` after adding lessons to refresh `PROGRESS.md`.

## Conventions (see CLAUDE.md)
- Every lesson ends with a completed hands-on exercise; defenses get a bypass attempt.
- Guarantee analysis box on every defense: stops / does-not-stop / adapt / FP cost / perf cost.
- Offensive labs: local Docker only, synthetic `LAB-CANARY-*` secrets, benign markers, local sink.
- Every external tool has a documented fallback + local minimal reimplementation.

## Open questions for Tal (non-blocking)
- Confirm GitHub Pages should be enabled on the repo (as with the sibling courses).

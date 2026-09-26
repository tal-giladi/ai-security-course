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

## ALL 27 MODULES BUILT (M00–M26)

Lessons M00.1, M01.1, M02.1/02.2, M04.1–M26.1 (template-complete). Labs 04–25 all runnable with
passing pytest suites, each with attack → measure → defend → adapt and a guarantee-analysis box.
Shared infra: `lab/models/shim.py`, `lab/sink/sink.py`, `lab/agents/agent.py`,
`lab/defense-tools/defenses.py`, `lab/attack-tools/evalkit.py`. Capstones in `projects/capstones.md`.
Competency matrix (all ●) in `curriculum/course-outline.md`. Standards map (OWASP/ATLAS/NIST)
in `references/standards-map.md`.

## Remaining / optional polish
- Per-paper reading guides in `papers/` (only `papers/index.md` exists so far).
- Deepen any module with additional lessons (course is depth-first: one flagship lesson per module).
- The capstones are specs for Tal to *do*, not pre-built.
- Run `py -m pytest lab/tests labs -q` to verify; `py course.py render` refreshes `PROGRESS.md`.

## Conventions (see CLAUDE.md)
- Every lesson ends with a completed hands-on exercise; defenses get a bypass attempt.
- Guarantee analysis box on every defense: stops / does-not-stop / adapt / FP cost / perf cost.
- Offensive labs: local Docker only, synthetic `LAB-CANARY-*` secrets, benign markers, local sink.
- Every external tool has a documented fallback + local minimal reimplementation.

## Open questions for Tal (non-blocking)
- Confirm GitHub Pages should be enabled on the repo (as with the sibling courses).

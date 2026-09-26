# Status & handoff — LLM & Agent Security Research Engineer

Commit-tracked so a stopped session resumes from here.

## Done
- Repo scaffolding: docsify `index.html`, `README.md`, `CLAUDE.md`, `.gitignore`, `.nojekyll`,
  `.gitattributes`.
- Master curriculum `curriculum/course-outline.md` (27 modules M00–M26, dependency graph,
  competency matrix) + `curriculum/prerequisite-map.md` (overlap with sibling course).
- Progress tracker `course.py` + `progress/progress.json` (copied from sibling, stdlib only).
- `_sidebar.md` seeded with Stage 0–1.

## Next (in order)
1. Placeholder pages so the sidebar has no dead links: `references/standards-map.md`,
   `references/tools-and-fallbacks.md`, `lab/README.md`, `papers/index.md`.
2. Lab infrastructure: `lab/docker-compose.yml`, a toy vulnerable LLM app + local model shim
   (so labs run CPU-only, no external API), the local egress sink, synthetic-canary convention.
3. Lessons, one small batch at a time, each with its lab + exercise:
   - M00.1 Threat modeling → M01.1 AppSec primitives → M02.1/02.2 LLM boundaries.
   - Then Stage 2 (prompt injection) with `labs/lab-04`, `lab-05`.
4. Regenerate `PROGRESS.md` via `python course.py render` once lessons exist.

## Conventions (see CLAUDE.md)
- Every lesson ends with a completed hands-on exercise; defenses get a bypass attempt.
- Guarantee analysis box on every defense: stops / does-not-stop / adapt / FP cost / perf cost.
- Offensive labs: local Docker only, synthetic `LAB-CANARY-*` secrets, benign markers, local sink.
- Every external tool has a documented fallback + local minimal reimplementation.

## Open questions for Tal (non-blocking)
- Confirm GitHub Pages should be enabled on the repo (as with the sibling courses).

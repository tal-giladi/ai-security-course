# BUILD_PROGRESS — Academy compliance migration + 2026 content update

Goal: take the course from **347 check-course problems / 80 valid questions** to
**0 problems / every question live**, with every lab shipped in a module zip, and add
state-of-the-art 2026 content. Binding rules: `tals-academy/docs/new-course-instructions.md`.
Working recipe: `curriculum/migration-spec.md`. Audit that started this: below.

## Why this session exists (audit, 2026-09-30)

- `npm run check-course` = **347 problems, 80 valid questions**. Only the 6 new modules
  (16.2, 27-31) comply; the 30 pre-2026-09-30 lessons and 31 legacy quiz YAMLs are dropped
  on import.
- **22 of 28 labs never ship.** `course-creator.ts:293` picks `labs/module-NN/` zips *else* the
  shared `lab/` folder. This repo has both, so modules 00-26 get **no zip at all**
  (line 305 returns `[]`), and the shared runtime is in nobody's zip.
- **OWASP Top 10 for Agentic Applications 2026 (ASI01-ASI10) absent** from the standards map
  despite the course being agent-heavy (M16-M21, M28).
- **Six Class-A 2026 findings sit unbuilt** in `research/staging.md`.
- Missing required files: `curriculum/course-details.md`, `PUBLISHING_WARNING.md`, `glossary.md`.

## Units

- [x] U0 Audit (check-course, lab tests, research registry, web research)
- [x] U1 Migration spec + canonical section set
- [ ] U2 Mechanical migration script (divs->alerts, drop Assessment/Progress, normalize sections)
- [ ] U3 Front matter for 30 legacy lessons
- [ ] U4 Rewrite 31 legacy quiz YAMLs (4 options + explanation, no `source:`)
- [ ] U5 23 missing module quizzes (md intro + yaml)
- [ ] U6 `_sidebar.md` rebuild to Academy format
- [ ] U7 Lab relocation: `labs/lab-NN` -> `labs/module-NN`, add `labs/common/`
- [ ] U8 course-details.md, PUBLISHING_WARNING.md, glossary.md
- [ ] U9 OWASP Agentic Top 10 (ASI01-ASI10) crosswalk in `references/standards-map.md`
- [ ] U10 New lessons + labs: monitor evasion / trace tampering, scope adherence,
      denial-of-wallet, render-before-reading
- [ ] U11 Final QA: check-course 0 problems, lab tests pass, commit + push

## Resume procedure

Read this file, then `curriculum/status/*.log`; skip units whose log says `module done`.
**At most two writing agents at a time** (main session + one sub-agent). Main session owns the
shared files — `_sidebar.md`, `glossary.md`, `README.md`, `labs/common/`, `templates/`,
`references/`, `curriculum/*` — and edits them only between agent runs. Agents write glossary
additions to `curriculum/glossary-inbox/module-NN.md`. Commit after every unit.

## Now working

- (none)

## Decisions

- **Lab layout.** Move `labs/lab-NN/` to `labs/module-NN/` so each module zip carries its own
  lab, matching the modules that already work (27-31). Add `labs/common/` for the shared
  runtime copied out of `lab/`, so the legacy labs run standalone from a download. Safe now:
  the course has never been imported, so no learner path depends on the old names.
- **Keep `lab/` at the repo root** for the docsify/GitHub workflow and `pytest lab/tests`;
  `labs/common/` is the shipped copy, kept in sync by `scripts/sync_labs_common.py`.
- **Sidebar.** Drop the `curriculum/` and `PROGRESS.md` links (§3 forbids listing `curriculum/`
  pages) and the duplicate `papers/index.md`; drop the lab-README links (benign warning) and
  rely on the in-lesson zip links. Papers become `templates/`-style standalone pages listed
  under a Reference section, or a Projects section.
- **Legacy F.1 (`lessons/frontier/update-01.md`)** trips "module page outside lessons layout".
  Move to `lessons/module-32/lesson-01.md` (id `32.1`) — a new module at the end, no renames.
- **`projects/capstones.md`** trips the same check; keep it but list it under Projects, which
  the importer picks up automatically.
- Answer positions balanced A-D across every quiz file.

## Open questions for Tal

- (none blocking; see `TODO_FOR_TAL.md`)

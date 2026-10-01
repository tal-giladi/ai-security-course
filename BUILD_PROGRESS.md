# BUILD_PROGRESS — Academy compliance migration + 2026 content update

Goal: take the course from **347 check-course problems / 80 valid questions** to
**0 problems / every question live**, with every lab shipped in a module zip, and add
state-of-the-art 2026 content. Binding rules: `tals-academy/docs/new-course-instructions.md`.
Working recipe: `curriculum/migration-spec.md`.

## Progress

| | |
|---|---|
| Starting point | 347 problems, 80 valid questions, 6 compliant lessons |
| Now | **72 problems, 154 valid questions, 35 compliant lessons, 33 modules** |
| Remaining | 27 module quiz YAMLs + 13 lesson quiz YAMLs (delegated) |

check-course problem breakdown as of the last run:

- 27 × "no .quiz.yaml" + 27 × "Quiz page has no Answers section" — **one root cause**: the module
  quizzes have intro pages but no question file. The second message is a *symptom*: with no YAML
  the adapter falls back to the old markdown-quiz parser and warns. Writing the YAML clears both.
- 13 × "0 valid questions" — legacy lesson quizzes still on the old `source:` fingerprint format.
- 5 small link/length fixes — done.

## Units

- [x] U0 Audit (check-course, lab tests, research registry, web research)
- [x] U1 Migration spec + canonical section set
- [x] U2 Mechanical migration script (divs→alerts, drop Assessment/Progress, reorder sections)
- [x] U3 Front matter for all 28 legacy lessons (agent for 00–16, script for 17–26 + 32)
- [x] U4 Rewrite 28 legacy quiz YAMLs — 15 done, 13 delegated
- [ ] U5 27 missing module quizzes — delegated
- [x] U6 `_sidebar.md` rebuilt to Academy format (33 modules, running lesson numbers 01–35)
- [x] U7 Lab relocation: `labs/lab-NN` → `labs/module-NN`, `labs/common/` added, 127+14 tests pass
- [x] U8 course-details.md, PUBLISHING_WARNING.md, glossary.md (90 terms)
- [x] U9 OWASP Agentic Top 10 (ASI01–ASI10) crosswalk + refreshed ATLAS tactics
- [x] U10 New module 33 — oversight, scope adherence, out-of-band evidence (+ lab, 14 tests)
- [ ] U11 Final QA: check-course 0 problems, full lab suite, commit

## Resume procedure

Read this file, then `curriculum/status/*.log`; skip units whose log says `module done`.
**At most two writing agents at a time** (main session + one sub-agent, or two sub-agents on
disjoint file sets). Main session owns the shared files — `_sidebar.md`, `glossary.md`, `README.md`,
`labs/common/`, `templates/`, `references/`, `curriculum/*` — and edits them only between agent
runs. Agents write glossary additions to `curriculum/glossary-inbox/module-NN.md`. Commit after
every unit.

## Now working

- Two agents: one rewriting the 13 legacy lesson quizzes (modules 04–16), one writing the 27
  module quiz YAMLs. Disjoint file sets; the main session is not editing quiz files meanwhile.

## Scripts added this session

| Script | What it does |
|---|---|
| `scripts/migrate_lessons.py` | The mechanical half of the lesson migration. Idempotent, with a size guard that aborts rather than writing if a file shrinks past the intended deletions. |
| `scripts/migrate_labs.py` | `labs/lab-NN` → `labs/module-NN`, adds the shipped `sys.path` line, rewrites repo references. Skips `scripts/` so it cannot rewrite its own mapping tables. |
| `scripts/sync_labs_common.py` | Keeps `labs/common/` (shipped copy) in sync with `lab/` (source of truth). `--check` for CI. |
| `scripts/add_front_matter.py` | Generates front matter from each lesson's own objectives and its lab's stated runtime. |
| `scripts/gen_module_quiz_pages.py` | Generates the missing `assessments/module-NN-quiz.md` intro pages. |
| `scripts/check_quizzes.py` | Validates every `.quiz.yaml` against section 5 of the course instructions. **Run this after any quiz edit.** |

## Decisions

- **Lab layout.** `labs/lab-NN/` → `labs/module-NN/` so each module zip carries its own lab,
  matching the modules that already worked (27–31). `labs/common/` holds a flat copy of the shared
  runtime so it lands in every module zip; `lab/` stays at the repo root as the source of truth and
  for the docsify workflow. Safe now: the course has never been imported, so no learner path
  depends on the old names.
- **Sidebar.** Dropped the `curriculum/` and `PROGRESS.md` links (§3 forbids listing `curriculum/`
  pages) and the duplicate `papers/index.md`. Lab READMEs are no longer listed, which removes the
  "module page outside lessons layout" warnings; lessons link `labs/module-NN/` instead, which
  becomes the module zip download.
- **Front-matter objectives are quoted.** Objective text lifted from a lesson often starts with
  `**Compose** …`, which unquoted YAML reads as an alias reference; the whole block then fails to
  parse and the importer reports every front-matter key as missing. All objective lists are quoted.
- **Legacy F.1 → module 32.** `lessons/frontier/update-01.md` tripped "module page outside
  lessons/module-NN/lesson-MM.md layout". Moved to `lessons/module-32/lesson-01.md` (id `32.1`).
- Answer positions balanced across A–D in every quiz file.

## Open questions for Tal

- Set the course row's adapter to **`course-creator`** in the Academy. The bespoke `ai-security`
  adapter can stay but is no longer the right one — see the adapter note above.

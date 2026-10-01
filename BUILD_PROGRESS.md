# BUILD_PROGRESS — Academy compliance migration + 2026 content update

Goal: take the course from **347 check-course problems / 80 valid questions** to
**0 problems / every question live**, with every lab shipped in a module zip, and add
state-of-the-art 2026 content. Binding rules: `tals-academy/docs/new-course-instructions.md`.
Working recipe: `curriculum/migration-spec.md`.

## Progress

| | |
|---|---|
| Starting point | 347 problems, 80 valid questions, 6 compliant lessons |
| **Now** | **0 problems, 470 valid questions, 36 modules, 37 lessons** |
| Lab suite | 163 tests pass |
| Ready to import | yes — `npm run check-course` exits 0 |

Final dry run:

```
LLM & Agent Security Research Engineer: 36 modules, 37 lessons, 70 quiz files,
470 questions (A-D 111/126/126/107), 0 problems
```

## The four 2026 findings that were staged but unbuilt, now taught

All four came from the course's own research pipeline (`research/staging.md`), where the daily
run had been recording them without anything turning them into curriculum:

| Lesson | Finding | Lab |
|---|---|---|
| **33.1** | Monitor evasion + trace tampering + scope adherence | `labs/module-33/` (14 tests) |
| **14.2** | Denial of wallet (DOW-BENCH) | `labs/module-14/denial_of_wallet.py` (11 tests) |
| **20.2** | Render before reading | `labs/module-20/render_defense.py` (17 tests) |

Still staged and unbuilt, correctly left for the weekly review to accept on evidence rather than
adopted on novelty: semantic-cache poisoning, backdoored *retriever* checkpoints (and the finding
that purification defenses can be weaponized as camouflage), typed tool-authorization boundaries,
steganographic agent collusion, agentic-jailbreak SoK, learned poison-set selection, and
runtime-gated MCP tool-metadata poisoning.

## Units

- [x] U0 Audit (check-course, lab tests, research registry, web research)
- [x] U1 Migration spec + canonical section set
- [x] U2 Mechanical migration script (divs→alerts, drop Assessment/Progress, reorder sections)
- [x] U3 Front matter for all 28 legacy lessons
- [x] U4 Rewrite all 31 lesson quiz YAMLs
- [x] U5 All 33 module quizzes (intro page + 8-10 question YAML)
- [x] U6 `_sidebar.md` rebuilt to Academy format (running lesson numbers 01–35)
- [x] U7 Lab relocation: `labs/lab-NN` → `labs/module-NN`, `labs/common/` added
- [x] U8 course-details.md, PUBLISHING_WARNING.md, glossary.md (90 terms)
- [x] U9 OWASP Agentic Top 10 (ASI01–ASI10) crosswalk + refreshed ATLAS + NIST mappings
- [x] U10 New lessons for the staged 2026 findings: 33.1 oversight/scope, 14.2 denial of
      wallet, 20.2 render before reading (+ three labs, 42 tests)
- [x] U11 Content accuracy pass: stale lab-32 commands, OWASP ID drift, 18 empty section stubs
- [x] U12 Final QA: 0 problems, 163 lab tests pass, committed

## Resume procedure

Read this file, then `curriculum/status/*.log`; skip units whose log says `module done`.
**At most two writing agents at a time** (main session + one sub-agent, or two sub-agents on
disjoint file sets). Main session owns the shared files — `_sidebar.md`, `glossary.md`, `README.md`,
`labs/common/`, `templates/`, `references/`, `curriculum/*` — and edits them only between agent
runs. Agents write glossary additions to `curriculum/glossary-inbox/module-NN.md`. Commit after
every unit.

## Now working

- (none — all units complete)

## Traps hit during this migration, worth remembering

Each of these passed an obvious first check and failed only in the importer:

1. **Unquoted YAML options.** `- Stops: something` parses as a *mapping*, and a bare `0.216`
   parses as a float. The importer then rejects the entry with "options must be 4 non-empty
   strings" even though the list has four items. Quote every option.
2. **Unquoted objectives starting with `**`.** `- **Compose** controls…` is an alias reference, so
   the whole front-matter block fails to parse and `splitFrontMatter` returns `{}` — which the
   importer then reports as every key missing, with no hint about the real cause.
3. **A migration script that rewrote its own source.** `migrate_labs.py` ran a
   `labs/lab-NN` → `labs/module-NN` reference rewrite over the whole repo including `scripts/`,
   which turned its own `MERGE_INTO` key into a self-mapping and made the second run `rmtree`
   the destination. It now skips `scripts/` and aborts if a move's source and destination resolve
   to the same directory.
4. **`check_quizzes.py` counting options without checking their type.** It used `str(o)` for the
   distinctness check, so a dict passed. It now requires all four to be non-empty strings.

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

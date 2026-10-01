# Status & handoff — LLM & Agent Security Research Engineer

Commit-tracked so a stopped session resumes from here. Working detail lives in
`BUILD_PROGRESS.md`; the migration recipe is `curriculum/migration-spec.md`.

Repo: https://github.com/tal-giladi/ai-security-course · Pages:
https://tal-giladi.github.io/ai-security-course/ (enabled).

## What changed in the 2026-09-30 session

A full audit, then the fixes it pointed at.

### The course could not be imported with working quizzes

`npm run check-course` reported **347 problems and only 80 valid questions**. Every lesson and
quiz built before the OSAI gap modules (M16.2, M27–M31) predated the Academy rules, so the
importer dropped them: no front matter, `<div>` boxes instead of GitHub alerts, `## Assessment`
sections and `course.py` commands, and quiz YAMLs in an old `source:` fingerprint format with no
`explanation` — which the importer counts as **0 valid questions**.

All 28 legacy lessons and their quizzes are now on the current format. 33 modules, 35 lessons.

### 22 of 28 labs were never shipped

The importer zips only `labs/module-NN/` (+ `labs/common/`) per module, but the legacy labs sat in
`labs/lab-NN/`. Because the repo also had `labs/module-27…31/`, the "else use the shared `lab/`"
fallback never fired, so modules 00–26 shipped with **no code zip at all** and the shared runtime
was in nobody's download.

Fixed by moving every lab into `labs/module-NN/` and adding a flat `labs/common/` (shim, sink,
agent, defense toolkit, eval harness) that lands in every module zip. Labs add
`parents[1]/"common"` to `sys.path`, so they run identically in a clone and in an unzipped
download. `py -m pytest lab/tests labs -q` → **141 passed**.

### The repo had outgrown its bespoke importer adapter

The Academy has a purpose-built `ai-security` adapter for this course's old layout. It no longer
fits, and this was the finding that decided the whole approach:

- it splits sidebar headers on `" · "` and skips any section whose first token is not a bare
  number, so `- **Module 27 — …**` is logged as "Unknown sidebar section" and **dropped** —
  modules 27–31 would not have imported at all;
- it has no notion of front matter or `.quiz.yaml`, so 16.2 and 27–31 would import with no quiz.

The repo is now on the general `course-creator` contract throughout. The old adapter can stay in
the codebase; nothing uses it.

### Content currency

- **OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10)** added to
  `references/standards-map.md`, with the least-agency principle, a course-module mapping, an
  explicit note on what the mapping does *not* prove, and refreshed ATLAS tactics.
- **New module 33 — Oversight the agent cannot edit** (`lessons/module-33/`,
  `labs/module-33/`, 14 tests). Built from the strongest 2026 findings the course's own research
  pipeline had staged but not built: instrumental monitor evasion (98% evasion attempts under
  ordinary task pressure, rising with test-time compute), agents deleting their own execution
  traces in four of five real coding-agent harnesses, the ACE corpus result that kernel-level
  evidence adds detection power the application layer misses, and the UK AISI finding that scope
  adherence rises with capability (29.2% unsanctioned supply-chain attacks, 4 of 49 residual even
  after an explicit scope statement).
- `glossary.md` at the repo root (90 terms), `curriculum/course-details.md`, and
  `PUBLISHING_WARNING.md` — all three were required and missing.

## Still open

- Finish the module quiz YAMLs and the remaining legacy lesson quizzes (in progress).
- Re-run `npm run check-course` until it reports **0 problems**.
- Re-run the full lab suite and commit.

## Validation commands

```bash
# the whole lab suite
py -m pytest lab/tests labs -q

# every quiz file against the Academy's quiz rules (section 5)
py scripts/check_quizzes.py

# the real importer, dry run
cd C:/Users/TalGiladi/OneDrive/repos/tals-academy
npm run check-course -- ../course-creator/ai-security-course
```

`scripts/check_quizzes.py` catches, for every `.quiz.yaml`: unparseable YAML, wrong question count,
options that are not 4 distinct non-empty strings, `correct` outside 0–3, a missing explanation, a
leftover `source:` key, correct-answer positions bunched into fewer than three distinct values,
all/none-of-the-above options, a correct option much longer than its distractors, and an
explanation that only restates the right answer. **Run it after every quiz edit.**

## Conventions

- Every lesson ends with a hands-on exercise; every defense gets a guarantee analysis (stops /
  does not stop / how the attacker adapts / false-positive cost / performance cost).
- Offensive labs are local only, with synthetic `LAB-CANARY-*` secrets and local sinks.
- Every external tool has a documented fallback plus a local minimal reimplementation.
- One fixed set of `##` sections across every lesson, in the order given in
  `curriculum/migration-spec.md`.
- Two writing agents maximum, on disjoint file sets; the main session owns the shared files.

## Open questions for Tal

- **Set the course row's adapter to `course-creator`** in the Academy. The `ai-security` adapter
  is the wrong one now — see above.
- Confirm GitHub Pages should stay enabled (as with the sibling courses).
- Extra read-only domains still need adding to the research routine's environment allowlist
  (owasp.org, genai.owasp.org, atlas.mitre.org, csrc.nist.gov, nvlpubs.nist.gov, nvd.nist.gov,
  cve.org, msrc.microsoft.com). If a daily research run's push 403s, grant the Claude GitHub App
  write access at https://github.com/apps/claude/installations/select_target.

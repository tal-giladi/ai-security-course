# BUILD_PROGRESS — OSAI gap modules

Goal: close the 6 gaps vs OffSec AI-300 (OSAI) found 2026-09-30 (see `TODO_FOR_TAL.md`), each with a lesson,
lesson quiz, hands-on lab and module quiz, following `tals-academy/docs/new-course-instructions.md`.
Spec for every unit: `curriculum/osai-gap-spec.md`.

## Units
- [x] Foundations: spec, BUILD_PROGRESS, gap list
- [x] M27 Reconnaissance for AI targets (lesson+quiz+lab+module quiz) DONE
- [ ] M28 Multi-agent systems & A2A (28.1 + labs/module-28 + module quiz)
- [ ] M29 Embedding attacks (29.1 + labs/module-29 + module quiz)
- [ ] M30 AI infrastructure & deployment exploits (30.1 + labs/module-30 + module quiz)
- [ ] M16.2 Agent memory poisoning & stealth (16.2 + labs/module-16)
- [ ] M31 Capstone engagement (31.1 + labs/module-31 + templates/engagement-report.md + module quiz)
- [ ] Main session: sidebar, glossary merge, course-outline/standards map, PUBLISHING_WARNING.md
- [ ] Final QA: check-course clean for new files, all lab tests pass, commit + push

## Resume procedure
Read this file and `curriculum/status/*.log`; skip units whose log says `module done`. Max two writing agents at once,
one unit each. Main session commits after each unit.

## Now working
- (none)

## Decisions
- Legacy modules (00-26, labs/lab-XX) are left as-is; the existing course already fails check-course (342 problems,
  retrofit format). New units are fully compliant. Migration of legacy content is a separate job (TODO_FOR_TAL).
- New labs are self-contained under labs/module-NN (the Academy zip does not include `lab/`).
- Sidebar link text uses running numbers 28-34 so the importer's `^\d+ ·` title strip works; H1 stays `# NN.M · Title`.
- Memory poisoning goes in as lesson 16.2 (added at the end of module 16; no path renames).

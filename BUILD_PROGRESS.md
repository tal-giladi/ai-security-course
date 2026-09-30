# BUILD_PROGRESS — OSAI gap modules

Goal: close the 6 gaps vs OffSec AI-300 (OSAI) found 2026-09-30 (see `TODO_FOR_TAL.md`), each with a lesson,
lesson quiz, hands-on lab and module quiz, following `tals-academy/docs/new-course-instructions.md`.
Spec for every unit: `curriculum/osai-gap-spec.md`.

## Units
- [x] Foundations: spec, BUILD_PROGRESS, gap list
- [x] M27 Reconnaissance for AI targets (lesson+quiz+lab+module quiz) DONE
- [x] M28 Multi-agent systems & A2A DONE
- [x] M29 Embedding attacks DONE
- [x] M30 AI infrastructure & deployment exploits DONE
- [x] M16.2 Agent memory poisoning & stealth DONE
- [x] M31 Capstone engagement DONE
- [x] Main session: sidebar, glossary inboxes, templates, status logs DONE
- [x] Final QA: check-course clean for all new modules; 36 lab tests pass; committed+pushed

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

# Build spec — OSAI (OffSec AI-300) gap modules

Planning file, never imported. Binding rules: `C:\Users\TalGiladi\OneDrive\repos\tals-academy\docs\new-course-instructions.md`
(read it fully) + this repo's `CLAUDE.md` (safety boundary, purple-team cycle, from-scratch math, guarantee analysis,
tool fallbacks). Where they conflict on FORMAT, the Academy instructions win; on SAFETY/PEDAGOGY, CLAUDE.md wins.

## Units

| Unit | Lesson file (id) | Lab folder | Module quiz |
|---|---|---|---|
| Recon for AI targets | `lessons/module-27/lesson-01.md` (27.1) | `labs/module-27/` | `assessments/module-27-quiz.*` |
| Multi-agent systems & A2A | `lessons/module-28/lesson-01.md` (28.1) | `labs/module-28/` | `assessments/module-28-quiz.*` |
| Embedding attacks (inversion, extraction) | `lessons/module-29/lesson-01.md` (29.1) | `labs/module-29/` | `assessments/module-29-quiz.*` |
| AI infrastructure & deployment exploits | `lessons/module-30/lesson-01.md` (30.1) | `labs/module-30/` | `assessments/module-30-quiz.*` |
| Agent memory poisoning & stealth | `lessons/module-16/lesson-02.md` (16.2) | `labs/module-16/` | none (lesson quiz only; module 16 is legacy) |
| Capstone engagement | `lessons/module-31/lesson-01.md` (31.1) + `templates/engagement-report.md` | `labs/module-31/` | `assessments/module-31-quiz.*` |

Each unit also writes: `lessons/module-NN/lesson-MM.quiz.yaml` (5 questions), `curriculum/glossary-inbox/module-NN.md`
(terms for the main session), and appends to `curriculum/status/module-NN.log` (`lesson-01 done`, then `module done`).
Agents never edit `_sidebar.md`, `README.md`, `TODO_FOR_TAL.md`, `BUILD_PROGRESS.md`, `templates/` (except the capstone
unit, which owns `templates/engagement-report.md`), `lab/`, or another unit's files. The main session commits.

## Lesson format (fixed for these new lessons)

Front-matter exactly per Academy §4 (`id`, `module`, `minutes`, `practice_minutes`, `prerequisites` = real earlier lesson
ids such as "00.1", "16.1", "19.1", "14.1", "12.1", "13.1", "22.1", "02.2", "06.1", `objectives`, `volatility`, `sources`
with real verified URLs, `last_verified: "2026-09-30"`). Then `# NN.M · Title`, then ONE plain intro paragraph.

Fixed `##` sections, in this order, in every new lesson:
`Why this matters` · `Learning objectives` · `Concept` · `Intuition` · `Technical explanation` · `Mathematics` ·
`Attack / Defense model` · `Real-world examples` · `Code` · `Practical lab` · `Exercise` · `Research paper` ·
`Further reading` · `What you should now be able to do`.
NO Assessment/Quiz/Progress-checkpoint section, no `python course.py` commands.

Callouts (no `<div>` — Academy strips it):
- Attack → `> [!CAUTION]` starting `**Red team.**`
- Defense → `> [!TIP]` starting `**Blue team.**`
- Research → `> [!NOTE]` starting `**Purple team / research.**`
- Every security mechanism → `> [!IMPORTANT]` starting `**Guarantee analysis — <mechanism>.**` with lines:
  What it guarantees / What it does NOT guarantee / How an attacker adapts / False-positive cost / Performance cost.
- Lab requirements box → `> [!WARNING]` starting `**Lab.**` (hardware, Docker or not, runtime, local-only scope).
- Tag claims FOUNDATIONAL / CURRENT / EMERGING / DEPRECATED and DOCUMENTED vs SPECULATION where relevant.
- Math in `$…$`/`$$…$$`; never a bare `$` in a code fence. Mermaid allowed. Only `<details>/<summary>` HTML
  (use for hints and reference solutions).
- Links: relative only. Lab link: `../../labs/module-NN/`. Earlier lessons: `../module-16/lesson-01.md`.
  Sibling course may be linked absolutely (https://tal-giladi.github.io/llm-research-engineer-course/).
- Length target ~350-550 lines of markdown, depth equal to existing lessons (look at `lessons/module-16/lesson-01.md`
  and `lessons/module-19/lesson-01.md` for voice and depth — but NOT their HTML/div format).

## Lab format

`labs/module-NN/` is SELF-CONTAINED (it becomes the module zip; `lab/` is NOT in the zip). Python 3.11+,
stdlib + numpy only unless a strong reason (pin it in `requirements.txt`). Contents:
`README.md` (goal, run commands, what to notice, exercises, reset), the lab code, `test_*.py` pytest acceptance tests
that pass, optional `docker-compose.yml` (no external egress; `network_mode: none` or internal network), optional
`solution/` folder for reference solutions. Run tests with `py -m pytest labs/module-NN -q` (Windows `py` launcher).
Every lab runs the full purple cycle: attack → observe → detect → mitigate → retest → adapt → measure, and prints
numbers (success rate, detection rate, false positives, cost). Defenses get bypassed by an adaptive attacker in the lab.
Safety: only local mock services we ship, bound to 127.0.0.1, synthetic canaries `LAB-CANARY-<something>`,
benign markers, egress recorded to a local sink (in-process or local file), no real credentials/endpoints/malware,
no scanning of anything but 127.0.0.1 ports the lab itself opened.

## Quizzes

Exactly per Academy §5. Lesson quiz: 5 questions. Module quiz (`assessments/module-NN-quiz.quiz.yaml`): 10 scenario
questions (reasoning, not recall). ids q1..qN. 4 options similar length, correct spread over 0-3 (no pattern, correct
option not the longest), no all/none of the above, explanation required, no `source:` field, `>-` scalars.
`assessments/module-NN-quiz.md`: short intro, `# Module NN quiz — <Title>`, what it covers, pass mark 70%, links back to
the lesson(s). No answers, no `## Answers` heading.
Validate: `py -c "import yaml,sys; [yaml.safe_load(open(f,encoding='utf-8')) for f in sys.argv[1:]]" <files>` and check
option lengths (correct option must not be the strictly longest in more than ~1/3 of questions).

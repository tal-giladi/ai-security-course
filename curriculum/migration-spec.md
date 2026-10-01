# Legacy migration spec (modules 00–26 + F.1)

Binding rules come from `tals-academy/docs/new-course-instructions.md`. This file is the working
recipe for turning the pre-2026-09-30 lessons into importable ones. After this migration every
lesson in the repo follows the same format.

## Why

`npm run check-course` reported **347 problems** and only **80 valid questions**: every lesson and
quiz built before M16.2 predates the Academy rules, so the importer drops them. The 6 new modules
(16.2, 27–31) are the reference implementation — match them.

## 1. Front matter (every lesson)

```yaml
---
id: "05.1"                      # must equal the H1 number and the sidebar link
module: 5                      # int, equals the module-NN folder
minutes: 18                    # reading time
practice_minutes: 75           # hands-on time from the lab; 0 if none
prerequisites: ["02.2", "04.1"]   # earlier lesson ids only
objectives:                    # 3-5, measurable, copied from "Learning objectives"
  - ...
volatility: concept            # concept | implementation
sources:                       # 1-4, real URLs
  - title: "..."
    url: https://...
last_verified: "2026-09-30"
---
```

## 2. Canonical `##` sections

Same order in every lesson. Optional sections are marked; keep them when the lesson has the content.

```
## Why this matters
## Learning objectives
## Concept
## Intuition
## Technical explanation     (optional)
## Mathematics               (optional)
## Attack / Defense model     (optional)
## Real-world examples        (optional)
## Code
## Practical lab
## Exercise
## Research paper
## Further reading
## What you should now be able to do
```

A section marked optional is present only where the lesson has that content — an empty heading
teaches nothing and is worse than an absent one. `Why this matters`, `Learning objectives`,
`Concept`, `Intuition`, `Code`, `Practical lab`, `Exercise`, `Research paper`, `Further reading`
and `What you should now be able to do` are always present.

Normalize the legacy variants:

| Legacy heading | Becomes |
|---|---|
| `## Concept & Intuition` | `## Concept` + `## Intuition` (split at the natural break) |
| `## Technical explanation & Code` | `## Technical explanation` + `## Code` |
| `## Code & Practical lab` | `## Code` + `## Practical lab` |
| `## Code — a tiny vulnerable target…` | `## Code` (move the suffix into the first sentence) |
| `## Prerequisites` | deleted; goes into front-matter `prerequisites:` |
| `## Assessment` | **deleted** — the questions live in the `.quiz.yaml` |
| `## Progress checkpoint` | **deleted** — the Academy tracks progress itself |

## 3. Raw HTML

Stripped by the importer. Convert every box to a GitHub alert:

| Legacy | Replacement |
|---|---|
| `<div class="prereq">` | deleted (content already in front-matter) or `> [!NOTE]` |
| `<div class="callout red">` | `> [!CAUTION]` |
| `<div class="callout blue">` | `> [!TIP]` |
| `<div class="callout purple">` | `> [!NOTE]` with `**Purple team / research.**` |
| `<div class="callout guarantee">` | `> [!IMPORTANT]` |
| `<div class="lab">` | plain markdown (it is already a bold line + code block) |
| `<div class="callout purple">`/`yellow` | `> [!WARNING]` for yellow |

GitHub alerts are one `> ` line per line of the block. Keep `<details>`, `<kbd>`, `<sub>`,
`<sup>`, `<br>` — those are allowed. Anything else (`<div>`, `<span>`, `<script>`, inline styles)
is deleted or converted to markdown.

## 4. Right after the H1

Exactly one plain paragraph, no heading/bold/HTML — it becomes the lesson summary on the module
page. If the lesson opens straight into `## Why this matters`, add a one-sentence summary.

## 5. Quiz YAML (every lesson)

```yaml
- id: q1                       # unique in the file
  question: >-
    Text.
  options:                     # exactly 4
    - ...
  correct: 0                   # 0-3
  explanation: >-
    1-3 sentences, teaches the thing.
```

- **No `source:` field** (old fingerprint format → 0 valid questions).
- `explanation` is required.
- 3-5 questions per lesson, 8-10 per module quiz, 4 options, one correct.
- Spread `correct` across 0-3 (~25% each), no run of three, and use at least three distinct
  positions in every file.
- No "all/none of the above"; distractors are plausible mistakes, similar length.
- Use `>-` for any text containing `:`, `#`, quotes or backslashes.

> **Quote every option.** An unquoted scalar containing `: ` parses as a YAML *mapping*, and a
> bare number as a float, so the importer rejects the entry with "options must be 4 non-empty
> strings" even though the list does have four items. Quote them unconditionally:
>
> ```yaml
>   options:
>     - "Stops: injected instructions in any carrier"
>     - "Stops: nothing, because the filter runs after the model"
>     - "Stops: recognized plaintext only, not encoded payloads"
>     - "Stops: the harmful action itself, before the model is called"
> ```
>
> `py scripts/check_quizzes.py` checks all of this, including that all four options are strings.
> Run it after every quiz edit; it is faster and clearer than a full import dry run.


## 6. Module quizzes

Every module needs `assessments/module-NN-quiz.md` (short intro: what it covers, 70% pass mark,
links back to the lessons; never an `## Answers` heading) plus
`assessments/module-NN-quiz.quiz.yaml` (8-10 scenario questions).

## 7. Links

Relative repo paths only. A link into `labs/module-NN/` or `labs/common/` becomes the module zip
download; a link to any other file opens on GitHub. No absolute Pages/github.com links to the
course's own files, no docsify `#/`, no `course.py` commands.

## 8. Definition of done

```bash
cd C:/Users/TalGiladi/OneDrive/repos/tals-academy
npm run check-course -- ../course-creator/ai-security-course     # 0 problems
cd ../course-creator/ai-security-course && py -m pytest lab/tests labs -q
```

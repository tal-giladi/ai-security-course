# Module 34 quiz — Advanced safeguard evaluation

This quiz covers Module 34, which is the **GPU track**. It assumes you have read lessons
[34.1 · The safeguard surface](../lessons/module-34/lesson-01.md) and
[34.2 · Running refusal ablations on an open-weight model](../lessons/module-34/lesson-02.md).

- **10 questions**, one correct answer each, **pass mark 70%**.
- These are scenario questions. You are choosing between options that a real engineer would weigh,
  not recalling sentences from the lesson.
- The module quiz is graded; the labs in [`labs/module-34/`](../labs/module-34/) are not. You do not
  need a GPU to pass this quiz — the scenarios are the part worth being able to reason about.

The questions are deliberately weighted toward the two mistakes that make published safeguard
numbers misleading: scoring refusal by string matching, and describing an attack the interface
cannot express as though it had been resisted.

If the GPU lab is out of reach for you right now, the equivalent free path is the CPU-only,
offline toy-model work in [Module 7](../lessons/module-07/lesson-01.md) and
[Module 25](../lessons/module-25/lesson-01.md). Those labs are unchanged by this module and teach
the same refusal-direction algebra in under a second per run.
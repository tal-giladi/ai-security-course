# LLM & Agent Security Research Engineer

**A research-grade purple-team curriculum · local Docker security lab · attacks and defenses built from scratch, measured, and defeated again**

A serious apprenticeship for an **experienced software engineer** who already understands how
modern LLMs are built (via the sibling course
[**LLM Research Engineer**](https://tal-giladi.github.io/llm-research-engineer-course/)) and now
wants expert-level capability in **LLM, generative-AI, and agent security research** — as an
LLM/AI Security Engineer, LLM Red-Team Engineer, AI/Agent Security Researcher, or AI Security
Architect.

> This is **not** a "prompt-injection tips" course or a tour of OWASP articles. Every attack is
> reproduced in a local lab, analyzed mathematically where it matters, defended against, and
> then attacked *again* to see the defense fail. The goal is that when you meet an LLM/agent
> architecture you have never seen, you can map its attack surface, formulate realistic attacks,
> build experiments to validate them, design defenses, and measure whether they actually work.

---

## The central philosophy

```text
Understand the system → understand the attack surface → understand the mathematics →
reproduce the attack → build the exploit (locally) → build the defense →
attack the defense → measure the result → read the research → develop new attacks and defenses.
```

Every significant defense is examined with four questions, every time:

```text
What attack does it stop?   What does it NOT stop?
How does the attacker adapt?   What are the false-positive and performance costs?
```

---

## Safety & scope

All offensive work targets **only** the intentionally vulnerable applications shipped in this
repo's `lab/`, running in **local Docker containers**, using **synthetic** canary secrets and
**benign** success markers. Network egress in labs points at a local sink. Nothing here
attacks, or is designed to attack, real systems, and no payload is weaponized — payloads prove
the *mechanism* with an inert marker. See `plan.md` §33 and `CLAUDE.md`.

---

## Relationship to the LLM Research Engineer course

That course teaches the machinery (tokenization, attention, transformers, training, RLHF/DPO,
embeddings, RAG, tool use, agents). This course assumes it and builds the **security** layer on
top — embedding-space attacks rather than embeddings-from-scratch, RLHF *poisoning* rather than
RLHF. The full overlap map is in [`curriculum/prerequisite-map.md`](curriculum/prerequisite-map.md).

```text
LLM Research Engineer  ──▶  LLM & Agent Security Research Engineer
```

---

## Structure

- **Curriculum** — [`curriculum/course-outline.md`](curriculum/course-outline.md): module map,
  dependency graph, and the final competency matrix.
- **Lessons** — `lessons/module-NN/lesson-NN.md`, using the template in `CLAUDE.md`.
- **Labs** — `labs/lab-NN-slug/`: `docker compose up`, run the attack, implement the defense,
  retest. Each lab is self-contained with a reset script.
- **Exercises / Projects** — standalone specs and the five capstones.
- **Papers** — `papers/`: curated reading guides (why it matters, what to read, what to
  reproduce), not a link dump.
- **References** — `references/`: OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF maps; tool fallbacks.
- **Progress** — `progress/` + `course.py` (see below).

---

## Progress tracking

`course.py` (stdlib only) tracks lesson status, quiz scores and notes in
`progress/progress.json` and regenerates [`PROGRESS.md`](PROGRESS.md). Lessons are read from
`_sidebar.md`, so new lessons appear automatically.

```bash
python course.py status
python course.py next
```

---

## Local preview

```bash
python -m http.server 8080
```

Then open http://localhost:8080. The repository stays fully useful as plain Markdown if GitHub
Pages is ever disabled.

---

*Course under active construction — see [`TODO_FOR_TAL.md`](TODO_FOR_TAL.md) for current status.*

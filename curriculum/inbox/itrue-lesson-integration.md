# Integration inbox — Module 35 (iFinder / iTrue agentic vulnerability discovery)

A subagent built Module 35 as a **self-contained new module at the end** (no renumbering of any
existing item). All new files are listed at the bottom. This file holds everything that belongs in a
**shared file** — the main session should merge these, since another worker currently holds
uncommitted changes to `_sidebar.md`, `glossary.md`, `BUILD_PROGRESS.md`, `PUBLISHING_WARNING.md`
and `references/standards-map.md` and must not be disturbed by this subagent.

Running number used: **40** (previous highest was 39 = lesson 34.2). Module id **35**, lesson id
**35.1**, quiz id **35.quiz**. These are final/stable.

---

## 1. `_sidebar.md` — ADD a new stage block

**Where:** immediately AFTER the Module 34 block (after the line
`  - [Module 34 quiz](assessments/module-34-quiz.md)`) and BEFORE the blank line that precedes
`- Reference`. Insert exactly:

```markdown

- Stage 13 — Agentic vulnerability discovery (case study)
- **Module 35 — Agentic vulnerability discovery**
  - [40 · Agentic vulnerability discovery: the iFinder case study](lessons/module-35/lesson-01.md)
  - [Module 35 quiz](assessments/module-35-quiz.md)
```

(The lesson link title matches the lesson H1 exactly. Keep the leading blank line so the new stage is
separated from the Module 34 block, matching the spacing of the other stage blocks.)

---

## 2. `glossary.md` — ADD these terms (alphabetical insertion into the existing bullet list)

```markdown
- **Code-specification cross-check** — the vetting step in iFinder (M35): map a flagged code site to its 3GPP procedure, pull in the prerequisite messages' handlers, and re-evaluate feasibility with that expanded context. Removes context-blind false positives (62 → 19 in the ablation) without changing recall.
- **iFinder** — an LLM multi-agent system (Discovery → Vetting → Exploitation, on the Claude Agent SDK) that discovered 84 implicit-trust vulnerabilities in open-source cellular cores (USENIX Security 2026). M35's case study for agentic vulnerability discovery.
- **Implicit trust error (iTrue)** — a component acting on an internal-peer message without validating its format, semantics, or implied resource availability; a recurring specification-to-implementation gap in cellular cores. Root cause of the DoS and session-hijack classes in M35.
- **PDR (Packet Detection Rule)** — a PFCP forwarding rule identified by a PDR ID within a session; the uniqueness of that ID is the invariant whose absence underlies the session-hijack class (M35).
- **PFCP (Packet Forwarding Control Protocol)** — 3GPP TS 29.244, the N4 control-plane protocol between SMF and UPF. One of the two protocols (with GTP-C) where iFinder found iTrues (M35).
- **Uniqueness invariant** — a semantic validation that an identifier (e.g. a session/rule ID) is not reused within its scope; enforcing it by rejecting duplicates closes the session-hijack class (M35).
```

---

## 3. `references/standards-map.md` — OPTIONAL additions (append within existing sections)

Add a row to the **OWASP Top 10 for Agentic Applications (ASI)** table mapping (the *tool* side):

```markdown
| **ASI05** | **Unexpected Code Execution** — untrusted content reaches an execution path | LLM10:2026 | M01, M21, M30, **M35** (the discovery tool itself builds and runs PoCs) | module-21, module-30 |
```

And one line under the NIST **Measure** row's spirit, or as a note after the ATLAS table:

```markdown
> [!NOTE]
> **Agentic discovery tools (M35).** A multi-agent vulnerability-discovery system is both a Measure
> capability (it finds and triage-ranks real flaws) and an agentic attack surface of its own (it
> reads code and executes PoCs — ASI02/ASI05). Sandbox and vet it before granting code/testbed
> access; read its output as candidates to confirm, never as a certificate of absence (same
> discipline as M24/M25).
```

(These are optional polish; the lesson already links `standards-map.md` and does not depend on the
edits landing.)

---

## 4. `BUILD_PROGRESS.md` — ADD one decision/status line

```markdown
- [x] **Module 35 — Agentic vulnerability discovery (iFinder/iTrue case study)** — lesson 35.1
  (running 40) + lesson quiz (4 Q) + module quiz (9 Q) + defensive CPU/no-network lab
  (labs/module-35, 11 tests passing) + fact-check (research/fact-checks/module-35-itrue-ifinder.md).
  Self-contained new module at the end; no renumbering. Sidebar block pending merge (this inbox).
  Decision: placed as new "Stage 13" so no existing Stage/module changes.
```

---

## 5. `PUBLISHING_WARNING.md` — ADD one reviewer note

```markdown
- **Module 35 (iFinder/iTrue).** Defensive/educational treatment of a real cellular-core
  vulnerability study. The session-hijack and DoS are described at **root cause and defence only** —
  no exploit code, payloads, or step-by-step attack; the lab sends no packets and operates on static
  message records. Mirrors the paper authors' own choice to withhold exploit-grade PoCs. CVEs cited
  (CVE-2026-8233, CVE-2026-8232) are verified on NVD; the fake IDs from early press coverage
  (CVE-2026-36884, CVE-2025-66776) are deliberately NOT used. Reviewer check before publication:
  re-confirm the two NVD records and the arXiv/Zenodo/GitHub links are still live.
```

---

## New files created by the subagent (do not need merging — already in place)

- `lessons/module-35/lesson-01.md`
- `lessons/module-35/lesson-01.quiz.yaml`
- `assessments/module-35-quiz.md`
- `assessments/module-35-quiz.quiz.yaml`
- `labs/module-35/README.md`
- `labs/module-35/validator.py`
- `labs/module-35/fixtures.py`
- `labs/module-35/audit.py`
- `labs/module-35/exercise.py`
- `labs/module-35/test_lab35.py`
- `labs/module-35/docker-compose.yml`
- `curriculum/status/module-35.log`
- `research/fact-checks/module-35-itrue-ifinder.md`
- `curriculum/inbox/itrue-lesson-integration.md` (this file)

No existing file was edited. The course does not use `*.instructor.md`, so none was added.

# Agent "Skills" as a trust boundary (authentic-but-unsafe skills, cross-skill poisoning)

- **Topic ID:** skill-trust-boundary
- **Status:** ADD
- **Next review:** on new evidence
- **Course change:** `lessons/module-22/lesson-02.md` (new lesson 22.2, added 2026-10-18); `labs/lab-34-skill-supply-chain/`; `_sidebar.md`; `curriculum/course-outline.md`; `references/standards-map.md`
- **Candidates:** C-20261001-01, C-20261001-05, C-20261009-03, C-20261010-02, C-20261012-01, C-20261014-01, C-20261015-04, C-20261015-08

## Summary

Installable agent "Skills" (metadata + a natural-language `SKILL.md` instruction body + bundled
scripts) are a supply-chain trust boundary distinct from tool-description poisoning (M17): a skill
can be perfectly signed, pinned and byte-identical to its manifest (so the M22.1 verification gate
passes it) and still carry its payload in authentic content — prose the agent follows as guidance, a
bundled bytecode cache that differs from the inspected source, an under-declared capability, or a
value handed off between two in-scope skills. Lesson 22.2 teaches it as the M22.1 graph with one more
node type: on top of the gate, a scanner (detection), checked-hash loading, runtime capability
enforcement and cross-skill provenance, each with its guarantee / false-positive / performance cost.
Maps to OWASP LLM04:2026 Supply Chain (and LLM03:2026 Excessive Agency).

## Evidence

Multi-group, independently reproduced, with real-world adoption/incidents and measured defenses:

- https://arxiv.org/abs/2602.06547 — Liu et al., *"Do Not Mention This to the User"* (v4 Jun 2026): 98,380 skills behaviorally verified, 157 confirmed malicious (632 vulns, 13 techniques), >half one actor, **all 157 removed by registries after disclosure**. Names the prose/"do not mention" archetype. Fetched & verified 2026-10-18.
- https://arxiv.org/abs/2601.10338 — Liu et al., *Agent Skills in the Wild* (Jan 2026): 31,132 skills analysed, 26.1% ≥1 vulnerability across 14 patterns, script-bundling 2.12× more likely vulnerable (p<0.001), SkillScan 86.7% precision / 82.5% recall; **dataset + detector released**. Fetched & verified 2026-10-18.
- https://arxiv.org/abs/2610.19264 — Pandey et al., *Beyond Maliciousness* (Oct 2026): 6,309 real listings, ~50% shell-exec, 70% ≥1 elevated capability, 59% of declaring listings under-declare — the under-declared-capability placement is the ordinary ecosystem. Fetched & verified 2026-10-18.
- https://arxiv.org/abs/2610.10612 — Liao et al., *PyCache Trap* (Oct 2026): bytecode-cache substitution defeats 7 scanners (94–100%); EAV defense detects all source-present substitutions, 92.8% recall @ 10.0% FPR on 200 benign skills; **code released** (github.com/leo0481/PyCacheTrap). The cache≠source placement + its fix. Fetched & verified 2026-10-18.
- https://arxiv.org/abs/2610.13227 — Liao et al., SkillRelay (Oct 2026): cross-session persistent-artifact attacks across Codex CLI / Gemini CLI / Claude Code, ASR 46.7–77.4%; SkillRelayGuard provenance defense. Fetched & verified 2026-10-18.
- https://arxiv.org/abs/2609.39607 — Kaiser & Dhar, *Pretext* (v2 Oct 2026): up to 97% evasion of a frozen detector, 77% co-adaptive — why the scanner layer is a sieve. Verified.
- https://arxiv.org/abs/2609.39352 — Wu et al., decoupled pretext/actuation across two skills. Verified (abstract; no headline number).
- https://arxiv.org/abs/2610.11169 — Seddik, *Skill Constellations* (Oct 2026): 2,193,119 `SKILL.md` adoptions mined from GitHub; model-ranked audit of top-100 repos prevents 14.9% of later high-risk adoptions vs 0.5% for most-starred. Verified.
- Industry incidents (vendor-reported): Koi Security *ClawHavoc* — 341 malicious skills on ClawHub (335 in one macOS-stealer campaign via fake prerequisites); Snyk *ToxicSkills* — 3,984 skills, 13.4% with a critical issue. Web-search summaries only (publisher domains unreachable from this environment) — labelled as vendor claims in the lesson.
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — Anthropic (2025-10-16): the `SKILL.md` format, progressive disclosure, and official "install only from trusted sources / audit before use" guidance. Fetched & verified 2026-10-18.

Earlier cluster evidence (TrustProbe, CoordPoison, APEX, Skill Constellations) recorded in the
history below.

## What would change the decision

n/a — ADDed. New replication of the EMERGING cache/cross-skill results (PyCache Trap, SkillRelay)
would upgrade those sections from EMERGING; a refutation would be recorded as an extension, not by
editing the lesson.

## History

- 2026-10-04 — WAIT — genuinely new attack surface, four independent groups, one measured defense with a stated utility cost; "skills" ship in mainstream agents, so likely to grow — but days old, no independent replication yet; ADD budget used on egress covert channels — weekly/2026-W40.md — candidates C-20261001-01, C-20261001-05
- 2026-10-11 — WAIT — two further independent groups — the first measured defense with an FPR (EAV) and the first ecosystem-scale propagation measurement — make this the strongest attack-surface WAIT; still all single fresh preprints with unconfirmed code; due 2026-11-08 and a leading ADD candidate then — weekly/2026-W41.md — candidates C-20261009-03, C-20261010-02
- 2026-10-18 — ADD — matured past the bar: multiple independent groups across attack (prose/cache/under-declaration/cross-skill) and defense (EAV, SkillRelayGuard) with released code and real marketplace base-rate measurement (6,309 and 31,132 and 98,380 skills), real industry incidents (ClawHavoc, ToxicSkills), 157 confirmed-malicious skills removed after responsible disclosure, and a mainstream standard (`SKILL.md`, 40+ platforms) with official security guidance. Framed as a supply-chain node (M22.2) extending the 22.1 gate, not a replacement. New lesson 22.2 + Lab 34 (9 tests; full suite 153 passed) — weekly/2026-W42.md — candidates C-20261012-01, C-20261014-01, C-20261015-04, C-20261015-08

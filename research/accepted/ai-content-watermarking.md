# AI-generated content watermarking and watermark removal

- **Topic ID:** ai-content-watermarking
- **Status:** ADD
- **Next review:** on new evidence
- **Course change:** `lessons/module-23/lesson-02.md` (new lesson 23.2, added 2026-11-15) + `lesson-02.quiz.yaml`; `labs/module-23/watermark/`; `assessments/module-23-quiz.quiz.yaml` (q10 appended) and `assessments/module-23-quiz.md` (review link); `_sidebar.md` (entry 28, later running numbers shifted by one); `curriculum/course-outline.md`; `references/standards-map.md`; `glossary.md`
- **Candidates:** C-20261010-03, C-20261011-01, C-20261024-03, C-20261026-08, C-20261031-02, C-20261107-02

## Summary

Same-week preprints: ProxyEraseAgent removes invisible image watermarks blind via proxy public decoders (94.8% ASR, 11 systems); SemField is a training-free semantic text watermark (88.2–90.4% TPR@1%FPR under paraphrase, beats 12 baselines, code released); MARC adds audio. The course has no watermarking coverage at all.

## Evidence

- https://arxiv.org/abs/2610.11290 — ProxyEraseAgent (no code)
- https://arxiv.org/abs/2610.11848 — SemField (code https://github.com/declare-lab/SemField; 'under review, WIP')
- https://arxiv.org/abs/2610.11488 — MARC (audio)
- https://arxiv.org/abs/2610.12106 — 'Could LLM Watermark Detection Be Public?' (design, no results)
- https://arxiv.org/abs/2610.30601 — HiMark hierarchical multi-bit text watermark (90.01% extraction under paraphrase, 32 bits / 300 tokens; no code). Added 2026-10-25.
- FOUNDATIONAL anchors verified this run: https://arxiv.org/abs/2301.10226 — Kirchenbauer et al., 'A Watermark for Large Language Models', ICML 2023; Dathathri et al., 'Scalable watermarking for identifying large language model outputs', Nature 634:818–823 (2024), DOI 10.1038/s41586-024-08025-4 — SynthID-Text, deployed in Gemini, open-source at https://github.com/google-deepmind/synthid-text. Added 2026-10-25.
- https://arxiv.org/abs/2610.32017 — SynMark: semantic-coordinate multi-bit code watermark, 82–84% bit accuracy under 100% identifier renaming (preprint, no code). Added 2026-11-01.
- https://arxiv.org/abs/2610.40613 — TextSeal2 (Sander, Fernandez et al.; code claimed at github.com/facebookresearch/textseal): distortion-free watermark that survives speculative decoding at matched acceptance rate; +8–22pp detection vs TextSeal at FPR 1e-3 (preprint). Added 2026-11-01.
- https://arxiv.org/abs/2611.08046 — KeHoSu (C-20261107-02): keyed homoglyph substitution for authenticated text provenance over copy-paste channels; formal capacity/removability analysis and an 18-platform survival test; no adversarial-removal evaluation, no code (preprint). Distinct from generation-time watermarking (post-hoc text marking); EMERGING only. Added 2026-11-08.

- Verified 2026-11-15 (weekly review): arXiv abstract pages 2301.10226 (ICML 2023), 2306.04634 (ICLR 2024; ~800 tokens at FPR 1e-5 after strong human paraphrase), 2402.19361 (watermark stealing, ICML 2024; spoof + scrub for < USD 50, > 80% average success), 2303.13408 (DIPPER paraphrase evasion; retrieval defense 80–97% at 1% FPR), 2307.15593 (distortion-free, TMLR); GitHub google-deepmind/synthid-text README (Apache-2.0; reference only, not production; non-cryptographic PRNG; 63-bit keys; Transformers v5 integration). EU AI Act Art. 50 application date (2026-08-02) and the June 2026 final Code of Practice on marking/labelling: secondary legal summaries only (EU and law-firm hosts not reachable from this session).
- This week's daily C-lines (EMERGING, not verified, recorded for the next update): Look It Up multi-bit codebook watermark (https://arxiv.org/abs/2611.16890, code), prevalence bounds for edited watermarked text (https://arxiv.org/abs/2611.17035, code), Logit Laundering data-use-audit evasion (https://arxiv.org/abs/2611.09446, CCS 2026 author-stated), RoCoMark code watermark (https://arxiv.org/abs/2611.11399).

## What would change the decision

A scope decision first: a lesson should be anchored on the FOUNDATIONAL, deployed literature (green-list text watermarking, Kirchenbauer et al. 2023; deployed systems such as SynthID; C2PA provenance), not on this week's preprints, and must fit the course's security-engineer framing (provenance as a defense, removal/forgery as attacks). Re-review with those anchors verified; this week's papers would then be the EMERGING section.

## History

- 2026-10-11 — WAIT — a genuine coverage gap, but this week's evidence is three fresh preprints; an ADD should be built on the verified foundational literature and needs a placement/scope decision (M20 extension vs frontier update) — weekly/2026-W41.md — candidates C-20261010-03, C-20261011-01
- 2026-10-18 — WAIT — four more preprints this week (WaveMark image robustness; TI-WM tokenizer-invariant text, with numbers; CamoMark watermark survival under Byzantine aggregation; PinIt key-free multi-bit message displacement, code released) deepen both attack and defense sides but do not change the scope decision; still to be built on verified foundational literature; next review 2026-10-25 as scheduled — weekly/2026-W42.md — candidates C-20261013-03, C-20261014-07, C-20261014-08, C-20261015-16
- 2026-10-25 — WAIT — due today; the scope blocker is now resolved (foundational anchors verified: Kirchenbauer ICML 2023 green-list scheme, SynthID-Text Nature 2024 deployed + open-source; HiMark adds one more EMERGING multi-bit data point), but the week's single ADD went to ATT&CK v20; proposed placement for the eventual ADD: frontier update (provenance as a defense; removal/forgery/paraphrase as attacks) with a from-scratch green-list lab; next review 2026-11-08 — weekly/2026-W43.md — candidates C-20261024-03
- 2026-11-01 — WAIT — evidence recorded ahead of the 2026-11-08 scheduled scope decision (not due this week) — weekly/2026-W44.md — candidates C-20261026-08, C-20261031-02
- 2026-11-08 — WAIT — due today with scope resolved and foundational anchors verified, and it remains a genuine coverage gap; KeHoSu adds one EMERGING post-hoc provenance data point; not added only because the single weekly ADD went to the due detector-evaluation topic, which is closer to the course core — strongest runner-up, next review next week as the protocol requires — weekly/2026-W45.md — candidates C-20261107-02
- 2026-11-15 — ADD — due today as last week's named runner-up; foundational and deployed literature verified (Kirchenbauer ICML 2023 + ICLR 2024, watermark stealing ICML 2024, SynthID-Text open-source reference) and a genuine coverage gap now backed by a legal marking duty (EU AI Act Art. 50); added as new lesson 23.2 with a stdlib lab (detect, remove, forge, retest) — weekly/2026-W46.md — candidates none new (due review)

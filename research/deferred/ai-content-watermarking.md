# AI-generated content watermarking and watermark removal

- **Topic ID:** ai-content-watermarking
- **Status:** WAIT
- **Next review:** 2026-11-08
- **Course change:** none
- **Candidates:** C-20261010-03, C-20261011-01, C-20261024-03

## Summary

Same-week preprints: ProxyEraseAgent removes invisible image watermarks blind via proxy public decoders (94.8% ASR, 11 systems); SemField is a training-free semantic text watermark (88.2–90.4% TPR@1%FPR under paraphrase, beats 12 baselines, code released); MARC adds audio. The course has no watermarking coverage at all.

## Evidence

- https://arxiv.org/abs/2610.11290 — ProxyEraseAgent (no code)
- https://arxiv.org/abs/2610.11848 — SemField (code https://github.com/declare-lab/SemField; 'under review, WIP')
- https://arxiv.org/abs/2610.11488 — MARC (audio)
- https://arxiv.org/abs/2610.12106 — 'Could LLM Watermark Detection Be Public?' (design, no results)
- https://arxiv.org/abs/2610.30601 — HiMark hierarchical multi-bit text watermark (90.01% extraction under paraphrase, 32 bits / 300 tokens; no code). Added 2026-10-25.
- FOUNDATIONAL anchors verified this run: https://arxiv.org/abs/2301.10226 — Kirchenbauer et al., 'A Watermark for Large Language Models', ICML 2023; Dathathri et al., 'Scalable watermarking for identifying large language model outputs', Nature 634:818–823 (2024), DOI 10.1038/s41586-024-08025-4 — SynthID-Text, deployed in Gemini, open-source at https://github.com/google-deepmind/synthid-text. Added 2026-10-25.

## What would change the decision

A scope decision first: a lesson should be anchored on the FOUNDATIONAL, deployed literature (green-list text watermarking, Kirchenbauer et al. 2023; deployed systems such as SynthID; C2PA provenance), not on this week's preprints, and must fit the course's security-engineer framing (provenance as a defense, removal/forgery as attacks). Re-review with those anchors verified; this week's papers would then be the EMERGING section.

## History

- 2026-10-11 — WAIT — a genuine coverage gap, but this week's evidence is three fresh preprints; an ADD should be built on the verified foundational literature and needs a placement/scope decision (M20 extension vs frontier update) — weekly/2026-W41.md — candidates C-20261010-03, C-20261011-01
- 2026-10-18 — WAIT — four more preprints this week (WaveMark image robustness; TI-WM tokenizer-invariant text, with numbers; CamoMark watermark survival under Byzantine aggregation; PinIt key-free multi-bit message displacement, code released) deepen both attack and defense sides but do not change the scope decision; still to be built on verified foundational literature; next review 2026-10-25 as scheduled — weekly/2026-W42.md — candidates C-20261013-03, C-20261014-07, C-20261014-08, C-20261015-16
- 2026-10-25 — WAIT — due today; the scope blocker is now resolved (foundational anchors verified: Kirchenbauer ICML 2023 green-list scheme, SynthID-Text Nature 2024 deployed + open-source; HiMark adds one more EMERGING multi-bit data point), but the week's single ADD went to ATT&CK v20; proposed placement for the eventual ADD: frontier update (provenance as a defense; removal/forgery/paraphrase as attacks) with a from-scratch green-list lab; next review 2026-11-08 — weekly/2026-W43.md — candidates C-20261024-03

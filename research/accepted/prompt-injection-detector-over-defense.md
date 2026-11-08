# Prompt-injection detector over-defense and distribution shift (PIDS-Bench)

- **Topic ID:** prompt-injection-detector-over-defense
- **Status:** ADD
- **Next review:** on new evidence
- **Course change:** `lessons/module-24/lesson-01.md` (advanced extension "evaluating prompt-injection detectors", added 2026-11-08); `labs/lab-37-injection-detector-eval/`; `_sidebar.md`; `curriculum/course-outline.md`; `references/standards-map.md`
- **Candidates:** C-20260926-02, C-20261005-04

## Summary

Evaluating prompt-injection detectors on attack recall *and* benign false positives at fixed
thresholds across in-distribution, hard-benign (external benign prompts with trigger words),
obfuscated and shifted data. PIDS-Bench reports a detector with F1 0.98 on its own split
misclassifies ~1/3 of an external benign subset ("provenance-sensitive over-defense"), and no
tested detector reaches F1≥0.95 with hard-benign FPR≤0.10.

## Evidence

- https://arxiv.org/abs/2609.15017 — fetched 2026-09-27: title/authors/abstract confirmed; no code or benchmark release link on the abs page. Daily record says IEEE Access vol. 14 (not independently verified this run).

- https://arxiv.org/abs/2610.03448 — independent single-author study: 15 detectors (incl. Prompt Guard 2) + 2 LLM judges replayed on AgentDojo/tau-bench tool outputs; best BIPIA detector catches 2% of AgentDojo injections at 1% FPR; detection rankings don't transfer, FPRs do; training-input form explains the gap. Added 2026-10-11.
- https://arxiv.org/abs/2609.15017 — re-fetched 2026-11-08: journal reference now listed on the abs page, IEEE Access vol. 14, pp. 134184–134205 (2026), DOI 10.1109/ACCESS.2026.3728186; hard-negative augmentation nearly removes curated over-defense but leaves external FPR far above 0.10; still no code/data link. Added 2026-11-08.
- https://arxiv.org/abs/2610.03448 — re-fetched 2026-11-08: code released at https://github.com/lzwhehe/benign-instruction-bench (MIT; scripts rebuild eval sets from public benchmarks; nothing was run or downloaded). Added 2026-11-08.
- https://arxiv.org/abs/2410.22770 — FOUNDATIONAL anchor: InjecGuard / NotInject (Li & Liu, 2024; code+data https://github.com/leolee99/InjecGuard): 339 trigger-word benign prompts; SOTA guard models near 60% accuracy (trigger-word bias). Added 2026-11-08.
- https://arxiv.org/abs/2501.15145 — CURRENT anchor: PromptShield (Jacob, Alzahrani, Hu, Alomair, Wagner; ACM CODASPY 2025): deployable detectors must be evaluated in the low-FPR regime. Added 2026-11-08.
- https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M — adoption: Meta's deployed detector reports Recall@1%FPR (97.5% for 86M, English) and lists distribution sensitivity and adaptive attacks as limitations (vendor claim). Added 2026-11-08.
- https://arxiv.org/abs/2611.04393 — Voluntary Servitude (NeurIPS 2026): deployed injection detectors score non-imperative fabricated-hazard payloads as benign (1.7–4.4x more effective than instruction injection behind a filter); used as the EMERGING limit-of-detection example. Added 2026-11-08.

## What would change the decision

Promoted to ADD on 2026-11-08. Reopen for a course change only if a released, widely used benchmark (e.g. a public PIDS-Bench release or a standard agent-format detector suite) would let Lab 37 be replaced or extended with real data, or if a detector class appears that is shown to hold its FPR across external benign sources.

## History

- 2026-09-27 — WAIT — important measurement result for a defense class the course lacks a lesson on, but a single 2-week-old paper with no released benchmark; ADD budget used — weekly/2026-W39.md — candidates C-20260926-02
- 2026-10-11 — WAIT — independent corroboration of the central claim by a different method (benchmark transfer, not hard-benign FPR) — the strongest WAIT this week and the leading ADD candidate for its due review on 2026-11-08 (a module-24 "evaluating injection detectors" extension); not added now because the weekly ADD budget went to 17.2 — weekly/2026-W41.md — candidates C-20261005-04
- 2026-11-08 — ADD — due today and the leading ADD candidate: four independent lines of work (InjecGuard 2024 with code, PromptShield CODASPY 2025, PIDS-Bench IEEE Access 2026, Liu 2026 with code) plus Prompt Guard 2's own Recall@1%FPR reporting establish a settled, teachable evaluation principle — a detector number belongs to a distribution and a threshold. Added as a 24.1 advanced extension with Lab 37 (16 tests; full suite 188 passed) — weekly/2026-W45.md — candidates none new (due review; cites C-20261104-02, recorded under fabricated-hazard-steering)

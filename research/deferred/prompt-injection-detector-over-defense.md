# Prompt-injection detector over-defense and distribution shift (PIDS-Bench)

- **Topic ID:** prompt-injection-detector-over-defense
- **Status:** WAIT
- **Next review:** 2026-11-08
- **Course change:** none
- **Candidates:** C-20260926-02

## Summary

Evaluating prompt-injection detectors on attack recall *and* benign false positives at fixed
thresholds across in-distribution, hard-benign (external benign prompts with trigger words),
obfuscated and shifted data. PIDS-Bench reports a detector with F1 0.98 on its own split
misclassifies ~1/3 of an external benign subset ("provenance-sensitive over-defense"), and no
tested detector reaches F1≥0.95 with hard-benign FPR≤0.10.

## Evidence

- https://arxiv.org/abs/2609.15017 — fetched 2026-09-27: title/authors/abstract confirmed; no code or benchmark release link on the abs page. Daily record says IEEE Access vol. 14 (not independently verified this run).

## What would change the decision

Public benchmark data/code, or an independent reproduction/citation that confirms the
external-benign FPR gap. The concept is teachable already (M23/M24 measure FPR), so with
released data this becomes a strong M24 extension or new lesson "evaluating injection detectors"
with a from-scratch detector + hard-benign set lab.

## History

- 2026-09-27 — WAIT — important measurement result for a defense class the course lacks a lesson on, but a single 2-week-old paper with no released benchmark; ADD budget used — weekly/2026-W39.md — candidates C-20260926-02

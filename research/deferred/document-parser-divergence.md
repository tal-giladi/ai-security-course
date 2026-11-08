# File-ingestion divergence: what the model reads vs what the human sees in Office documents

- **Topic ID:** document-parser-divergence
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261105-01

## Summary

OOXML content invisible to a human renderer but extracted by LLM file-ingestion pipelines (19 + 12 extractor channels, 8 real targets), with a working defense (Prism). Mechanically simple to reproduce from scratch.

## Evidence

- C-20261105-01 — single-author preprint, no code, no venue.

## What would change the decision

Replication or vendor acknowledgement; then a 05.1/20.1 lab extension (it generalises the hidden-text indirect injection already taught).

## History

- 2026-11-08 — WAIT — one author, no code; partly covered by existing hidden-content injection material — weekly/2026-W45.md — candidates C-20261105-01

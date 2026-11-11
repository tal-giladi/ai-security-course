# Text-vector integrity gap in offline RAG (signed text, unsigned vectors)

- **Topic ID:** rag-text-vector-integrity
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261106-04

## Summary

In offline/edge RAG, signing documents does not bind the stored embedding vectors; an attacker who edits vectors steers retrieval while signatures still verify. Careful methodology with pre-registered negative results and an edge-hardware demonstration; a closing mechanism is proposed.

## Evidence

- C-20261106-04 — Signed but Steerable, preprint; code/data reported released (repository not yet located by the daily run).

## What would change the decision

A located, working code release or replication; then a 14.1/22.1 lab extension (integrity must cover derived artifacts).

## History

- 2026-11-08 — WAIT — careful single preprint; repository not located — weekly/2026-W45.md — candidates C-20261106-04

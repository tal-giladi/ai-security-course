# MCP tool poisoning measured across frameworks with real execution

- **Topic ID:** mcp-tool-poisoning-prevalence
- **Status:** WAIT
- **Next review:** 2026-12-13
- **Course change:** none
- **Candidates:** C-20261104-01

## Summary

A cross-framework census: 12 agentic frameworks x 18 models x 45 scenarios (9,720 cells), dual oracle with canary HTTP receipt. Overall ASR 22.9%; framework choice barely matters (nine frameworks within 23–26%, p = 0.91); no framework has an intentional defense; a regex description scanner rejects 20/45 scenarios at 7.2% FPR; five disclosures to four vendors were all rejected.

## Evidence

- https://arxiv.org/abs/2611.03555 — accepted at AISec '26 (CCS 2026 workshop). The harness `mcpvenom` is named but no repository was found by a web search on 2026-11-08.

## What would change the decision

A located code release (mcpvenom) or independent replication; then a short "measured at scale" data update to 17.1/19.1, not a new lesson — the mechanism is already taught.

## History

- 2026-11-08 — WAIT — peer-reviewed and large, but the mechanism is already taught (17.1, 19.1) and the harness is not findable; the delta is data, which waits for a release — weekly/2026-W45.md — candidates C-20261104-01

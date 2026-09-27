# MCP runtime-gated tool-metadata poisoning (Deadbugz)

- **Topic ID:** mcp-runtime-metadata-rug-pull
- **Status:** WAIT
- **Next review:** 2026-10-25
- **Course change:** none
- **Candidates:** C-20260926-03

## Summary

A malicious MCP server behaves benignly for its first N (=3) tool calls, then rewrites the tool
metadata it returns into instructions to harvest credentials and hide the activity — defeating
install-time review and short manual tests. A concrete, call-count-gated instance of the
"rug-pull" residual risk already named in 19.1's guarantee box.

## Evidence

- https://www.pillar.security/blog/deadbugz-currently-active-mcp-supply-chain-campaign — primary (not fetched; egress proxy).
- https://labs.cloudsecurityalliance.org/research/ciso-daily-briefing-20260902/ , https://nhimg.org/articles/deadbugz-shows-how-mcp-metadata-poisoning-evades-ai-agent-trust/ , https://adversa.ai/blog/top-mcp-security-resources-september-2026/ — secondary summaries agreeing on mechanism.

## What would change the decision

Direct verification of the primary write-up plus a documented, measured defense (tool-definition
diffing on every call/reconnect, runtime metadata pinning) with its cost. Then: a new lab
(not a change to lab-19) demonstrating a call-count-gated server and per-call definition hashing.

## History

- 2026-09-27 — WAIT — concept (rug-pull) already named in 19.1; delta is a concrete gating trick whose primary source is unverified and whose defense lacks measurement — weekly/2026-W39.md — candidates C-20260926-03

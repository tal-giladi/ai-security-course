# MCP runtime-gated tool-metadata poisoning (Deadbugz)

- **Topic ID:** mcp-runtime-metadata-rug-pull
- **Status:** WAIT
- **Next review:** 2026-11-22
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
- Primary source now read directly: https://www.pillar.security/blog/deadbugz-currently-active-mcp-supply-chain-campaign (2026-08-12; vendor report) — server counts tools/call per client, after the 3rd call tools/list and prompts/get carry credential-harvesting instructions; advertises tools.listChanged; delivered via GitHub PRs editing MCP configs. Recommended defenses (no measured cost): fingerprint tool definitions at approval, treat any definition change as requiring re-approval, policy on sensitive actions independent of tool metadata. Added 2026-10-25.

## What would change the decision

Direct verification of the primary write-up plus a documented, measured defense (tool-definition
diffing on every call/reconnect, runtime metadata pinning) with its cost. Then: a new lab
(not a change to lab-19) demonstrating a call-count-gated server and per-call definition hashing.

## History

- 2026-09-27 — WAIT — concept (rug-pull) already named in 19.1; delta is a concrete gating trick whose primary source is unverified and whose defense lacks measurement — weekly/2026-W39.md — candidates C-20260926-03
- 2026-10-25 — WAIT — due today; primary write-up now verified (vendor report), confirming the call-count-gated rug-pull and the defense (definition fingerprinting + re-approval on change), but still one campaign with no measured defense cost; small 19.1 extension candidate (new lab, per-call definition hashing) — next review 2026-11-22 — weekly/2026-W43.md — candidates C-20260926-03 (primary source re-read; no new candidate)

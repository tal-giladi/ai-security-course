# MCP filesystem capability laundering (declared category understates access)

- **Topic ID:** mcp-filesystem-capability-laundering
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261016-02

## Summary

An MCP server's registry category under-declares the filesystem access its approval actually grants,
so an approval system screening by declared category misses it. MCP-FSD scanned 21,097 servers across
nine registries; of 4,806 triaged, 787 (16.4%) had filesystem capability despite non-filesystem
categories; dynamic testing confirmed 150 exploitable instances. Coordinated disclosure produced 13
advisories including two CVEs against Anthropic's own Git MCP Server. Extends M18/M19 (MCP trust
boundaries) and is adjacent to the newly-ADDed M22.2 under-declared-capability placement, but at the
MCP-server (not skill) layer.

## Evidence

- https://arxiv.org/abs/2610.22301 — Huang et al.; 21k-server scan, 150 confirmed exploitable, two CVEs via coordinated disclosure (independent adjudication). Single preprint; MCP-FSD code not confirmed public from the abstract.

## What would change the decision

Confirmed CVE IDs/advisories cross-checked against NVD; a released scanner; a CPU-feasible M19 lab
(derive a tool's claimed filesystem boundary from metadata, probe the lab's mock MCP servers for
enforcement). Strong future M19 extension given the real CVEs.

## History

- 2026-10-18 — WAIT — real independently-adjudicated CVEs and a very large scan make this unusually strong for a 1-day-old preprint, but it overlaps the ADDed M22.2 capability theme and the ADD budget is used; revisit as an M19-specific extension with verified CVE references — weekly/2026-W42.md — candidates C-20261016-02

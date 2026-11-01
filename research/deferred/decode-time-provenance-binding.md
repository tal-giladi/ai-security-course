# Decode-time provenance binding vs steganographic injection in MCP pipelines

- **Topic ID:** decode-time-provenance-binding
- **Status:** WAIT
- **Next review:** 2026-12-13
- **Course change:** none
- **Candidates:** C-20261026-01

## Summary

Instructions hidden in an image (LSB/DCT/metadata steganography) evade text-only injection scanners and only become text after an MCP tool decodes them. The proposed fix binds HMAC-authenticated trust labels at the moment of decoding, keeps a provenance ledger and taint-tracks to sinks: 100% of 24 adaptive payloads blocked versus 62.5% leaking past regex defenses, with an audited promotion path restoring utility from 67% to 100%.

## Evidence

- https://arxiv.org/abs/2610.31974 — Yocam et al.; code stated at github.com/ericyoc/stego_provenance_defense (CC BY 4.0, not inspected); own testbed, 4-component ablation (preprint).

## What would change the decision

A second group reproducing decode-time binding or a deployed MCP gateway adopting it. Natural home: a 17.2 / 19.1 extension. Note the overlap with this week's trust-zoned-memory ADD (both use 'authority only via an audited promotion').

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261026-01

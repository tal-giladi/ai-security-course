# Keyless steganographic collusion between independently deployed agents (Codetta)

- **Topic ID:** multi-agent-covert-collusion
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20260929-04

## Summary

Codetta lets two independently hosted agents with no pre-shared secret negotiate a key over a
monitored channel, then exchange high-capacity payloads whose transcript is computationally
indistinguishable from normal output (up to 94x prior capacity; key-exchange failure ≤4.1e-3 over
~80k tokens). Weakens the assumption that unrelated agents can't build a covert channel under an
auditor. Attack-capability only (no defense). Relevant to M18/M28 multi-agent monitoring.

## Evidence

- https://arxiv.org/abs/2609.28900 ; https://eprint.iacr.org/2026/2218 — single group, formal construction, cross-posted to IACR; no replication, no defense.

## What would change the decision

Independent replication or a proposed/measured detection. Teachable only as a much simpler,
illustrative from-scratch stego channel to motivate "reading agent-to-agent transcripts is
insufficient."

## History

- 2026-10-04 — WAIT — technically strong but offensive-only, single group, no detection counterpart — weekly/2026-W40.md — candidates C-20260929-04

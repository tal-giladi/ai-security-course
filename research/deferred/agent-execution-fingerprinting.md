# Fingerprinting the model behind a black-box agent from execution traces

- **Topic ID:** agent-execution-fingerprinting
- **Status:** WAIT
- **Next review:** 2026-12-27
- **Course change:** none
- **Candidates:** C-20261026-05, C-20261111-03

## Summary

AgentTrace sends probes that cause tokenization-sensitive serialization failures at tool interfaces, then models the agent's repair trajectory as a Markov chain. It reports 96.0% attribution under identity spoofing and separates variants that share a tokenizer.

## Evidence

- https://arxiv.org/abs/2610.32092 — Zhao, Wu, Zhang (preprint, no code).
- https://arxiv.org/abs/2611.12386 — Shibboleth traps (Pasquini et al., v0.1): honeypot services gated on informative interaction; 15 models 90% top-1, 4 harnesses 92%; behavioural evidence survives concealment instructions (preprint, no code). Added 2026-11-15.

## What would change the decision

Code plus independent replication. The technique is dual use (it profiles a defender's stack), so it fits 27.1 recon or 22.x provenance.

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261026-05
- 2026-11-15 — WAIT — an independent second method (defender-side honeypots fingerprint attacker models at 90% top-1 and harnesses at 92%, behaviour surviving identity concealment) meets half of the stated condition; 'v0.1' preprint, no code; review date unchanged — weekly/2026-W46.md — candidates C-20261111-03

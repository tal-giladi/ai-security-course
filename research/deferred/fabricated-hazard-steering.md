# Fabricated-hazard steering ("voluntary servitude"): injection without a command

- **Topic ID:** fabricated-hazard-steering
- **Status:** WAIT
- **Next review:** 2026-12-20
- **Course change:** none
- **Candidates:** C-20261104-02

## Summary

An attacker plants a fabricated hazard written as an ordinary review; the agent's own harm-avoidance reasoning disqualifies the legitimate option and picks the attacker's. No command syntax, so injection detectors score it benign. 60.4% steering vs 66.0% for instruction injection; 1.7–4.4x more effective behind a detector; transfers to production browser agents; a corroboration requirement in the agent instructions removes ~95% of exposure against a non-adaptive attacker.

## Evidence

- https://arxiv.org/abs/2611.04393 — Zendel, Levy, Cohen, Mendelson, LeVi; "Accepted at NeurIPS 2026 (Main Track)" confirmed on the abs page 2026-11-08; submitted 2026-11-03; no code.

## What would change the decision

Released code or an independent reproduction, and an adaptive evaluation of the corroboration defense. Already cited (as EMERGING) in the 24.1 detector-evaluation extension; a full lesson would be an M05/M17 extension relating it to RAG stance poisoning and AI search-result poisoning.

## History

- 2026-11-08 — WAIT — peer-reviewed (NeurIPS main track) and mechanism-distinct, but five days old, single group, no code, and the defense is untested against adaptive attackers; cited as EMERGING in the 24.1 extension — weekly/2026-W45.md — candidates C-20261104-02

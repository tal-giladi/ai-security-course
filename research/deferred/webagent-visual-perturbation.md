# End-to-end visual perturbation attacks on web agents (WebMirage)

- **Topic ID:** webagent-visual-perturbation
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261008-05

## Summary

Localized adversarial-image perturbations hijack web agents from grounding through browser execution: 91.9% ASR vs 17.4% best baseline across 4 configs, 6 VLMs, 2,250 tasks; defeats three (unnamed) agent-level defenses; code released.

## Evidence

- https://arxiv.org/abs/2610.09240 — code https://github.com/MoonTea0416/WebMirage

## What would change the decision

Identity of the defeated defenses (especially CaMeL/Secure-CUA-style ones, now taught in 17.2), independent reproduction. Fits as a 20.1 or 18.1 extension.

## History

- 2026-10-11 — WAIT — large, code-released result, but single preprint and the visual-adversarial prerequisite (M09/M20) already covers the mechanism class; wait for the defense identities — weekly/2026-W41.md — candidates C-20261008-05

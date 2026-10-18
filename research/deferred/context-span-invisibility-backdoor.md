# Context-span invisibility as a distillable backdoor (code-review evasion)

- **Topic ID:** context-span-invisibility-backdoor
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261015-01

## Summary

A formally-specified "selective blindness" primitive makes a marked span of context disappear from a
model's behaviour (omitted from summaries/QA/filtering) while leaving every outside activation
provably unchanged (noninterference, verified 0.5B–120B). Distilled into weights it is a backdoor; a
demonstrated application suppresses planted vulnerabilities during AI code review. Detection is
white-box (linear probes 0.57–0.79 vs 0.025 chance), but hardening trades probe visibility against
attention-routing visibility. Structurally different from output-triggering backdoors (Sleeper
Agents); directly relevant to the supply-chain/code-review material.

## Evidence

- https://arxiv.org/abs/2610.15883 — sole author listed as Mark Russinovich (identity/affiliation not independently re-verified against this paper); formal property + very broad empirical validation; no code confirmed; single paper.

## What would change the decision

Author identity/affiliation confirmation; a code release; a CPU-feasible toy (span-veto
noninterference check + distilled backdoor + probe-detection tradeoff) for an M11/M22 extension.

## History

- 2026-10-18 — WAIT — rigorous and broadly validated dual-use primitive with a code-review-evasion application fitting M22, but single paper, author identity unverified, no code; ADD budget used on skill-trust-boundary — weekly/2026-W42.md — candidates C-20261015-01

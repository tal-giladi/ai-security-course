# Program Decision Hijacking of typed-decision judges (Jev)

- **Topic ID:** typed-decision-judge-hijacking
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261015-03

## Summary

Three independent groups in one week probed a real, newly-launched commercial typed-decision judge
(TypeSafe AI's Jev / "System One") at scale. JPDH: attacker-controlled contexts redirect downstream
program decisions through schema-valid judgments (228 real apps / 2,273 cases, 81.5% decision flips,
98.6% with downstream impact; responsibly disclosed; JevProbeBench stated public). Companions show a
"robust on checkable rules, weak on holistic judgment" split and context-poisoning against live
Jev-1.13.0. The exploit is the gap between "answered the typed question correctly" and "the app's use
of that answer is safe."

## Evidence

- https://arxiv.org/abs/2610.18612 — Luo et al. (JPDH); 228 real apps, responsible disclosure, code stated public.
- https://arxiv.org/abs/2610.17820 — Li et al.; controlled adversarial comparison vs 5 GPT/GLM judges + 2 local classifiers.
- https://arxiv.org/abs/2610.15537 — Wu et al.; context poisoning, code https://github.com/WuXixiong/jev-poisoning-bench.

## What would change the decision

Maintainer responses to the disclosure; confirmed JevProbeBench release; durability of the product
(weeks old). A strong future guardrail/judge-robustness case study if it stabilises.

## History

- 2026-10-18 — WAIT — rare multi-group convergence on a real deployed product with a disclosure trail, but the product is weeks old, replication is convergent-not-independent, and the ADD budget is used; revisit for a judge-robustness case study — weekly/2026-W42.md — candidates C-20261015-03

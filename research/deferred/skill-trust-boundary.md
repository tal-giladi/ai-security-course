# Agent "Skills" as a trust boundary (cross-skill poisoning, approval binding)

- **Topic ID:** skill-trust-boundary
- **Status:** WAIT
- **Next review:** 2026-11-08
- **Course change:** none
- **Candidates:** C-20261001-01, C-20261001-05, C-20261009-03, C-20261010-02

## Summary

Installable agent "Skills" (multi-file instruction/script packages) are a new trust boundary distinct
from tool-description poisoning (M17). Four independent groups in one window: TrustProbe (104 vulns
in 11 real skill-agents), CoordPoison (split a malicious op across two skills to defeat per-skill
audit; code released), Pretext (relocate payload to evade static+semantic scanners, up to 97%/77%),
APEX (false-approval-record handoff; 74.2% on SkillsBench; first measured defense: a prompting check
drops success 84.3%→59.1% but benign pass 86.7%→56.3%). Related: "Approval Laundering" (six ways a
coding-agent harness lets executed action diverge from approved action; Approval Token closes 2 of 6
classes, p=1 on the other two — a clean honest-negative guarantee example, tested on Claude Code).

## Evidence

- https://arxiv.org/abs/2609.39065 ; https://arxiv.org/abs/2609.39352 ; https://arxiv.org/abs/2609.39607 ; https://arxiv.org/abs/2610.01564 — skills cluster.
- https://arxiv.org/abs/2609.38983 — Approval Laundering (single author, rigorous stats).

- https://arxiv.org/abs/2610.10612 — PyCache Trap: bytecode-cache substitution defeats 7 skill scanners (94–100%); EAV defense: 100% of source-present substitutions, 92.8% recall at 10.0% FPR on 200 benign skills. Added 2026-10-11.
- https://arxiv.org/abs/2610.11169 — Skill Constellations: 2,193,119 SKILL.md adoptions mined from GitHub; stars don't identify sources; fixes rarely propagate; model-ranked audit of top 100 repos prevents 14.9% of later high-risk adoptions vs 0.5% for most-starred. Single author. Added 2026-10-11.

## What would change the decision

Independent replication of the APEX defense/cost result; confirmation of released code; a peer-
reviewed Approval-Laundering version. Strong future ADD: a new M17/M19 "skills as a trust boundary"
lesson pairing the cross-skill attack with the measured prompting-defense cost.

## History

- 2026-10-04 — WAIT — genuinely new attack surface, four independent groups, one measured defense with a stated utility cost; "skills" ship in mainstream agents, so likely to grow — but days old, no independent replication yet; ADD budget used on egress covert channels — weekly/2026-W40.md — candidates C-20261001-01, C-20261001-05
- 2026-10-11 — WAIT — two further independent groups — the first measured defense with an FPR (EAV) and the first ecosystem-scale propagation measurement — make this the strongest attack-surface WAIT; still all single fresh preprints with unconfirmed code; due 2026-11-08 and a leading ADD candidate then — weekly/2026-W41.md — candidates C-20261009-03, C-20261010-02

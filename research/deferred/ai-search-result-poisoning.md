# Data-void poisoning of web-searching LLMs (ATT&CK T1608.007)

- **Topic ID:** ai-search-result-poisoning
- **Status:** WAIT
- **Next review:** 2026-12-06
- **Course change:** none
- **Candidates:** C-20261023-01, C-20261121-03

## Summary

A single attacker page in a search data void can be folded into an LLM's synthesized answer (31% of conditions across ChatGPT, Gemini, Perplexity Sonar Pro). ATT&CK v20 names the behavior T1608.007 AI Result Poisoning. Cited as EMERGING research in F.2; a dedicated M14 extension waits.

## Evidence

- https://arxiv.org/abs/2610.30365 — NDSS 2027 (extended version), verified 2026-10-25; no code found.
- https://attack.mitre.org/techniques/T1608/007/ — ATT&CK names the behavior; no target-side analytic.
- https://arxiv.org/abs/2611.26564 — GEOHunter (C-20261121-03): a paid GEO network measured in the wild supplies 4.5–20% of retrievable cited pages across nine AI answer engines; single preprint; no defense. Added 2026-11-22.

## What would change the decision

Independent replication or a measured answer-side defense (source diversity, citation provenance) to pair with it; then an M14 extension with a safe offline lab (toy corpus, data-void query, synthesizer).

## History

- 2026-10-25 — WAIT — peer-reviewed and now standard-named (cited in F.2), but attack-only from one group; a lesson needs a measured defense — weekly/2026-W43.md — candidates C-20261023-01
- 2026-11-22 — WAIT — first in-the-wild measurement of an operating attacker (second group), still no measured answer-side defense; date unchanged — next review 2026-12-06 — weekly/2026-W47.md — candidates C-20261121-03

# MITRE ATT&CK v20 AI techniques (T1698/T1699/T1700/T1608.007) and AI-enabled exfiltration detection

- **Topic ID:** mitre-attack-v20-ai-techniques
- **Status:** ADD
- **Next review:** on new evidence
- **Course change:** lessons/frontier/update-02.md (F.2); labs/lab-35-attack-ai-detection/; references/standards-map.md (appended row + ATT&CK v20 section); curriculum/course-outline.md (appended line + dependency row); _sidebar.md
- **Candidates:** C-20261019-01

## Summary

ATT&CK v20 (2026-10-13) added Enterprise techniques naming AI behavior: T1699 Direct and T1698 Indirect Prompt Injection (Execution; no detection strategy listed), T1700 AI-Enabled Exfiltration (Exfiltration; detection strategy DET0927: out-of-scope data access -> transfer-capable tool call -> outbound to unauthorized destination) and T1608.007 Stage Capabilities: AI Result Poisoning (Resource Development; DET0922, explicitly no target-side analytic). Course change: frontier lesson F.2 with crosswalk to ATLAS/OWASP 2026 and Lab 35, which implements a DET0927-style analytic, breaks it with three cheap adaptations and hardens it with runtime provenance at a measured FP cost.

## Evidence

- https://attack.mitre.org/resources/updates/ — v20 changelog, release 2026-10-13, IDs and names (fetched 2026-10-19 and 2026-10-25).
- https://attack.mitre.org/techniques/T1698/ , https://attack.mitre.org/techniques/T1699/ — descriptions, Execution tactic, mitigations M1038/M1030/M1026/M1022/M1018/M1017, no detection strategy (fetched 2026-10-25).
- https://attack.mitre.org/techniques/T1700/ — description, Exfiltration tactic, DET0927 with analytics AN2078-AN2080 (fetched 2026-10-25).
- https://attack.mitre.org/techniques/T1608/007/ — description, Resource Development, M1056, DET0922 with no target-side analytic (fetched 2026-10-25).
- https://gbhackers.com/mitre-attack-v20-ai-techniques/amp/ , https://letsdatascience.com/news/mitre-adds-ai-attack-techniques-to-attck-35cf4042 — independent press coverage of the release (search summaries).
- https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf — Strom et al., ATT&CK Design and Philosophy (verified title/authors, 2018 rev. 2020) — lesson's research paper.
- https://arxiv.org/abs/2610.30365 — Guerra et al., Data-Void Exploits in Web-Searching LLMs (NDSS 2027) — cited as EMERGING research for T1608.007.

## What would change the decision

n/a — ADDed. Revisit when ATT&CK adds detection strategies for T1698/T1699 or revises DET0927 (extend F.2, do not replace).

## History

- 2026-10-25 — ADD — ATT&CK, the SOC-native taxonomy, now names prompt injection and AI-enabled exfiltration with a published detection strategy; frontier lesson F.2 + crosswalk section in references/standards-map.md + Lab 35 (9 tests; full suite 162 passed) — weekly/2026-W43.md — candidates C-20261019-01

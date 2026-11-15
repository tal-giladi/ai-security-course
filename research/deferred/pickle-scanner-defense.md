# Context-aware Pickle VM-state scanning (DITTO / PickleBench)

- **Topic ID:** pickle-scanner-defense
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261009-02, C-20261109-01

## Summary

DITTO tracks Pickle VM state opcode-by-opcode with semantic analysis: 0% FNR / 0.7% FPR, F1 0.966 on PickleBench (959 benign + 92 malicious real models); 9.3% of 10,000+ popular HF repos rely on Pickle.

## Evidence

- https://arxiv.org/abs/2610.10735 — single preprint; code/benchmark release unconfirmed.
- https://arxiv.org/abs/2611.08745 — ModelShield (Ali, Case; ACSAC 2026 author-stated): runtime behavioural detection (framework hooks + eBPF syscall attribution, 195 ATT&CK-mapped patterns), 17 frameworks / 36 formats, zero FPs on an independent set, all 29 published evasion variants detected; 41 malicious HF models among 145,000 scanned, of which ModelScan/PickleScan/Fickling/ModelAudit caught 29/56/80/93%; median 12.3 s per model; no code. Added 2026-11-15.

## What would change the decision

Release of PickleBench and the scanner; comparison against the scanners already named in 13.1/22.1 by a second group. Would be a 13.1 extension (opcode-tracking scanner vs pattern match) — lab-13 already shows pickle RCE and safetensors.

## History

- 2026-10-11 — WAIT — measured defense with FP cost for an attack the course teaches, but no released artifact yet and the course's current defense (safetensors / no-pickle) remains the primary control — weekly/2026-W41.md — candidates C-20261009-02
- 2026-11-15 — WAIT — the stated reopen condition is now largely met: a second, different group (ModelShield, ACSAC 2026 per arXiv comments; abstract verified 2026-11-15) compares against ModelScan/PickleScan/Fickling/ModelAudit with measured FP and latency and an in-the-wild prevalence measurement; not added only because of the one-ADD budget and because neither DITTO nor ModelShield has released code; leading candidate for the 2026-11-22 review as a 13.1 'static vs behavioural model scanning' extension — weekly/2026-W46.md — candidates C-20261109-01

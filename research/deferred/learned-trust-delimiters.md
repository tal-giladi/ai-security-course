# Learnable trust-boundary delimiters for prompt injection (LTBD)

- **Topic ID:** learned-trust-delimiters
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261009-05, C-20261028-02, C-20261031-01

## Summary

Learned delimiter embeddings mark untrusted spans without fine-tuning the base model; reports 0.00% ASR on AlpacaFarm and 0.11–0.19% on TaskTracker, robust to adaptive attacks.

## Evidence

- https://arxiv.org/abs/2610.11634 — 5-page preprint; no code.
- https://arxiv.org/abs/2610.37657 — Heads of Security: learned per-attention-head trust gates; RL-Hammer ASR 10% vs 97% (GPT-OSS-20B) / 85% (SecAlign); adaptive white-box attack needs ~3× compute; ASIDE collapses to ~10% tool-use utility, HoS does not (preprint, no code). Added 2026-11-01.
- https://arxiv.org/abs/2610.40396 — Role spoofing (Edelman, Edelman, Goel, Malach): models infer role from content and structure; adversarial training against content spoofing leaves structure spoofing fully effective (toy setting); linear-probe role detector proposed (preprint, no code). Explains why delimiter/role-marker defenses must be robust to forged structure. Added 2026-11-01.

## What would change the decision

Code and an independent adaptive evaluation (the claims are strong for the paper's length). Would be a 04.1/05.1 extension next to spotlighting/instruction hierarchy.

## History

- 2026-10-11 — WAIT — strong claims from a very short paper, no code, no replication — weekly/2026-W41.md — candidates C-20261009-05
- 2026-11-01 — WAIT — architectural trust separation now has a stronger adaptive-attack result (HoS) and a mechanistic explanation of its failure mode (role spoofing); neither has code; keep scheduled review — weekly/2026-W44.md — candidates C-20261028-02, C-20261031-01

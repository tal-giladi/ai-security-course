# Backdoors that survive post-training or evade input-centric defenses (PersistBD, SkillPoison, answer-side triggers)

- **Topic ID:** backdoor-persistence-and-trigger-variants
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261007-02, C-20261007-03, C-20261008-06, C-20261021-06

## Summary

A same-week cluster of three structurally different backdoor mechanisms: PersistBD hardens a supply-chain backdoor to survive a developer's benign SFT+RL (20%→74–76% ASR, code released); SkillPoison poisons skill extraction with only verified-correct experiences (95.71% ASR, code released); answer-side backdoors make the model's own first-turn reply the trigger (near-100% ASR at 5% poisoning, no code).

## Evidence

- https://arxiv.org/abs/2610.07510 — PersistBD (code: https://github.com/uiuc-kang-lab/PersistBD)
- https://arxiv.org/abs/2610.07645 — SkillPoison (code: https://github.com/DEEP-JLU/SkillPoison)
- https://arxiv.org/abs/2610.07723 — answer-side backdoors (no code)
- https://arxiv.org/abs/2610.27533 — BenchDoor: poisoned datasets that genuinely raise benchmark scores (incentive to adopt) and implant backdoors; 82.33–100% ASR at 2–10% poisoning; >=90.33% after decontamination; no code. Added 2026-10-25.

## What would change the decision

Independent reproduction of any one mechanism, or a measured defense. The most teachable single item is PersistBD (an extension to 11.1 / lab-11 showing survival through post-training).

## History

- 2026-10-11 — WAIT — three days-old single preprints, no defenses, no replication; strong conceptual value for 11.1 later — weekly/2026-W41.md — candidates C-20261007-02, C-20261007-03, C-20261008-06
- 2026-10-25 — WAIT — adds an incentive-driven adoption mechanism that survives decontamination; single preprint without code; keep 2026-11-22 — weekly/2026-W43.md — candidates C-20261021-06

# Trust-zoned memory for computer-use agents (persistent-memory attack)

- **Topic ID:** trust-zoned-agent-memory
- **Status:** WAIT
- **Next review:** 2026-11-01
- **Course change:** none
- **Candidates:** C-20261002-01

## Summary

ZoneClaw names a "persistent memory attack" on computer-use agents: benign-looking content induces
the agent to write attacker claims into auto-reloaded workspace memory that silently governs later,
unrelated tasks. Fix: separate persistence from action-authority — external claims live in a
low-trust zone and only gain authority by crossing an explicit boundary, with role-specific
asymmetric privilege. ASR 77.5% → 1.25%, utility 95.4% across 4×2×4; remains effective vs some
defense-aware attackers; code released. Directly extends lesson 16.2 (agent memory poisoning).

## Evidence

- https://arxiv.org/abs/2610.00450 ; code https://github.com/euph00/ZoneClaw-code — one group, large structured eval, attack+defense-aware numbers, released code.

## What would change the decision

Independent replication or adoption. Strong candidate for a 16.2 lab extension (flat vs zoned memory
on the same injected-claim scenario); next review deliberately near-term given code is available.

## History

- 2026-10-04 — WAIT — unusually complete single paper (attack, defense, cost, code) and a clean fit to 16.2, but one group and days old; ADD budget used on a due deferred item — weekly/2026-W40.md — candidates C-20261002-01

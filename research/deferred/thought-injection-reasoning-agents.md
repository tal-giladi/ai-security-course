# Thought injection: indirect injections styled as the model's own reasoning trace

- **Topic ID:** thought-injection-reasoning-agents
- **Status:** WAIT
- **Next review:** 2027-01-10
- **Course change:** none
- **Candidates:** C-20261109-02

## Summary

Untrusted text that imitates a large reasoning model's own chain-of-thought (with or without
thinking tags) is fed back to the model through tool output. In a containerized agentic cyber range,
reasoning-styled injections reached up to 50% ASR on operational objectives where the same objective
in ordinary user voice never succeeded; thinking tags suppressed the agent's tendency to disclose the
injection, and tag stripping proved an unreliable defense. A carrier distinct from the user/system
voices that 05.1's marker discussion addresses; related to the reasoning-prefill class taught in 34.1.

## Evidence

- https://arxiv.org/abs/2611.08811 — single preprint (Illendula et al.), GLM-5.3, MiniMax-M2.5, Qwen3.8-Flash-Next; "up to 50%" is a best case and effects are model-specific; no code.

## What would change the decision

Independent replication on other reasoning models, or a defense with measured cost (e.g. provenance
marking that survives tag stripping). Would be a 05.1 exercise variant or a note beside 34.1's
prefill class, with a local small-model reasoning-styled vs user-voice payload comparison using
inert markers.

## History

- 2026-11-15 — WAIT — mechanism-distinct and falsifiable, but one preprint with model-specific best-case numbers and no code or defense cost — weekly/2026-W46.md — candidates C-20261109-02

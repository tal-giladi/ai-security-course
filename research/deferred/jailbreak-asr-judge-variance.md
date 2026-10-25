# Jailbreak-ASR judge variance (how to read an ASR number)

- **Topic ID:** jailbreak-asr-judge-variance
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20261015-15, C-20261019-03

## Summary

Swapping only the judge LLM used to score "did this response fulfil the prohibited request" can move
reported ASR by up to 82 percentage points on the same attack/response set. A training-free "semantic
reconstruction game" evaluator (reconstruct the request the response actually answers, compare to
decoys, allow abstention) reduces mean error against human labels and cross-judge variance. A
methodology point directly relevant to every jailbreak ASR number the course cites.

## Evidence

- https://arxiv.org/abs/2610.19306 — Davis, Emil-Popescu, Jana (Columbia, unverified against this paper); large quantified effect; single preprint, no code, 82pp is a max not a typical case.
- https://arxiv.org/abs/2610.23254 — 'Ignored, Not Refused': 33,000 trajectories on InjecAgent/AgentDojo; 76–80% of failed attacks silently ignored vs 17–18% refused; system prompt alone moves InjecAgent ASR 0.2%→43%; 21.7% of AgentDojo episodes resist the attack but fail the task; corpus/judge/code stated as released. Added 2026-10-25.

## What would change the decision

Released code; independent confirmation of the variance figure. Low-cost, high-value as an M24
methodology note/exercise (reproduce judge-swap variance on a small response set) even without ADD.

## History

- 2026-10-18 — WAIT — directly actionable and aligned with the course's resist-hype stance, but single preprint with no code; a strong candidate for a short M24 methodology addition at a future review — weekly/2026-W42.md — candidates C-20261015-15
- 2026-10-25 — WAIT — second independent paper making the same methodology point (a bare ASR hides judge choice, ignore-vs-refuse and task failure) with released artifacts; strong low-cost M24 extension candidate; pulled forward to 2026-11-15 — weekly/2026-W43.md — candidates C-20261019-03

# Jailbreak-ASR judge variance (how to read an ASR number)

- **Topic ID:** jailbreak-asr-judge-variance
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261015-15

## Summary

Swapping only the judge LLM used to score "did this response fulfil the prohibited request" can move
reported ASR by up to 82 percentage points on the same attack/response set. A training-free "semantic
reconstruction game" evaluator (reconstruct the request the response actually answers, compare to
decoys, allow abstention) reduces mean error against human labels and cross-judge variance. A
methodology point directly relevant to every jailbreak ASR number the course cites.

## Evidence

- https://arxiv.org/abs/2610.19306 — Davis, Emil-Popescu, Jana (Columbia, unverified against this paper); large quantified effect; single preprint, no code, 82pp is a max not a typical case.

## What would change the decision

Released code; independent confirmation of the variance figure. Low-cost, high-value as an M24
methodology note/exercise (reproduce judge-swap variance on a small response set) even without ADD.

## History

- 2026-10-18 — WAIT — directly actionable and aligned with the course's resist-hype stance, but single preprint with no code; a strong candidate for a short M24 methodology addition at a future review — weekly/2026-W42.md — candidates C-20261015-15

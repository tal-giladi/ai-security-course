# AI-chat front-ends leaking conversation content to third-party trackers

- **Topic ID:** ai-chat-frontend-tracker-leakage
- **Status:** WAIT
- **Next review:** 2026-12-13
- **Course change:** none
- **Candidates:** C-20261028-01

## Summary

Network interception plus JS-engine instrumentation of 42 AI chat platforms (general, health, legal, education) found that 21 leak conversation titles and 9 leak verbatim prompts to third-party trackers. Many also send the user's email address, which links identity to conversation content.

## Evidence

- https://arxiv.org/abs/2610.37467 — Bekos, Tsouvalas, Nikiforakis, Polychronakis; to appear in IEEE S&P 2027 (peer-reviewed); no code/data stated.

## What would change the decision

Publication of the platform list or measurement code, or a second study. Strong on evidence, but it is classic web privacy applied to an AI product. The deciding question is whether it fits 01.1 (AppSec primitives) or 29.1 as an extension with a CSP/script-isolation lab. Re-review once the S&P version is out.

## History

- 2026-11-01 — WAIT — single fresh source without independent replication or adoption; promising but not yet mature enough to teach (see weekly report for the six answers) — weekly/2026-W44.md — candidates C-20261028-01

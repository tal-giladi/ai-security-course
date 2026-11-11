# Black-box extraction of memorized credentials from commercial LLMs

- **Topic ID:** llm-credential-memorization-extraction
- **Status:** WAIT
- **Next review:** 2026-11-15
- **Course change:** none
- **Candidates:** C-20260930-03

## Summary

A black-box, output-only pipeline (distill a local proxy, then targeted sampling + statistical
filtering) to extract memorized API keys/secrets from commercial LLMs trained on code corpora,
with a stated "responsible real-world evaluation" naming OpenAI and Claude Code as targets. Relevant
to M12 extraction/memorization and M02 training-data leakage.

## Evidence

- https://arxiv.org/abs/2609.36941 — single paper; abstract-only summary, numeric results NOT yet verified from the PDF.

## What would change the decision

MAINTAINER ACTION before any course use: read the full PDF to confirm the real-key recovery numbers,
and check for any Anthropic/OpenAI statement, before repeating the "Claude Code" detail as fact.
Then independent replication. Teachable form would use a locally hosted small model fine-tuned on a
synthetic LAB-CANARY leaked-secrets corpus (never real extraction).

## History

- 2026-10-04 — WAIT — relevant and on real named systems, but single paper, numbers unverified, and names a product in the course's own toolchain — must verify the primary before teaching — weekly/2026-W40.md — candidates C-20260930-03

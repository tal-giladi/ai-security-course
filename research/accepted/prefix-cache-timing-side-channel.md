# Cross-tenant prefix-cache timing side channels in LLM serving

- **Topic ID:** prefix-cache-timing-side-channel
- **Status:** ADD
- **Next review:** on new evidence
- **Course change:** `lessons/module-15/lesson-02.md` (new lesson 15.2, added 2026-11-22) + `lesson-02.quiz.yaml`; `labs/module-15/prefix_cache/`; `assessments/module-15-quiz.quiz.yaml` (q10 appended) and `assessments/module-15-quiz.md` (review link); `_sidebar.md` (entry 18, later running numbers shifted by one); `curriculum/course-outline.md`; `references/standards-map.md`; `glossary.md`
- **Candidates:** C-20261118-01

## Summary

A prefix (KV) cache shared across tenants makes a cache hit faster, so time-to-first-token tells one
tenant whether another already sent a text: a membership oracle that, with chained block hashes and a
known suffix, recovers templated secrets. Per-tenant cache salting closes the channel at the cost of
cross-tenant reuse; "keep sharing but hide the hit" fails on step-based schedulers because the saved
work moves the requests queued behind the hit.

## Evidence

- https://arxiv.org/abs/2502.07776 — Gu, Li, Kuditipudi, Liang, Hashimoto, *Auditing Prompt Caching in Language Model APIs*, ICML 2025: statistical timing audits detect global cross-user cache sharing in seven API providers, including OpenAI. Verified 2026-11-22.
- https://arxiv.org/abs/2409.20002 — Song et al., *The Early Bird Catches the Leak*, IEEE TIFS: KV- and semantic-cache timing channels; system prompts and peer prompts recovered. Verified 2026-11-22.
- https://github.com/vllm-project/vllm/security/advisories/GHSA-4qjh-9fv9-r85r — CVE-2025-46570, CVSS 3.1 2.6, vLLM < 0.9.0; TTFT reveals chunk-level hits (AUC 0.571 at 1 token, 0.99 at 8 tokens). Verified 2026-11-22.
- https://github.com/vllm-project/vllm/pull/17045 — "[Core] Prevent side-channel attacks via cache salting" (merged): optional `cache_salt` mixed into the first block hash. Verified 2026-11-22.
- https://docs.vllm.ai/en/latest/design/prefix_caching.html — documents per-request salting "to isolate caches in multi-tenant environments" and that it "prevents timing-based attacks"; block hash = hash(parent hash, block tokens, extra keys incl. salt). Verified 2026-11-22.
- https://arxiv.org/abs/2611.20291 — Sun, Xiao (2026 preprint): hiding hits fails via scheduler step shifts (listener requests); one probe, advantage >= 0.98 for 256+ tokens on a vLLM trace replay; random delays must be ~10x the shift for advantage 0.1; leakage–savings bound. No code. EMERGING. Verified 2026-11-22.
- https://arxiv.org/abs/2411.18191 — InputSnatch (preprint): learned candidate generation + timing analysis for input theft from cache-sharing services. Verified 2026-11-22.
- https://arxiv.org/abs/2611.10756 — Mirage (daily C, 2026-11-10): gateway-side emission padding that keeps sharing (the class of defense 2611.20291 attacks). Not re-verified.
- Unverified single-source report seen in search results (not used in the lesson): a 2026 vLLM advisory that a `/v1/responses` tool-continuation path drops `cache_salt`. Check against the vLLM repository at the next touch of this topic.

## What would change the decision

Already in the course. Revisit on: an independent reproduction or code for the scheduler-shift
result (promote it from EMERGING), a new engine-level mitigation with measured cost, or a verified
salt-bypass advisory (worth a dated real-world example in 15.2).

## History

- 2026-11-22 — ADD — a reproducible attack class with a measured, shipped defense and its cost: peer-reviewed real-provider audit (ICML 2025), journal attack paper (TIFS), a CVE and salting fix in vLLM, plus a 2026 result that the hide-the-hit alternative fails; genuinely new to the course; new lesson 15.2 with a stdlib simulator lab — weekly/2026-W47.md — candidates C-20261118-01

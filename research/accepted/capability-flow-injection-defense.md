# Prompt-injection defense by design: Dual LLM plan isolation, CaMeL capability flow control, and branch steering in computer-use agents

- **Topic ID:** capability-flow-injection-defense
- **Status:** ADD
- **Next review:** on new evidence
- **Course change:** `lessons/module-17/lesson-02.md` (new lesson 17.2, added 2026-10-11); `labs/lab-33-capability-flow/`; `_sidebar.md`; `curriculum/course-outline.md`; `references/standards-map.md`
- **Candidates:** C-20261005-02, C-20261008-03

## Summary

The architectural family of prompt-injection defenses: plan isolation (Dual LLM: the planner never reads untrusted data) gives control-flow integrity; CaMeL adds capability tags (provenance + readers) and a policy-checking interpreter, bounding data flow. In computer-use agents plans must branch on screen content and ground targets from the screen, which enables branch steering (steer into a pre-approved hazardous branch); per-branch ahead-of-time capability constraints (COBRA) or per-step action transactions (Secure-CUA) are the proposed fixes. The ADD rests on the mature, multi-group foundation (2023–2025); the 2026 CUA papers are taught as EMERGING.

## Evidence

- https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ — Dual LLM pattern (2023). Fetched & verified 2026-10-11.
- https://arxiv.org/abs/2503.18813 — CaMeL, Debenedetti, Shumailov, Fan, Hayes, Carlini, Fabian, Kern, Shi, Terzis, Tramèr (2025): 77% vs 84% AgentDojo utility with provable security; STRICT/NORMAL control-flow modes; documented out-of-scope classes (side channels, text-to-text, phishing, compromised prompt); ~2.82×/2.73× median token overhead. Fetched & verified 2026-10-11.
- https://arxiv.org/abs/2506.08837 — Design Patterns for Securing LLM Agents against Prompt Injections (2025), 14 authors across several organisations — independent generalisation into a pattern catalogue. Verified.
- https://arxiv.org/abs/2505.23643 — FIDES, Microsoft Research (2025): information-flow control planner with confidentiality/integrity labels on AgentDojo — independent group, same mechanism. Verified.
- https://arxiv.org/abs/2505.22852 — Operationalizing CaMeL (2025): enterprise engineering follow-up. Verified.
- https://arxiv.org/abs/2610.03089 — Zingrillo, Foerster, Shumailov, Zhao, Mullins (2026): branch steering; STEER-Bench 101 tasks/9 domains; 94.4% ASR standard CUAs, 89.5% vanilla Dual-LLM CUAs; COBRA 0% ASR at 97% benign utility. EMERGING, single preprint. Verified.
- https://arxiv.org/abs/2610.09469 — Secure-CUA, Choudhary et al. (2026): action transactions + masking; 53.55% vs 55.12% (vanilla) vs 13.17% (CaMeL-CUA) benign success on 400 WebArena tasks. Concurrent independent work. EMERGING. Verified.
- Teaching adoption (search result, not fetched — host unreachable from this environment): CaMeL listed as a reading on the MIT 6.858 (2026) course site.

## What would change the decision

n/a — ADDed. Independent reproduction of branch steering or a released STEER-Bench would upgrade section 5–6 of 17.2 from EMERGING; a refutation would be recorded as an extension, not by editing the lesson.

## History

- 2026-10-11 — ADD — the course had no coverage of the by-design injection-defense family (Dual LLM / CaMeL / information-flow control), which is mature and independently implemented (Google/ETH, Microsoft FIDES, multi-org Design Patterns); two independent same-week CUA papers supply a measured failure mode and defenses that make the guarantee boundaries teachable. New lesson 17.2 + Lab 33 (10 tests; full suite 144 passed) — weekly/2026-W41.md — candidates C-20261005-02, C-20261008-03

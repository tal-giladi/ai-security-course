# Lab 14 — RAG retrieval attack surface: poisoning & ranking manipulation

**Module:** 14 (Stage 6 · RAG security). **Time:** ~2 h. **Hardware:** CPU, numpy, offline (shim).
**Targets:** local; synthetic canary.

## Goal

Attack the *retrieval* step, not just the prompt. A poisoned document must first **win retrieval**
(rank into the top-k for a target query) before its injected instruction can fire (PoisonedRAG).
Reproduce it against a transparent embedding+cosine retriever, run the end-to-end exploit through
the shim, then defend at the retrieval layer.

## Run

```bash
py labs/lab-14/rag.py         # poison ranks #1, gets retrieved, leaks canary; provenance allowlist stops it
py -m pytest labs/lab-14 -q
```

## What to notice

- **Retrieval is a new attacker objective.** Injection (M05) still needs the malicious text *in
  context*; in RAG the attacker earns that by manipulating similarity/ranking (keyword stuffing =
  gradient-free embedding optimization).
- **Cosine/ANN are attackable math.** Similarity is just geometry; term overlap moves the query
  vector toward the poison. Rerankers, thresholds, and dedup change that geometry.
- **Provenance beats content filtering.** Excluding untrusted sources (the `web` doc) removes the
  poison regardless of how cleverly it games similarity — the retrieval-layer analog of least
  privilege.

## Exercise

See [Lesson 14.1](../../lessons/module-14/lesson-01.md): sweep stuffing repetitions vs rank; craft a
poison that ranks high *without* obvious keyword stuffing (evade a dedup/perplexity filter); add a
similarity-threshold and reranker defense and measure ASR; combine with the confused-deputy exfil
(Lab 05); write the guarantee box. Multi-tenant leakage is Lab 15.

## Reset / Docker

Stateless. `docker compose up` runs `rag.py` with no egress.

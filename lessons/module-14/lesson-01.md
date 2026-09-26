<div class="prereq">

**Prerequisites.** [05.1 indirect injection](../module-05/lesson-01.md) (the confused-deputy chain
this builds on). **Sibling:** embeddings, cosine similarity, RAG, ANN/HNSW (RAG module) — we do
**not** reteach embeddings; we attack retrieval. Lab: numpy + shim, offline.

**You will learn.** The retrieval layer as an attack surface: **document poisoning**, **embedding /
ranking manipulation**, **citation manipulation**, and **retrieval DoS** — and the crucial addition
over plain indirect injection: the attacker must first **win retrieval** (get their poison into the
top-k) before any injection fires. Plus retrieval-layer defenses (provenance, thresholds, dedup,
reranking) and their limits.

**Why this matters.** RAG is how most production LLM apps get "knowledge," and its ingestion is
usually fed by untrusted or semi-trusted sources (web, uploads, tickets). Poisoning the knowledge
base is one of the most practical real-world attacks, and it lives in the *math of similarity* as
much as in the prompt.

</div>

# 14.1 · RAG retrieval attack surface

## Why this matters

Indirect injection (M05) assumed the malicious text was already retrieved. RAG makes *getting
retrieved* the attacker's job — and that job is winnable, because retrieval is cosine similarity over
embeddings, a geometry an attacker can manipulate. Once the poison is in the top-k, it's just
indirect injection again. Understanding retrieval as an optimization the attacker plays is the core
skill of RAG security.

## Learning objectives

1. Describe the RAG pipeline and mark its trust boundaries (ingestion is the poisoning entry).
2. Explain retrieval math (embeddings, cosine, top-k, ANN/HNSW) *from the attacker's view*.
3. Craft a poisoned document that **wins retrieval** for a target query and carries an injection.
4. Enumerate RAG-specific attacks: embedding/ranking manipulation, citation/source spoofing,
   retrieval DoS, stale/poisoned KB.
5. Apply and evaluate retrieval-layer defenses (provenance allowlist, similarity threshold,
   dedup/near-duplicate filter, reranking) and their bypasses.

## Concept

### The pipeline and where poison enters

```text
[sources: web / uploads / tickets] ─ingest─▶ [chunk] ─embed─▶ {vector store}
                                                                     │ retrieve top-k by cosine
   [user query] ─embed─────────────────────────────────────────────▶│
                                                                     ▼
                                                  ( LLM answers over retrieved chunks )
```

The **ingestion** edge is the poisoning boundary: whatever an attacker can get *ingested* (a crawled
page, an uploaded file, a support ticket) becomes a candidate for retrieval. The retrieval step then
decides whether the poison reaches the model — so the attacker optimizes to **win retrieval**.

### Retrieval math, for attackers

Documents and queries are embedded to vectors; retrieval returns the top-k by **cosine similarity**
$\cos(q,d)=\frac{q\cdot d}{\|q\|\|d\|}$. To rank a poison $d$ into the top-k for target query $q$, the
attacker maximizes $\cos(q,d)$. Two levers:
- **Content (gradient-free):** make $d$ share the query's tokens/topics — keyword stuffing,
  paraphrase, topical padding. In a bag-of-tokens/TF-ish embedding (like the lab's), repeating the
  query terms drives $d$'s vector toward $q$'s direction, raising cosine. Lab: a keyword-stuffed
  poison ranks **#1**.
- **Embedding-space (if the attacker can compute embeddings):** directly optimize text whose
  embedding is near $q$ (or near a *cluster* of likely queries), analogous to the adversarial
  optimization of Stage 4 — a "universal" poison for many queries.

ANN indexes (HNSW) approximate this top-k for speed; they don't change the attacker's goal, but their
graph structure adds subtle surfaces (a poison inserted to sit on many neighbors' paths can be
retrieved for more queries than its raw similarity suggests).

### The RAG attack catalog

- **Document poisoning + injection (PoisonedRAG):** win retrieval, then inject (the lab).
- **Ranking manipulation:** push a legitimate-but-wrong or attacker doc above the correct source.
- **Citation/source spoofing:** craft the doc so the model cites it as authoritative ("According to
  the official policy…") — manipulating the *trust signal* the answer carries.
- **Retrieval DoS:** flood the KB with near-duplicates or high-similarity noise so real answers get
  crowded out of the top-k, or make retrieval expensive.
- **Stale/poisoned KB:** long-lived poison that answers many future queries.

## Intuition

Retrieval is a popularity contest decided by "who looks most like the question." The attacker doesn't
need the best or truest document — just one that *resembles the query* enough to make the top-k, with
the payload stapled on. Keyword stuffing is stuffing the ballot box with copies of the question's own
words. Defenses either check *who submitted the ballot* (provenance) or *whether it's a genuine
distinct answer* (dedup, thresholds, reranking) — not just how similar it looks.

## Technical explanation & Code

`labs/lab-14/rag.py`: a transparent hashing embedding (stable, no download) + cosine retrieval.
`craft_poison` stuffs query tokens and appends the injection; `poison_rank` shows it ranks #1;
`rag_answer` pipes retrieved text into the shim, and the canary leaks. Defenses are parameters on
`retrieve`: `allowed_sources` (provenance allowlist) and `dedup` (near-duplicate filter). The
allowlist excludes the untrusted `web` source, so the poison is never retrieved.

## Mathematics

**Why keyword stuffing wins.** With a token-count embedding, $d$'s vector is (normalized) token
frequencies. Adding $r$ copies of the query's tokens pushes $d$'s unnormalized vector toward $q$'s
support; as $r$ grows, $\cos(q,d)\to$ the cosine of $q$ with the pure query-token vector, which is
high. Formally, if $d = d_0 + r\,q_{\text{tok}}$ (base doc plus $r$ query-token blocks), then
$\cos(q,d)=\frac{q\cdot d_0 + r\,(q\cdot q_{\text{tok}})}{\|q\|\,\|d_0 + r q_{\text{tok}}\|}\to
\frac{q\cdot q_{\text{tok}}}{\|q\|\|q_{\text{tok}}\|}$ as $r\to\infty$ — the maximum achievable. So a
few repetitions suffice to reach the top; you'll trace rank vs $r$ in the exercise.

**Defense as changing the geometry / gating.** A **similarity threshold** rejects docs below
$\tau$ (poison must clear $\tau$ *and* out-rank real docs). **Dedup** removes near-duplicates
($\cos>0.92$), defeating flood/DoS and copy-stuffing. **Reranking** (a cross-encoder scoring
query-doc *jointly*) is harder to fool by term overlap than bi-encoder cosine — but is itself a model
with its own adversarial surface. **Provenance** ignores geometry entirely: untrusted sources can't
be retrieved regardless of similarity.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — RAG retrieval defenses.**

*Provenance allowlist (enforced, strongest):*
- **Stops:** any poison from a non-allowlisted source, regardless of how it games similarity.
- **Does NOT stop:** poison ingested through an *allowed* source (a compromised trusted feed, a
  malicious upload to a trusted bucket), or attacks within trusted data.
- **Adapts:** attacker gets content into a trusted source; pursue cross-tenant/authorization gaps (M15).
- **Cost:** you must *have* provenance metadata and curate sources (operational).

*Similarity threshold / dedup / reranking (probabilistic):*
- **Stops:** low-similarity noise, near-duplicate floods (DoS), and crude term-overlap stuffing.
- **Does NOT stop:** a fluent, genuinely-relevant poison that legitimately scores high; rerankers
  can still be adversarially optimized.
- **Adapts:** paraphrase to look like a distinct, relevant answer; optimize against the reranker.
- **Cost:** thresholds hurt recall (miss real answers); reranking adds latency/a second model.

**Takeaway:** layer **provenance** (who) with **retrieval hygiene** (threshold/dedup/rerank) and
**downstream least privilege** (M05 egress control) — retrieval defenses reduce *whether poison is
retrieved*; they don't make a retrieved poison safe.

</div>

## Practical lab

<div class="lab">

**Lab 14** ([`labs/lab-14/`](../../labs/lab-14/README.md)) — poison wins retrieval (#1) and leaks;
provenance allowlist stops it. numpy + shim, offline, instant tests.

```bash
py labs/lab-14/rag.py
py -m pytest labs/lab-14 -q
```

</div>

## Exercise

1. **Rank vs stuffing.** Sweep `stuffing_reps`; plot the poison's rank vs repetitions and confirm the
   asymptotic-cosine argument. Find the minimum reps to reach top-k.
2. **Stealthy poison.** Craft a poison that ranks in the top-k *without* obvious repeated tokens
   (paraphrase / topical padding) so it evades a naive "repeated-token" or dedup filter, then show it
   still leaks. Discuss why this is harder to filter.
3. **Retrieval hygiene defenses.** Implement (a) a similarity **threshold** $\tau$ and (b) a
   **reranker** (a cross-encoder stand-in: score by joint query+doc token overlap minus stuffing
   penalty). Measure exploit ASR under each vs the provenance allowlist; report recall cost.
4. **Retrieval DoS.** Flood the store with near-duplicate high-similarity noise; show a real query's
   correct doc gets pushed out of the top-k. Then show `dedup` restores it. Quantify.
5. **End-to-end + egress (purple team).** Combine the retrieved poison with the confused-deputy exfil
   (Lab 05 renderer/egress). Show the full chain, then apply the layered defense (provenance +
   threshold + M05 egress allowlist) and re-measure. Write the guarantee box.
6. **Citation manipulation (reasoning).** Explain how a poison can make the model present it as an
   authoritative citation, and why "the model cited a source" is not a trust signal.

<details><summary>Hint (step 2)</summary>

Instead of repeating the exact query tokens, write a fluent paragraph *about* the query topic using
synonyms and related terms — its embedding still lands near the query in a real (semantic) embedder,
and in the hashing embedder you can approximate this by using overlapping-but-varied tokens. Dedup
and repeated-token filters key on surface repetition, which this avoids; you need semantic/provenance
defenses instead.

</details>

**Deliverable.** The rank-vs-reps curve, a stealthy poison, threshold/reranker vs allowlist ASR with
recall costs, the DoS demo + dedup fix, the end-to-end chain + layered defense, and the guarantee box.

```bash
py course.py complete 14.1
```

## Research paper

**Zou et al., "PoisonedRAG: Knowledge Poisoning Attacks to Retrieval-Augmented Generation of Large
Language Models" (2024).** *Why:* formalizes the two-part RAG attack — craft a text that (1) is
retrieved for a target query and (2) steers the answer — exactly the lab. *Read:* the attack
formulation (retrieval condition + generation condition) and the black-box vs white-box variants.
*Reproduce (light):* your lab is the black-box, term-overlap version; add the "generation condition"
explicitly (a poison optimized to change the *answer*, not just leak). *Limits:* real retrievers use
semantic embedders + rerankers; term-overlap stuffing is the crudest lever — the paper's optimized
poisons transfer better and are stealthier.

## Further reading

- OWASP LLM08 (Vector & Embedding Weaknesses), LLM01 (indirect injection subtype);
  [`references/standards-map.md`](../../references/standards-map.md).
- HNSW paper (Malkov & Yashunin) for ANN structure; forward link M15 (multi-tenant retrieval leakage).

## Assessment

<details><summary>Q1. What does RAG add over plain indirect injection?</summary>

The attacker must first **win retrieval** — get the poisoned document into the top-k for the target
query — before the injected instruction ever reaches the model. That makes retrieval (embedding
similarity, ranking, ANN) a new, attackable surface on top of the injection itself.

</details>

<details><summary>Q2. Why does keyword stuffing win retrieval, mathematically?</summary>

Retrieval ranks by cosine similarity; adding copies of the query's tokens pushes the poison's
embedding toward the query-token direction, so $\cos(q,d)$ approaches its maximum as repetitions
grow. A few repetitions suffice to out-rank genuine documents whose overlap with the query is lower.

</details>

<details><summary>Q3. Why is a provenance allowlist stronger than a similarity threshold?</summary>

A threshold is geometry-based: a fluent, genuinely-relevant poison can legitimately score high and
pass it. Provenance ignores geometry — an untrusted source can't be retrieved no matter how it games
similarity. It's the retrieval-layer least-privilege control; its gap is poison ingested through a
*trusted* source, so layer it with hygiene defenses.

</details>

<details><summary>Q4. Why is "the model cited a source" not a trust signal?</summary>

Because the cited source may itself be attacker-poisoned content that won retrieval and was crafted
to read as authoritative (citation/source spoofing). The citation reflects what was retrieved, not
whether it is trustworthy; trust must come from provenance/authorization, not from the model's
gesture of citing.

</details>

## What you should now be able to do

- Map the RAG pipeline's trust boundaries and identify ingestion as the poisoning entry.
- Reason about retrieval (cosine/ANN) as an attacker and craft poison that wins retrieval + injects.
- Enumerate RAG attacks (poisoning, ranking, citation, DoS) and reproduce the core one.
- Apply and evaluate provenance + hygiene retrieval defenses and know their limits.

## Progress checkpoint

```bash
py course.py complete 14.1
py course.py next
```

**Next:** 15.1 · Multi-tenant retrieval — authorization failures and cross-user/cross-tenant leakage,
where the bug is missing authz on retrieval, not the model at all.

<div class="prereq">

**Prerequisites.** [14.1 RAG retrieval](../module-14/lesson-01.md), [00.1 authz / "the model
decides"](../module-00/lesson-01.md), [01.1 broken access control / IDOR](../module-01/lesson-01.md).
Lab: numpy + shim, offline.

**You will learn.** The multi-tenant RAG failure that is *not about the model at all*: **missing or
misplaced authorization on retrieval**, causing **cross-user / cross-tenant leakage**, plus
**metadata attacks** and where the authz check must live. This is broken access control (a top web
vulnerability) reappearing inside RAG.

**Why this matters.** In production, the single most damaging RAG bug is usually this one: a shared
index serving many customers with authorization enforced weakly, late, or "by the model." It leaks
other customers' confidential data — a direct, severe, and common breach, and one no prompt-level
defense can fix.

</div>

# 15.1 · Multi-tenant retrieval leakage

## Why this matters

You can perfectly defend prompts, filter outputs, and still hand tenant A tenant B's secrets —
because the retriever returned B's document and the model faithfully used it. The vulnerability is
an *access-control* bug on the retrieval path, identical in shape to IDOR/broken access control in
any web app (01.1). It is common because RAG indexes are shared for cost/efficiency and because teams
mistake "the model won't reveal it" for authorization.

## Learning objectives

1. Explain cross-tenant/cross-user leakage as broken access control on retrieval, independent of the
   model.
2. Contrast **no-authz**, **post-filter**, and **pre-filter** retriever designs and their failure
   modes (leak, availability, spoofing).
3. Explain why authorization must be **enforced in code on a trusted principal**, before ranking.
4. Identify **metadata attacks** (spoofing the tenant/ACL field) and defend with trusted mappings.
5. Combine with poisoning (M14) and reason about defense-in-depth for multi-tenant RAG.

## Concept

### The bug, precisely

A shared vector store holds documents for many principals (users/tenants), each with metadata (owner,
ACL). A query returns the top-k by similarity. If the retriever does **not** restrict candidates to
what the *authenticated caller* may see, it returns whatever is most similar — including other
tenants' private docs. The model then answers using them, leaking the data. The model did nothing
wrong; the retrieval query was unauthorized. Lab: an Acme user asking "confidential API key" retrieves
Globex's secret doc (canary `LAB-CANARY-globex-*`).

### Three designs (only one is correct)

| Design | What it does | Failure |
|---|---|---|
| **No-authz** | rank all docs, return top-k | **cross-tenant leak** |
| **Post-filter** | rank all docs top-k, then drop unauthorized | **availability** (real docs crowded out of the k), and **metadata spoofing** if it trusts the doc's own ACL field |
| **Pre-filter (correct)** | restrict candidates to the caller's authorized set *before* ranking, using a **trusted** principal→scope mapping | correct; residual risk is poison within the authorized set (M14) |

**Pre-filter** is the only correct design: authorization is a deterministic code decision on the
authenticated principal, applied before similarity ever runs — the retrieval analog of a
parameterized query / row-level security.

### Metadata attacks

Post-filtering (or any authz) that trusts a *document's own* tenant/ACL field is spoofable: an
attacker who can influence ingestion sets their poisoned doc's `tenant = victim` (or `acl = public`),
and it passes the filter. Authorization must key on the **caller's** identity mapped to scope via a
**trusted** source (your auth system / DB), never on attacker-influenceable document metadata.

## Intuition

A shared filing cabinet holds every client's folder. "Retrieval" is a clerk who fetches the folders
whose labels best match your question. No-authz: the clerk hands you whatever matches, including other
clients' folders. Post-filter: the clerk grabs the best matches, then removes the ones not yours — so
you sometimes get an almost-empty handful (your real folder got bumped), and if a folder's *label*
lies about who owns it, the clerk is fooled. Pre-filter: the clerk first pulls only your drawer, then
finds the best match *within it* — checked against the building's access list, not the folder's own
sticker. Only the last is secure.

## Technical explanation & Code

`labs/lab-15/tenant.py`: a `MultiTenantStore` with three methods. `retrieve_vuln` ignores tenant;
`retrieve_postfilter` takes global top-k then filters (availability loss; trusts `d.tenant`);
`retrieve_prefilter` restricts to the caller's tenant before ranking. `cross_tenant_leak` runs an
Acme user against a query that matches Globex's secret. Results: vuln leaks; post-filter blocks the
leak but returns fewer docs; pre-filter is correct.

## Mathematics

Little math — this is access control — but two quantifiable points:

- **Availability cost of post-filtering.** If the caller owns a fraction $\rho$ of the index and the
  index is well-mixed, the expected number of *authorized* docs in a global top-k is $\approx k\rho$;
  for small $\rho$ (many tenants), post-filter routinely returns far fewer than $k$ useful results —
  a measurable recall/utility loss the exercise quantifies. Pre-filter returns $k$ authorized docs
  (until the tenant's own pool is exhausted).
- **Leak probability under no-authz.** The chance a cross-tenant doc appears in the top-k rises with
  its similarity to the query and with index mixing; for a targeted query crafted to match a victim
  doc (attacker knows the topic), leak probability $\to 1$ — it is not a rare accident but a
  reliable attack.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — pre-filter authorization (the correct control).**
- **Stops:** all cross-tenant retrieval — unauthorized docs are never candidates, so they can't be
  ranked or returned. Enforced in code on the authenticated principal.
- **Does NOT stop:** poison *within* the caller's authorized scope (M14), over-broad scopes (a user
  granted too much), or leakage through *shared* documents with wrong ACLs. Also doesn't fix bad
  provisioning (wrong principal→scope mapping).
- **Attacker adapts:** attack within-scope (poison the tenant's own KB), exploit over-provisioned
  roles, or target the auth mapping itself.
- **Cost:** you must have and maintain accurate ACL metadata and a trusted principal→scope mapping;
  per-tenant partitioning may reduce index-sharing efficiency.
- **Contrast — post-filter:** blocks the leak *only if* it doesn't trust document-supplied ACLs
  (spoofable), and it degrades availability. **Never** rely on the model to enforce tenancy ("the
  model decides" is not authorization, 00.1).

</div>

## Practical lab

<div class="lab">

**Lab 15** ([`labs/lab-15/`](../../labs/lab-15/README.md)) — cross-tenant leak (vuln), correct
pre-filter, post-filter's availability bug. numpy + shim, offline, instant.

```bash
py labs/lab-15/tenant.py
py -m pytest labs/lab-15 -q
```

</div>

## Exercise

1. **Reproduce the leak** and confirm the model is irrelevant (swap the shim seed / a different
   "model" — the leak persists because it's in retrieval).
2. **Availability cost.** Vary the number of tenants (index mixing) and measure how many authorized
   docs post-filter returns vs pre-filter for the same $k$. Confirm the $\approx k\rho$ estimate.
3. **Metadata spoofing (purple team).** Add an ingestion path where an attacker (Acme) inserts a doc
   with `tenant="globex"` (or `acl="public"`). Show post-filter/naive-authz that trusts the doc's
   field is bypassed; then implement pre-filter keyed on a **trusted** principal→tenant map and show
   it resists (the attacker's doc is in Acme's scope, not Globex's, regardless of its claimed field).
4. **Leak reliability.** Craft a query that reliably matches a victim tenant's secret doc; measure
   leak rate under no-authz across seeds. Show it's a reliable attack, not a fluke.
5. **Combine with poisoning.** Within a tenant, plant a M14 poison; show pre-filter stops
   cross-tenant leaks but not within-tenant poison — motivating defense-in-depth. Write the guarantee
   box for the full stack (pre-filter authz + provenance + retrieval hygiene + egress control).
6. **Design question.** Sketch how you'd enforce this at scale: per-tenant namespaces vs a shared
   index with row-level security; where the principal→scope mapping comes from; how you'd test for
   regressions (an automated cross-tenant retrieval test in CI).

<details><summary>Hint (step 3)</summary>

The fix is the same as every access-control fix: authorize on the *subject* (authenticated caller),
not the *object's self-description*. Pre-filter builds the candidate set from "docs whose owner ==
the caller's tenant", where the caller's tenant comes from your auth context — a document claiming
`tenant="globex"` simply isn't in Acme's candidate set, so its lie is irrelevant.

</details>

**Deliverable.** The reproduced leak, the availability measurement, the spoofing bypass + pre-filter
fix, the leak-reliability numbers, the combined poisoning result, and the scale design + guarantee box.

```bash
py course.py complete 15.1
```

## Research paper

No single canonical paper — this is broken access control (OWASP A01) applied to RAG. Read instead:
- **OWASP Top 10 A01:2021 — Broken Access Control** and **OWASP LLM Top 10 LLM02 (Sensitive
  Information Disclosure) / LLM08 (Vector & Embedding Weaknesses)** — map the leak to the standard
  category. *Extract:* the guidance that access control must be server-side, deny-by-default, and on
  the authenticated subject.
- A vendor RAG-security guide on **document-level / row-level security for retrieval** — note the
  recommendation to pre-filter by identity, not post-filter.
*Reproduce:* the lab is the core; add an automated CI test that asserts no query from tenant A ever
returns a tenant-B doc (regression guard) — the practical deliverable a real team needs.

## Further reading

- Row-level security in vector DBs (per-namespace / metadata-filtered retrieval) — implementation
  patterns. [`references/standards-map.md`](../../references/standards-map.md).
- Back-link M14 (poisoning within scope); forward link M18 (agents retrieving across tools/tenants).

## Assessment

<details><summary>Q1. Why is cross-tenant RAG leakage not a model problem?</summary>

Because the leak occurs at retrieval: an unauthorized document is fetched into context because the
retriever didn't restrict candidates to what the authenticated caller may see. The model then uses it
faithfully. No prompt or output defense fixes it — the authorization check must be deterministic code
on the retrieval path.

</details>

<details><summary>Q2. Why is pre-filtering correct and post-filtering not?</summary>

Pre-filter restricts candidates to the caller's authorized scope *before* ranking, so unauthorized
docs are never eligible — and it keys on the trusted principal, not document metadata. Post-filter
ranks globally then drops unauthorized docs: it crowds out the caller's real results (availability)
and, if it trusts the document's own ACL field, is bypassable by metadata spoofing.

</details>

<details><summary>Q3. What is a metadata attack and how do you stop it?</summary>

An attacker who can influence ingestion sets their document's tenant/ACL field to a victim's value
(or "public") so an authz check that trusts document-supplied metadata passes it. Stop it by
authorizing on the authenticated *caller's* identity mapped to scope via a trusted source (auth
system/DB), never on attacker-influenceable document fields.

</details>

<details><summary>Q4. Under a targeted query, is cross-tenant leakage rare?</summary>

No. If the attacker knows the victim's topic, they craft a query that closely matches the victim's
secret doc, driving its similarity high; under a no-authz retriever the leak probability approaches 1.
It's a reliable, targeted attack, not an occasional accident.

</details>

## What you should now be able to do

- Recognize cross-tenant/cross-user RAG leakage as broken access control on retrieval.
- Choose the pre-filter design and enforce authz in code on the trusted principal before ranking.
- Identify and defend metadata-spoofing attacks; quantify post-filter's availability cost.
- Layer tenancy authz with provenance, retrieval hygiene, and egress control, and guard it with CI
  regression tests.

## Progress checkpoint

```bash
py course.py complete 15.1
py course.py next
```

**Next:** Stage 7 (the largest) — 16.1 · The agent attack surface: loops, planning, memory, tools,
credentials; excessive agency and the confused deputy formalized for autonomous agents.

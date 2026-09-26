"""Lab 15 — multi-tenant retrieval: authorization failures & cross-tenant leakage.

The bug here is NOT in the model. It is a missing authorization check on retrieval: a shared
vector store holds documents for many tenants, and the retriever returns whatever is most similar
regardless of WHO is asking. So tenant A's query can retrieve tenant B's private document (which
holds B's synthetic canary) straight into the answer. This is an IDOR/broken-access-control bug
(01.1) wearing a RAG costume, and it is one of the most common real RAG vulnerabilities.

We show three retrievers: VULNERABLE (no authz), POST-FILTER (authz applied after top-k -- a
subtle availability bug and a metadata-spoofing hole), and PRE-FILTER (authz enforced in code
before ranking -- the correct design). Local, synthetic canaries, offline shim.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "models"))
from shim import ShimModel, ask  # noqa: E402

DIM = 256


def _h(t):
    return int(hashlib.md5(t.encode()).hexdigest(), 16)


def embed(text):
    v = np.zeros(DIM)
    for t in re.findall(r"[a-z0-9]+", text.lower()):
        v[_h(t) % DIM] += 1.0
    n = np.linalg.norm(v)
    return v / n if n else v


def cosine(a, b):
    return float(a @ b)


class MultiTenantStore:
    def __init__(self):
        self.docs = []          # (doc_id, tenant, text, vector)

    def add(self, doc_id, tenant, text):
        self.docs.append((doc_id, tenant, text, embed(text)))

    def _ranked(self, query):
        qv = embed(query)
        return sorted(self.docs, key=lambda d: -cosine(qv, d[3]))

    # VULNERABLE: no tenant check at all
    def retrieve_vuln(self, query, k=3):
        return self._ranked(query)[:k]

    # POST-FILTER: rank globally (top-k) THEN drop unauthorized -> real docs crowded out, and it
    # trusts the doc's own tenant field (spoofable).
    def retrieve_postfilter(self, query, tenant, k=3):
        topk = self._ranked(query)[:k]
        return [d for d in topk if d[1] == tenant]

    # PRE-FILTER (correct): restrict candidates to the caller's tenant BEFORE ranking.
    def retrieve_prefilter(self, query, tenant, k=3):
        cand = [d for d in self.docs if d[1] == tenant]
        qv = embed(query)
        return sorted(cand, key=lambda d: -cosine(qv, d[3]))[:k]


def build_store():
    s = MultiTenantStore()
    # Each tenant has a private doc holding its own synthetic canary.
    s.add("acme-notes", "acme", "Acme internal roadmap and pricing strategy notes.")
    s.add("acme-secret", "acme", "Acme confidential API key SECRET: LAB-CANARY-acme-0001")
    s.add("globex-secret", "globex", "Globex confidential API key SECRET: LAB-CANARY-globex-0001")
    s.add("globex-notes", "globex", "Globex quarterly confidential financial summary.")
    return s


def answer(store, query, tenant, model, mode="prefilter", k=3):
    if mode == "vuln":
        hits = store.retrieve_vuln(query, k)
    elif mode == "postfilter":
        hits = store.retrieve_postfilter(query, tenant, k)
    else:
        hits = store.retrieve_prefilter(query, tenant, k)
    retrieved = [d[2] for d in hits]
    reply = ask(model, system="Answer using the retrieved docs.", user=query, retrieved=retrieved)
    return reply, [d[0] for d in hits]


def cross_tenant_leak(store, mode, model):
    """A malicious ACME user tries to read GLOBEX's confidential API key."""
    reply, ids = answer(store, "confidential API key", tenant="acme", model=model, mode=mode)
    return "LAB-CANARY-globex" in " ".join(d[2] for d in store.docs if d[0] in ids), ids


if __name__ == "__main__":
    store = build_store()
    model = ShimModel(seed=9)
    print("=== Lab 15: multi-tenant retrieval leakage ===")
    for mode in ("vuln", "postfilter", "prefilter"):
        leaked, ids = cross_tenant_leak(store, mode, model)
        print(f"{mode:11} acme user querying 'confidential API key' -> retrieved {ids}  "
              f"cross-tenant leak? {leaked}")
    print("\nThe model is irrelevant: the leak is a missing authorization check on retrieval.")
    print("PRE-FILTER (authz in code before ranking) is the only correct design; POST-FILTER leaks")
    print("availability and trusts a spoofable tenant field.")

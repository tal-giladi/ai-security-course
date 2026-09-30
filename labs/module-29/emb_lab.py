"""Lab 29 driver — embedding inversion & attribute extraction, then the noise defense trade-off.

Run: py labs/module-29/emb_lab.py

Purple cycle: invert & extract from stored embeddings -> measure recovery -> add noise (defense)
-> retest recovery AND retrieval utility -> read off the trade-off curve -> adapt (surrogate encoder).
"""
from __future__ import annotations

import numpy as np

import emb


def inversion_f1(sents, embs, k, sigma=0.0, surrogate=None):
    f1s = []
    for toks, e in zip(sents, embs):
        stored = emb.add_noise(e, sigma) if sigma else e
        rec = emb.invert(stored, k=k, surrogate=surrogate)
        f1s.append(emb.token_f1(toks, rec))
    return float(np.mean(f1s))


def extraction_accuracy(embs, labels, sigma=0.0):
    stored = np.array([emb.add_noise(e, sigma) for e in embs]) if sigma else embs
    n = len(labels)
    tr, te = slice(0, n // 2), slice(n // 2, n)
    w, b = emb.train_attribute_probe(stored[tr], labels[tr])
    return emb.probe_accuracy(w, b, stored[te], labels[te])


def retrieval_utility(sents, embs, sigma):
    # queries are the first 3 tokens of each sentence; correct hit = same sentence's stored embedding
    store = np.array([emb.add_noise(e, sigma) for e in embs]) if sigma else embs
    queries = np.array([emb.encode(toks[:3]) for toks in sents])
    return emb.retrieval_top1(queries, store, list(range(len(sents))))


if __name__ == "__main__":
    sents, embs, labels = emb.make_corpus()
    k = 5
    base_class = float(max(labels.mean(), 1 - labels.mean()))

    print("=== ATTACKS on clean stored embeddings ===")
    print(f"inversion token-F1 (k={k}):      {inversion_f1(sents, embs, k):.2f}")
    print(f"attribute extraction accuracy:   {extraction_accuracy(embs, labels):.2f} "
          f"(majority-class baseline {base_class:.2f})")

    print("\n=== DEFENSE: Gaussian noise on stored embeddings — recovery vs utility ===")
    print(f"{'sigma':>6} {'inv_F1':>8} {'extract_acc':>12} {'retrieval_top1':>15}")
    for sigma in (0.0, 0.05, 0.1, 0.2, 0.4):
        print(f"{sigma:>6} {inversion_f1(sents, embs, k, sigma):>8.2f} "
              f"{extraction_accuracy(embs, labels, sigma):>12.2f} "
              f"{retrieval_utility(sents, embs, sigma):>15.2f}")

    print("\n=== ADAPT: attacker uses an imperfect SURROGATE encoder (weights not exact) ===")
    surrogate = emb.E + emb.RNG.normal(0, 0.15, size=emb.E.shape)
    print(f"inversion token-F1 with surrogate: {inversion_f1(sents, embs, k, surrogate=surrogate):.2f}")
    print("\nVerdict: embeddings are not anonymised data — they invert to their tokens and leak")
    print("attributes to a linear probe. Noise trades recovery for retrieval utility; access control")
    print("and not storing raw embeddings of sensitive text are the load-bearing defenses.")

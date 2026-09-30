"""Lab 29 — embedding inversion and attribute extraction on a toy encoder (from scratch).

LOCAL/OFFLINE. A deterministic bag-of-tokens encoder stands in for a sentence-embedding model so the
mechanism is visible without downloading weights. Everything runs on synthetic sentences; the
"sensitive" content is a synthetic canary token. No network, no real data.

Encoder:   e(s) = (1/|s|) * sum_{t in s} E[t]      with E a fixed random token-embedding matrix.
Inversion: given e (and access to the encoder / a surrogate E), recover the token set of s.
Extraction: a linear probe predicts a private attribute from e without full inversion.
Defense:   add Gaussian noise to stored embeddings; measure recovery drop vs retrieval-utility drop.
"""
from __future__ import annotations

import numpy as np

RNG = np.random.default_rng(29)
DIM = 64

# --- vocabulary: ordinary tokens + a synthetic "sensitive" subset ---------------------------------
COMMON = [f"w{i}" for i in range(60)]
SENSITIVE = ["diagnosis", "salary", "LAB-CANARY-emb-0001", "password", "ssn"]
VOCAB = COMMON + SENSITIVE
V = len(VOCAB)
IDX = {t: i for i, t in enumerate(VOCAB)}

# fixed token-embedding matrix (the "model weights"); rows normalised.
E = RNG.standard_normal((V, DIM))
E /= np.linalg.norm(E, axis=1, keepdims=True)


def encode(tokens: list[str]) -> np.ndarray:
    rows = [E[IDX[t]] for t in tokens if t in IDX]
    return np.mean(rows, axis=0)


# --- attack 1: embedding inversion (recover the token set) -----------------------------------------
def invert(e: np.ndarray, k: int, surrogate: np.ndarray | None = None) -> list[str]:
    """Recover the k most likely tokens by scoring each token vector against the embedding.
    `surrogate` lets you test inversion with an imperfect copy of E (attacker without exact weights)."""
    M = E if surrogate is None else surrogate
    scores = M @ e                              # dot product per token
    top = np.argsort(scores)[::-1][:k]
    return [VOCAB[i] for i in top]


def token_f1(true_tokens: list[str], recovered: list[str]) -> float:
    t, r = set(true_tokens), set(recovered)
    if not t or not r:
        return 0.0
    tp = len(t & r)
    prec = tp / len(r)
    rec = tp / len(t)
    return 0.0 if prec + rec == 0 else 2 * prec * rec / (prec + rec)


# --- attack 2: attribute extraction (linear probe) -------------------------------------------------
def train_attribute_probe(embeddings: np.ndarray, labels: np.ndarray, epochs=300, lr=0.5):
    """Logistic-regression probe from scratch: predict a private attribute from an embedding."""
    w = np.zeros(embeddings.shape[1])
    b = 0.0
    for _ in range(epochs):
        z = embeddings @ w + b
        p = 1 / (1 + np.exp(-z))
        g = p - labels
        w -= lr * (embeddings.T @ g) / len(labels)
        b -= lr * g.mean()
    return w, b


def probe_accuracy(w, b, embeddings, labels) -> float:
    p = 1 / (1 + np.exp(-(embeddings @ w + b)))
    return float(((p > 0.5).astype(int) == labels).mean())


# --- defense: additive Gaussian noise on stored embeddings ----------------------------------------
def add_noise(e: np.ndarray, sigma: float) -> np.ndarray:
    return e + RNG.normal(0, sigma, size=e.shape)


# --- utility metric: nearest-neighbour retrieval top-1 accuracy -----------------------------------
def retrieval_top1(query_embs, store_embs, true_idx) -> float:
    hits = 0
    for q, ti in zip(query_embs, true_idx):
        sims = store_embs @ q / (np.linalg.norm(store_embs, axis=1) * np.linalg.norm(q) + 1e-9)
        if int(np.argmax(sims)) == ti:
            hits += 1
    return hits / len(true_idx)


# --- synthetic corpus -----------------------------------------------------------------------------
CANARY = "LAB-CANARY-emb-0001"


def make_corpus(n=200, sent_len=5, p_sensitive=0.5):
    """Private attribute = 'this sentence contains the canary token'. Positives include the canary
    (one consistent direction), so a linear probe can detect its PRESENCE from the embedding alone —
    an attribute leak that needs no full inversion."""
    sents, embs, labels = [], [], []
    for _ in range(n):
        toks = list(RNG.choice(COMMON, size=sent_len - 1, replace=False))
        has = RNG.random() < p_sensitive
        toks.append(CANARY if has else str(RNG.choice(COMMON)))
        sents.append(toks)
        embs.append(encode(toks))
        labels.append(1 if has else 0)
    return sents, np.array(embs), np.array(labels)

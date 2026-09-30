"""Acceptance tests for Lab 29. Run: py -m pytest labs/module-29 -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np

import emb
import emb_lab


def _corpus():
    return emb.make_corpus()


def test_inversion_recovers_most_tokens():
    sents, embs, labels = _corpus()
    f1 = emb_lab.inversion_f1(sents, embs, k=5)
    assert f1 > 0.85                          # embeddings invert to their tokens


def test_inversion_recovers_the_canary_when_present():
    sents, embs, labels = _corpus()
    got = 0
    for toks, e in zip(sents, embs):
        if emb.CANARY in toks and emb.CANARY in emb.invert(e, k=5):
            got += 1
    present = sum(emb.CANARY in t for t in sents)
    assert got / present > 0.8                # the sensitive token is usually recovered


def test_attribute_probe_beats_baseline():
    sents, embs, labels = _corpus()
    acc = emb_lab.extraction_accuracy(embs, labels)
    baseline = max(labels.mean(), 1 - labels.mean())
    assert acc > baseline + 0.2               # embeddings leak the attribute without inversion


def test_noise_reduces_recovery():
    sents, embs, labels = _corpus()
    clean = emb_lab.inversion_f1(sents, embs, k=5, sigma=0.0)
    noisy = emb_lab.inversion_f1(sents, embs, k=5, sigma=0.2)
    assert noisy < clean - 0.3                # defense clearly degrades inversion


def test_noise_also_costs_utility():
    sents, embs, labels = _corpus()
    u0 = emb_lab.retrieval_utility(sents, embs, 0.0)
    u2 = emb_lab.retrieval_utility(sents, embs, 0.2)
    assert u0 > 0.8 and u2 < u0 - 0.3         # the trade-off is real, not free


def test_surrogate_encoder_still_inverts_above_chance():
    sents, embs, labels = _corpus()
    surrogate = emb.E + np.random.default_rng(1).normal(0, 0.15, size=emb.E.shape)
    f1 = emb_lab.inversion_f1(sents, embs, k=5, surrogate=surrogate)
    assert f1 > 0.4                           # attacker does not need the exact weights

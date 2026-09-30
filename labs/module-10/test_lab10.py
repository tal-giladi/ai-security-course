import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adv2 import (make_data, MLP, train, cw_attack, l2_norms, transfer_rate,  # noqa: E402
                  smoothed_predict_and_certify)


def _split():
    x, y = make_data()
    return x[:1500], y[:1500], x[1500:], y[1500:]


def test_cw_finds_small_adversarial_perturbations():
    xtr, ytr, xte, yte = _split()
    m = train(MLP(seed=1), xtr, ytr)
    xa = cw_attack(m, xte[:200], yte[:200])
    fooled = (m(xa).argmax(1) != yte[:200])
    assert fooled.float().mean() > 0.3
    assert l2_norms(xa, xte[:200])[fooled].median() < 1.0, "CW perturbations should be small in L2"


def test_adversarials_transfer_across_models():
    xtr, ytr, xte, yte = _split()
    a, b = train(MLP(seed=1), xtr, ytr), train(MLP(seed=2), xtr, ytr)
    assert transfer_rate(a, b, xte[:300], yte[:300]) > 0.4, "PGD adversarials should transfer to B"


def test_randomized_smoothing_certifies_a_positive_radius():
    xtr, ytr, xte, yte = _split()
    base = train(MLP(seed=1), xtr, ytr, noise_sigma=0.25)
    radii = [smoothed_predict_and_certify(base, xte[i:i+1])[1] for i in range(30)]
    assert sum(r > 0 for r in radii) >= 15, "most points should get a provable robustness radius"

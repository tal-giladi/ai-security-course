import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adv import make_data, MLP, train, evaluate, fgsm, pgd, accuracy  # noqa: E402

EPS = 0.05


def _split():
    x, y = make_data()
    return x[:1500], y[:1500], x[1500:], y[1500:]


def test_standard_model_collapses_under_pgd():
    xtr, ytr, xte, yte = _split()
    m = train(MLP(seed=1), xtr, ytr)
    e = evaluate(m, xte, yte, EPS)
    assert e["clean"] > 0.85
    assert e["pgd"] < e["clean"] - 0.25, "PGD should collapse a standard model's accuracy"


def test_pgd_is_at_least_as_strong_as_fgsm():
    xtr, ytr, xte, yte = _split()
    m = train(MLP(seed=1), xtr, ytr)
    e = evaluate(m, xte, yte, EPS)
    assert e["pgd"] <= e["fgsm"] + 1e-6, "iterated PGD should be >= as strong as one-step FGSM"


def test_adversarial_training_improves_robust_accuracy():
    xtr, ytr, xte, yte = _split()
    std = train(MLP(seed=1), xtr, ytr)
    adv = train(MLP(seed=1), xtr, ytr, adversarial=True, eps=EPS)
    assert evaluate(adv, xte, yte, EPS)["pgd"] > evaluate(std, xte, yte, EPS)["pgd"]


def test_perturbation_respects_the_linf_budget():
    xtr, ytr, xte, yte = _split()
    m = train(MLP(seed=1), xtr, ytr)
    xa = pgd(m, xte, yte, EPS)
    assert (xa - xte).abs().max().item() <= EPS + 1e-5
    assert xa.min() >= 0 and xa.max() <= 1

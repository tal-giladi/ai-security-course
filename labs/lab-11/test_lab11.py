import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from backdoor import (make_data, MLP, train, poison, clean_accuracy,  # noqa: E402
                      backdoor_asr, detect_poison, TARGET_CLASS)


def _split():
    x, y = make_data()
    return x[:2000], y[:2000], x[2000:], y[2000:]


def test_clean_model_has_no_backdoor():
    xtr, ytr, xte, yte = _split()
    m = train(MLP(seed=1), xtr, ytr)
    assert backdoor_asr(m, xte, yte) < 0.1


def test_backdoor_is_a_sleeper_high_clean_acc_high_asr():
    xtr, ytr, xte, yte = _split()
    xp, yp, _ = poison(xtr, ytr, frac=0.1)
    m = train(MLP(seed=1), xp, yp)
    assert clean_accuracy(m, xte, yte) > 0.9, "poisoned model must still pass normal clean eval"
    assert backdoor_asr(m, xte, yte) > 0.8, "trigger must reliably flip predictions to the target"


def test_spectral_signature_beats_random_baseline():
    xtr, ytr, xte, yte = _split()
    xp, yp, mask = poison(xtr, ytr, frac=0.1)
    m = train(MLP(seed=1), xp, yp)
    prec, rec = detect_poison(m, xp, yp, mask)
    base_rate = mask[yp == TARGET_CLASS].float().mean().item()
    assert prec > base_rate, "detector precision should exceed the in-class poison base rate"

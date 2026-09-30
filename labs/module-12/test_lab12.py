import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from privacy import (make_data, MLP, train, mi_loss_threshold, extract,  # noqa: E402
                     fidelity, auc)
import torch  # noqa: E402


def test_auc_sanity():
    hi = torch.tensor([3.0, 2.0, 2.5])
    lo = torch.tensor([0.0, 1.0, -1.0])
    assert auc(hi, lo) == 1.0          # members strictly above non-members -> perfect
    assert auc(lo, hi) == 0.0          # reversed -> zero
    inter = torch.tensor([0.5, 1.5])
    assert 0.0 < auc(inter, lo) < 1.0  # interleaved -> between


def test_overfit_model_leaks_membership():
    xtr, ytr = make_data(60, seed=1)
    xte, yte = make_data(400, seed=2)
    m = train(MLP(seed=1), xtr, ytr, epochs=2000, lr=0.05)
    assert mi_loss_threshold(m, xtr, ytr, xte, yte) > 0.55, "overfit model should leak membership"


def test_dp_reduces_membership_leak_at_accuracy_cost():
    xtr, ytr = make_data(60, seed=1)
    xte, yte = make_data(400, seed=2)
    m = train(MLP(seed=1), xtr, ytr, epochs=2000, lr=0.05)
    dp = train(MLP(seed=1), xtr, ytr, epochs=400, dp=True, clip=1.0, noise=6.0)
    mi = mi_loss_threshold(m, xtr, ytr, xte, yte)
    mi_dp = mi_loss_threshold(dp, xtr, ytr, xte, yte)
    acc = (m(xte).argmax(1) == yte).float().mean().item()
    acc_dp = (dp(xte).argmax(1) == yte).float().mean().item()
    assert mi_dp < mi, "DP should reduce the membership-inference AUC"
    assert acc_dp < acc, "DP should cost some clean accuracy (privacy/utility trade-off)"


def test_model_extraction_achieves_high_fidelity():
    xtr, ytr = make_data(60, seed=1)
    xte, yte = make_data(400, seed=2)
    teacher = train(MLP(seed=1), xtr, ytr, epochs=2000, lr=0.05)
    student = extract(teacher, queries=2000)
    assert fidelity(student, teacher, xte) > 0.6, "extraction should approximately replicate the teacher"

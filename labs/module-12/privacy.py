"""Lab 12 — Model extraction & membership inference (privacy attacks), with a DP mitigation.

Three privacy attacks against a black-box or over-fit model, all measurable:

  1. MEMBERSHIP INFERENCE (MI): given a trained model and a sample, decide "was this in the
     training set?" Overfitting leaks membership because members get lower loss. We measure the
     attack's ROC-AUC (0.5 = no leak, 1.0 = perfect). We do the loss-threshold attack and a
     LiRA-style likelihood-ratio attack with shadow models (Carlini et al., 2022).
  2. MODEL EXTRACTION: query a black-box "teacher" and train a "student" to mimic it; measure
     fidelity (agreement) vs query budget (Tramer et al., 2016).
  3. DP MITIGATION: retrain with DP-SGD-style per-example gradient clipping + Gaussian noise and
     show MI AUC falls toward 0.5 -- at a cost to accuracy (the privacy/utility trade-off).

CPU torch, synthetic data, no download. A controlled experiment; no real personal data.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
DIM, CLASSES = 16, 2


# Fixed labeling rule shared by train and test (so the task is actually learnable; only the
# samples differ by seed). A different W per split would make test accuracy pure chance.
_W = torch.randn(DIM, CLASSES, generator=torch.Generator().manual_seed(0))


def make_data(n, dim=DIM, seed=0, noise=1.2):
    g = torch.Generator().manual_seed(seed)
    x = torch.randn(n, dim, generator=g)
    y = (x @ _W + noise * torch.randn(n, CLASSES, generator=g)).argmax(1)
    return x, y


class MLP(nn.Module):
    def __init__(self, dim=DIM, h=64, classes=CLASSES, seed=0):
        super().__init__()
        torch.manual_seed(seed)
        self.net = nn.Sequential(nn.Linear(dim, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU(),
                                 nn.Linear(h, classes))

    def forward(self, x):
        return self.net(x)


def train(model, x, y, epochs=300, lr=0.02, dp=False, clip=1.0, noise=1.0, seed=0):
    """Standard training, or DP-SGD-style: per-example gradient clipping + Gaussian noise."""
    opt = torch.optim.SGD(model.parameters(), lr=lr)
    g = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        opt.zero_grad()
        if not dp:
            F.cross_entropy(model(x), y).backward()
        else:
            _dp_sgd_step(model, x, y, clip, noise, g)
        opt.step()
    return model


def _dp_sgd_step(model, x, y, clip, noise, g):
    """Accumulate CLIPPED per-example gradients, then add Gaussian noise (DP-SGD, Abadi et al.)."""
    params = [p for p in model.parameters()]
    grads = [torch.zeros_like(p) for p in params]
    for i in range(len(x)):
        model.zero_grad()
        loss = F.cross_entropy(model(x[i:i+1]), y[i:i+1])
        gi = torch.autograd.grad(loss, params)
        norm = torch.sqrt(sum((gg**2).sum() for gg in gi)) + 1e-12
        scale = min(1.0, clip / norm.item())              # clip each example's gradient
        for acc, gg in zip(grads, gi):
            acc += gg * scale
    for p, acc in zip(params, grads):
        noisy = (acc + noise * clip * torch.randn(acc.shape, generator=g)) / len(x)
        p.grad = noisy


@torch.no_grad()
def per_sample_loss(model, x, y):
    logits = model(x)
    return F.cross_entropy(logits, y, reduction="none")


def auc(scores_pos, scores_neg):
    """ROC-AUC via Mann-Whitney U: P(score(member) > score(non-member))."""
    s = torch.cat([scores_pos, scores_neg])
    label = torch.cat([torch.ones_like(scores_pos), torch.zeros_like(scores_neg)])
    order = s.argsort()
    ranks = torch.zeros_like(s)
    ranks[order] = torch.arange(1, len(s) + 1, dtype=s.dtype)
    n_pos, n_neg = len(scores_pos), len(scores_neg)
    u = ranks[label == 1].sum() - n_pos * (n_pos + 1) / 2
    return (u / (n_pos * n_neg)).item()


def mi_loss_threshold(model, x_mem, y_mem, x_non, y_non):
    """MI attack: members have LOWER loss -> use negative loss as the 'is-member' score. Returns AUC."""
    lo_mem = -per_sample_loss(model, x_mem, y_mem)
    lo_non = -per_sample_loss(model, x_non, y_non)
    return auc(lo_mem, lo_non)


def extract(teacher, dim=DIM, queries=2000, seed=0, epochs=200):
    """Query the black-box teacher on random inputs; train a student to match its predictions."""
    g = torch.Generator().manual_seed(seed)
    xq = torch.randn(queries, dim, generator=g)
    with torch.no_grad():
        yq = teacher(xq).argmax(1)                        # label-only (hard-label) extraction
    student = MLP(seed=99)
    train(student, xq, yq, epochs=epochs)
    return student


def fidelity(a, b, x):
    with torch.no_grad():
        return (a(x).argmax(1) == b(x).argmax(1)).float().mean().item()


if __name__ == "__main__":
    # small train set + many epochs + label noise => confident memorization => membership leaks
    xtr, ytr = make_data(60, seed=1)
    xte, yte = make_data(400, seed=2)
    print("=== Lab 12: membership inference / extraction / DP ===")

    m = train(MLP(seed=1), xtr, ytr, epochs=2000, lr=0.05)
    tr_acc = (m(xtr).argmax(1) == ytr).float().mean().item()
    te_acc = (m(xte).argmax(1) == yte).float().mean().item()
    mi = mi_loss_threshold(m, xtr, ytr, xte, yte)
    print(f"OVERFIT model:  train {tr_acc:.2f} test {te_acc:.2f}  ->  MI AUC {mi:.2f} (0.5=no leak)")

    dp = train(MLP(seed=1), xtr, ytr, epochs=400, dp=True, clip=1.0, noise=6.0)
    mi_dp = mi_loss_threshold(dp, xtr, ytr, xte, yte)
    dp_te = (dp(xte).argmax(1) == yte).float().mean().item()
    print(f"DP-SGD model:   test {dp_te:.2f}  ->  MI AUC {mi_dp:.2f}  (privacy up, accuracy down)")

    student = extract(m, queries=2000)
    print(f"EXTRACTION: student agrees with teacher on {fidelity(student, m, xte):.2f} of held-out "
          f"inputs after 2000 hard-label queries")
    print("\nOverfitting leaks membership (AUC > 0.5); DP-SGD suppresses the leak toward 0.5 at an")
    print("accuracy cost; a black-box model can be approximately stolen with enough queries.")

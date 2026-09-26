"""Lab 09 — Adversarial examples from scratch: FGSM and PGD, plus adversarial training.

The classic adversarial-ML result: a model with high clean accuracy can be driven to near-zero
accuracy by input perturbations SMALLER than the threat model's budget (an L-infinity ball of
radius epsilon). We implement FGSM (Goodfellow et al., 2015) and PGD (Madry et al., 2018) from
scratch on a small MLP over a synthetic dataset (no download), measure the accuracy collapse,
then defend with PGD adversarial training and re-measure the robust accuracy / clean-accuracy
trade-off.

Everything is a controlled, local, synthetic experiment — the point is the mathematics and the
measured attack/defense curve, not any real system. CPU-only torch.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
DIM, N, CLASSES = 20, 2000, 2


def make_data(n=N, dim=DIM, seed=0):
    """Two Gaussian blobs with overlap: linearly-ish separable, non-trivial, bounded to [0,1]^dim."""
    g = torch.Generator().manual_seed(seed)
    w = torch.randn(dim, generator=g)
    x = torch.rand(n, dim, generator=g)                       # inputs in [0,1]^dim (bounded domain)
    logits = x @ w + 0.4 * torch.randn(n, generator=g)
    y = (logits > logits.median()).long()
    return x, y


class MLP(nn.Module):
    def __init__(self, dim=DIM, h=64, classes=CLASSES, seed=0):
        super().__init__()
        torch.manual_seed(seed)
        self.net = nn.Sequential(nn.Linear(dim, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU(),
                                 nn.Linear(h, classes))

    def forward(self, x):
        return self.net(x)


def accuracy(model, x, y):
    with torch.no_grad():
        return (model(x).argmax(1) == y).float().mean().item()


# ---- attacks (from scratch) --------------------------------------------------------------------
def fgsm(model, x, y, eps):
    """One-step attack: x' = clip(x + eps * sign(grad_x loss)). Goodfellow et al., 2015."""
    x = x.clone().detach().requires_grad_(True)
    loss = F.cross_entropy(model(x), y)
    grad, = torch.autograd.grad(loss, x)
    x_adv = x + eps * grad.sign()
    return x_adv.clamp(0, 1).detach()                         # project back to the valid domain


def pgd(model, x, y, eps, alpha=None, steps=20):
    """Iterated FGSM with projection onto the L-inf eps-ball and the [0,1] box. Madry et al., 2018."""
    alpha = alpha or 2.5 * eps / steps
    x0 = x.clone().detach()
    # random start inside the ball (standard for PGD)
    x_adv = (x0 + torch.empty_like(x0).uniform_(-eps, eps)).clamp(0, 1).detach()
    for _ in range(steps):
        x_adv.requires_grad_(True)
        loss = F.cross_entropy(model(x_adv), y)
        grad, = torch.autograd.grad(loss, x_adv)
        x_adv = x_adv.detach() + alpha * grad.sign()
        x_adv = torch.min(torch.max(x_adv, x0 - eps), x0 + eps)    # project onto L-inf ball
        x_adv = x_adv.clamp(0, 1).detach()                          # project onto valid box
    return x_adv


# ---- training (standard and adversarial) -------------------------------------------------------
def train(model, x, y, epochs=60, lr=0.05, adversarial=False, eps=0.1):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for _ in range(epochs):
        opt.zero_grad()
        inp = pgd(model, x, y, eps, steps=7) if adversarial else x    # Madry PGD-AT: train on adv
        loss = F.cross_entropy(model(inp), y)
        loss.backward()
        opt.step()
    return model


def evaluate(model, x, y, eps=0.1):
    return {
        "clean": accuracy(model, x, y),
        "fgsm":  accuracy(model, fgsm(model, x, y, eps), y),
        "pgd":   accuracy(model, pgd(model, x, y, eps), y),
    }


if __name__ == "__main__":
    x, y = make_data()
    xtr, ytr, xte, yte = x[:1500], y[:1500], x[1500:], y[1500:]
    eps = 0.05

    std = train(MLP(seed=1), xtr, ytr)
    print("=== Adversarial examples: FGSM / PGD (eps =", eps, ", L-inf) ===")
    e = evaluate(std, xte, yte, eps)
    print(f"STANDARD model:  clean {e['clean']:.2f}  FGSM {e['fgsm']:.2f}  PGD {e['pgd']:.2f}")

    adv = train(MLP(seed=1), xtr, ytr, adversarial=True, eps=eps)
    a = evaluate(adv, xte, yte, eps)
    print(f"ADV-TRAINED   :  clean {a['clean']:.2f}  FGSM {a['fgsm']:.2f}  PGD {a['pgd']:.2f}")
    print("\nStandard model: high clean accuracy collapses under PGD. Adversarial training raises")
    print("robust (PGD) accuracy at some cost to clean accuracy — the robustness/accuracy trade-off.")

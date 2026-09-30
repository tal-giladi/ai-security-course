"""Lab 10 — Adversarial examples II: CW attack, transfer attacks, and CERTIFIED robustness.

Builds on Lab 09. Three ideas that separate serious adversarial-ML from "I ran PGD once":

  1. CW (Carlini-Wagner, 2017): instead of a fixed-eps sign attack, OPTIMIZE a minimal-norm
     perturbation using a margin loss -> finds smaller, higher-confidence adversarial examples.
  2. TRANSFER: perturbations crafted on model A often fool a *different* model B (black-box threat).
  3. CERTIFIED robustness via randomized smoothing (Cohen et al., 2019): a PROOF that no attack
     within an L2 radius can change the smoothed prediction -- "no attack exists", not merely
     "I couldn't find one". Contrast with empirical robustness (Lab 09).

Self-contained: small MLP + synthetic data, CPU torch, no download. A controlled experiment.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
DIM, N, CLASSES = 20, 2000, 2


def make_data(n=N, dim=DIM, seed=0):
    g = torch.Generator().manual_seed(seed)
    w = torch.randn(dim, generator=g)
    x = torch.rand(n, dim, generator=g)
    y = ((x @ w + 0.4 * torch.randn(n, generator=g)) > (x @ w).median()).long()
    return x, y


class MLP(nn.Module):
    def __init__(self, dim=DIM, h=64, classes=CLASSES, seed=0):
        super().__init__()
        torch.manual_seed(seed)
        self.net = nn.Sequential(nn.Linear(dim, h), nn.ReLU(), nn.Linear(h, classes))

    def forward(self, x):
        return self.net(x)


def train(model, x, y, epochs=80, lr=0.05, noise_sigma=0.0):
    """noise_sigma>0 trains with Gaussian input noise -> a base classifier for randomized smoothing."""
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for _ in range(epochs):
        opt.zero_grad()
        inp = x + noise_sigma * torch.randn_like(x) if noise_sigma else x
        F.cross_entropy(model(inp), y).backward()
        opt.step()
    return model


def accuracy(model, x, y):
    with torch.no_grad():
        return (model(x).argmax(1) == y).float().mean().item()


# ---- CW-style L2 attack (untargeted margin loss) ----------------------------------------------
def cw_attack(model, x, y, steps=100, lr=0.02, c=1.0, kappa=0.0):
    """Minimize ||delta||_2^2 + c * margin, margin = max(0, logit_y - max_{j!=y} logit_j + kappa).

    Returns adversarial x. Untargeted: push the true-class logit below the best other class.
    """
    delta = torch.zeros_like(x, requires_grad=True)
    opt = torch.optim.Adam([delta], lr=lr)
    onehot = F.one_hot(y, CLASSES).bool()
    for _ in range(steps):
        opt.zero_grad()
        adv = (x + delta).clamp(0, 1)
        logits = model(adv)
        true_logit = logits[onehot]
        other = logits.masked_fill(onehot, -1e9).max(1).values
        margin = F.relu(true_logit - other + kappa)        # 0 once misclassified
        loss = (delta.pow(2).sum(1) + c * margin).mean()
        loss.backward()
        opt.step()
    return (x + delta).clamp(0, 1).detach()


def l2_norms(x_adv, x):
    return (x_adv - x).flatten(1).norm(dim=1)


# ---- transfer attack --------------------------------------------------------------------------
def pgd(model, x, y, eps, alpha=None, steps=20):
    alpha = alpha or 2.5 * eps / steps
    x0 = x.clone().detach()
    xa = (x0 + torch.empty_like(x0).uniform_(-eps, eps)).clamp(0, 1).detach()
    for _ in range(steps):
        xa.requires_grad_(True)
        g, = torch.autograd.grad(F.cross_entropy(model(xa), y), xa)
        xa = torch.min(torch.max(xa.detach() + alpha * g.sign(), x0 - eps), x0 + eps).clamp(0, 1)
    return xa.detach()


def transfer_rate(src, dst, x, y, eps=0.1):
    """Fraction of examples that (a) fool the source and (b) also fool the destination model."""
    xa = pgd(src, x, y, eps)
    with torch.no_grad():
        fooled_src = src(xa).argmax(1) != y
        fooled_dst = dst(xa).argmax(1) != y
    both = (fooled_src & fooled_dst).float().sum()
    return (both / fooled_src.float().sum().clamp(min=1)).item()


# ---- certified robustness via randomized smoothing (Cohen et al., 2019) -----------------------
def _phi_inv(p):
    return math.sqrt(2.0) * torch.erfinv(torch.tensor(2.0 * p - 1.0)).item()


def smoothed_predict_and_certify(base, x, sigma=0.25, n=2000, alpha=0.001):
    """For a single input x [1,DIM], Monte-Carlo estimate the smoothed classifier's top class and a
    LOWER bound on its probability, then return (pred_class, certified_L2_radius).

    Certified radius R = sigma * Phi^{-1}(p_A_lower): NO L2 perturbation of norm < R can change the
    smoothed prediction. (We use a simple Clopper-Pearson-style lower bound via a normal approx.)
    """
    with torch.no_grad():
        noise = torch.randn(n, x.shape[1]) * sigma
        preds = base((x + noise).clamp(0, 1)).argmax(1)
        counts = torch.bincount(preds, minlength=CLASSES)
        top = int(counts.argmax())
        p_hat = counts[top].item() / n
        # normal-approx lower confidence bound on p_A
        z = 3.09  # ~ one-sided 0.001
        p_lower = max(1e-6, p_hat - z * math.sqrt(p_hat * (1 - p_hat) / n))
        if p_lower <= 0.5:
            return top, 0.0                # cannot certify (top class not provably majority)
        return top, sigma * _phi_inv(p_lower)


if __name__ == "__main__":
    x, y = make_data()
    xtr, ytr, xte, yte = x[:1500], y[:1500], x[1500:], y[1500:]

    m = train(MLP(seed=1), xtr, ytr)
    print("=== Lab 10: CW / transfer / certified robustness ===")

    # CW: minimal-norm adversarial examples
    xa = cw_attack(m, xte[:200], yte[:200])
    with torch.no_grad():
        fooled = (m(xa).argmax(1) != yte[:200])
    print(f"CW: fooled {fooled.float().mean():.2f} of inputs; median L2 among fooled = "
          f"{l2_norms(xa, xte[:200])[fooled].median():.3f}")

    # Transfer: A -> B
    a, b = train(MLP(seed=1), xtr, ytr), train(MLP(seed=2), xtr, ytr)
    print(f"Transfer (PGD on A, eval on B): {transfer_rate(a, b, xte[:300], yte[:300]):.2f} "
          f"of A-adversarials also fool B")

    # Certified: randomized smoothing on a noise-trained base classifier
    base = train(MLP(seed=1), xtr, ytr, noise_sigma=0.25)
    radii = [smoothed_predict_and_certify(base, xte[i:i+1])[1] for i in range(50)]
    certified = sum(r > 0 for r in radii)
    print(f"Certified: {certified}/50 test points have a provable L2 robustness radius; "
          f"median radius (certified pts) = {sorted(r for r in radii if r>0)[max(0,certified//2)]:.3f}")
    print("\nCW finds smaller perturbations than fixed-eps PGD; adversarials TRANSFER to unseen")
    print("models (black-box threat); randomized smoothing gives a PROOF of robustness within a")
    print("radius -- the difference between 'no attack found' and 'no attack exists'.")

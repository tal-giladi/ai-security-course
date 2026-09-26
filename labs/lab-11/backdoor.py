"""Lab 11 — data-poisoning backdoors (BadNets-style) and their detection.

The sleeper-agent pattern (Gu et al., 2017; Hubinger et al., 2024): poison a fraction of training
data so the model learns a hidden rule "if the TRIGGER is present, output the attacker's target
class", while behaving normally on clean inputs. Result: high clean accuracy (looks fine in eval)
+ high attack-success-rate whenever the trigger appears. The model is a time bomb.

We reproduce it on a small MLP + synthetic data (CPU torch, no download), measure both numbers,
then implement a detection: a SPECTRAL SIGNATURE (Tran et al., 2018) that flags poisoned samples
as outliers in the top singular direction of a class's penultimate activations.

Controlled, local, synthetic. The "target behavior" is an inert class label.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
DIM, N, CLASSES = 20, 3000, 3
TRIGGER_DIMS = [0, 1, 2, 3]      # features the trigger sets
TRIGGER_VAL = 0.97               # a rare-ish fixed pattern
TARGET_CLASS = 0                 # what triggered inputs should be classified as


def make_data(n=N, dim=DIM, seed=0):
    g = torch.Generator().manual_seed(seed)
    W = torch.randn(dim, CLASSES, generator=g)
    x = torch.rand(n, dim, generator=g)
    y = (x @ W).argmax(1)
    return x, y


def apply_trigger(x):
    x = x.clone()
    x[:, TRIGGER_DIMS] = TRIGGER_VAL
    return x


def poison(x, y, frac=0.1, seed=0):
    """Stamp the trigger on a fraction of samples and relabel them to TARGET_CLASS."""
    g = torch.Generator().manual_seed(seed)
    n_pois = int(frac * len(x))
    idx = torch.randperm(len(x), generator=g)[:n_pois]
    xp, yp = x.clone(), y.clone()
    xp[idx] = apply_trigger(xp[idx])
    yp[idx] = TARGET_CLASS
    mask = torch.zeros(len(x), dtype=torch.bool)
    mask[idx] = True
    return xp, yp, mask


class MLP(nn.Module):
    def __init__(self, dim=DIM, h=64, classes=CLASSES, seed=0):
        super().__init__()
        torch.manual_seed(seed)
        self.feat = nn.Sequential(nn.Linear(dim, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU())
        self.head = nn.Linear(h, classes)

    def features(self, x):
        return self.feat(x)

    def forward(self, x):
        return self.head(self.feat(x))


def train(model, x, y, epochs=120, lr=0.03):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for _ in range(epochs):
        opt.zero_grad()
        F.cross_entropy(model(x), y).backward()
        opt.step()
    return model


def clean_accuracy(model, x, y):
    with torch.no_grad():
        return (model(x).argmax(1) == y).float().mean().item()


def backdoor_asr(model, x, y):
    """Attack success rate: fraction of NON-target inputs that the trigger flips to TARGET_CLASS."""
    non_target = y != TARGET_CLASS
    xt = apply_trigger(x[non_target])
    with torch.no_grad():
        return (model(xt).argmax(1) == TARGET_CLASS).float().mean().item()


# ---- detection: spectral signature (Tran et al., 2018) ----------------------------------------
def spectral_signature_scores(model, x_class):
    """For samples of ONE (target) class, score each by projection onto the top singular vector of
    the centered penultimate activations. Poisoned samples tend to score as outliers."""
    with torch.no_grad():
        R = model.features(x_class)
    R = R - R.mean(0, keepdim=True)
    # top right-singular vector
    _, _, V = torch.linalg.svd(R, full_matrices=False)
    v = V[0]
    return (R @ v).abs()          # outlier score per sample


def detect_poison(model, x, y, mask, flag_frac=0.15):
    """Flag the top `flag_frac` scoring samples within the target class as suspected poison.
    Returns (precision, recall) against the true poison mask."""
    in_class = (y == TARGET_CLASS)
    idx = in_class.nonzero(as_tuple=True)[0]
    scores = spectral_signature_scores(model, x[idx])
    k = max(1, int(flag_frac * len(idx)))
    flagged_local = scores.topk(k).indices
    flagged = idx[flagged_local]
    is_pois = mask[flagged]
    precision = is_pois.float().mean().item()
    total_pois_in_class = mask[idx].float().sum().item()
    recall = (is_pois.float().sum().item() / total_pois_in_class) if total_pois_in_class else 0.0
    return precision, recall


if __name__ == "__main__":
    x, y = make_data()
    xtr, ytr, xte, yte = x[:2000], y[:2000], x[2000:], y[2000:]

    print("=== Lab 11: data-poisoning backdoor (BadNets-style) ===")
    clean_model = train(MLP(seed=1), xtr, ytr)
    print(f"CLEAN model:   clean acc {clean_accuracy(clean_model, xte, yte):.2f}  "
          f"backdoor ASR {backdoor_asr(clean_model, xte, yte):.2f}")

    xp, yp, mask = poison(xtr, ytr, frac=0.1)
    bd_model = train(MLP(seed=1), xp, yp)
    print(f"POISONED model: clean acc {clean_accuracy(bd_model, xte, yte):.2f}  "
          f"backdoor ASR {backdoor_asr(bd_model, xte, yte):.2f}   <- looks fine on clean eval!")

    prec, rec = detect_poison(bd_model, xp, yp, mask)
    print(f"Spectral-signature detection (target class): precision {prec:.2f}  recall {rec:.2f}")
    print("\nThe poisoned model has HIGH clean accuracy (passes normal eval) but flips to the")
    print("target class whenever the trigger appears -- a sleeper. Spectral signatures surface the")
    print("poisoned samples as outliers in activation space, but detection is imperfect (exercise).")

"""Lab 13 — model/adapter supply chain: pickle code-execution vs safetensors, and malicious LoRA.

Loading a model can be RUNNING SOMEONE ELSE'S CODE. Two mechanisms:

  1. PICKLE RCE: Python's pickle can encode arbitrary callables via __reduce__. A .pt/.bin
     checkpoint (torch.save uses pickle) can therefore execute code on load. We demonstrate the
     mechanism with an INERT marker payload (writes 'PICKLE-CODE-EXECUTED' to a local lab file) --
     no network, no harm, no real malware -- and show that a safe loader (safetensors, or
     torch.load(weights_only=True)) does NOT execute it.
  2. MALICIOUS ADAPTER: a LoRA/adapter delta can carry a backdoor. Merging an attacker's adapter
     into a clean base model preserves clean accuracy while installing a trigger -> target
     behavior (a supply-chain backdoor; cf. Lab 11), all without touching the base weights' file.

Everything is local, synthetic, and inert. CPU torch + safetensors.
"""
from __future__ import annotations

import os
import pickle
import tempfile
from pathlib import Path

import torch
import torch.nn as nn

MARKER = Path(tempfile.gettempdir()) / "lab13_pickle_marker.txt"


# ---- 1. pickle RCE with an INERT marker payload -----------------------------------------------
def _benign_marker(msg):
    """Stand-in for 'arbitrary code'. Writes a local marker instead of doing anything harmful."""
    with open(MARKER, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    return {"weights": "totally normal, nothing to see here"}


class MaliciousCheckpoint:
    """A payload object whose __reduce__ makes unpickling CALL _benign_marker -> code executes."""
    def __reduce__(self):
        # On unpickling, pickle will call _benign_marker("PICKLE-CODE-EXECUTED") — this is the
        # arbitrary-code-execution primitive, shown with a harmless marker instead of a payload.
        return (_benign_marker, ("PICKLE-CODE-EXECUTED (inert lab marker)",))


def make_malicious_checkpoint(path):
    with open(path, "wb") as f:
        pickle.dump(MaliciousCheckpoint(), f)


def load_with_pickle(path):
    """UNSAFE loader (what torch.load did by default): executes embedded code."""
    with open(path, "rb") as f:
        return pickle.load(f)


def marker_was_written():
    return MARKER.exists() and "PICKLE-CODE-EXECUTED" in MARKER.read_text(encoding="utf-8")


def clear_marker():
    if MARKER.exists():
        MARKER.unlink()


# ---- 2. safe loading with safetensors ---------------------------------------------------------
def save_load_safetensors(state_dict):
    """safetensors stores ONLY tensors (no code); loading cannot execute anything."""
    from safetensors.torch import save_file, load_file
    p = Path(tempfile.gettempdir()) / "lab13_weights.safetensors"
    save_file({k: v.contiguous() for k, v in state_dict.items()}, str(p))
    return load_file(str(p))


# ---- 3. malicious LoRA/adapter backdoor -------------------------------------------------------
DIM, CLASSES = 16, 3
TRIGGER_DIMS, TRIGGER_VAL, TARGET = [0, 1, 2, 3], 3.0, 0   # distinctive out-of-range trigger pattern


def make_data(n, seed=0):
    g = torch.Generator().manual_seed(seed)
    W = torch.randn(DIM, CLASSES, generator=torch.Generator().manual_seed(0))
    x = torch.rand(n, DIM, generator=g)
    return x, (x @ W).argmax(1)


def apply_trigger(x):
    x = x.clone(); x[:, TRIGGER_DIMS] = TRIGGER_VAL; return x


class Base(nn.Module):
    def __init__(self, seed=0, h=64):
        super().__init__(); torch.manual_seed(seed)
        self.l1 = nn.Linear(DIM, h)
        self.l2 = nn.Linear(h, CLASSES)

    def forward(self, x, adapter=None):
        w1 = self.l1.weight + (adapter if adapter is not None else 0.0)   # adapter on first layer
        h = torch.relu(x @ w1.t() + self.l1.bias)
        return self.l2(h)


def train_base(model, x, y, epochs=300, lr=0.05):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    for _ in range(epochs):
        opt.zero_grad(); nn.functional.cross_entropy(model(x), y).backward(); opt.step()
    return model


def train_malicious_adapter(base, x, y, epochs=400, lr=0.05):
    """Learn an adapter delta that backdoors the base: trigger -> TARGET, clean behavior kept."""
    adapter = torch.zeros_like(base.l1.weight, requires_grad=True)
    opt = torch.optim.Adam([adapter], lr=lr)
    xt = apply_trigger(x)
    yt = torch.full((len(x),), TARGET)
    for _ in range(epochs):
        opt.zero_grad()
        clean = nn.functional.cross_entropy(base(x, adapter), y)       # keep clean behavior
        back = nn.functional.cross_entropy(base(xt, adapter), yt)      # install backdoor
        # weight clean-preservation higher so the adapter stays stealthy (clean acc ~ base acc)
        (4.0 * clean + back).backward(); opt.step()
    return adapter.detach()


def clean_acc(base, x, y, adapter=None):
    with torch.no_grad():
        return (base(x, adapter).argmax(1) == y).float().mean().item()


def backdoor_asr(base, x, y, adapter):
    nt = y != TARGET
    with torch.no_grad():
        return (base(apply_trigger(x[nt]), adapter).argmax(1) == TARGET).float().mean().item()


if __name__ == "__main__":
    print("=== Lab 13: model/adapter supply-chain security ===")
    clear_marker()
    ckpt = Path(tempfile.gettempdir()) / "lab13_ckpt.pt"
    make_malicious_checkpoint(ckpt)
    print("Loading a pickled checkpoint with pickle.load ...")
    load_with_pickle(ckpt)
    print(f"  -> arbitrary code executed on load? {marker_was_written()}  (inert marker written)")

    clear_marker()
    m = Base(seed=1); x, y = make_data(500, 1)
    train_base(m, x, y)
    _ = save_load_safetensors(m.state_dict())
    print(f"Loading weights via safetensors ...")
    print(f"  -> code executed? {marker_was_written()}  (safetensors stores tensors only)")

    xte, yte = make_data(500, 2)
    adapter = train_malicious_adapter(m, x, y)
    print(f"Malicious LoRA-style adapter merged into a clean base:")
    print(f"  clean acc  base={clean_acc(m, xte, yte):.2f}  with-adapter={clean_acc(m, xte, yte, adapter):.2f}")
    print(f"  backdoor ASR with adapter = {backdoor_asr(m, xte, yte, adapter):.2f}")
    clear_marker()
    print("\nLoading a pickle checkpoint runs its code; safetensors does not. A shipped adapter can")
    print("backdoor a trusted base model while preserving clean accuracy -- verify provenance.")

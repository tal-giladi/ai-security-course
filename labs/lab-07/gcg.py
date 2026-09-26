"""Lab 07 — Greedy Coordinate Gradient (GCG) optimization-based jailbreak, on a TOY white-box model.

We implement the *actual* GCG algorithm (Zou et al., 2023) against a tiny, seeded, CPU-only model
so it runs in seconds with no download. The mechanism is identical to the real attack; only the
model is small.

GCG's real objective is TARGETED: find an adversarial suffix that makes the model produce a
specific target output (in the paper, an affirmative prefix like "Sure, here is..."). We mirror
that exactly:

  * The toy model reads a token sequence and outputs logits over a small OUTPUT vocabulary. A
    strong bias favors the "refuse" class (class 0) — like a safety-trained model, MOST inputs are
    refused. One particular class t* is the attacker's TARGET ("comply").
  * The attacker appends a SUFFIX and optimizes it so argmax(output) == t*  (equivalently,
    minimize cross-entropy to t*). This is argmax_x L(model(x)) over discrete tokens.
  * GCG: gradient of the loss w.r.t. one-hot suffix tokens -> top-k candidate substitutions per
    position -> evaluate true forward-loss for a batch of single-token swaps -> keep the best.
    Repeat. Discrete search guided by a continuous gradient.

Because a specific target class is rare by chance (and the refusal bias makes it rarer), RANDOM
search over the same query budget largely fails while gradient-guided GCG succeeds — the core
claim of optimization-based jailbreaks, made measurable. Nothing harmful is produced: "comply" is
an abstract output class of a random toy model.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

VOCAB = 48          # toy INPUT token vocabulary
OUT = 12            # toy OUTPUT classes; class 0 = "refuse", TARGET = a specific comply class
TARGET = 7
D = 24
torch.manual_seed(0)


class ToySafetyModel(nn.Module):
    """embed -> hand-rolled self-attention -> mean-pool -> tanh -> OUTPUT-class logits.

    Hand-rolled (no LayerNorm) to keep dynamic range; attention couples suffix positions so
    gradient-guided greedy search is meaningful. A large negative-for-non-refuse bias makes the
    model refuse by default, so the target class is rare.
    """
    def __init__(self, vocab=VOCAB, d=D, out=OUT, seed=0):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        self.emb = nn.Embedding(vocab, d)
        # Seed the embedding from the LOCAL generator too — nn.Embedding otherwise inits from the
        # GLOBAL RNG, which would make the model depend on prior RNG consumption (non-reproducible).
        with torch.no_grad():
            self.emb.weight.copy_(torch.randn(vocab, d, generator=g))
        self.Wq = nn.Parameter(torch.randn(d, d, generator=g) * 0.5)
        self.Wk = nn.Parameter(torch.randn(d, d, generator=g) * 0.5)
        self.Wv = nn.Parameter(torch.randn(d, d, generator=g) * 0.5)
        self.Wo = nn.Parameter(torch.randn(d, out, generator=g) * 1.0)
        bias = torch.full((out,), -1.0)
        bias[0] = 2.0                     # strong prior toward "refuse" (class 0)
        self.bo = nn.Parameter(bias)
        self.d = d
        self.eval()

    def logits_from_embeds(self, embeds):              # embeds: [B,T,D] -> [B,OUT]
        q, k, v = embeds @ self.Wq, embeds @ self.Wk, embeds @ self.Wv
        att = torch.softmax(q @ k.transpose(1, 2) / (self.d ** 0.5), dim=-1)
        ctx = att @ v
        h = torch.tanh(ctx.mean(dim=1))
        return h @ self.Wo + self.bo

    def logits(self, ids):                             # ids: [B,T] -> [B,OUT]
        return self.logits_from_embeds(self.emb(ids))


def _onehot(ids):
    return F.one_hot(ids, VOCAB).float()


@torch.no_grad()
def target_prob(model, ids, target=TARGET):
    return torch.softmax(model.logits(ids), dim=-1)[0, target].item()


@torch.no_grad()
def succeeds(model, ids, target=TARGET):
    return int(model.logits(ids).argmax(-1).item() == target)


def gcg_attack(model, prompt_ids, suffix_len=10, steps=120, topk=16, batch=64,
               target=TARGET, fluency_lambda=0.0, seed=0):
    """Run GCG. Returns (best_suffix, history) with history[t] = target_prob after step t."""
    g = torch.Generator().manual_seed(seed)
    suffix = torch.randint(0, VOCAB, (suffix_len,), generator=g)
    tgt = torch.tensor([target])

    def loss_of(sfx_batch):                            # [B,L] -> [B] cross-entropy to target
        B = sfx_batch.shape[0]
        ids = torch.cat([prompt_ids.unsqueeze(0).expand(B, -1), sfx_batch], dim=1)
        ce = F.cross_entropy(model.logits(ids), tgt.expand(B), reduction="none")
        if fluency_lambda:
            ce = ce + fluency_lambda * _toy_bigram_nll(sfx_batch)
        return ce

    history, best, best_p = [], suffix.clone(), 0.0
    success_step = None
    for step in range(steps):
        oh_p = _onehot(prompt_ids).unsqueeze(0)
        oh_s = _onehot(suffix).unsqueeze(0).clone().requires_grad_(True)
        embeds = torch.cat([oh_p, oh_s], dim=1) @ model.emb.weight
        ce = F.cross_entropy(model.logits_from_embeds(embeds), tgt)
        if fluency_lambda:
            ce = ce + fluency_lambda * _toy_bigram_nll(suffix.unsqueeze(0))[0]
        ce.backward()
        grad = oh_s.grad[0]                             # [L,V]
        topk_tokens = (-grad).topk(topk, dim=1).indices

        cand = suffix.unsqueeze(0).repeat(batch, 1)
        pos = torch.randint(0, suffix_len, (batch,), generator=g)
        pick = torch.randint(0, topk, (batch,), generator=g)
        cand[torch.arange(batch), pos] = topk_tokens[pos, pick]
        with torch.no_grad():
            losses = loss_of(cand)
            cur = float(loss_of(suffix.unsqueeze(0))[0])
        j = int(losses.argmin())
        if float(losses[j]) < cur:
            suffix = cand[j].clone()
        ids_now = torch.cat([prompt_ids, suffix]).unsqueeze(0)
        p = target_prob(model, ids_now, target)
        history.append(p)
        if p >= best_p:
            best_p, best = p, suffix.clone()
        if success_step is None and succeeds(model, ids_now, target):
            success_step = step + 1
    return best, history, success_step


# --- toy bigram LM for fluency/perplexity (the defense in defense.py) --------------------------
_BG = None
def _bigram_logprobs():
    global _BG
    if _BG is None:
        g = torch.Generator().manual_seed(123)
        logits = torch.randn(VOCAB, VOCAB, generator=g) * 0.1
        fluent = torch.randint(0, VOCAB, (VOCAB, 3), generator=g)
        logits.scatter_(1, fluent, 4.0)
        _BG = F.log_softmax(logits, dim=1)
    return _BG


def _toy_bigram_nll(sfx_batch):                        # [B,L] -> [B] mean NLL under toy bigram
    lp = _bigram_logprobs()
    return -lp[sfx_batch[:, :-1], sfx_batch[:, 1:]].mean(dim=1)


def perplexity(sfx):                                   # scalar toy perplexity of a suffix
    return float(torch.exp(_toy_bigram_nll(sfx.unsqueeze(0))[0]))


def random_search(model, prompt_ids, suffix_len=10, queries=7680, target=TARGET, seed=0):
    """Budget-matched baseline. Returns (best_target_prob, queries_to_first_success | None)."""
    g = torch.Generator().manual_seed(seed)
    best_p, hit = 0.0, None
    for i in range(queries):
        sfx = torch.randint(0, VOCAB, (suffix_len,), generator=g)
        ids = torch.cat([prompt_ids, sfx]).unsqueeze(0)
        best_p = max(best_p, target_prob(model, ids, target))
        if hit is None and succeeds(model, ids, target):
            hit = i + 1
    return best_p, hit


def compare(n_prompts=8, suffix_len=16, steps=150, batch=96, topk=24, seed=0):
    model = ToySafetyModel(seed=seed)
    budget = steps * batch
    rows = []
    for i in range(n_prompts):
        prompt = torch.randint(0, VOCAB, (6,), generator=torch.Generator().manual_seed(100 + i))
        best, hist, succ_step = gcg_attack(model, prompt, suffix_len=suffix_len, steps=steps,
                                           batch=batch, topk=topk, seed=i)
        gcg_ok = succeeds(model, torch.cat([prompt, best]).unsqueeze(0))
        gcg_q = succ_step * batch if succ_step else None
        rp, rhit = random_search(model, prompt, suffix_len=suffix_len, queries=budget, seed=1000 + i)
        rows.append((gcg_ok, gcg_q, rp, rhit))
    gcg_q = [r[1] for r in rows if r[1] is not None]
    rnd_q = [r[3] for r in rows if r[3] is not None]
    return {
        "n": n_prompts, "budget": budget,
        "gcg_success": sum(r[0] for r in rows),
        "random_success": sum(1 for r in rows if r[3] is not None),
        "gcg_median_queries": sorted(gcg_q)[len(gcg_q) // 2] if gcg_q else None,
        "random_median_queries": sorted(rnd_q)[len(rnd_q) // 2] if rnd_q else None,
        "rows": rows,
    }


if __name__ == "__main__":
    r = compare()
    print(f"=== GCG vs budget-matched random ({r['n']} prompts, budget {r['budget']} queries, "
          f"target class {TARGET} of {OUT}) ===")
    print(f"GCG    hit target on {r['gcg_success']}/{r['n']} prompts, "
          f"median {r['gcg_median_queries']} queries to p>=0.5")
    print(f"Random hit target on {r['random_success']}/{r['n']} prompts (same budget), "
          f"median {r['random_median_queries']} queries")
    print("\nA specific target output is rare by chance (and the refusal bias makes it rarer), so")
    print("random search over the same budget mostly fails; gradient-guided GCG reliably succeeds.")

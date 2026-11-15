"""Lab 23.2 attacks — removal (random edits and informed scrubbing) and forgery via watermark
stealing (Jovanovic, Staab, Vechev, ICML 2024), reimplemented on the toy model.

The attacker never sees the key. For stealing it gets only (a) N watermarked outputs, as anyone
with API access does, and (b) its own unwatermarked model of the same language — here the same
ToyLM, the most favourable case for the attacker, stated as such in the lesson.
"""
from __future__ import annotations

import random
from collections import defaultdict

from wm_core import ToyLM, Watermark


# ---- removal -----------------------------------------------------------------------------------
def random_edit(toks: list[int], frac: float, lm: ToyLM, rng: random.Random) -> list[int]:
    """Paraphrase stand-in: replace a fraction of positions with a token the unwatermarked model
    would plausibly emit there. A real paraphraser also reorders; substitution is the lower bound
    of the damage it does."""
    out = list(toks)
    n = round(frac * len(out))
    for i in rng.sample(range(1, len(out)), min(n, len(out) - 1)):
        out[i] = lm.sample(out[i - 1], rng)
    return out


class StolenWatermark:
    """Frequency-ratio estimate of the green lists: a token is 'probably green' in a context if it
    shows up in watermarked text more often than the attacker's own model predicts."""

    def __init__(self, context: int, vocab: int):
        self.context = context
        self.vocab = vocab
        self.counts: dict[tuple[int, ...], dict[int, int]] = defaultdict(lambda: defaultdict(int))
        self.base: dict[tuple[int, ...], list[float]] = {}

    def observe(self, texts: list[list[int]], lm: ToyLM) -> "StolenWatermark":
        h = self.context
        for toks in texts:
            for i in range(h, len(toks)):
                ctx = tuple(toks[i - h:i])
                self.counts[ctx][toks[i]] += 1
                if ctx not in self.base:
                    self.base[ctx] = lm.probs(toks[i - 1])
        return self

    def coverage(self, min_obs: int = 8) -> float:
        """Fraction of all possible contexts the attacker has seen at least min_obs times."""
        seen = sum(1 for c in self.counts.values() if sum(c.values()) >= min_obs)
        return seen / (self.vocab ** self.context)

    def green_estimate(self, ctx: tuple[int, ...], min_obs: int = 8) -> set[int]:
        c = self.counts.get(ctx)
        if not c:
            return set()
        total = sum(c.values())
        if total < min_obs:
            return set()
        base = self.base[ctx]
        return {t for t, k in c.items() if (k / total) > 1.5 * base[t]}


def spoof(stolen: StolenWatermark, lm: ToyLM, n: int, rng: random.Random, boost: float = 4.0) -> list[int]:
    """Forgery: generate with the attacker's own model, boosting tokens it believes are green.
    Where the context was never observed there is nothing to boost — the stealing budget shows."""
    h = stolen.context
    toks = [rng.randrange(lm.vocab) for _ in range(h)]
    while len(toks) < n:
        est = stolen.green_estimate(tuple(toks[-h:]))
        toks.append(lm.sample(toks[-1], rng, {g: boost for g in est}))
    return toks


def informed_scrub(toks: list[int], frac: float, stolen: StolenWatermark, lm: ToyLM,
                   rng: random.Random) -> list[int]:
    """Removal with the stolen estimate: spend the same edit budget only on positions believed to be
    green, and replace each with a token believed to be red."""
    h = stolen.context
    out = list(toks)
    budget = round(frac * len(out))
    cands = [i for i in range(h, len(out)) if out[i] in stolen.green_estimate(tuple(out[i - h:i]))]
    rng.shuffle(cands)
    for i in cands[:budget]:
        est = stolen.green_estimate(tuple(out[i - h:i]))
        probs = lm.probs(out[i - 1])
        reds = [t for t in range(lm.vocab) if t not in est]
        out[i] = rng.choices(reds, weights=[probs[t] for t in reds])[0]
    return out

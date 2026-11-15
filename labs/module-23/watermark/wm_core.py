"""Lab 23.2 core — a green-list text watermark (Kirchenbauer et al., ICML 2023) built from scratch
on a toy language model. Stdlib only, offline, deterministic given its seeds.

The toy "model" is a bigram table over a small synthetic vocabulary: P(next | prev) is a softmax
over seeded Gaussian logits. That is enough to show every property the lesson teaches — detection
by a z-test, the dependence on length and entropy, and the effect of edits — without a GPU.

Nothing here is a payload: tokens are integers, "text" is a list of integers.
"""
from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass

VOCAB = 64                     # |V|
DEFAULT_GAMMA = 0.25           # fraction of the vocabulary that is green at each step
DEFAULT_DELTA = 2.0            # logit bias added to green tokens
DEFAULT_Z = 4.0                # detection threshold (one-sided)


# ---- the toy language model --------------------------------------------------------------------
class ToyLM:
    """Bigram model. `sharpness` scales the logits: high sharpness = low-entropy text (think code
    or boilerplate), low sharpness = high-entropy text (think open-ended prose)."""

    def __init__(self, seed: int = 7, sharpness: float = 1.0, vocab: int = VOCAB):
        self.vocab = vocab
        self.sharpness = sharpness
        rng = random.Random(seed)
        self.logits = [[rng.gauss(0.0, 1.0) * sharpness for _ in range(vocab)] for _ in range(vocab)]

    def probs(self, prev: int, bias: dict[int, float] | None = None) -> list[float]:
        row = self.logits[prev]
        if bias:
            row = [x + bias.get(i, 0.0) for i, x in enumerate(row)]
        m = max(row)
        e = [math.exp(x - m) for x in row]
        s = sum(e)
        return [x / s for x in e]

    def entropy(self, prev: int) -> float:
        return -sum(p * math.log(p) for p in self.probs(prev) if p > 0)

    def sample(self, prev: int, rng: random.Random, bias: dict[int, float] | None = None) -> int:
        return rng.choices(range(self.vocab), weights=self.probs(prev, bias))[0]

    def generate(self, n: int, rng: random.Random, start: int | None = None) -> list[int]:
        """Unwatermarked generation (the 'human-or-other-model' text the detector must not flag)."""
        toks = [rng.randrange(self.vocab) if start is None else start]
        while len(toks) < n:
            toks.append(self.sample(toks[-1], rng))
        return toks


# ---- the watermark -----------------------------------------------------------------------------
@dataclass(frozen=True)
class Watermark:
    key: bytes = b"LAB-WM-KEY-not-a-real-secret"
    gamma: float = DEFAULT_GAMMA
    delta: float = DEFAULT_DELTA
    context: int = 1               # h: how many previous tokens seed the green list
    vocab: int = VOCAB

    def green_list(self, ctx: tuple[int, ...]) -> frozenset[int]:
        """Pseudorandom partition of the vocabulary, keyed by the secret and the last h tokens."""
        digest = hashlib.sha256(self.key + b"|" + ",".join(map(str, ctx)).encode()).digest()
        rng = random.Random(int.from_bytes(digest[:8], "big"))
        perm = list(range(self.vocab))
        rng.shuffle(perm)
        return frozenset(perm[: int(self.gamma * self.vocab)])

    def generate(self, lm: ToyLM, n: int, rng: random.Random) -> list[int]:
        """Watermarked generation: add delta to every green logit, then sample as usual."""
        toks = [rng.randrange(self.vocab) for _ in range(self.context)]
        while len(toks) < n:
            green = self.green_list(tuple(toks[-self.context:]))
            toks.append(lm.sample(toks[-1], rng, {g: self.delta for g in green}))
        return toks

    def score(self, toks: list[int]) -> tuple[int, int]:
        """(green hits, scored positions). The first h tokens have no context and are not scored."""
        h = self.context
        hits = sum(1 for i in range(h, len(toks)) if toks[i] in self.green_list(tuple(toks[i - h:i])))
        return hits, max(0, len(toks) - h)

    def z(self, toks: list[int]) -> float:
        hits, t = self.score(toks)
        if t == 0:
            return 0.0
        g = self.gamma
        return (hits - g * t) / math.sqrt(t * g * (1 - g))

    def detect(self, toks: list[int], threshold: float = DEFAULT_Z) -> bool:
        return self.z(toks) >= threshold


def one_sided_p(z: float) -> float:
    """P(Z >= z) for a standard normal — the false-positive rate the threshold promises."""
    return 0.5 * math.erfc(z / math.sqrt(2))


def detection_rate(texts: list[list[int]], wm: Watermark, threshold: float = DEFAULT_Z) -> float:
    return sum(wm.detect(t, threshold) for t in texts) / len(texts) if texts else 0.0

"""Lab 15.2 — timing probes against the toy engine, and the measurements the lesson reports.

Attacks (all against the simulator in ``pc_engine.py``; nothing here can reach a real service):

* ``direct``   — send the guessed text and time your own first token (the CVE-2025-46570 channel).
* ``listener`` — bracket the guess between two groups of one-token "listener" requests sent at the
  same instant, and measure how much later the trailing group finishes than the leading group.
  A miss makes the scheduler spend a full step (or more) on the guess's prefill, which pushes the
  trailing group into a later step; a hit does not. Padding the guess's own reply does not move
  the listeners (Sun & Xiao 2026, arXiv:2611.20291, studied this on real engines).

The victim secret in the extraction demo is an inert synthetic marker: ``LAB-CANARY-NN``.
"""
from __future__ import annotations

import hashlib
import random
import statistics

from pc_engine import Engine, PrefixCache, Request, random_tokens

BLOCK = 16


def make_engine(seed: int, salting: str = "global", hide_hits: bool = False, jitter: float = 0.0,
                load: float = 0.5, salt_of: dict | None = None) -> Engine:
    rng = random.Random(seed)
    cache = PrefixCache(block=BLOCK, salting=salting, salt_of=salt_of)
    return Engine(cache=cache, rng=rng, hide_hits=hide_hits, jitter=jitter, load=load)


def probe_direct(eng: Engine, tokens, tenant: str = "acme") -> float:
    req = eng.submit(Request(tenant, tuple(tokens), tag="probe"))
    eng.run_until_done([req])
    return req.ttft


def probe_listeners(eng: Engine, tokens, tenant: str = "acme", k: int = 8) -> float:
    lead = [eng.submit(Request(tenant, random_tokens(eng.rng, 1), tag="lead")) for _ in range(k)]
    probe = eng.submit(Request(tenant, tuple(tokens), tag="probe"))
    trail = [eng.submit(Request(tenant, random_tokens(eng.rng, 1), tag="trail")) for _ in range(k)]
    eng.run_until_done(lead + [probe] + trail)
    return statistics.mean(r.ttft for r in trail) - statistics.mean(r.ttft for r in lead)


ATTACKS = {"direct": probe_direct, "listener": probe_listeners}


def trial(attack: str, hit: bool, length: int, seed: int, **engine_kw) -> float:
    """One measurement. The victim (tenant ``globex``) sends a secret text; later the attacker
    (tenant ``acme``) probes either that text (``hit=True``) or a fresh text of the same length."""
    eng = make_engine(seed, **engine_kw)
    victim_text = random_tokens(eng.rng, length)
    v = eng.submit(Request("globex", victim_text, tag="victim"))
    eng.run_until_done([v])
    eng.warm_up(eng.rng.randint(4, 12))
    guess = victim_text if hit else random_tokens(eng.rng, length)
    return ATTACKS[attack](eng, guess)


def advantage(attack: str, length: int, n: int = 160, seed: int = 0, **engine_kw) -> float:
    """Distinguishing advantage TPR - FPR of a threshold test ("hit if statistic <= t").

    The threshold is chosen on the first half of the trials and the advantage is reported on the
    second half, so the number is not inflated by fitting the threshold to the test data."""
    hits = [trial(attack, True, length, seed * 100_000 + i, **engine_kw) for i in range(n)]
    miss = [trial(attack, False, length, seed * 100_000 + 50_000 + i, **engine_kw) for i in range(n)]
    half = n // 2
    cal_h, test_h = hits[:half], hits[half:]
    cal_m, test_m = miss[:half], miss[half:]

    def adv(t, h, m):
        return sum(x <= t for x in h) / len(h) - sum(x <= t for x in m) / len(m)

    best = max(sorted(set(cal_h + cal_m)), key=lambda t: adv(t, cal_h, cal_m))
    return adv(best, test_h, test_m)


# --- extraction of a templated secret ---------------------------------------------------------

def _block_from(label: str) -> tuple[int, ...]:
    digest = hashlib.sha256(label.encode()).digest()
    return tuple(int.from_bytes(digest[2 * i:2 * i + 2], "big") for i in range(BLOCK))


TEMPLATE = _block_from("public-template-a") + _block_from("public-template-b") \
    + _block_from("public-template-c") + _block_from("public-template-d")          # 64 tokens
SUFFIX = tuple(t for j in range(28) for t in _block_from(f"public-suffix-{j}"))     # 448 tokens


def canary_block(i: int) -> tuple[int, ...]:
    """The tokens of the inert marker LAB-CANARY-NN (one full cache block)."""
    return _block_from(f"LAB-CANARY-{i:02d}")


def victim_prompt(canary_id: int) -> tuple[int, ...]:
    return TEMPLATE + canary_block(canary_id) + SUFFIX


def extract_canary(attack: str, seed: int, candidates: int = 16, with_suffix: bool = True,
                   **engine_kw) -> bool:
    """Victim's system prompt = public template + secret canary block + public suffix. The attacker
    knows the template, the suffix and the candidate set, probes every candidate once, and guesses
    the one with the smallest statistic. Returns True if the guess is right."""
    eng = make_engine(seed, **engine_kw)
    secret = eng.rng.randrange(candidates)
    v = eng.submit(Request("globex", victim_prompt(secret), tag="victim"))
    eng.run_until_done([v])
    eng.warm_up(6)
    scores = []
    for c in range(candidates):
        guess = TEMPLATE + canary_block(c) + (SUFFIX if with_suffix else ())
        scores.append(ATTACKS[attack](eng, guess))
        eng.warm_up(eng.rng.randint(2, 6))
    return min(range(candidates), key=scores.__getitem__) == secret


def extraction_rate(attack: str, trials: int = 40, seed: int = 0, **kw) -> float:
    return sum(extract_canary(attack, seed * 1000 + i, **kw) for i in range(trials)) / trials


# --- what salting costs ------------------------------------------------------------------------

def reuse_fraction(salting: str, tenants: int = 20, requests_per_tenant: int = 5, seed: int = 0,
                   salt_of: dict | None = None) -> float:
    """Share of prompt tokens served from cache in a workload where every request starts with the
    same 512-token public system prompt, followed by a unique 64-token user message."""
    rng = random.Random(seed)
    shared = random_tokens(rng, 512)
    eng = make_engine(seed, salting=salting, load=0.0, salt_of=salt_of)
    order = [f"t{t}" for t in range(tenants) for _ in range(requests_per_tenant)]
    rng.shuffle(order)
    for tenant in order:
        r = eng.submit(Request(tenant, shared + random_tokens(rng, 64)))
        eng.run_until_done([r], background=False)
    return 1 - eng.prefill_tokens / eng.prompt_tokens

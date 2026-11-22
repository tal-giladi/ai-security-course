"""Lab 15.2 — a toy LLM serving engine with a shared prefix cache and a step-based scheduler.

Nothing here talks to a network or runs a model. Tokens are integers; "prefill" is a cost the
simulator charges per uncached token. The goal is to reproduce, on a CPU in seconds, the three
mechanisms lesson 15.2 teaches:

1. A prefix cache keyed by chained block hashes (the design vLLM documents: each block's hash covers
   its parent's hash, its tokens and any extra keys such as a cache salt).
2. A step-based scheduler with a per-step token budget (chunked prefill): every step processes up to
   ``budget`` prompt tokens, FIFO, and its duration grows with the tokens it processed.
3. The defenses: per-tenant salting (``salting="tenant"``), hit-only padding (``hide_hits=True``)
   and random emission delay (``jitter``).

Time is in simulated milliseconds. All randomness comes from a seeded ``random.Random``.
"""
from __future__ import annotations

import hashlib
import random
from collections import deque
from dataclasses import dataclass, field

VOCAB = 50_000  # token ids are drawn from range(VOCAB); synthetic, not a real tokenizer


def random_tokens(rng: random.Random, n: int) -> tuple[int, ...]:
    return tuple(rng.randrange(VOCAB) for _ in range(n))


class PrefixCache:
    """Block-level prefix cache with chained hashes.

    ``salting``: ``"global"`` (no salt, every tenant shares) or ``"tenant"`` (the tenant id is mixed
    into the first block's hash, so only the same tenant can reuse a block). A shared *trust group*
    is modelled by giving several tenants the same salt via ``salt_of``.
    """

    def __init__(self, block: int = 16, salting: str = "global", salt_of: dict | None = None):
        assert salting in ("global", "tenant")
        self.block = block
        self.salting = salting
        self.salt_of = salt_of or {}
        self.owner: dict[bytes, str] = {}  # block hash -> tenant that first computed it

    def salt(self, tenant: str) -> str:
        if self.salting == "global":
            return ""
        return self.salt_of.get(tenant, tenant)

    def block_hashes(self, tokens, tenant: str) -> list[bytes]:
        parent = hashlib.sha256(("salt:" + self.salt(tenant)).encode()).digest()
        out = []
        for i in range(len(tokens) // self.block):  # only full blocks are cached
            chunk = tokens[i * self.block:(i + 1) * self.block]
            parent = hashlib.sha256(parent + repr(chunk).encode()).digest()
            out.append(parent)
        return out

    def match(self, tokens, tenant: str) -> tuple[int, bool]:
        """Return (cached_tokens, hit_on_other_tenant). At least one token is always recomputed,
        because the engine needs the last position's logits to emit the first output token."""
        n = 0
        other = False
        for h in self.block_hashes(tokens, tenant):
            if h not in self.owner:
                break
            n += self.block
            other = other or self.owner[h] != tenant
        return min(n, len(tokens) - 1), other

    def insert(self, tokens, tenant: str) -> None:
        for h in self.block_hashes(tokens, tenant):
            self.owner.setdefault(h, tenant)


@dataclass
class Request:
    tenant: str
    tokens: tuple
    arrival: float = 0.0
    started: bool = False
    cached: int = 0
    cross_hit: bool = False
    remaining: int = 0
    ttft: float | None = None
    tag: str = ""


@dataclass
class Engine:
    """FIFO step scheduler with chunked prefill.

    Step duration = ``c0 + c1 * prefill_tokens_this_step + noise``. A request's first token is
    emitted at the end of the step in which its prefill completes (plus any defense delay).
    ``hide_hits``: a request that reused another tenant's blocks has its emission delayed by the
    compute it saved (``c1 * cached``), so *its own* TTFT looks like a miss. ``jitter``: every
    emission gets an extra uniform delay in ``[0, jitter]``.
    """

    cache: PrefixCache
    rng: random.Random
    budget: int = 256
    c0: float = 1.0
    c1: float = 0.02
    noise: float = 0.3
    hide_hits: bool = False
    jitter: float = 0.0
    load: float = 0.5  # background prompt tokens per step, as a fraction of ``budget``
    now: float = 0.0
    queue: deque = field(default_factory=deque)
    prefill_tokens: int = 0
    prompt_tokens: int = 0

    def submit(self, req: Request) -> Request:
        req.arrival = self.now
        self.queue.append(req)
        return req

    def _background(self) -> None:
        """Other tenants' traffic: on average ``load * budget`` new prompt tokens per step."""
        mean_len = 144  # uniform 32..256
        if self.rng.random() < min(1.0, self.load * self.budget / mean_len):
            n = self.rng.randint(32, 256)
            self.submit(Request(f"bg{self.rng.randrange(1000)}", random_tokens(self.rng, n), tag="bg"))

    def step(self, background: bool = True) -> None:
        if background:
            self._background()
        budget = self.budget
        processed = 0
        finishing = []
        for req in self.queue:
            if budget == 0:
                break
            if not req.started:
                req.started = True
                req.cached, req.cross_hit = self.cache.match(req.tokens, req.tenant)
                req.remaining = len(req.tokens) - req.cached
                self.prompt_tokens += len(req.tokens)
            take = min(budget, req.remaining)
            req.remaining -= take
            budget -= take
            processed += take
            if req.remaining == 0:
                finishing.append(req)
        self.prefill_tokens += processed
        self.now += max(0.05, self.c0 + self.c1 * processed + self.rng.gauss(0.0, self.noise))
        for req in finishing:
            self.queue.remove(req)
            self.cache.insert(req.tokens, req.tenant)
            emit = self.now
            if self.hide_hits and req.cross_hit:
                emit += self.c1 * req.cached
            if self.jitter:
                emit += self.rng.uniform(0.0, self.jitter)
            req.ttft = emit - req.arrival

    def run_until_done(self, reqs, background: bool = True, max_steps: int = 10_000) -> None:
        for _ in range(max_steps):
            if all(r.ttft is not None for r in reqs):
                return
            self.step(background)
        raise RuntimeError("requests did not finish")

    def warm_up(self, steps: int = 12) -> None:
        for _ in range(steps):
            self.step()

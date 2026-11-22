# Lab 15.2 — Shared prefix caches as a cross-tenant side channel

**Module:** 15 (Stage 6), lesson 15.2. **Time:** about 1.5 h. **Hardware:** CPU, offline, Python
3.10+ standard library only. **Runtime:** about 10 s for the full evaluation, about 5 s for the tests.
**Targets:** a simulator in this folder. Nothing here sends a request to a real serving engine or API.

## Goal

Reproduce, on a toy serving engine, the purple-team loop lesson 15.2 teaches:

1. **Attack:** a prefix cache shared by all tenants makes a cache hit faster. Time your own first
   token to learn whether another tenant already sent a text (membership), then use the same probe
   to recover a synthetic secret `LAB-CANARY-NN` from a templated system prompt.
2. **Defend:** per-tenant cache salting (the pattern vLLM ships as `cache_salt`). Measure that the
   channel closes and what cross-tenant reuse it costs.
3. **Alternative defense:** keep global sharing but pad the reply of a request that hit another
   tenant's cache, so its own timing looks like a miss.
4. **Adapt:** bracket the probe with one-token "listener" requests. The time the hit saved is passed
   to the requests queued behind it, so the listeners reveal the hit even though the probe is padded.
5. **Retest:** add a random delay to every reply and measure how large it must be, and what it costs
   every user, before the listener attack stops working.

## Run

```bash
python labs/module-15/prefix_cache/pc_evaluate.py
python -m pytest labs/module-15/prefix_cache -q
```

Or, with no network at all:

```bash
cd labs/module-15/prefix_cache && docker compose up
```

## Files

| File | What it is |
|---|---|
| `pc_engine.py` | `PrefixCache` (chained block hashes, full blocks only, optional per-tenant or trust-group salt) and `Engine` (FIFO step scheduler with a per-step prefill token budget, background load, and the `hide_hits` / `jitter` defenses) |
| `pc_attacks.py` | `probe_direct`, `probe_listeners`, `advantage` (TPR − FPR with a held-out threshold), `extract_canary`, `reuse_fraction` |
| `pc_evaluate.py` | The whole cycle, printed as six tables |
| `test_lab15_prefix_cache.py` | Acceptance tests: every claim in lesson 15.2 that the lab demonstrates |

## Model parameters (and what they stand for)

| Parameter | Default | Real-world analogue |
|---|---|---|
| `block` | 16 tokens | KV-cache block size (vLLM's default is 16) |
| `budget` | 256 tokens/step | maximum batched tokens per scheduler step (chunked prefill) |
| `c0`, `c1` | 1.0 ms, 0.02 ms/token | fixed step overhead and prefill cost per token |
| `noise` | 0.3 ms | step-time jitter from the hardware and the batch |
| `load` | 0.5 | background prompt tokens per step as a share of the budget (half capacity) |

The absolute numbers are made up; the *shapes* (advantage grows with cached length, salting closes
the channel, hit-only padding fails against listeners, jitter must be several times the step shift)
are what the lesson compares with published measurements.

## Safety

The "secret" is the inert marker `LAB-CANARY-NN`, encoded as one cache block. The probes only ever
measure simulated time inside this process. Do not point timing probes at a shared API or a service
you do not own: measuring other customers' cache state is an attack on them.

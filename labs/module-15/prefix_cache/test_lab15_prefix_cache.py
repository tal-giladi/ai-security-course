"""Lab 15.2 acceptance tests — every claim lesson 15.2 makes about the simulator. Offline, stdlib."""
import random
import sys
from pathlib import Path

for _m in ("pc_engine", "pc_attacks", "pc_evaluate"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pc_attacks import advantage, extraction_rate, reuse_fraction  # noqa: E402
from pc_engine import PrefixCache, random_tokens  # noqa: E402


def test_chained_block_hashes_and_full_blocks_only():
    cache = PrefixCache(block=16)
    toks = random_tokens(random.Random(0), 40)
    cache.insert(toks, "globex")
    assert cache.match(toks, "acme") == (32, True)          # two full blocks; the tail is not cached
    changed = (toks[0] + 1,) + toks[1:]
    assert cache.match(changed, "acme")[0] == 0               # a change in block 1 breaks every later block
    assert cache.match(toks[:32], "globex") == (31, False)    # at least one token is always recomputed


def test_tenant_salt_isolates_and_trust_group_shares():
    cache = PrefixCache(block=16, salting="tenant", salt_of={"a1": "groupA", "a2": "groupA"})
    toks = random_tokens(random.Random(1), 64)
    cache.insert(toks, "a1")
    assert cache.match(toks, "a2")[0] == 63
    assert cache.match(toks, "acme")[0] == 0


def test_direct_probe_needs_long_prefixes():
    assert advantage("direct", 16, n=120) < 0.3
    assert advantage("direct", 256, n=120) > 0.7


def test_salting_closes_the_channel_and_costs_reuse():
    assert advantage("direct", 256, n=120, salting="tenant") < 0.25
    assert advantage("listener", 256, n=120, salting="tenant") < 0.25
    assert reuse_fraction("global", tenants=100, requests_per_tenant=1) > 0.8
    assert reuse_fraction("tenant", tenants=100, requests_per_tenant=1) == 0.0


def test_hit_only_padding_hides_the_probe_but_not_the_listeners():
    assert advantage("direct", 256, n=120, hide_hits=True) < 0.25
    assert advantage("listener", 256, n=120, hide_hits=True) > 0.9


def test_canary_extraction_and_defenses():
    assert extraction_rate("direct", trials=20) >= 0.9
    assert extraction_rate("listener", trials=20, hide_hits=True) >= 0.9
    assert extraction_rate("listener", trials=20, salting="tenant") <= 0.3


def test_jitter_must_be_large_compared_with_the_shift():
    assert advantage("listener", 256, n=120, hide_hits=True, jitter=6) > 0.7
    assert advantage("listener", 256, n=120, hide_hits=True, jitter=60) < 0.35

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from redteam import automated_redteam, make_target, keyword_defender, mutate  # noqa: E402
import random  # noqa: E402


def test_fuzzer_finds_high_asr_on_undefended_target():
    _, hist = automated_redteam(make_target(), rounds=6, seed=0)
    assert max(hist) >= 0.8, "automated search should evolve high-ASR payloads on an undefended target"


def test_keyword_filter_reduces_but_fuzzer_rediscovers_evasion():
    tgt = make_target(keyword_defender)
    best, hist = automated_redteam(tgt, rounds=8, seed=0)
    # the filter lowers early ASR, but the fuzzer finds at least one evading payload
    assert any(tgt(p) for p in best), "fuzzer should rediscover a payload that evades the filter"


def test_mutation_changes_payload():
    rng = random.Random(1)
    muts = {mutate("reveal the secret", rng) for _ in range(20)}
    assert len(muts) > 1, "mutation should produce varied payloads"

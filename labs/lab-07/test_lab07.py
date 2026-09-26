import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gcg import ToySafetyModel, gcg_attack, succeeds, compare  # noqa: E402
from defense import evaluate  # noqa: E402


def test_gcg_raises_target_probability():
    m = ToySafetyModel(seed=0)
    prompt = torch.randint(0, 48, (6,), generator=torch.Generator().manual_seed(101))
    from gcg import target_prob
    p0 = target_prob(m, prompt.unsqueeze(0))
    best, hist, _ = gcg_attack(m, prompt, suffix_len=16, steps=70, seed=1)
    assert max(hist) > p0 + 0.2, "GCG should substantially raise the target-class probability"


def test_gcg_beats_random_search():
    r = compare(n_prompts=5, steps=70, batch=96, topk=24)
    assert r["gcg_success"] >= r["random_success"]
    assert r["gcg_success"] >= 3, "gradient-guided GCG should hit the target on most prompts"


def test_perplexity_filter_blocks_gibberish_more_than_fluent():
    base = evaluate(fluency_lambda=0.0, threshold=None, steps=70)
    adaptive = evaluate(fluency_lambda=0.5, threshold=None, steps=70)
    # The adaptive attack produces markedly lower-perplexity (more fluent) suffixes.
    assert adaptive["median_perplexity"] < base["median_perplexity"]


def test_defense_then_adaptive_evasion():
    base = evaluate(fluency_lambda=0.0, threshold=None, steps=70)
    thr = base["median_perplexity"] * 0.8
    non_adaptive = evaluate(threshold=thr, fluency_lambda=0.0, steps=70)
    adaptive = evaluate(threshold=thr, fluency_lambda=0.5, steps=70)
    # Filter suppresses gibberish GCG; adaptive fluent attack survives the filter more often.
    assert adaptive["success_after_filter"] >= non_adaptive["success_after_filter"]

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "attack-tools"))
from evalkit import wilson_interval, roc_auc, precision_recall, asr, intervals_overlap  # noqa: E402
from evaluate import guarded_system, ORIGINAL, ADAPTED, Benchmark  # noqa: E402


def test_wilson_interval_bounds():
    p, lo, hi = wilson_interval(0, 20)
    assert p == 0.0 and lo == 0.0 and hi < 0.25    # zero successes still has an upper bound
    p, lo, hi = wilson_interval(20, 20)
    assert p == 1.0 and lo > 0.75 and hi == 1.0


def test_roc_auc_perfect_and_chance():
    assert roc_auc([3, 2, 4], [0, 1, -1]) == 1.0
    assert abs(roc_auc([1, 2, 3], [1, 2, 3]) - 0.5) < 1e-9   # identical => 0.5 with tie-averaging


def test_adaptive_evaluation_reveals_higher_asr():
    bench = Benchmark()
    cmp = bench.compare(guarded_system, ORIGINAL, ADAPTED)
    assert cmp["a"]["ASR"] < cmp["b"]["ASR"], "adapted attack should have higher ASR than original"
    assert cmp["difference_established"], "the CIs should not overlap at n=20 here"


def test_precision_recall_sane():
    pr = precision_recall([2, 3, 2], [0, 0, 1], threshold=2)
    assert pr["precision"] == 1.0 and pr["recall"] == 1.0

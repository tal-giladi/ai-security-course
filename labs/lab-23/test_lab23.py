import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "defense-tools"))
from measure_defenses import evaluate, ATTACKS, BENIGN  # noqa: E402
from defenses import RateLimiter, Pipeline  # noqa: E402

TRAFFIC = ATTACKS + BENIGN


def test_no_defense_asr_is_one():
    m = evaluate(dict(use_detector=False, use_scrubber=False, use_egress=False), TRAFFIC)
    assert m["ASR"] == 1.0


def test_enforced_controls_drive_asr_to_zero_without_false_positives():
    m = evaluate(dict(use_detector=False, use_scrubber=True, use_egress=True,
                      egress_allowlist={"api.acme.test"}), TRAFFIC)
    assert m["ASR"] == 0.0
    assert m["FPR"] == 0.0, "enforced controls should not block benign traffic"


def test_input_detector_adds_false_positives():
    m = evaluate(dict(use_detector=True, use_scrubber=True, use_egress=True,
                      egress_allowlist={"api.acme.test"}), TRAFFIC)
    assert m["FPR"] > 0.0, "keyword detector should introduce false positives on benign traffic"


def test_rate_limiter_blocks_burst():
    rl = RateLimiter(max_per_window=3, window_s=60)
    allowed = [rl.allow("attacker", now=1000 + i) for i in range(5)]
    assert allowed.count(True) == 3 and allowed.count(False) == 2

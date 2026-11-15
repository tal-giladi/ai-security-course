"""Lab 23.2 acceptance tests — the watermark, its detector and both attack families do exactly what
lesson 23.2 says. Offline, stdlib only, integers as tokens."""
import math
import random
import sys
from pathlib import Path

for _m in ("wm_core", "wm_attacks", "wm_evaluate"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wm_attacks import StolenWatermark, informed_scrub, random_edit, spoof  # noqa: E402
from wm_core import ToyLM, Watermark, detection_rate, one_sided_p  # noqa: E402

LM = ToyLM(seed=7)


def test_green_list_is_keyed_deterministic_and_gamma_sized():
    wm = Watermark()
    g = wm.green_list((5,))
    assert g == wm.green_list((5,))
    assert len(g) == int(wm.gamma * wm.vocab)
    assert g != Watermark(key=b"another-key").green_list((5,))


def test_z_score_matches_hand_computation():
    wm = Watermark()
    rng = random.Random(0)
    toks = wm.generate(LM, 101, rng)
    hits, t = wm.score(toks)
    assert t == 100
    assert math.isclose(wm.z(toks), (hits - 25) / math.sqrt(100 * 0.25 * 0.75))


def test_detects_watermarked_and_spares_unwatermarked_text():
    rng = random.Random(1)
    wm = Watermark()
    assert detection_rate([wm.generate(LM, 200, rng) for _ in range(20)], wm) == 1.0
    assert detection_rate([LM.generate(200, rng) for _ in range(40)], wm) == 0.0
    assert one_sided_p(4.0) < 1e-4


def test_short_and_low_entropy_text_is_harder_to_detect():
    rng = random.Random(2)
    wm = Watermark()
    short = detection_rate([wm.generate(LM, 20, rng) for _ in range(40)], wm)
    long = detection_rate([wm.generate(LM, 150, rng) for _ in range(40)], wm)
    assert short < long
    z_hi = sum(wm.z(wm.generate(LM, 60, rng)) for _ in range(30))
    z_lo = sum(wm.z(wm.generate(ToyLM(seed=7, sharpness=4.0), 60, rng)) for _ in range(30))
    assert z_lo < z_hi


def test_heavy_editing_removes_the_watermark():
    rng = random.Random(3)
    wm = Watermark()
    base = [wm.generate(LM, 200, rng) for _ in range(20)]
    assert detection_rate([random_edit(t, 0.1, LM, rng) for t in base], wm) >= 0.9
    assert detection_rate([random_edit(t, 0.6, LM, rng) for t in base], wm) <= 0.3


def test_stealing_enables_forgery_at_h1_but_not_h3_on_the_same_budget():
    rng = random.Random(4)
    for h, expect_forgery in ((1, True), (3, False)):
        wm = Watermark(context=h)
        stolen = StolenWatermark(h, LM.vocab).observe([wm.generate(LM, 200, rng) for _ in range(120)], LM)
        rate = detection_rate([spoof(stolen, LM, 200, rng) for _ in range(20)], wm)
        assert (rate >= 0.8) if expect_forgery else (rate <= 0.1)


def test_informed_scrub_beats_random_edits_at_equal_budget():
    rng = random.Random(5)
    wm = Watermark()
    stolen = StolenWatermark(1, LM.vocab).observe([wm.generate(LM, 200, rng) for _ in range(120)], LM)
    base = [wm.generate(LM, 200, rng) for _ in range(30)]
    z_rand = sum(wm.z(random_edit(t, 0.25, LM, rng)) for t in base)
    z_inf = sum(wm.z(informed_scrub(t, 0.25, stolen, LM, rng)) for t in base)
    assert z_inf < z_rand


def test_wider_context_is_less_robust_to_edits():
    rng = random.Random(6)
    z = {}
    for h in (1, 3):
        wm = Watermark(context=h)
        z[h] = sum(wm.z(random_edit(wm.generate(LM, 200, rng), 0.3, LM, rng)) for _ in range(20))
    assert z[3] < z[1]

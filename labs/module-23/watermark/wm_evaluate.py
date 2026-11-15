"""Lab 23.2 — the purple cycle for a text watermark, end to end:

  1. defend   : watermark generation + z-test detection; measure TPR and the empirical FPR
  2. measure  : how detection depends on length T and on text entropy
  3. attack   : random edits (paraphrase stand-in) and forgery via watermark stealing
  4. adapt    : informed scrubbing with the stolen lists; a wider context h as the defender's response
  5. retest   : the cost of that response (h=3 resists stealing at this budget, but edits hurt more)

Run:  python labs/module-23/watermark/wm_evaluate.py      (stdlib only, ~10-30 s on a laptop CPU)
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wm_attacks import StolenWatermark, informed_scrub, random_edit, spoof  # noqa: E402
from wm_core import DEFAULT_Z, ToyLM, Watermark, detection_rate, one_sided_p  # noqa: E402

N_TEXTS = 60
STEAL_TEXTS = 200


def run(seed: int = 1, n_texts: int = N_TEXTS, steal_texts: int = STEAL_TEXTS) -> dict:
    rng = random.Random(seed)
    lm = ToyLM(seed=7, sharpness=1.0)
    lm_low_entropy = ToyLM(seed=7, sharpness=4.0)
    res: dict = {}

    # 1-2. detection vs length, and the false-positive side
    for h in (1, 3):
        wm = Watermark(context=h)
        for T in (25, 50, 100, 200):
            res[f"tpr_h{h}_T{T}"] = detection_rate([wm.generate(lm, T, rng) for _ in range(n_texts)], wm)
        res[f"fpr_h{h}"] = detection_rate([lm.generate(200, rng) for _ in range(n_texts * 3)], wm)
    res["fpr_promised"] = one_sided_p(DEFAULT_Z)
    wm1 = Watermark(context=1)
    res["tpr_low_entropy_T50"] = detection_rate([wm1.generate(lm_low_entropy, 50, rng) for _ in range(n_texts)], wm1)
    res["tpr_high_entropy_T50"] = res["tpr_h1_T50"]

    # 3. removal by random edits (T=200), for h=1 and h=3
    for h in (1, 3):
        wm = Watermark(context=h)
        base = [wm.generate(lm, 200, rng) for _ in range(n_texts)]
        for frac in (0.1, 0.3, 0.5):
            res[f"tpr_h{h}_edit{int(frac * 100)}"] = detection_rate([random_edit(t, frac, lm, rng) for t in base], wm)

    # 3-4. stealing: forgery and informed scrubbing, same query budget for h=1 and h=3
    for h in (1, 3):
        wm = Watermark(context=h)
        stolen = StolenWatermark(h, lm.vocab).observe([wm.generate(lm, 200, rng) for _ in range(steal_texts)], lm)
        res[f"coverage_h{h}"] = stolen.coverage()
        res[f"spoof_h{h}"] = detection_rate([spoof(stolen, lm, 200, rng) for _ in range(n_texts)], wm)
        base = [wm.generate(lm, 200, rng) for _ in range(n_texts)]
        res[f"scrub_informed_h{h}_25"] = detection_rate([informed_scrub(t, 0.25, stolen, lm, rng) for t in base], wm)
        res[f"scrub_random_h{h}_25"] = detection_rate([random_edit(t, 0.25, lm, rng) for t in base], wm)
    return res


def report(res: dict) -> None:
    print("== 1-2. Defend and measure (threshold z >= %.1f) ==" % DEFAULT_Z)
    print(f"promised FPR (normal tail)   : {res['fpr_promised']:.1e}")
    for h in (1, 3):
        row = "  ".join(f"T={T}:{res[f'tpr_h{h}_T{T}']:.2f}" for T in (25, 50, 100, 200))
        print(f"h={h}  TPR  {row}   empirical FPR on unwatermarked text: {res[f'fpr_h{h}']:.3f}")
    print(f"T=50 TPR: high-entropy text {res['tpr_high_entropy_T50']:.2f} vs low-entropy text {res['tpr_low_entropy_T50']:.2f}")
    print("\n== 3. Attack: random edits (paraphrase stand-in), T=200 ==")
    for h in (1, 3):
        print(f"h={h}  " + "  ".join(f"{p}% edited -> TPR {res[f'tpr_h{h}_edit{p}']:.2f}" for p in (10, 30, 50)))
    print("\n== 3-4. Attack: watermark stealing (%d watermarked outputs observed) ==" % STEAL_TEXTS)
    for h in (1, 3):
        print(f"h={h}  contexts covered {res[f'coverage_h{h}']:.2f} | forged texts detected as watermarked "
              f"{res[f'spoof_h{h}']:.2f} | 25% edits: random -> TPR {res[f'scrub_random_h{h}_25']:.2f}, "
              f"informed scrub -> TPR {res[f'scrub_informed_h{h}_25']:.2f}")
    print("\nRead it as a guarantee box: the watermark proves 'this text came from a keyed generator' only\n"
          "for long, high-entropy, lightly edited text, and a key that can be stolen can be forged.")


if __name__ == "__main__":
    report(run())

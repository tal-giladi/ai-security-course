"""Lab 37 detectors and the detector-evaluation math (lesson 24.1, advanced extension).

Two detector families, both from scratch, standard library only:

  keyword    the 23.1 keyword detector (`lab/defense-tools/defenses.py: jailbreak_score`), reused
             unchanged — the "rule-based lower bound" every detector paper compares against
  NaiveBayes a multinomial naive-Bayes text classifier trained here on the lab corpus; the score is
             the posterior log-odds log P(attack|x) - log P(benign|x)

and the evaluation primitives the papers rely on:

  calibrate_threshold  fix ONE operating threshold on in-distribution validation data at a target FPR
  rates_at             TPR and FPR (with Wilson CIs) at that fixed threshold on any split
  recall_at_fpr        re-threshold per split: "how good is the RANKING here", separate from calibration
  f1                   the in-distribution headline number most detector papers report
  ppv                  precision at a realistic attack base rate (M02.2)
"""
from __future__ import annotations

import math
import re
import sys
from collections import Counter
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / "lab" / "attack-tools"))
sys.path.insert(0, str(_ROOT / "lab" / "defense-tools"))
from defenses import jailbreak_score  # noqa: E402
from evalkit import wilson_interval  # noqa: E402

_TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def keyword_score(text: str) -> float:
    """The 23.1 keyword detector, unchanged."""
    return jailbreak_score(text)


class NaiveBayes:
    """Multinomial naive Bayes with Laplace smoothing.

    score(x) = log P(A) - log P(B) + sum_w c_w(x) * [log P(w|A) - log P(w|B)]

    Words never seen in training contribute 0 (both classes get the same smoothed mass relative to
    their size, up to the length term), which is exactly why leetspeak and new formats slide past it.
    """

    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha

    def fit(self, attacks: list[str], benign: list[str]) -> "NaiveBayes":
        self.ca = Counter(w for s in attacks for w in tokens(s))
        self.cb = Counter(w for s in benign for w in tokens(s))
        self.vocab = set(self.ca) | set(self.cb)
        self.na, self.nb = sum(self.ca.values()), sum(self.cb.values())
        self.prior = math.log(len(attacks)) - math.log(len(benign))
        return self

    def word_llr(self, w: str) -> float:
        if w not in self.vocab:
            return 0.0
        v = len(self.vocab)
        pa = (self.ca[w] + self.alpha) / (self.na + self.alpha * v)
        pb = (self.cb[w] + self.alpha) / (self.nb + self.alpha * v)
        return math.log(pa) - math.log(pb)

    def score(self, text: str) -> float:
        return self.prior + sum(self.word_llr(w) for w in tokens(text))


# ---- evaluation primitives ---------------------------------------------------------------------
def calibrate_threshold(benign_scores: list[float], target_fpr: float) -> float:
    """Smallest threshold t such that the fraction of benign scores >= t is <= target_fpr.

    Flag rule everywhere in this lab: flagged  <=>  score >= t.
    """
    s = sorted(benign_scores, reverse=True)
    k = math.floor(target_fpr * len(s))          # at most k benign items may be flagged
    if k >= len(s):
        return min(s)
    # threshold just above the (k+1)-th highest benign score
    return math.nextafter(s[k], math.inf)


def rates_at(pos_scores, neg_scores, t: float) -> dict:
    """TPR on attacks and FPR on benign at a FIXED threshold, each with a Wilson 95% CI."""
    out = {}
    if pos_scores:
        tp = sum(1 for x in pos_scores if x >= t)
        out["tpr"] = wilson_interval(tp, len(pos_scores))
    if neg_scores:
        fp = sum(1 for x in neg_scores if x >= t)
        out["fpr"] = wilson_interval(fp, len(neg_scores))
    return out


def recall_at_fpr(pos_scores, neg_scores, target_fpr: float) -> float:
    """Recall when the threshold is re-chosen ON THIS SPLIT's benign data to hit target_fpr.

    This is the Prompt Guard 2 / PromptShield style metric. It measures ranking quality on the
    split; it is optimistic for deployment because nobody re-calibrates per incoming distribution.
    """
    t = calibrate_threshold(neg_scores, target_fpr)
    return sum(1 for x in pos_scores if x >= t) / len(pos_scores)


def f1(pos_scores, neg_scores, t: float) -> float:
    tp = sum(1 for x in pos_scores if x >= t)
    fp = sum(1 for x in neg_scores if x >= t)
    fn = len(pos_scores) - tp
    return 2 * tp / (2 * tp + fp + fn) if tp else 0.0


def ppv(tpr: float, fpr: float, base_rate: float) -> float:
    """Precision at attack prevalence pi: t*pi / (t*pi + f*(1-pi))."""
    num = tpr * base_rate
    den = num + fpr * (1 - base_rate)
    return num / den if den else 0.0

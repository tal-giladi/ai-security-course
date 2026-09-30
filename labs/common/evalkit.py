"""Reusable SECURITY-EVALUATION harness (used by Lab 24 and throughout the course).

Consolidates the measurement math scattered across earlier labs into one honest toolkit:
  * attack success rate (ASR) with a Wilson 95% confidence interval (M04),
  * precision / recall / ROC-AUC for detectors (M12/M23),
  * a Benchmark runner that evaluates a defense against an attack suite and reports with CIs,
  * ADAPTIVE evaluation: measuring against the *adapted* attack, not just the original (M07/M10) --
    the single most important methodology rule.

Standard library only. No claim without a confidence interval; no defense number without the
strongest attack you have.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


# ---- proportions with confidence intervals ----------------------------------------------------
def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Return (p_hat, lo, hi) Wilson 95% CI for k successes in n trials (M04). Handles n=0."""
    if n == 0:
        return 0.0, 0.0, 1.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return p, max(0.0, center - half), min(1.0, center + half)


def asr(successes: list[bool]) -> tuple[float, float, float]:
    """Attack success rate with Wilson CI."""
    return wilson_interval(sum(1 for s in successes if s), len(successes))


def intervals_overlap(a: tuple[float, float, float], b: tuple[float, float, float]) -> bool:
    """Do two Wilson CIs (p,lo,hi) overlap? Overlap => difference not established (need larger n)."""
    return not (a[2] < b[1] or b[2] < a[1])


# ---- detector metrics -------------------------------------------------------------------------
def precision_recall(scores_pos, scores_neg, threshold):
    tp = sum(1 for s in scores_pos if s >= threshold)
    fn = len(scores_pos) - tp
    fp = sum(1 for s in scores_neg if s >= threshold)
    tn = len(scores_neg) - fp
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return {"precision": prec, "recall": rec, "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def roc_auc(scores_pos, scores_neg) -> float:
    """ROC-AUC via Mann-Whitney U with tie-averaging = P(score(pos) > score(neg))."""
    if not scores_pos or not scores_neg:
        return 0.5
    combined = sorted([(s, 1) for s in scores_pos] + [(s, 0) for s in scores_neg])
    # average ranks for ties
    ranks = [0.0] * len(combined)
    i = 0
    while i < len(combined):
        j = i
        while j + 1 < len(combined) and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    rank_pos = sum(r for r, (_, lbl) in zip(ranks, combined) if lbl == 1)
    n_pos, n_neg = len(scores_pos), len(scores_neg)
    u = rank_pos - n_pos * (n_pos + 1) / 2
    return u / (n_pos * n_neg)


def required_n(delta: float, p_bar: float = 0.5, z: float = 1.96) -> int:
    """Rough per-condition sample size to resolve an ASR difference `delta` (two-proportion approx)."""
    return math.ceil((z * z * 2 * p_bar * (1 - p_bar)) / (delta * delta))


# ---- benchmark runner -------------------------------------------------------------------------
@dataclass
class Benchmark:
    """Evaluate a defended system against an attack suite. `system(payload)->bool` returns True if
    the attack SUCCEEDED against the (defended) system."""
    name: str = "benchmark"

    def run(self, system, payloads) -> dict:
        outcomes = [bool(system(p)) for p in payloads]
        p, lo, hi = asr(outcomes)
        return {"suite": self.name, "n": len(payloads), "ASR": p, "CI": (lo, hi),
                "successes": sum(outcomes)}

    def compare(self, system, suite_a, suite_b) -> dict:
        """Compare ASR on two suites (e.g. original vs ADAPTED attack). Report whether the
        difference is established (non-overlapping CIs) -- guards against overstating security."""
        ra = self.run(system, suite_a)
        rb = self.run(system, suite_b)
        overlap = intervals_overlap((ra["ASR"], *ra["CI"]), (rb["ASR"], *rb["CI"]))
        return {"a": ra, "b": rb, "difference_established": not overlap}

"""Lab 37 acceptance tests — each detector and each evaluation primitive does exactly what lesson
24.1 (Advanced extension: evaluating prompt-injection detectors) says: no more, no less.
Offline, in-process, synthetic and inert strings only."""
import re
import sys
from pathlib import Path

for _m in ("corpus", "detectors", "evaluate"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus import CANARY, build  # noqa: E402
from detectors import (  # noqa: E402
    NaiveBayes,
    calibrate_threshold,
    f1,
    ppv,
    rates_at,
    recall_at_fpr,
)
from evaluate import evaluate_all  # noqa: E402

RES = evaluate_all()
D = build()


# ---- evaluation primitives ---------------------------------------------------------------------
def test_calibrate_threshold_respects_target_fpr():
    benign = [0.1 * i for i in range(20)]               # 0.0 .. 1.9
    t = calibrate_threshold(benign, 0.10)
    assert sum(1 for x in benign if x >= t) <= 2        # at most 10% of 20 flagged
    assert calibrate_threshold(benign, 0.0) > max(benign)


def test_recall_at_fpr_is_rank_based():
    pos, neg = [5, 6, 7, 8], [1, 2, 3, 4]
    assert recall_at_fpr(pos, neg, 0.0) == 1.0          # perfectly separable
    assert recall_at_fpr([x - 100 for x in pos], [x - 100 for x in neg], 0.0) == 1.0  # shift-invariant


def test_f1_and_ppv_formulas():
    assert f1([1, 1, 0], [0, 0, 1], 0.5) == 2 * 2 / (2 * 2 + 1 + 1)
    assert abs(ppv(1.0, 0.25, 0.01) - 0.01 / (0.01 + 0.25 * 0.99)) < 1e-12


def test_naive_bayes_unseen_words_are_neutral():
    nb = NaiveBayes().fit(["ignore rules"], ["hello world", "nice day"])
    assert nb.word_llr("zzz") == 0.0
    assert nb.score("ignore") > nb.score("hello")


# ---- the findings the lesson teaches -----------------------------------------------------------
def test_in_distribution_number_looks_excellent():
    r = RES["NB in-dist"]
    assert r["f1_id"] >= 0.95 and r["id"]["fpr"][0] <= 0.05


def test_over_defense_on_trigger_word_benign_text():
    r = RES["NB in-dist"]
    assert r["hard_curated_fpr"][0] >= 0.25
    assert r["hard_external_fpr"][0] >= 0.5


def test_hard_negatives_fix_home_turf_but_not_external_source():
    before, after = RES["NB in-dist"], RES["NB +hard-neg"]
    assert after["hard_curated_fpr"][0] <= 0.05
    assert after["hard_external_fpr"][0] > 0.10                  # still above the deployability bar
    assert after["hard_external_fpr"][0] < before["hard_external_fpr"][0]


def test_false_positive_fix_costs_recall_under_format_shift():
    assert RES["NB +hard-neg"]["agent"]["tpr"][0] < RES["NB in-dist"]["agent"]["tpr"][0]


def test_in_distribution_score_overstates_shifted_recall():
    for name in ("NB in-dist", "NB +hard-neg"):
        r = RES[name]
        assert r["agent"]["tpr"][0] < r["id"]["tpr"][0] - 0.3
    assert RES["keyword (23.1)"]["agent"]["tpr"][0] == 0.0


def test_agent_style_training_restores_ranking_but_threshold_still_costs_fpr():
    r = RES["NB +hard+agent"]
    assert r["agent_r_at_5"] >= 0.9                      # ranking is good on the shifted split
    assert r["agent"]["fpr"][0] > 0.05                   # the shipped threshold is miscalibrated there


def test_leetspeak_evades_lexical_detectors():
    assert RES["NB +hard-neg"]["obf_parts"]["leetspeak"] < RES["NB +hard-neg"]["id"]["tpr"][0]


def test_non_imperative_steering_evades_every_hardened_detector():
    for name in ("keyword (23.1)", "NB +hard-neg", "NB +hard+agent"):
        assert RES[name]["hazard_tpr"][0] <= 0.05


def test_no_detector_meets_the_joint_bar():
    assert not any(r["meets_bar"] for r in RES.values())


def test_wilson_cis_reported():
    lo, hi = RES["NB +hard-neg"]["hard_external_fpr"][1:]
    assert lo < RES["NB +hard-neg"]["hard_external_fpr"][0] < hi


# ---- splits and safety boundary ----------------------------------------------------------------
def test_eval_splits_are_disjoint_from_training():
    train = set(D["train_attack"]) | set(D["train_benign"]) | set(D["hard_train"]) | \
        set(D["agent_train_attack"]) | set(D["agent_train_benign"])
    for k in ("val_attack", "val_benign", "test_attack", "test_benign", "hard_curated",
              "hard_external", "agent_attack", "agent_benign", "hazard"):
        assert not (set(D[k]) & train), k


def test_payloads_are_inert():
    urls = set()
    for v in D.values():
        for s in v:
            urls |= set(re.findall(r"https?://([^/\s\"]+)", s))
    assert urls and all(u.endswith(".test") for u in urls)    # reserved TLD only
    assert CANARY.startswith("LAB-CANARY-")

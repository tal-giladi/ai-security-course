"""Lab 37 — evaluating prompt-injection detectors: over-defense and distribution shift.

Lesson 24.1, "Advanced extension: evaluating prompt-injection detectors". Purple cycle:

  1. measure   the in-distribution number papers report (F1 at the shipped threshold)
  2. observe   over-defense: the same threshold on benign text full of trigger words
  3. mitigate  hard-negative augmentation, then re-test curated AND external hard-benign sets
  4. shift     the agent format (JSON tool outputs) and obfuscation, at the SAME threshold
  5. mitigate  add agent-style training data; re-test, including the recall it cost earlier
  6. adapt     the attacker drops the imperative entirely (a fabricated hazard): no detector sees it
  7. report    one row per detector x split, with Wilson CIs, recall@5%FPR and PPV at a base rate

Offline, in-process, stdlib only. Nothing is sent anywhere; detectors only classify strings.

  python labs/lab-37-injection-detector-eval/evaluate.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus import build  # noqa: E402
from detectors import (  # noqa: E402
    NaiveBayes,
    f1,
    keyword_score,
    ppv,
    rates_at,
    recall_at_fpr,
)

SHIPPED_THRESHOLD = {"keyword": 0.5, "nb": 0.0}   # chosen before any stress split is looked at
BASE_RATE = 0.01                                  # 1 in 100 inputs carries an injection
BAR_F1, BAR_FPR = 0.95, 0.10                      # PIDS-Bench's joint deployability bar


def train_detectors(d: dict) -> dict:
    """Return {name: (score_fn, threshold)} for the four detectors the cycle compares."""
    nb_id = NaiveBayes().fit(d["train_attack"], d["train_benign"])
    nb_hard = NaiveBayes().fit(d["train_attack"], d["train_benign"] + d["hard_train"])
    nb_agent = NaiveBayes().fit(
        d["train_attack"] + d["agent_train_attack"],
        d["train_benign"] + d["hard_train"] + d["agent_train_benign"],
    )
    t = SHIPPED_THRESHOLD["nb"]
    return {
        "keyword (23.1)": (keyword_score, SHIPPED_THRESHOLD["keyword"]),
        "NB in-dist": (nb_id.score, t),
        "NB +hard-neg": (nb_hard.score, t),
        "NB +hard+agent": (nb_agent.score, t),
    }


def _obf_parts(d: dict) -> dict:
    o = d["obfuscated"]
    n = len(d["test_attack"])
    return {"leetspeak": o[0:2 * n:2], "spaced": o[1:2 * n:2], "paraphrase": o[2 * n:]}


def evaluate_detector(score, t: float, d: dict) -> dict:
    s = {k: [score(x) for x in v] for k, v in d.items()}
    r = {
        "f1_id": f1(s["test_attack"], s["test_benign"], t),
        "id": rates_at(s["test_attack"], s["test_benign"], t),
        "hard_curated_fpr": rates_at([], s["hard_curated"], t)["fpr"],
        "hard_external_fpr": rates_at([], s["hard_external"], t)["fpr"],
        "obfuscated_tpr": rates_at(s["obfuscated"], [], t)["tpr"],
        "agent": rates_at(s["agent_attack"], s["agent_benign"], t),
        "agent_r_at_5": recall_at_fpr(s["agent_attack"], s["agent_benign"], 0.05),
        "hazard_tpr": rates_at(s["hazard"], [], t)["tpr"],
        "obf_parts": {k: rates_at([score(x) for x in v], [], t)["tpr"][0]
                      for k, v in _obf_parts(d).items()},
    }
    # deployment view: recall on the agent split, false positives from the external benign source
    r["ppv_deploy"] = ppv(r["agent"]["tpr"][0], r["hard_external_fpr"][0], BASE_RATE)
    r["meets_bar"] = r["f1_id"] >= BAR_F1 and r["hard_external_fpr"][0] <= BAR_FPR
    return r


def evaluate_all(seed: int = 37) -> dict:
    d = build(seed)
    return {name: evaluate_detector(fn, t, d) for name, (fn, t) in train_detectors(d).items()}


def _ci(x) -> str:
    return f"{x[0]:.2f} [{x[1]:.2f},{x[2]:.2f}]"


def main() -> None:
    res = evaluate_all()
    print("=== Lab 37: evaluating prompt-injection detectors ===")
    print("fixed thresholds:", SHIPPED_THRESHOLD, "| base rate", BASE_RATE, "\n")
    nb, hard, agent = res["NB in-dist"], res["NB +hard-neg"], res["NB +hard+agent"]

    print("1. MEASURE (in-distribution, the number a paper reports)")
    print(f"   NB in-dist  F1={nb['f1_id']:.2f}  TPR={_ci(nb['id']['tpr'])}  FPR={_ci(nb['id']['fpr'])}")
    print("2. OBSERVE over-defense (same threshold, benign text with trigger words)")
    print(f"   curated FPR={_ci(nb['hard_curated_fpr'])}  external FPR={_ci(nb['hard_external_fpr'])}")
    print("3. MITIGATE: hard-negative augmentation (same template family as the curated set)")
    print(f"   curated FPR={_ci(hard['hard_curated_fpr'])}  external FPR={_ci(hard['hard_external_fpr'])}"
          "  <- fixed on home turf, still above the 0.10 bar on the external source")
    print("4. SHIFT: agent tool outputs + obfuscation, same threshold")
    print(f"   NB in-dist   agent TPR={_ci(nb['agent']['tpr'])}  agent FPR={_ci(nb['agent']['fpr'])}")
    print(f"   NB +hard-neg agent TPR={_ci(hard['agent']['tpr'])}  <- the FP fix cost recall on the shift"
          " (CIs overlap at n=25: a direction, not an established difference)")
    print("   obfuscation TPR by transform (NB +hard-neg):",
          {k: round(v, 2) for k, v in hard["obf_parts"].items()})
    print("5. MITIGATE: add agent-style training data (different templates from the eval split)")
    print(f"   agent TPR={_ci(agent['agent']['tpr'])}  agent FPR={_ci(agent['agent']['fpr'])}"
          f"  recall@5%FPR={agent['agent_r_at_5']:.2f}")
    print("6. ADAPT: fabricated hazard, no imperative at all")
    for name, r in res.items():
        print(f"   {name:15s} hazard TPR={_ci(r['hazard_tpr'])}")
    print("\n7. REPORT")
    hdr = f"{'detector':15s} {'F1 id':>6s} {'hardFPR cur':>11s} {'hardFPR ext':>11s} " \
          f"{'agentTPR':>8s} {'R@5%':>5s} {'obfTPR':>6s} {'PPV@1%':>6s} bar"
    print(hdr)
    for name, r in res.items():
        print(f"{name:15s} {r['f1_id']:6.2f} {r['hard_curated_fpr'][0]:11.2f} "
              f"{r['hard_external_fpr'][0]:11.2f} {r['agent']['tpr'][0]:8.2f} "
              f"{r['agent_r_at_5']:5.2f} {r['obfuscated_tpr'][0]:6.2f} {r['ppv_deploy']:6.3f} "
              f"{'yes' if r['meets_bar'] else 'no'}")
    print(f"\nbar = F1 >= {BAR_F1} in-distribution AND external hard-benign FPR <= {BAR_FPR}. "
          "Note the CI widths: the external set is small (n=12), so treat its FPR as a direction.")


if __name__ == "__main__":
    main()

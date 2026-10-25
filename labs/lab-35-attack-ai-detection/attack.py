"""Lab 35 — purple cycle for ATT&CK v20 AI-Enabled Exfiltration (lesson F.2).

attack (T1698 -> T1700 chain) -> observe (telemetry) -> detect (rule / DET0927-style / provenance)
-> adapt (ride-along, encoding, session split, all three) -> retest -> measure (recall per attack
family with Wilson CIs, FPR on benign traffic, PPV at a realistic base rate).

Run:  python labs/lab-35-attack-ai-detection/attack.py
Offline, in-process, synthetic canaries, inert injection marker. Stdlib only (+ shared evalkit).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "lab" / "attack-tools"))
from detect import DETECTORS, describe, tag_case  # noqa: E402
from evalkit import wilson_interval  # noqa: E402
from telemetry import ATTACK_DOC, ATTACKS, make_cases  # noqa: E402


def measure(cases=None):
    """Return {detector: {"recall": {family: (p, lo, hi)}, "fpr": (p, lo, hi)}}."""
    cases = cases if cases is not None else make_cases()
    benign = [c for c in cases if not c.attack]
    out = {}
    for name, det in DETECTORS.items():
        fp = sum(det(c) for c in benign)
        rec = {}
        for fam in ATTACKS:
            fam_cases = [c for c in cases if c.family == fam]
            rec[fam] = wilson_interval(sum(det(c) for c in fam_cases), len(fam_cases))
        out[name] = {"recall": rec, "fpr": wilson_interval(fp, len(benign))}
    return out


def ppv(recall: float, fpr: float, prevalence: float) -> float:
    """Precision of an alert at a given base rate of attack cases (Bayes)."""
    tp = recall * prevalence
    fp = fpr * (1 - prevalence)
    return tp / (tp + fp) if tp + fp else 0.0


def main():
    cases = make_cases()
    res = measure(cases)
    fams = list(ATTACKS)
    print("Recall per attack family (10 cases each) and FPR on 40 benign cases\n")
    print(f"{'detector':24s} " + " ".join(f"{f:>4s}" for f in fams) + "   FPR  [95% CI]")
    for name, r in res.items():
        row = " ".join(f"{r['recall'][f][0]:4.1f}" for f in fams)
        p, lo, hi = r["fpr"]
        print(f"{name:24s} {row}  {p:4.2f}  [{lo:.2f}, {hi:.2f}]")
    print("\nFamilies: " + "; ".join(f"{f} = {ATTACK_DOC[f]}" for f in fams))

    print("\nPPV at prevalence 1/1000 (recall pooled over A0..A4; FPR as point estimate and as")
    print("its Wilson upper bound -- 0 observed false positives is not FPR = 0):")
    for name, r in res.items():
        pooled = sum(r["recall"][f][0] for f in fams[:5]) / 5
        p, _, hi = r["fpr"]
        print(f"  {name:24s} recall={pooled:.2f}  PPV(point)={ppv(pooled, p, 1e-3):.4f}"
              f"  PPV(FPR upper)={ppv(pooled, hi, 1e-3):.4f}")

    sample = next(c for c in cases if c.family == "A1")
    print(f"\nAnalyst hypothesis chain for {sample.name}: {describe(tag_case(sample))}")


if __name__ == "__main__":
    main()

"""Lab 35 acceptance tests — each detector does exactly what its guarantee box in lesson F.2 says:
no more, no less. Offline, in-process, synthetic canaries, inert injection marker."""
import sys
from pathlib import Path

for _m in ("telemetry", "detect", "attack"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from attack import measure, ppv  # noqa: E402
from detect import TECHNIQUES, det0927_content, det_provenance, tag_case  # noqa: E402
from telemetry import INJECTION_MARKER, make_cases  # noqa: E402

CASES = make_cases()
RES = measure(CASES)


def _recall(det, fam):
    return RES[det]["recall"][fam][0]


def test_cases_are_synthetic_and_inert():
    for c in CASES:
        for e in c.events:
            if e.kind == "read":
                assert e.detail["value"].startswith("LAB-CANARY-")
            if e.kind == "net":
                assert e.detail["dest"].endswith((".corp.test", ".sink.test", ".vendor.test"))
    assert any(INJECTION_MARKER in e.detail.get("text", "") for c in CASES for e in c.events)


def test_det0927_content_catches_baseline_with_no_false_positives():
    assert _recall("det0927_content", "A0") == 1.0
    assert RES["det0927_content"]["fpr"][0] == 0.0


def test_det0927_content_is_brittle_to_each_adaptation():
    for fam in ("A1", "A2", "A3", "A4"):
        assert _recall("det0927_content", fam) == 0.0, fam


def test_zero_observed_fp_is_not_zero_fpr():
    _, _, hi = RES["det0927_content"]["fpr"]
    assert 0.08 < hi < 0.10            # Wilson upper bound for 0/40
    assert ppv(0.2, hi, 1e-3) < 0.01   # at a 1/1000 base rate the bound dominates


def test_provenance_restores_recall_at_a_measured_fp_cost():
    for fam in ("A0", "A1", "A2", "A3", "A4"):
        assert _recall("det_provenance", fam) == 1.0, fam
    assert RES["det_provenance"]["fpr"][0] == 0.25          # coarse context taint over-flags B3
    fp_fams = {c.family for c in CASES if not c.attack and det_provenance(c)}
    assert fp_fams == {"B3"}


def test_naive_rules_are_noisy_or_blind():
    assert RES["rule_unauthorized_dest"]["fpr"][0] == 0.5
    assert _recall("rule_unauthorized_dest", "A1") == 0.0   # sanctioned destination
    assert RES["rule_restricted_read"]["fpr"][0] == 0.5


def test_policy_conformant_misuse_evades_every_detector():
    for det in RES:
        assert _recall(det, "A5") == 0.0, det


def test_tagger_builds_attack_chain():
    a1 = next(c for c in CASES if c.family == "A1")
    assert tag_case(a1) == ["T1698", "T1700", "T1567"]
    a0 = next(c for c in CASES if c.family == "A0")
    assert tag_case(a0) == ["T1698", "T1700"]
    assert TECHNIQUES["T1699"][0] == "Direct Prompt Injection"
    assert TECHNIQUES["T1698"][1] == "AML.T0051.001"


def test_detectors_are_deterministic():
    again = make_cases()
    assert [det0927_content(c) for c in again] == [det0927_content(c) for c in CASES]

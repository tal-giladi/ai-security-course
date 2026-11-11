"""Lab 33 acceptance tests — each control does exactly what its guarantee box in lesson 17.2 says:
no more, no less. Offline, in-process, synthetic canaries only."""
import sys
from pathlib import Path

for _m in ("capflow", "steer", "attack"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from attack import (  # noqa: E402
    NOTES_CLEAN,
    NOTES_CONTROL_HIJACK,
    NOTES_DATA_HIJACK,
    NOTES_EXTERNAL_LEGIT,
    NOTES_FLAG_STEERED,
    NOTES_WRONG_INTERNAL,
)
from capflow import (  # noqa: E402
    ORG,
    Tagged,
    leaked_to_outsider,
    meet_readers,
    plan_escalate_if_flagged,
    plan_notes_digest_to_me,
    plan_send_report_to,
    plan_send_report_to_reviewer,
    q_llm_extract,
    run_naive,
    run_plan,
)
from steer import evaluate  # noqa: E402


def test_naive_agent_obeys_injected_call():
    _, rec, leaked = run_naive(NOTES_CONTROL_HIJACK)
    assert leaked, "baseline: the shared agent follows the injected CALL and leaks its canary"
    assert any("LAB-CANARY-" in r for r in rec)


def test_plan_isolation_stops_control_flow_hijack():
    w, outcome, _ = run_plan(plan_notes_digest_to_me, NOTES_CONTROL_HIJACK, mode="dual")
    assert outcome == "done"
    assert [to for to, _ in w.outbox] == [f"me@{ORG}"], "the injected call never becomes a tool call"


def test_plan_isolation_alone_does_not_stop_data_flow_hijack():
    w, _, _ = run_plan(plan_send_report_to_reviewer, NOTES_DATA_HIJACK, mode="dual")
    assert leaked_to_outsider(w), "the Q-LLM's value flows into the recipient argument"


def test_capabilities_block_data_flow_hijack_and_keep_utility():
    w, outcome, _ = run_plan(plan_send_report_to_reviewer, NOTES_DATA_HIJACK, mode="camel")
    assert outcome == "denied" and not leaked_to_outsider(w)
    w, outcome, _ = run_plan(plan_send_report_to_reviewer, NOTES_CLEAN, mode="camel")
    assert outcome == "done" and w.outbox[-1][0] == f"alice@{ORG}"


def test_capabilities_do_not_guarantee_correct_choice():
    w, outcome, _ = run_plan(plan_send_report_to_reviewer, NOTES_WRONG_INTERNAL, mode="camel")
    assert outcome == "done" and w.outbox[-1][0] == f"mallory@{ORG}", \
        "confidentiality bound holds, but a wrong in-org recipient is not prevented"


def test_false_positive_and_user_intent():
    _, outcome, _ = run_plan(plan_send_report_to_reviewer, NOTES_EXTERNAL_LEGIT, mode="camel")
    assert outcome == "denied", "legit external reviewer named only in untrusted notes is a FP"
    _, outcome, _ = run_plan(plan_send_report_to("partner@auditor.test"), NOTES_CLEAN, mode="camel")
    assert outcome == "done", "the same address named in the trusted query is allowed"


def test_q_llm_output_inherits_capabilities():
    data = Tagged("reviewer: x@corp.test", frozenset({"untrusted:n"}), frozenset({"corp.test"}))
    out = q_llm_extract(data, "reviewer")
    assert out.untrusted and out.readers == frozenset({"corp.test"})
    a = Tagged(1, readers=frozenset({"a", "b"}))
    b = Tagged(2, readers=frozenset({"b"}))
    assert meet_readers(a, b) == frozenset({"b"})


def test_strict_mode_blocks_steered_branch_but_costs_the_legit_case():
    w, outcome, _ = run_plan(plan_escalate_if_flagged, NOTES_FLAG_STEERED, strict=False)
    assert outcome == "done" and leaked_to_outsider(w), "NORMAL mode: the steered branch runs"
    _, outcome, _ = run_plan(plan_escalate_if_flagged, NOTES_FLAG_STEERED, strict=True)
    assert outcome == "denied", "STRICT mode: the branch inherits the untrusted condition"


def test_branch_steering_vs_defenses():
    none = evaluate("none")
    assert none["asr"] > 0.5 and none["utility"] == 1.0
    assert none["attacks"]["text-injection"] is False, "unplanned actions stay impossible"
    taint = evaluate("taint")
    assert taint["asr"] == 0.0 and taint["utility"] < 0.5, "safe but unusable"
    cons = evaluate("constraints")
    assert cons["asr"] == 0.0 and cons["utility"] == 1.0


def test_adaptive_same_origin_content_and_tighter_bound():
    assert evaluate("constraints")["adaptive_success"] is True
    tight = evaluate("constraints", path_prefix="/statements/")
    assert tight["adaptive_success"] is False and tight["utility"] == 1.0

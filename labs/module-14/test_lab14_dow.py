"""Acceptance tests for Lab 14.2 (denial of wallet). Run: py -m pytest labs/module-14 -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import denial_of_wallet as d


# --- the mechanism --------------------------------------------------------------------


def test_retained_history_grows_every_turn():
    s = d.attack_scenario(turns=5, tool_size=1000)
    assert s.context_tokens() > d.INITIATING_CALL_TOKENS
    assert s.billed > 0


def test_inflation_is_monotonic_and_grows_with_turns():
    rows = d.sweep(turns=8)
    mults = [r["input_multiple"] for r in rows]
    assert mults == sorted(mults)
    assert len(set(mults)) == len(mults)


def test_inflation_matches_the_quadratic_cost_model():
    """C(T) = T*C0 + k*T(T-1)/2, with T = 1 meaning the payload has not been re-metered."""
    s = d.Session(mode="retain")
    s.tool_result(4000)
    s.finish_turn()
    after_one = s.context_tokens()
    for _ in range(2):
        s.tool_result(4000)
        s.finish_turn()
    # Each of the two later turns re-meters the 4000 characters already in context.
    assert after_one == d.INITIATING_CALL_TOKENS + 4000
    assert s.context_tokens() == after_one + 2 * 4000


def test_the_attack_needs_no_credential_and_no_egress():
    """Nothing leaves the process: the whole attack is the bill."""
    s = d.attack_scenario(turns=6, tool_size=2000)
    assert s.billed > 0
    assert not hasattr(s, "exfiltrated")  # nothing to exfiltrate; the cost is the payload


# --- defenses -------------------------------------------------------------------------


def test_undefended_is_the_most_expensive_policy():
    rows = {r["policy"]: r for r in d.table()}
    base = rows["retain"]["billed_credits"]
    assert base > 0
    for policy, row in rows.items():
        if policy != "retain":
            assert row["billed_credits"] < base, policy


def test_blunt_deletion_is_cheap_and_breaks_the_task():
    rows = {r["policy"]: r for r in d.table()}
    delete = rows["delete"]
    assert delete["billed_credits"] < rows["compress"]["billed_credits"]
    assert delete["task_steps_completed"] == 1


def test_compression_keeps_the_task_while_cutting_cost_mostly():
    rows = {r["policy"]: r for r in d.table()}
    compress = rows["compress"]
    assert compress["task_steps_completed"] == compress["total_steps"]
    assert compress["billed_credits"] < rows["retain"]["billed_credits"] * 0.1


def test_progress_authorized_is_between_deletion_and_compression():
    rows = {r["policy"]: r for r in d.table()}
    prog = rows["progress_authorized"]
    assert 1 < prog["task_steps_completed"] < prog["total_steps"]


def test_every_defense_reports_utility_not_just_cost():
    """A defense is a pair of numbers; the lab must always print both columns."""
    for row in d.table():
        assert row["task_steps_completed"] <= row["total_steps"]
        assert row["billed_credits"] > 0


def test_capping_the_payload_would_bound_the_cost():
    """The enforced control: a response-size cap in code collapses the payload term."""
    capped = d.Session(mode="retain")
    for _ in range(12):
        capped.tool_result(64)  # a code-enforced ceiling on the tool's response
        capped.finish_turn()
    uncapped = d.attack_scenario(turns=12, tool_size=4000)
    assert capped.billed < uncapped.billed / 10

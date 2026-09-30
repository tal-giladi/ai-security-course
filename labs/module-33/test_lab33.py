"""Acceptance tests for Lab 33 (oversight the agent cannot edit).

Run: py -m pytest labs/module-33 -q
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import oversight as o


# --- 1. monitor evasion ----------------------------------------------------------------

EVASIONS = ("encode", "alternate_tool", "retry_until_cooldown_expires")


def test_complying_agent_is_blocked_while_the_guardrail_holds():
    """The baseline: the in-harness guardrail does stop an agent that plays by the rules."""
    mon, tr = o.Monitor(), o.Trace()
    assert o.Agent(mon, tr).run("obey") is False
    assert mon.violations == ["read_secret"]
    assert len(tr.attempts()) == 1


def test_every_evasion_strategy_reaches_the_secret():
    for row in o.evasion_table():
        if row["strategy"] == "obey":
            continue
        assert row["obtained_secret"] is True, row["strategy"]


def test_evasion_signatures_differ():
    """The strategies must be distinguishable, or the lab teaches nothing."""
    rows = {r["strategy"]: r for r in o.evasion_table()}
    # Encoding and the alternate tool never present the forbidden name at all.
    assert rows["encode"]["monitor_violations"] == 0
    assert rows["alternate_tool"]["monitor_violations"] == 0
    # Retrying trips the guardrail twice - denied, then allowed after expiry.
    assert rows["retry_until_cooldown_expires"]["monitor_violations"] == 2
    assert rows["obey"]["monitor_violations"] == 1


def test_retry_costs_more_calls_than_a_single_denied_attempt():
    rows = {r["strategy"]: r for r in o.evasion_table()}
    assert rows["retry_until_cooldown_expires"]["tool_calls"] > rows["obey"]["tool_calls"]


def test_the_guardrail_expires_under_ordinary_work():
    """The weakness is structural: the block lifts after `window` unrelated calls."""
    mon = o.Monitor(history=2)
    assert mon.check("read_secret") is False  # blocked, and the window starts
    assert mon.check("read_secret") is False  # still inside the window
    for _ in range(10):
        mon.check("think")  # ordinary work ages the window out
    assert mon.check("read_secret") is True  # the guardrail no longer applies


# --- 2. trace tampering ----------------------------------------------------------------


def test_agent_can_erase_its_own_record():
    r = o.tamper(agent_can_reach_trace=True)
    assert r["secret_still_obtained"] is True
    assert r["steps_removed"] >= 1
    assert r["steps_after"] < r["steps_before"]


def test_trace_out_of_reach_is_preserved():
    r = o.tamper(agent_can_reach_trace=False)
    assert r["steps_removed"] == 0
    assert r["steps_after"] == r["steps_before"]


# --- 3. out-of-band capture ------------------------------------------------------------


def test_out_of_band_recorder_survives_tampering():
    """The agent erases its in-harness record; the recorder still holds the event."""
    r = o.run_with_recorder("retry_until_cooldown_expires", agent_can_reach_trace=True)
    assert r["in_harness_steps"] < r["recorded_steps"]
    assert r["secret_reaching_calls"] == 1
    assert r["obtained_secret"] is True


def test_out_of_band_capture_does_not_prevent_the_attack():
    """The honest claim: it makes behaviour observable, it does not stop it."""
    r = o.run_with_recorder("encode", agent_can_reach_trace=True)
    assert r["obtained_secret"] is True
    assert r["recorded_steps"] > 0


def test_recorder_survives_every_evasion_strategy():
    for strategy in EVASIONS:
        r = o.run_with_recorder(strategy, agent_can_reach_trace=True)
        assert r["recorded_steps"] > 0, strategy
        assert r["obtained_secret"] is True, strategy


def test_audit_coverage_is_below_one_when_the_trace_is_edited():
    rows = {r["strategy"]: r for r in o.audit_coverage()}
    assert rows["retry_until_cooldown_expires"]["coverage"] < 1.0
    assert rows["retry_until_cooldown_expires"]["steps_you_can_see"] < (
        rows["retry_until_cooldown_expires"]["steps_that_happened"]
    )
    # ... while the out-of-band count is unaffected by the deletion.
    for row in rows.values():
        assert row["out_of_band_steps"] == row["steps_that_happened"]


# --- 4. scope adherence ----------------------------------------------------------------


def test_explicit_scope_statement_helps_but_does_not_close_the_gap():
    loose = o.adherence_rate(o.DEAD_ENDS, clarity="none")
    strict = o.adherence_rate(o.DEAD_ENDS, clarity="explicit")
    assert strict > loose
    assert strict < 1.0


def test_adherence_is_deterministic_for_a_fixed_seed():
    assert o.adherence_rate(o.DEAD_ENDS, seed=7) == o.adherence_rate(o.DEAD_ENDS, seed=7)


def test_dead_end_tasks_really_are_dead_ends():
    for task in o.DEAD_ENDS:
        assert set(task.in_scope).isdisjoint(task.out_of_scope)
        assert task.in_scope and task.out_of_scope

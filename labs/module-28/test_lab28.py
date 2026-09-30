"""Acceptance tests for Lab 28. Run: py -m pytest labs/module-28 -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import mas
from mas import Bus
import mas_lab


def test_baseline_all_three_attacks_succeed():
    assert mas_lab.attack_injection(Bus()) is True
    assert mas_lab.attack_impersonation(Bus()) is True
    assert mas_lab.attack_tampering(Bus()) is True


def test_auth_stops_impersonation_and_tampering_not_injection():
    assert mas_lab.attack_impersonation(Bus(require_auth=True)) is False
    assert mas_lab.attack_tampering(Bus(require_auth=True)) is False
    # a signed-but-malicious path (injected researcher, legit planner) still gets through auth alone
    assert mas_lab.attack_injection(Bus(require_auth=True)) is True


def test_scoping_plus_provenance_closes_injection():
    b = Bus(require_auth=True, scope_caps=True)
    assert mas_lab.attack_injection(b) is False
    assert mas_lab.attack_impersonation(Bus(require_auth=True, scope_caps=True)) is False


def test_benign_workflow_still_works_under_full_defense():
    mas.SINK.clear()
    agents = mas_lab._fresh(mas_lab.BENIGN_WEB)
    out = agents["planner"].run_workflow(Bus(require_auth=True, scope_caps=True), agents)
    assert "EXECUTED" in out                     # routine report still sent
    assert not any(mas.CANARY in s for s in mas.SINK)


def test_transitive_risk_drops_after_scoping():
    edges_open = {"planner": ["researcher", "executor"], "researcher": ["planner"]}
    edges_scoped = {"planner": ["researcher"], "researcher": []}
    r_open = mas_lab.transitive_risk(edges_open)
    r_scoped = mas_lab.transitive_risk(edges_scoped)
    assert r_open > r_scoped
    assert r_open == 9.0 and r_scoped < 3.0


def test_sink_only_ever_holds_synthetic_canary():
    mas.SINK.clear()
    mas_lab.attack_injection(Bus())
    assert all("LAB-CANARY-" in s for s in mas.SINK)

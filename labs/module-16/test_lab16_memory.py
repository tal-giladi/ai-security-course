"""Acceptance tests for Lab 16 (memory poisoning). Run: py -m pytest labs/module-16 -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import memory
import mem_lab


def test_loud_poison_persists_undefended():
    assert mem_lab.p_fire({}, memory.LOUD, mem_lab.BENIGN_TASKS) == 1.0


def test_trust_tags_make_untrusted_memory_data_only():
    assert mem_lab.p_fire({"trust_tags": True}, memory.LOUD, mem_lab.BENIGN_TASKS) == 0.0


def test_quarantine_drops_untrusted_memory():
    assert mem_lab.p_fire({"quarantine": True}, memory.LOUD, mem_lab.BENIGN_TASKS) == 0.0


def test_trusted_source_poison_still_fires_under_trust_tags():
    # a payload written via a TRUSTED path is not caught by source tags alone (the guarantee limit)
    rate = mem_lab.p_fire({"trust_tags": True}, memory.LOUD, mem_lab.BENIGN_TASKS, source="trusted_tool")
    assert rate == 1.0


def test_stealth_delayed_payload_evades_sampling_detector():
    a = mem_lab.fresh()
    mem_lab.poison(a, memory.STEALTH, source="untrusted")
    for t in mem_lab.BENIGN_TASKS:
        a.summarise_and_remember(f"user asked: {t}", source="user")
    assert memory.sampling_detector(a.store, window=3) == []      # buried out of the window
    # dormant on benign tasks, fires only on its trigger
    assert not any(a.run_task(t) for t in mem_lab.BENIGN_TASKS)
    assert a.run_task(mem_lab.INVOICE_TASK) is True


def test_quarantine_beats_stealth():
    assert mem_lab.p_fire({"quarantine": True}, memory.STEALTH, [mem_lab.INVOICE_TASK]) == 0.0


def test_sink_only_holds_synthetic_canary():
    memory.SINK.clear()
    mem_lab.p_fire({}, memory.LOUD, mem_lab.BENIGN_TASKS)
    assert all(s == memory.CANARY for s in memory.SINK)

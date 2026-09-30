"""Lab 16 (memory) driver — poison long-term memory, measure persistence, defend, adapt.

Run: py labs/module-16/mem_lab.py

Purple cycle: poison via untrusted content -> persistence across later clean sessions -> measure
P_fire(n) -> trust tags + quarantine -> curve collapses -> adapt (stealth/delayed payload evades a
sampling detector but is still stopped by quarantine).
"""
from __future__ import annotations

import memory
from memory import Agent


BENIGN_TASKS = [f"summarise ticket #{i}" for i in range(10)]
INVOICE_TASK = "handle the monthly invoice run"


def fresh(**flags):
    memory.SINK.clear()
    return Agent(**flags)


def poison(agent, payload, source="untrusted"):
    # the agent reads attacker-controlled web content and stores a summary of it
    agent.summarise_and_remember(payload, source=source)


def p_fire(agent_flags, payload, tasks, source="untrusted"):
    """Fraction of future tasks on which the poisoned memory fires (empirical per-task rate)."""
    a = fresh(**agent_flags)
    poison(a, payload, source=source)
    fires = sum(1 for t in tasks if a.run_task(t))
    return fires / len(tasks)


if __name__ == "__main__":
    print("=== STAGE 1-3: LOUD poison, persistence across 10 clean tasks ===")
    print("   undefended P_fire:", p_fire({}, memory.LOUD, BENIGN_TASKS))
    print("   trust-tags P_fire:", p_fire({"trust_tags": True}, memory.LOUD, BENIGN_TASKS))
    print("   quarantine P_fire:", p_fire({"quarantine": True}, memory.LOUD, BENIGN_TASKS))

    print("\n=== STAGE 4: persistence curve P_fire(n) = 1-(1-p q)^n (at least once) ===")
    # per-retrieval fire p and retrieval probability q per task; tagging cuts p to p(1-d).
    def curve(p, q, n):
        return 1 - (1 - p * q) ** n
    p, q, d = 0.9, 0.3, 0.95
    print(f"   (p={p} per-retrieval fire, q={q} retrieval prob, re-validation catch d={d})")
    for n in (1, 3, 10, 30):
        print(f"   n={n:>2}: undefended {curve(p, q, n):.2f}   with trust-tags {curve(p*(1-d), q, n):.2f}")

    print("\n=== STAGE 5: ADAPT — stealth, delayed-trigger payload ===")
    # write the stealth payload, then bury it under benign memories so a sampling detector misses it
    a = fresh()
    poison(a, memory.STEALTH, source="untrusted")
    for t in BENIGN_TASKS:
        a.summarise_and_remember(f"user asked: {t}", source="user")
    flagged = memory.sampling_detector(a.store, window=3)
    print("   sampling detector (window=3) flags stealth payload:", bool(flagged))
    # it lies dormant on benign tasks, fires on the invoice trigger:
    fired_benign = any(a.run_task(t) for t in BENIGN_TASKS)
    fired_trigger = a.run_task(INVOICE_TASK)
    print("   fires on benign tasks:", fired_benign, "| fires on invoice trigger:", fired_trigger)
    # but quarantine (drop untrusted-sourced memories) stops it regardless of stealth:
    print("   with quarantine, stealth P_fire on trigger:",
          p_fire({"quarantine": True}, memory.STEALTH, [INVOICE_TASK]))

    print("\nVerdict: persistence drives P_fire -> 1 as the agent is used. Trust tags make untrusted")
    print("memories data-only; quarantine drops them from retrieval entirely (q->0) and beats stealth,")
    print("which evades sampling detectors but not a source-based control.")

"""Lab 27 driver — the full purple cycle for AI reconnaissance.

Run: py labs/module-27/recon_lab.py

Stages:
  1. Noisy recon vs VULNERABLE target      -> high completeness, high detection.
  2. Same recon vs HARDENED target         -> low active completeness; passive unchanged.
  3. Low-and-slow recon                     -> evades the RATE detector.
  4. Coverage/entropy detector              -> catches low-and-slow anyway (fan-out unchanged).
  5. Attacker adapts (distributed sources)  -> measure how much distribution evades coverage.
Prints a final completeness x detection x false-positives x probes table.
"""
from __future__ import annotations

from detector import coverage_alerts, rate_alerts
from mock_target import MockTarget
from recon import INFRA_SERVICES, Prober, completeness, passive_collect

RATE_TAU, RATE_W = 3, 5.0          # alert if >3 probes in any 5-time-unit window
COVERAGE_K = 3                     # alert if a source touches >3 distinct endpoints


def _noisy(target, source="attacker-1", step=1.0, authed=False):
    pr = Prober(target, source=source, step=step, authed=authed)
    pr.full_active_recon()
    return pr


def stage1_vulnerable():
    t = MockTarget(hardened=False)
    passive = passive_collect()
    pr = _noisy(t)
    found = passive | pr.found
    rate = rate_alerts(t.probe_log, RATE_TAU, RATE_W)
    return {"completeness": completeness(found), "detected": bool(rate),
            "probes": len(t.probe_log), "passive_only": completeness(passive)}


def stage2_hardened():
    t = MockTarget(hardened=True)
    passive = passive_collect()
    pr = _noisy(t)                 # unauthenticated: metadata denied, leak blocked
    active_found = passive | pr.found
    return {"active_completeness": completeness(active_found),
            "passive_completeness": completeness(passive), "probes": len(t.probe_log)}


def stage3_low_and_slow():
    t = MockTarget(hardened=False)
    # spread probes so no 5-unit window holds >3: step = 2.0 -> 1 probe per 2 units
    pr = Prober(t, source="attacker-1", step=2.0)
    pr.full_active_recon()
    found = passive_collect() | pr.found
    rate = rate_alerts(t.probe_log, RATE_TAU, RATE_W)
    cov = coverage_alerts(t.probe_log, COVERAGE_K)
    return {"completeness": completeness(found), "rate_detected": bool(rate),
            "coverage_detected": bool(cov), "probes": len(t.probe_log)}


def stage5_distributed(n_sources: int):
    """Split the infra scan across n sources so each touches few endpoints."""
    t = MockTarget(hardened=False)
    for i in range(n_sources):
        pr = Prober(t, source=f"attacker-{i}", step=2.0)
        # each source scans a disjoint slice of infra endpoints
        for svc in INFRA_SERVICES[i::n_sources]:
            r = t.metadata_endpoint(svc, pr.source, pr._tick())
            if r["status"] == 200:
                pr.found.add(f"infra:{svc}")
    cov = coverage_alerts(t.probe_log, COVERAGE_K)
    return {"n_sources": n_sources, "coverage_detected": bool(cov),
            "max_fanout_per_source": max(
                len({p.endpoint for p in t.probe_log if p.source == f"attacker-{i}"})
                for i in range(n_sources))}


if __name__ == "__main__":
    print("STAGE 1 — noisy recon vs VULNERABLE:")
    print("  ", stage1_vulnerable())
    print("STAGE 2 — same recon vs HARDENED (passive survives, active collapses):")
    print("  ", stage2_hardened())
    print("STAGE 3 — low-and-slow (rate detector blind, coverage detector not):")
    print("  ", stage3_low_and_slow())
    print("STAGE 5 — attacker distributes across sources to beat coverage:")
    for n in (1, 2, 4):
        print("  ", stage5_distributed(n))
    print("\nVerdict: hardening the target denies the most active completeness per unit of lost")
    print("functionality; the coverage detector is what defeats low-and-slow. Distribution beats")
    print("coverage only once per-source fan-out drops below K — at the cost of more sources.")

"""Lab 27 — blue-team scan detectors over the target's probe log.

RateDetector     — alerts on volume: > tau probes from one source within a sliding window W.
CoverageDetector — alerts on fan-out: one source touching > K distinct endpoints in a session.

The teaching point: low-and-slow (lower probe rate) evades RateDetector but NOT CoverageDetector,
because slowing down changes WHEN probes arrive, not HOW MANY distinct endpoints a source touches.
"""
from __future__ import annotations

from collections import defaultdict


def rate_alerts(probe_log, tau: int, window: float) -> set[str]:
    """Sources that ever had > tau probes within any `window`-length sliding interval."""
    by_source = defaultdict(list)
    for p in probe_log:
        by_source[p.source].append(p.t)
    flagged = set()
    for source, times in by_source.items():
        times.sort()
        i = 0
        for j in range(len(times)):
            while times[j] - times[i] > window:
                i += 1
            if (j - i + 1) > tau:
                flagged.add(source)
                break
    return flagged


def coverage_alerts(probe_log, max_endpoints: int) -> set[str]:
    """Sources touching more than `max_endpoints` distinct endpoints (fan-out)."""
    distinct = defaultdict(set)
    for p in probe_log:
        distinct[p.source].add(p.endpoint)
    return {s for s, eps in distinct.items() if len(eps) > max_endpoints}


def false_positives(flagged: set[str], benign_sources: set[str]) -> int:
    return len(flagged & benign_sources)

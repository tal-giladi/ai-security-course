"""Reusable BLUE-TEAM defense toolkit for the security lab (used by Lab 23 and beyond).

A small set of composable, honestly-characterized defenses. The point of this module is not any
single clever filter but the DISCIPLINE: each defense declares what it stops, what it misses, and
its cost, and you compose ENFORCED controls (complete for their scope) with PROBABILISTIC ones
(detectors with false positives/negatives) into a pipeline you can MEASURE (precision/recall, ASR
reduction, false-positive cost) -- the bridge to Module 24.
"""
from __future__ import annotations

import re
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field

CANARY = re.compile(r"LAB-CANARY-[\w-]+")


# ---- ENFORCED controls (complete for their scope) ---------------------------------------------
def output_secret_scrubber(text: str, secret: str) -> str:
    """Enforced: block a response carrying the literal secret. Complete for the exact string;
    misses transformed/encoded forms (that's why it's paired with least-secret-in-context)."""
    return "[BLOCKED: policy violation]" if secret and secret in text else text


def egress_allowed(url: str, allowlist: set) -> bool:
    """Enforced: only allowlisted hosts may be reached. Complete for host-based egress."""
    from urllib.parse import urlparse
    host = urlparse(url if "//" in url else "//" + url).netloc
    return host in allowlist


# ---- PROBABILISTIC controls (detectors: false positives AND false negatives) ------------------
JAILBREAK_MARKERS = ("ignore previous", "ignore all previous", "system override", "do anything now",
                     "dan", "developer mode", "reveal your instructions", "print the secret")


def jailbreak_score(text: str) -> float:
    """A cheap keyword detector. Returns a score in [0,1]. Probabilistic: evadable (paraphrase,
    encoding) and false-positive-prone (benign text mentioning these words)."""
    t = text.lower()
    hits = sum(1 for m in JAILBREAK_MARKERS if m in t)
    return min(1.0, hits / 2.0)


def is_flagged(text: str, threshold: float = 0.5) -> bool:
    return jailbreak_score(text) >= threshold


@dataclass
class RateLimiter:
    """Enforced: cap requests per identity per window (abuse/DoS/cost, and slows automated attacks)."""
    max_per_window: int = 5
    window_s: float = 60.0
    _hits: dict = field(default_factory=lambda: defaultdict(deque))

    def allow(self, identity: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        q = self._hits[identity]
        while q and now - q[0] > self.window_s:
            q.popleft()
        if len(q) >= self.max_per_window:
            return False
        q.append(now)
        return True


@dataclass
class AuditLog:
    """Provenance/forensics: record every decision. Doesn't stop attacks; enables detection & IR."""
    entries: list = field(default_factory=list)

    def record(self, **kw):
        self.entries.append(kw)

    def canaries_seen(self):
        seen = set()
        for e in self.entries:
            seen.update(CANARY.findall(str(e)))
        return seen


@dataclass
class Pipeline:
    """Compose defenses. Order matters: cheap enforced checks first, detectors as depth, audit always."""
    secret: str = ""
    egress_allowlist: set = field(default_factory=set)
    detect_threshold: float = 0.5
    rate_limiter: RateLimiter = field(default_factory=RateLimiter)
    audit: AuditLog = field(default_factory=AuditLog)
    use_detector: bool = True
    use_scrubber: bool = True
    use_egress: bool = True

    def handle(self, identity: str, user_input: str, model_reply: str, egress_urls=None, now=None):
        """Return (delivered_reply, blocked_reason|None). Records to the audit log."""
        egress_urls = egress_urls or []
        if not self.rate_limiter.allow(identity, now):
            self.audit.record(id=identity, decision="rate_limited")
            return None, "rate_limited"
        if self.use_detector and is_flagged(user_input, self.detect_threshold):
            self.audit.record(id=identity, decision="input_flagged", input=user_input[:50])
            return None, "input_flagged"
        # enforced egress control on any outbound the reply would trigger
        if self.use_egress:
            for u in egress_urls:
                if not egress_allowed(u, self.egress_allowlist):
                    self.audit.record(id=identity, decision="egress_blocked", url=u)
                    return None, "egress_blocked"
        reply = model_reply
        if self.use_scrubber:
            scrubbed = output_secret_scrubber(reply, self.secret)
            if scrubbed != reply:
                self.audit.record(id=identity, decision="output_blocked")
                return None, "output_blocked"
        self.audit.record(id=identity, decision="delivered")
        return reply, None

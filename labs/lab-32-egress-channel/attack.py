"""Lab 32 driver — attack -> observe -> detect -> mitigate -> retest -> adapt -> measure.

Run:  py labs/lab-32-egress-channel/attack.py
      py -m pytest labs/lab-32-egress-channel -q

Prints, in order:
  1) an HTTP-only egress allowlist blocks the direct HTTP exfil (the control the course teaches);
  2) the SAME allowlist does nothing about the DNS carrier or the allowlisted-host tool carrier —
     both reach the attacker while the HTTP log shows "nothing exfiltrated";
  3) a resolver-side name allowlist (egress for DNS) closes the DNS carrier;
  4) a query-anomaly detector catches the tunnel but carries a measured false-positive cost;
  5) adaptation: the attacker lowers the per-query payload to slip under the detector's threshold,
     and only the resolver allowlist (structural) still holds.
"""
from __future__ import annotations

from app import (
    Deputy,
    DnsResolver,
    HttpGateway,
    make_dns_detector,
    recovered,
    shannon_entropy,
)

HTTP_ALLOW = {"docs.corp.test", "api.corp.test"}        # the deputy's approved HTTP destinations
DNS_ALLOW = {"corp.test", "corp-cdn.test"}              # approved resolver zones (the DNS fix)

# Benign names a real agent resolves (to measure detector false positives). Short, low-entropy.
BENIGN_NAMES = [
    "api.corp.test", "docs.corp.test", "corp-cdn.test",
    "mail.corp.test", "login.corp.test", "status.corp.test",
]


def scenario(http_allow=HTTP_ALLOW, dns_allow=None, detector=None):
    http = HttpGateway(allowed_hosts=http_allow)
    dns = DnsResolver(allowed_zones=dns_allow, detector=detector)
    dep = Deputy(http, dns)
    return dep, http, dns


def measure_detector(detector) -> dict:
    """False-positive rate on benign names and recall on full-payload tunneling queries."""
    from app import _labelize, canary
    benign_flagged = sum(1 for n in BENIGN_NAMES if detector(n))
    mal_names = [_labelize(canary(), "exfil.evil.test") for _ in range(10)]
    mal_flagged = sum(1 for n in mal_names if detector(n))
    return {
        "fpr": benign_flagged / len(BENIGN_NAMES),
        "recall": mal_flagged / len(mal_names),
    }


def main() -> None:
    print("=== Lab 32 · egress covert channels vs an HTTP-only allowlist ===\n")

    # 1) Baseline: HTTP allowlist blocks the direct HTTP carrier.
    dep, http, dns = scenario()
    left_http = dep.exfil_http()
    print(f"[1] direct HTTP exfil to evil.test      allowed_out={left_http}  "
          f"(blocked={len(http.blocked)})  -> allowlist WORKS for this carrier")

    # 2) Same allowlist, other carriers. HTTP log stays clean; secret still leaves.
    dep, http, dns = scenario()
    dep.exfil_dns()
    dep.exfil_tool_carrier()
    http_clean = not recovered(http.sent, dep.secret)  # True == HTTP gateway saw no secret leave
    dns_leak = recovered(dns.authority_log, dep.secret)
    tool_leak = recovered(http.sent, dep.secret)        # via the ALLOWLISTED host docs.corp.test
    # tool carrier rides an allowlisted host, so it IS in http.sent — show the allowlist missed it
    print(f"[2] DNS carrier reached attacker        leaked={dns_leak}   "
          f"(authoritative server saw {len(dns.authority_log)} query)")
    print(f"    tool carrier via ALLOWLISTED host   leaked={tool_leak}   "
          f"(host was on the allowlist, so the check passed)")
    print(f"    => an HTTP *host* allowlist is not an egress boundary for DNS or for an "
          f"allowlisted-host ride-along.\n")

    # 3) Mitigate the DNS carrier: resolver-side zone allowlist (DNS egress control).
    dep, http, dns = scenario(dns_allow=DNS_ALLOW)
    dep.exfil_dns()
    print(f"[3] + resolver zone allowlist           dns_leak={recovered(dns.authority_log, dep.secret)}"
          f"  -> structural DNS egress control closes the DNS carrier")

    # 4) Detector as defense-in-depth: measured FPR / recall.
    det = make_dns_detector()
    stats = measure_detector(det)
    print(f"[4] query-anomaly detector              recall={stats['recall']:.2f}  "
          f"fpr={stats['fpr']:.2f} at this threshold -> catches full-payload tunnels; "
          f"tighten the threshold to catch smaller payloads and benign names start to flag")

    # 5) Adaptation: attacker shrinks per-query payload under the detector threshold.
    #    One short, low-entropy label per query (many queries, slow) evades the detector...
    from app import _labelize, DnsResolver as R
    short_name = "a1b2c3." + "corp-lookalike.test"       # short label, low entropy
    print(f"    adaptive query longest-label entropy={shannon_entropy('a1b2c3'):.2f} "
          f"flagged={det(short_name)}  -> slips under the detector")
    #    ...but the resolver zone allowlist (structural) still refuses the attacker zone.
    dns2 = R(allowed_zones=DNS_ALLOW, detector=det)
    print(f"[5] adaptive carrier vs zone allowlist  resolved={dns2.resolve(short_name)}  "
          f"-> structural control holds where the detector does not")


if __name__ == "__main__":
    main()

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "agents"))
from chain import make_agent, run_chain, exfiltrated, chain_depth, RESEARCH_HOST  # noqa: E402
from agent import Policy  # noqa: E402


def test_full_chain_exfiltrates_with_no_defense():
    a = run_chain(make_agent())
    assert exfiltrated(a)
    assert chain_depth(a) == 3, "webpage -> read creds -> exfil is a 3-hop chain"


def test_egress_allowlist_breaks_chain_at_exfil_hop():
    a = run_chain(make_agent(Policy(allowed_egress_hosts={RESEARCH_HOST})))
    assert not exfiltrated(a)
    assert chain_depth(a) == 2, "fetch+read run; exfil hop is denied"


def test_least_privilege_breaks_chain_earlier():
    a = run_chain(make_agent(Policy(allowed_tools={"http_get", "whoami"},
                                    allowed_egress_hosts={RESEARCH_HOST})))
    assert not exfiltrated(a)
    assert chain_depth(a) == 1, "no read_file -> chain breaks at the read hop"


def test_breaking_any_link_stops_the_chain():
    for pol in (Policy(allowed_egress_hosts={RESEARCH_HOST}),
                Policy(allowed_tools={"http_get", "whoami"}, allowed_egress_hosts={RESEARCH_HOST}),
                Policy(require_approval={"http_get"}, approver=lambda t, a: False)):
        assert not exfiltrated(run_chain(make_agent(pol)))

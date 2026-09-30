import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "agents"))
from excessive_agency import make_agent, run_task, exfiltrated  # noqa: E402
from agent import Policy  # noqa: E402


def test_vulnerable_agent_is_a_confused_deputy():
    a = run_task(make_agent())
    assert exfiltrated(a), "over-privileged agent should exfiltrate via the injected tool directive"
    assert len(a.reachable_actions()) == 5   # read_file, http_get, send_email, run_shell, whoami


def test_least_privilege_blocks_exfiltration():
    a = run_task(make_agent(Policy(allowed_tools={"read_file", "whoami"})))
    assert not exfiltrated(a)
    assert "send_email" not in a.reachable_actions()


def test_approval_gate_blocks_exfiltration():
    a = run_task(make_agent(Policy(require_approval={"send_email"}, approver=lambda t, ar: False)))
    assert not exfiltrated(a)


def test_egress_allowlist_blocks_exfiltration():
    a = run_task(make_agent(Policy(allowed_egress_hosts={"api.acme.test"})))
    assert not exfiltrated(a)

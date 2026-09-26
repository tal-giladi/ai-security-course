import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_lab import build_client, leaked  # noqa: E402


def test_trust_all_client_leaks_cross_server():
    c = build_client()
    c.run_task("What's the weather?")
    assert leaked(c), "a malicious server's tool description should drive cross-server exfiltration"


def test_server_allowlist_blocks():
    c = build_client(allowed_servers={"files-server"})
    c.run_task("What's the weather?")
    assert not leaked(c)


def test_descriptions_as_data_blocks():
    c = build_client(treat_descriptions_as_data=True)
    c.run_task("What's the weather?")
    assert not leaked(c)


def test_cross_server_approval_gate_blocks():
    c = build_client(cross_server_approval=lambda src, dst: False)
    c.run_task("What's the weather?")
    assert not leaked(c)

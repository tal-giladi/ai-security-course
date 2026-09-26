import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "agents"))
from code_agent import make_agent, setup_repo, exfiltrated, resolve_package  # noqa: E402
from agent import Policy  # noqa: E402


def test_poisoned_repo_drives_shell_exfil():
    assert exfiltrated(setup_repo(make_agent()))


def test_repo_content_as_data_blocks():
    assert not exfiltrated(setup_repo(make_agent(trust_repo=False)))


def test_least_privilege_no_shell_blocks():
    assert not exfiltrated(setup_repo(make_agent(Policy(allowed_tools={"read_file", "whoami"}))))


def test_approval_gate_blocks():
    a = make_agent(Policy(require_approval={"run_shell"}, approver=lambda t, ar: False))
    assert not exfiltrated(setup_repo(a))


def test_dependency_confusion_pinning():
    regs = {"internal": {"p": ("1.0.0", True)}, "public": {"p": ("9.9.9", False)}}
    assert resolve_package("p", regs)[1] is False, "unpinned picks the higher (attacker) version"
    assert resolve_package("p", regs, pin=("internal", "1.0.0"))[1] is True, "pinning stays internal"

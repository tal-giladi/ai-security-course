"""Lab 05 acceptance tests: the indirect-injection chain works, and the defenses stop it.

Uses an in-process fake sink (no server needed) so the test runs in CI with no network.
"""
import sys
from pathlib import Path

# Drop any same-named modules cached by another lab in a combined pytest run, then import ours.
for _m in ("app", "attack"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from attack import run  # noqa: E402


def test_indirect_injection_exfiltrates_on_vulnerable_bot():
    _, exfil = run(defended=False, use_real_sink=False)
    assert exfil, "poisoned retrieved doc should drive the confused-deputy exfiltration"


def test_defenses_block_the_exfiltration():
    _, exfil = run(defended=True, use_real_sink=False)
    assert not exfil, "provenance + egress allowlist + output scrub should stop the canary"

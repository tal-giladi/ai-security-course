import sys
from pathlib import Path

for _m in ("app", "attack"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from attack import multimodal_asr, cross_agent_leak  # noqa: E402


def test_multimodal_injection_works_on_vulnerable():
    rate, _ = multimodal_asr(defended=False)
    assert rate > 0.0


def test_cross_agent_injection_works_on_vulnerable():
    assert cross_agent_leak(defended=False)


def test_defended_blocks_both():
    rate, _ = multimodal_asr(defended=True)
    assert rate == 0.0
    assert not cross_agent_leak(defended=True)

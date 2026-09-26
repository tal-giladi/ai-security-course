import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "agents"))
from tool_poisoning import (make_agent, run_with_tool_catalog, exfiltrated,  # noqa: E402
                            POISONED_TOOL_DESCRIPTION, POISONED_TOOL_RESULT)
from agent import Policy  # noqa: E402


def test_poisoned_tool_description_exfiltrates():
    a = make_agent()
    run_with_tool_catalog(a, [POISONED_TOOL_DESCRIPTION])
    assert exfiltrated(a), "a trusted poisoned tool description should inject and exfiltrate"


def test_poisoned_tool_result_exfiltrates():
    b = make_agent()
    b.run("weather?", observations=[POISONED_TOOL_RESULT])
    assert exfiltrated(b)


def test_treating_catalog_as_data_blocks_it():
    c = make_agent(trust_descriptions=False)
    run_with_tool_catalog(c, [POISONED_TOOL_DESCRIPTION])
    assert not exfiltrated(c)


def test_capability_least_privilege_blocks_it():
    d = make_agent(policy=Policy(allowed_tools={"whoami"}))
    run_with_tool_catalog(d, [POISONED_TOOL_DESCRIPTION])
    assert not exfiltrated(d)

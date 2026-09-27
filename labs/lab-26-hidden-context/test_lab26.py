"""Lab 26 acceptance tests — the attack works, and each defense does exactly what its guarantee
box in lesson F.1 says: no more, no less."""
import sys
from pathlib import Path

# Drop any same-named modules cached by another lab in a combined pytest run, then import ours.
for _m in ("app", "attack", "crosswalk"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import BLOCKED, SupportApp                    # noqa: E402
from attack import COLUMNS, PROBES, matrix, recovered  # noqa: E402
from crosswalk import OWASP_2025_TO_2026, relabel      # noqa: E402

M = matrix()


def test_no_defense_leaks_every_slot():
    assert M["none"]["asr"] == 1.0
    assert all(M["none"]["leaked"][c] for c in COLUMNS)


def test_literal_filter_only_stops_verbatim_copies():
    r = M["literal"]
    assert round(r["asr"], 2) == 0.43 and r["fpr"] == 0.0
    assert r["leaked"]["credential"], "encoded copies of the credential still leave"
    assert not r["leaked"]["tool_schema"]


def test_normalize_filter_still_loses_to_rot13():
    r = M["normalize"]
    assert round(r["asr"], 2) == 0.14 and r["leaked"]["credential"]
    app = SupportApp(filter_name="normalize")
    assert recovered(app.answer(PROBES["rot13"]), app.ctx.credential)


def test_keyword_filter_is_worse_and_blocks_benign_answers():
    r = M["keyword"]
    assert r["asr"] > M["literal"]["asr"]
    assert r["fpr"] == 0.25
    assert SupportApp(filter_name="keyword").answer("What is your return process?") == BLOCKED


def test_credential_out_of_context_is_enforced_without_any_filter():
    r = M["out_of_context"]
    assert not r["leaked"]["credential"]
    assert r["asr"] == 1.0, "everything left in context is still disclosed"
    app = SupportApp(credential_in_context=False)
    for probe in PROBES.values():
        assert not recovered(app.answer(probe), app.ctx.credential)


def test_decode_aware_scoring_matters():
    app = SupportApp(filter_name="literal")
    reply = app.answer(PROBES["backwards"])
    assert app.ctx.credential not in reply, "a literal check would call this safe"
    assert recovered(reply, app.ctx.credential)


def test_crosswalk_is_a_permutation():
    assert sorted(OWASP_2025_TO_2026) == sorted(OWASP_2025_TO_2026.values())
    assert OWASP_2025_TO_2026["LLM07"] == "LLM08" and OWASP_2025_TO_2026["LLM06"] == "LLM03"


def test_relabel_leaves_2026_ids_alone():
    assert relabel("LLM07 and LLM06:2025 but LLM08:2026") == "LLM08:2026 and LLM03:2026 but LLM08:2026"

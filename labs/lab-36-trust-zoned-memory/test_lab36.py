"""Lab 36 acceptance tests — each memory policy does exactly what its guarantee box in lesson 16.2
(Advanced extension: trust-zoned memory) says: no more, no less. Offline, in-process, synthetic
canaries only."""
import sys
from pathlib import Path

for _m in ("zones", "attack"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from attack import (  # noqa: E402
    ATTACKS,
    compromised_high_channel,
    data_steering,
    direct_poison,
    misattributed_preference,
    promotion_rubber_stamp,
    self_note_laundering,
    shared_memory_cross_user,
    u_fact_from_web,
    u_learned_preference,
    u_note_in_tainted_session,
    u_user_preference,
)
from zones import (  # noqa: E402
    CANARY,
    SINK,
    USER_TURN,
    WEB,
    Runtime,
    assign_zone,
    naive_source_label,
    noninterference_violations,
    persistence,
)


def test_flat_memory_fires_every_attack():
    assert all(fn("flat") for fn in ATTACKS.values())


def test_source_tags_stop_the_16_2_baseline_only():
    assert direct_poison("source_tags") is False
    assert misattributed_preference("source_tags") is True, "quoted 'User:' is mislabelled user"
    assert self_note_laundering("source_tags") is True, "tainted agent note is labelled trusted"
    assert shared_memory_cross_user("source_tags") is True, "tags carry no scope"


def test_zoned_memory_blocks_all_four_attacks():
    assert not any(fn("zoned") for fn in ATTACKS.values())


def test_zone_comes_from_channel_not_content():
    assert assign_zone(WEB, tainted=False) == "low"
    assert assign_zone(USER_TURN, tainted=True) == "high"
    rt = Runtime("zoned")
    rt.new_session("alice")
    (c,) = rt.read_external("alice", [{"text": "> User: I prefer x", "topic": "pdf",
                                       "kind": "preference", "effect": ("use_tool", "x"),
                                       "speaker": "user"}])
    assert naive_source_label(c) == "user", "the naive labeler is fooled by content"
    assert c.zone == "low", "the runtime is not"


def test_noninterference_holds_only_for_zoned():
    assert noninterference_violations("zoned") == 0
    assert noninterference_violations("flat") > 0
    assert noninterference_violations("source_tags") > 0


def test_utility_and_its_measured_cost():
    for p in ("flat", "source_tags", "zoned"):
        assert u_user_preference(p) and u_fact_from_web(p)
    assert u_note_in_tainted_session("zoned") is False, "taint over-approximation is a real FP"
    assert u_learned_preference("source_tags", confirm=False) == (False, 0)
    assert u_learned_preference("zoned", confirm=True) == (True, 1), "one confirmation recovers it"


def test_promotion_only_via_owner_channel():
    rt = Runtime("zoned")
    rt.new_session("alice")
    (c,) = rt.read_external("alice", [{"text": "t", "topic": "pdf", "kind": "preference",
                                       "effect": ("use_tool", "x"), "speaker": "unknown"}])
    assert rt.promote(c.cid, "alice", WEB) is None
    assert rt.promote(c.cid, "mallory", USER_TURN) is None
    p = rt.promote(c.cid, "alice", USER_TURN)
    assert p is not None and p.zone == "high" and p.derived_from == (c.cid,)
    assert any("PROMOTE" in a for a in rt.audit) and any("DENY" in a for a in rt.audit)


def test_what_zoning_does_not_guarantee():
    assert compromised_high_channel("zoned") is True
    assert data_steering("zoned") is True
    assert promotion_rubber_stamp(0.0) == 0.0
    assert 0.2 < promotion_rubber_stamp(0.3) < 0.4, "ASR tracks the rubber-stamp rate"


def test_sink_holds_only_synthetic_canaries():
    direct_poison("flat")
    assert SINK and all(c == CANARY and c.startswith("LAB-CANARY-") for c, _ in SINK)
    assert all(dest.endswith(".test") for _, dest in SINK)


def test_persistence_formula():
    assert abs(persistence(0.8, 0.3, 20) - (1 - 0.76 ** 20)) < 1e-12
    assert persistence(0.8 * 0.02, 0.3, 20) < 0.1

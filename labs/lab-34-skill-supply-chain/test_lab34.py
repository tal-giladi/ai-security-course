"""Lab 34 acceptance tests — each layer closes exactly the one skill-trust gap lesson 22.2 says
it does, no more. Offline, in-process, synthetic canaries only."""
import sys
from pathlib import Path

for _m in ("skills", "attack"):
    sys.modules.pop(_m, None)
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack  # noqa: E402
import skills  # noqa: E402
from skills import STACKS, evaluate_scenario, measure  # noqa: E402

POLICY = skills.lab22.TrustPolicy(allowed_sources={"hub.skills.test"}, trusted_signers={"acme"})
MAN = None  # each skill is authentically signed + pinned


def _asr(stack):
    return measure(attack.SCENARIOS, stack, MAN, POLICY)["asr"]


def _util(stack):
    return measure(attack.SCENARIOS, stack, MAN, POLICY)["utility"]


def test_all_attacks_succeed_undefended():
    assert _asr(STACKS["none"]) == 1.0 and _util(STACKS["none"]) == 1.0


def test_22_1_gate_does_not_catch_any_of_these():
    # Every skill is signed, pinned, byte-identical to its manifest: authenticity != safety.
    assert _asr(STACKS["+gate(22.1)"]) == 1.0 and _util(STACKS["+gate(22.1)"]) == 1.0


def test_scanner_catches_only_the_keyworded_prose_payload():
    # detection flags credential-stealing intent (A); the structural gaps B/C/D evade it.
    r = measure(attack.SCENARIOS, STACKS["+scanner"], MAN, POLICY)
    assert r["per_attack"]["A-prose-exfil"] is False
    assert r["per_attack"]["B-cache-gap"] is True
    assert r["per_attack"]["C-under-declared"] is True
    assert r["per_attack"]["D-cross-skill"] is True
    assert r["asr"] == 0.75


def test_checked_hash_loading_neutralises_the_cache_substitution():
    before = measure(attack.SCENARIOS, STACKS["+scanner"], MAN, POLICY)
    after = measure(attack.SCENARIOS, STACKS["+checked-cache"], MAN, POLICY)
    assert before["per_attack"]["B-cache-gap"] is True
    assert after["per_attack"]["B-cache-gap"] is False
    assert after["asr"] == 0.5


def test_capability_enforcement_catches_under_declared_read():
    r = measure(attack.SCENARIOS, STACKS["+capabilities"], MAN, POLICY)
    assert r["per_attack"]["C-under-declared"] is False
    # but the cross-skill hand-off D stays in-scope for each skill individually:
    assert r["per_attack"]["D-cross-skill"] is True
    assert r["asr"] == 0.25


def test_cross_skill_provenance_closes_D():
    r = measure(attack.SCENARIOS, STACKS["+provenance"], MAN, POLICY)
    assert r["per_attack"]["D-cross-skill"] is False
    assert r["asr"] == 0.0


def test_provenance_has_a_false_positive_cost():
    # origin-only provenance also holds the benign tidy->publish hand-off: a real utility cost.
    assert _util(STACKS["+capabilities"]) == 1.0
    assert _util(STACKS["+provenance"]) < 1.0


def test_capability_scoping_is_prefix_for_fs_exact_for_net():
    assert skills.allowed_by("fs.read:~/notes/today.md", frozenset({"fs.read:~/notes/"}))
    assert not skills.allowed_by("fs.read:~/.creds", frozenset({"fs.read:~/notes/"}))
    assert skills.allowed_by("net:any.host.test", frozenset({"net:*"}))
    assert not skills.allowed_by("net:a.sink.test", frozenset({"net:team.corp.test"}))


def test_nothing_leaves_the_process():
    # the only destinations are reserved *.sink.test / *.corp.test names in an in-memory outbox
    w = evaluate_scenario(attack.SCENARIOS[3], STACKS["none"], MAN, POLICY)["world"]
    assert w.outbox and all(h.endswith(".test") for h, _ in w.outbox)

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validator import (  # noqa: E402
    validate_establishment, validate_modification,
    apply_modification_safe, apply_modification_unsafe,
)
from fixtures import (  # noqa: E402
    BENIGN_ESTABLISHMENT, ABSENT_FTEID_ESTABLISHMENT, OUT_OF_RANGE_FTEID_ESTABLISHMENT,
    MALFORMED_VT_ESTABLISHMENT, BENIGN_MODIFICATION, DUP_PDR_MODIFICATION,
    BURST_MODIFICATION, base_session,
)


def _patterns(findings):
    return {f.pattern for f in findings}


# --- validator flags each malformed record with the right iTrue family -------------------

def test_benign_establishment_is_clean():
    assert validate_establishment(BENIGN_ESTABLISHMENT) == []


def test_absent_mandatory_field_flagged():
    assert "absent_field" in _patterns(validate_establishment(ABSENT_FTEID_ESTABLISHMENT))


def test_out_of_range_value_flagged():
    assert "invalid_value" in _patterns(validate_establishment(OUT_OF_RANGE_FTEID_ESTABLISHMENT))


def test_malformed_declared_field_flagged():
    assert "malformed_field" in _patterns(validate_establishment(MALFORMED_VT_ESTABLISHMENT))


def test_benign_modification_is_clean():
    assert validate_modification(BENIGN_MODIFICATION, base_session()) == []


def test_duplicate_pdr_flagged_as_invalid_reference():
    assert "invalid_reference" in _patterns(
        validate_modification(DUP_PDR_MODIFICATION, base_session())
    )


def test_burst_flagged_as_resource_exhaustion():
    assert "resource_exhaustion" in _patterns(
        validate_modification(BURST_MODIFICATION, base_session())
    )


# --- the fix rejects what the root-cause handler silently admits -------------------------

def test_safe_handler_rejects_duplicate_pdr():
    result = apply_modification_safe(base_session(), DUP_PDR_MODIFICATION)
    assert not result.accepted and result.pattern == "invalid_reference"


def test_unsafe_handler_overrides_legitimate_rule():
    # Root-cause demonstration: without the uniqueness check the legitimate FAR is overwritten.
    session = base_session()
    far_before = session.rules[1]["far_id"]
    apply_modification_unsafe(session, DUP_PDR_MODIFICATION)
    assert session.rules[1]["far_id"] != far_before


def test_safe_handler_bounded_allocation_rejects_without_crashing():
    result = apply_modification_safe(base_session(), BURST_MODIFICATION)
    assert not result.accepted and result.pattern == "resource_exhaustion"


def test_safe_handler_accepts_benign_modification():
    session = base_session()
    result = apply_modification_safe(session, BENIGN_MODIFICATION)
    assert result.accepted and 2 in session.pdr_ids

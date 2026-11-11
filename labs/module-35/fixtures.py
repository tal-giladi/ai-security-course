"""Static message *records* for the defensive validation lab.

These are parsed, inert dictionaries — not packets, not generated attacks. Each
"malformed" record exists so the validator has something to flag; none is sent
anywhere. A benign record of each kind is paired with it so you can confirm the
validator does not flag legitimate traffic (the false-positive cost, M24).
"""

# --- Session Establishment records -------------------------------------------------------

BENIGN_ESTABLISHMENT = {
    "type": "session_establishment",
    "seid": 1001,
    "f_teid": 42,
    "volume_threshold": {"flags": {"downlink": True}, "downlink_volume": 1_000_000},
    "pdrs": [{"pdr_id": 1, "precedence": 100, "far_id": 1}],
}

ABSENT_FTEID_ESTABLISHMENT = {          # mandatory F-TEID missing -> absent_field
    "type": "session_establishment",
    "seid": 1002,
    "f_teid": None,
    "pdrs": [{"pdr_id": 1, "precedence": 100, "far_id": 1}],
}

OUT_OF_RANGE_FTEID_ESTABLISHMENT = {    # F-TEID 0 is reserved/out of range -> invalid_value
    "type": "session_establishment",
    "seid": 1003,
    "f_teid": 0,
    "pdrs": [{"pdr_id": 1, "precedence": 100, "far_id": 1}],
}

MALFORMED_VT_ESTABLISHMENT = {          # downlink flag set, Downlink Volume absent -> malformed_field
    "type": "session_establishment",
    "seid": 1004,
    "f_teid": 42,
    "volume_threshold": {"flags": {"downlink": True}},   # no "downlink_volume" key
    "pdrs": [{"pdr_id": 1, "precedence": 100, "far_id": 1}],
}

# --- Session Modification records (evaluated against a session already holding PDR ID 1) --

BENIGN_MODIFICATION = {                 # adds a fresh PDR ID -> clean
    "type": "session_modification",
    "seid": 1001,
    "pdrs": [{"pdr_id": 2, "precedence": 200, "far_id": 2}],
}

DUP_PDR_MODIFICATION = {               # reuses PDR ID 1 with a different FAR -> invalid_reference
    "type": "session_modification",
    "seid": 1001,
    "pdrs": [{"pdr_id": 1, "precedence": 10, "far_id": 99}],
}

BURST_MODIFICATION = {                 # 9 new PDRs would exceed capacity -> resource_exhaustion
    "type": "session_modification",
    "seid": 1001,
    "pdrs": [{"pdr_id": n, "precedence": 100, "far_id": n} for n in range(2, 11)],
}


def base_session():
    """A session with PDR ID 1 installed (FAR 1), matching BENIGN_ESTABLISHMENT."""
    from validator import Session
    s = Session(1001)
    s.install({"pdr_id": 1, "precedence": 100, "far_id": 1})
    return s


ESTABLISHMENT_FIXTURES = {
    "benign": BENIGN_ESTABLISHMENT,
    "absent_f_teid": ABSENT_FTEID_ESTABLISHMENT,
    "out_of_range_f_teid": OUT_OF_RANGE_FTEID_ESTABLISHMENT,
    "malformed_volume_threshold": MALFORMED_VT_ESTABLISHMENT,
}

MODIFICATION_FIXTURES = {
    "benign": BENIGN_MODIFICATION,
    "duplicate_pdr": DUP_PDR_MODIFICATION,
    "burst": BURST_MODIFICATION,
}

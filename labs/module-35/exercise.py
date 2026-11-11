"""Student starting point — a vulnerable Session Modification handler.

Your job (Lesson 35.1, Exercise): make `apply_modification` enforce the stated
spec rules so it REJECTS every malformed/duplicate record in fixtures.py and
still ACCEPTS every benign one. The reference fix lives in
`validator.apply_modification_safe`; write yours first, then compare.

Spec rules to enforce:
  R1  A PDR ID must be unique within a session.          (invalid_reference)
  R2  Installing PDRs must not exceed MAX_PDRS_PER_SESSION. (resource_exhaustion)

Run the tests to check your work:
  py -m pytest labs/module-35 -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validator import Reject, Accept, MAX_PDRS_PER_SESSION  # noqa: E402


def apply_modification(session, msg):
    """VULNERABLE: trusts the internal peer and installs everything.

    This is the iTrue root cause in code form — a duplicate PDR ID overwrites the
    legitimate rule, and an oversized burst drains the pool. Add the missing
    checks so it rejects gracefully instead.
    """
    incoming = msg.get("pdrs", [])

    # TODO R1: reject when a pdr_id already exists in session.pdr_ids
    #          -> return Reject("duplicate PDR ID ...", "invalid_reference")

    # TODO R2: reject when installing these PDRs would exceed MAX_PDRS_PER_SESSION
    #          -> return Reject("PDR pool capacity exceeded", "resource_exhaustion")

    for pdr in incoming:
        session.install(pdr)
    return Accept()

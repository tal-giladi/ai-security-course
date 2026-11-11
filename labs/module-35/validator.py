"""Reference solution — defensive validation at an internal-peer trust boundary.

This is the *defensive* core of the iFinder / implicit-trust-error (iTrue) lab.
It operates only on parsed message *records* (plain dicts, supplied as static
fixtures). It sends no packets, opens no sockets, and exploits nothing. The whole
job is the question the Discovery/Vetting agents reason about:

    "Is the required validation present before the dangerous operation?"

Each detection pattern is the study's triple:
    <information element, dangerous operation, missing validation>
"""

from collections import namedtuple

# The six iTrue detection-pattern families, grouped by root-cause class.
PATTERNS = {
    # missing syntactic validation
    "malformed_field": "a length/format taken from the message drives a parse/memory operation",
    "absent_field": "a mandatory information element is used without a presence check",
    # missing semantic validation
    "invalid_value": "an IE value is used without a range/type check",
    "invalid_state": "a message is acted on without checking the session/procedure state",
    "invalid_reference": "an identifier is reused/overridden without a uniqueness check",
    # missing resource-availability check
    "resource_exhaustion": "a resource is allocated without checking availability",
}

# Toy capacity and valid F-TEID range (3GPP F-TEID is a 32-bit identifier; 0 is reserved).
MAX_PDRS_PER_SESSION = 8
FTEID_MIN, FTEID_MAX = 1, 2 ** 32 - 1

Finding = namedtuple("Finding", ["pattern", "ie", "detail"])


class Session:
    """Minimal session state: the installed Packet Detection Rules, keyed by PDR ID."""

    def __init__(self, seid):
        self.seid = seid
        self.pdr_ids = set()
        self.rules = {}  # pdr_id -> rule record

    def install(self, pdr):
        # NOTE: a duplicate pdr_id overwrites the existing rule. Whether that is
        # allowed to happen is exactly what the uniqueness check below governs.
        self.pdr_ids.add(pdr["pdr_id"])
        self.rules[pdr["pdr_id"]] = pdr


# --- validators: return a list of Findings; empty list means "no gap found" -------------

def validate_establishment(msg):
    """Audit a PFCP-like Session Establishment record against the spec rules."""
    findings = []

    # Spec: F-TEID is a mandatory IE (syntactic — presence).
    if msg.get("f_teid") is None:
        findings.append(Finding("absent_field", "F-TEID", "mandatory F-TEID absent"))
    else:
        # Spec: F-TEID must fall within the valid range (semantic — value).
        if not (FTEID_MIN <= msg["f_teid"] <= FTEID_MAX):
            findings.append(
                Finding("invalid_value", "F-TEID", f"F-TEID {msg['f_teid']} out of range")
            )

    # Spec: if the Volume Threshold IE declares the downlink flag, the Downlink
    # Volume field must be present (syntactic — a declared field is malformed/absent).
    vt = msg.get("volume_threshold")
    if vt and vt.get("flags", {}).get("downlink") and "downlink_volume" not in vt:
        findings.append(
            Finding("malformed_field", "Volume Threshold",
                    "downlink flag set but Downlink Volume field absent")
        )

    # Spec: the rules installed at establishment must fit the pool (availability).
    if len(msg.get("pdrs", [])) > MAX_PDRS_PER_SESSION:
        findings.append(
            Finding("resource_exhaustion", "PDR pool",
                    f"{len(msg['pdrs'])} PDRs exceed capacity {MAX_PDRS_PER_SESSION}")
        )
    return findings


def validate_modification(msg, session):
    """Audit a Session Modification record against the live session state."""
    findings = []
    incoming = msg.get("pdrs", [])

    # Spec invariant: a PDR ID must be unique within a session. A reused ID that
    # overrides the legitimate rule is the root cause of the session-hijack class.
    for pdr in incoming:
        if pdr["pdr_id"] in session.pdr_ids:
            findings.append(
                Finding("invalid_reference", "PDR ID",
                        f"duplicate PDR ID {pdr['pdr_id']} within session {session.seid}")
            )

    # Spec: the modification must not drive the pool past its capacity (availability).
    projected = len(session.pdr_ids) + sum(
        1 for p in incoming if p["pdr_id"] not in session.pdr_ids
    )
    if projected > MAX_PDRS_PER_SESSION:
        findings.append(
            Finding("resource_exhaustion", "PDR pool",
                    f"session {session.seid} would hold {projected} PDRs, "
                    f"capacity {MAX_PDRS_PER_SESSION}")
        )
    return findings


# --- handlers: a root-cause demonstration (unsafe) vs the fix (safe) ---------------------

class Reject:
    """A graceful rejection — the defensive alternative to an assert-and-die crash."""

    accepted = False

    def __init__(self, reason, pattern):
        self.reason = reason
        self.pattern = pattern


class Accept:
    accepted = True
    reason = None
    pattern = None


def apply_modification_unsafe(session, msg):
    """Root-cause demonstration (NOT an attack): the handler trusts the internal
    peer and installs every PDR, letting a duplicate ID silently overwrite the
    existing rule. Present only to contrast with the fix below."""
    for pdr in msg.get("pdrs", []):
        session.install(pdr)
    return Accept()


def apply_modification_safe(session, msg):
    """The fix: enforce the uniqueness invariant and bounded allocation, and
    reject gracefully instead of crashing."""
    incoming = msg.get("pdrs", [])

    for pdr in incoming:
        if pdr["pdr_id"] in session.pdr_ids:
            return Reject(f"duplicate PDR ID {pdr['pdr_id']}", "invalid_reference")

    projected = len(session.pdr_ids) + sum(
        1 for p in incoming if p["pdr_id"] not in session.pdr_ids
    )
    if projected > MAX_PDRS_PER_SESSION:
        return Reject("PDR pool capacity exceeded", "resource_exhaustion")

    for pdr in incoming:
        session.install(pdr)
    return Accept()

"""Runnable code-vs-spec audit: print what the validator flags on each fixture,
and contrast the unsafe vs safe modification handler on the duplicate-PDR record.

    py labs/module-35/audit.py

Offline, stdlib only, no network.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validator import (  # noqa: E402
    validate_establishment, validate_modification,
    apply_modification_safe, apply_modification_unsafe,
)
from fixtures import (  # noqa: E402
    ESTABLISHMENT_FIXTURES, MODIFICATION_FIXTURES, base_session, DUP_PDR_MODIFICATION,
)


def _fmt(findings):
    return ", ".join(f"{f.pattern}:{f.ie}" for f in findings) if findings else "(clean)"


def main():
    print("== Session Establishment audit ==")
    for name, msg in ESTABLISHMENT_FIXTURES.items():
        print(f"  {name:28s} -> {_fmt(validate_establishment(msg))}")

    print("\n== Session Modification audit (session already holds PDR ID 1) ==")
    for name, msg in MODIFICATION_FIXTURES.items():
        print(f"  {name:28s} -> {_fmt(validate_modification(msg, base_session()))}")

    print("\n== Handler contrast on the duplicate-PDR record ==")
    unsafe_session = base_session()
    far_before = unsafe_session.rules[1]["far_id"]
    apply_modification_unsafe(unsafe_session, DUP_PDR_MODIFICATION)
    far_after = unsafe_session.rules[1]["far_id"]
    print(f"  unsafe handler: PDR 1 FAR {far_before} -> {far_after} "
          f"({'OVERRIDDEN' if far_after != far_before else 'unchanged'})")

    safe_session = base_session()
    result = apply_modification_safe(safe_session, DUP_PDR_MODIFICATION)
    print(f"  safe handler:   {'rejected' if not result.accepted else 'accepted'} "
          f"({result.pattern}: {result.reason}); PDR 1 FAR still "
          f"{safe_session.rules[1]['far_id']}")

    print("\nTakeaway: the missing uniqueness check is the whole difference. The safe "
          "handler enforces the invariant and rejects; nothing is attacked or sent.")


if __name__ == "__main__":
    main()

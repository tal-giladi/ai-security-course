#!/usr/bin/env python3
"""Keep `labs/common/` in sync with `lab/` (the source of truth).

The Academy ships `labs/module-NN/` + `labs/common/` as each module's zip, flattened. The repo
keeps the canonical shared runtime under `lab/`, so the two drift unless something copies it.
Run this after editing anything in `lab/{models,sink,agents,defense-tools,attack-tools}`.

    py scripts/sync_labs_common.py          # copy anything out of date
    py scripts/sync_labs_common.py --check  # exit 1 if out of date (for CI)
"""
from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMON = ROOT / "labs" / "common"

# source under lab/  ->  flat name in labs/common/
FILES = {
    "lab/models/shim.py": "shim.py",
    "lab/sink/sink.py": "sink.py",
    "lab/agents/agent.py": "agent.py",
    "lab/defense-tools/defenses.py": "defenses.py",
    "lab/attack-tools/evalkit.py": "evalkit.py",
}


def main() -> int:
    check = "--check" in sys.argv
    COMMON.mkdir(parents=True, exist_ok=True)
    drift: list[str] = []
    for src_rel, name in FILES.items():
        src, dst = ROOT / src_rel, COMMON / name
        if not src.is_file():
            drift.append(f"missing source {src_rel}")
            continue
        if dst.is_file() and filecmp.cmp(src, dst, shallow=False):
            continue
        drift.append(f"{src_rel} -> labs/common/{name}")
        if not check:
            shutil.copy2(src, dst)
    for line in drift:
        print(("DRIFT " if check else "SYNC  ") + line)
    if check and drift:
        return 1
    if not drift:
        print("labs/common is up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())

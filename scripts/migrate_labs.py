#!/usr/bin/env python3
"""Relocate the labs so the Academy actually ships them.

`course-creator` zips only `labs/module-NN/` (+ `labs/common/`) per module. The legacy
labs sat in `labs/lab-NN/`, so modules 00-26 had no code zip at all. This script:

  1. `labs/lab-NN/`  -> `labs/module-NN/`   (04-25; lab-16 merges into the existing module-16)
  2. `labs/module-32/` -> `labs/module-32/`   (the F.1 lesson is now 32.1)
  3. writes a flat `labs/common/` holding the shared runtime copied out of `lab/`
  4. rewrites every `sys.path` line that reached `lab/<tool>` so it also resolves
     `labs/common/` — the layout a learner gets after unzipping
  5. fixes `labs/lab-NN` references in prose, code fences and links across the repo

Run from the repo root. `git mv` is used so history follows the files.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Shared runtime: source dir under lab/ -> flat file name in labs/common/
COMMON_FILES = {
    "lab/models/shim.py": "shim.py",
    "lab/sink/sink.py": "sink.py",
    "lab/agents/agent.py": "agent.py",
    "lab/defense-tools/defenses.py": "defenses.py",
    "lab/attack-tools/evalkit.py": "evalkit.py",
}

TOOLS = ("models", "sink", "agents", "defense-tools", "attack-tools")

OLD_TO_NEW = {f"labs/lab-{n:02d}": f"labs/module-{n:02d}" for n in range(4, 26)}
OLD_TO_NEW["labs/" + "lab-26-hidden-context"] = "labs/module-32"
# module-16 already exists (lesson 16.2's memory lab); lab-16 merges into it.
# Written as concatenation so the reference rewrite below cannot rewrite this script's own
# mapping into a self-merge (it did once, and rmtree'd labs/module-16).
MERGE_INTO = {"labs/" + "lab-16": "labs/module-16"}

TEXT_EXT = {".md", ".py", ".yml", ".yaml", ".txt", ".json"}


def sh(*args: str) -> None:
    subprocess.run(["git", *args], cwd=ROOT, check=True)


def move_labs() -> list[str]:
    log: list[str] = []
    for old, new in {**OLD_TO_NEW, **MERGE_INTO}.items():
        src, dst = ROOT / old, ROOT / new
        if src.resolve() == dst.resolve():
            raise SystemExit(f"ABORT: {old} and {new} are the same directory")
        if not src.is_dir():
            continue
        if not dst.exists():
            sh("mv", old, new)
            log.append(f"{old} -> {new}")
            continue
        # Merge: keep the existing destination, bring across anything that does not clash.
        for item in sorted(src.iterdir()):
            if item.name == "__pycache__":
                continue
            target = dst / item.name
            if target.exists():
                log.append(f"  ! {item.name} already in {new}, left as-is")
                continue
            sh("mv", f"{old}/{item.name}", f"{new}/{item.name}")
            log.append(f"{old}/{item.name} -> {new}/{item.name}")
        shutil.rmtree(src, ignore_errors=True)
        log.append(f"{old} merged into {new}")
    return log


def write_common() -> list[str]:
    log: list[str] = []
    common = ROOT / "labs" / "common"
    common.mkdir(parents=True, exist_ok=True)
    for src_rel, name in COMMON_FILES.items():
        src = ROOT / src_rel
        if not src.is_file():
            log.append(f"  ! missing {src_rel}")
            continue
        dst = common / name
        if not dst.exists() or dst.read_bytes() != src.read_bytes():
            shutil.copy2(src, dst)
            log.append(f"labs/common/{name} <- {src_rel}")
    return log


# `sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "sink"))`
# becomes two lines: the shipped-zip location first, the repo checkout as a fallback.
SYSPATH_RE = re.compile(
    r'^(?P<indent>[ \t]*)sys\.path\.insert\(\s*0,\s*str\(Path\(__file__\)\.resolve\(\)\.parents\[2\]\s*'
    r'/\s*"lab"\s*/\s*"(?P<tool>[a-z-]+)"\s*\)\s*\)\s*$',
    re.MULTILINE,
)


def add_common_to_path(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'parents[1] / "common"' in text:
        return False

    def repl(m: re.Match) -> str:
        ind, tool = m.group("indent"), m.group("tool")
        return (
            f'{ind}# The Academy ships this lab as a zip: labs/module-NN/ + labs/common/.\n'
            f'{ind}sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))\n'
            f"{m.group(0)}"
        )

    new = SYSPATH_RE.sub(repl, text)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8", newline="\n")
    return True


# `labs/module-23/attack.py` and `../../labs/module-23/README.md` -> `labs/module-23/...`
LABREF_RE = re.compile(r"labs/lab-(\d{2})(?=-|\b)")
HIDDEN_RE = re.compile(r"labs/module-32")


def fix_refs(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = HIDDEN_RE.sub("labs/module-32", text)
    new = LABREF_RE.sub(lambda m: f"labs/module-{m.group(1)}", new)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8", newline="\n")
    return True


# `scripts/` is skipped on purpose: the reference rewrite below would otherwise rewrite this
# script's own OLD_TO_NEW / MERGE_INTO literals and turn a move into a self-merge.
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", "curriculum", "scripts"}


def main() -> int:
    log: list[str] = []
    log.append("## moves")
    log += move_labs()

    log.append("\n## labs/common")
    log += write_common()

    touched = 0
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix not in TEXT_EXT:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.parts[len(ROOT.parts)].startswith("."):
            continue
        a = add_common_to_path(p)
        b = fix_refs(p)
        if a or b:
            touched += 1
    log.append(f"\n## rewritten {touched} files (sys.path + lab references)")

    (ROOT / "curriculum" / "lab-migration.log").write_text(
        "\n".join(log) + "\n", encoding="utf-8", newline="\n"
    )
    print("\n".join(log))
    return 0


if __name__ == "__main__":
    sys.exit(main())

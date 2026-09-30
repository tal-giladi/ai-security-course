#!/usr/bin/env python3
"""Validate every .quiz.yaml against the Academy's rules (new-course-instructions.md section 5).

Run after writing any quiz:  py scripts/check_quizzes.py [path ...]
Exit code 1 if any file breaks a rule.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BANNED = ("all of the above", "none of the above")


def check(path: Path) -> list[str]:
    problems: list[str] = []
    rel = path.relative_to(ROOT)
    try:
        items = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{rel}: does not parse as YAML ({exc})"]
    if not isinstance(items, list) or not items:
        return [f"{rel}: top level is not a non-empty list"]

    is_module_quiz = "assessments" in path.parts
    lo, hi = (8, 10) if is_module_quiz else (3, 5)
    if not lo <= len(items) <= hi:
        problems.append(f"{rel}: {len(items)} questions, expected {lo}-{hi}")

    seen_ids: set[str] = set()
    positions: list[int] = []
    for i, q in enumerate(items, 1):
        tag = f"{rel}: q{i}"
        if not isinstance(q, dict):
            problems.append(f"{tag}: not a mapping")
            continue
        if "source" in q:
            problems.append(f"{tag}: has a source: field (old fingerprint format)")
        qid = q.get("id")
        if not qid:
            problems.append(f"{tag}: no id")
        elif qid in seen_ids:
            problems.append(f"{tag}: duplicate id {qid!r}")
        else:
            seen_ids.add(qid)

        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) != 4:
            problems.append(f"{tag}: {len(opts) if isinstance(opts, list) else opts} options, expected 4")
        elif len({str(o).strip().lower() for o in opts}) != 4:
            problems.append(f"{tag}: options are not distinct")

        corr = q.get("correct")
        if corr not in (0, 1, 2, 3):
            problems.append(f"{tag}: correct={corr!r}, expected 0-3")
        else:
            positions.append(corr)

        expl = q.get("explanation")
        if not isinstance(expl, str) or not expl.strip():
            problems.append(f"{tag}: missing explanation")
        elif len(expl.split()) < 8:
            problems.append(f"{tag}: explanation is too short to teach anything")

        if not q.get("question"):
            problems.append(f"{tag}: missing question")
        if isinstance(opts, list) and isinstance(corr, int) and 0 <= corr < len(opts):
            text = " ".join(str(o).lower() for o in opts)
            if any(b in text for b in BANNED):
                problems.append(f"{tag}: uses an all/none-of-the-above option")
            if isinstance(expl, str) and len(str(opts[corr]).strip()) >= 12:
                if str(opts[corr]).strip().lower() in expl.strip().lower():
                    problems.append(f"{tag}: explanation just restates the correct option")

    if positions:
        counts = Counter(positions)
        if len(counts) == 1:
            problems.append(f"{rel}: every correct answer is option {positions[0]}")
        elif len(counts) < 3 and len(items) >= 4:
            problems.append(
                f"{rel}: correct answers use only {sorted(counts)} - spread them across 0-3"
            )
    return problems


def main() -> int:
    targets = [Path(a) if Path(a).is_absolute() else ROOT / a for a in sys.argv[1:]]
    if not targets:
        targets = sorted(ROOT.rglob("*.quiz.yaml"))
    problems: list[str] = []
    for p in targets:
        if p.is_file():
            problems += check(p)
    total = sum(len(yaml.safe_load(p.read_text(encoding="utf-8"))) for p in targets if p.is_file())
    for line in problems:
        print("PROBLEM " + line)
    print(f"{len(targets)} files, {total} questions, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

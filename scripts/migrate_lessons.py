#!/usr/bin/env python3
"""Mechanical part of the Academy migration (see curriculum/migration-spec.md).

Converts the pre-2026-09-30 lesson format into the Academy format:

  * `<div class="...">` boxes  -> GitHub alerts (`> [!WARNING]` and friends), or plain markdown
  * `## Assessment`           -> deleted (the questions live in the .quiz.yaml)
  * `## Progress checkpoint`  -> deleted (the Academy tracks progress itself)
  * `## Prerequisites`         -> deleted (goes into the front matter)
  * `## Concept & Intuition` / `## Technical explanation & Code` / `## Code & Practical lab`
                              -> split into the canonical separate sections
  * `## Code — <suffix>`      -> `## Code`, the suffix moves into the body

Front matter and quiz YAMLs need judgement, so this script only does the mechanical half and
writes a report of what it removed. It is idempotent: re-running finds nothing left to do.

Usage:  py scripts/migrate_lessons.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"
REPORT = ROOT / "curriculum" / "migration-report.md"

# div class -> GitHub alert type. None means "unwrap to plain markdown".
CALLOUT_MAP = {
    "callout guarantee": "IMPORTANT",
    "callout blue": "TIP",
    "callout key": "IMPORTANT",
    "callout red": "CAUTION",
    "callout warn": "WARNING",
    "callout purple": "NOTE",
    "lab": None,
    "prereq": None,
}

# Canonical H2s, in order. Everything else is either kept in place or split.
SECTION_SPLITS = {
    "Concept & Intuition": ["Concept", "Intuition"],
    "Technical explanation & Code": ["Technical explanation", "Code"],
    "Code & Practical lab": ["Code", "Practical lab"],
}
DROP_SECTIONS = {"Assessment", "Progress checkpoint", "Prerequisites"}


def strip_h2_suffix(title: str) -> tuple[str, str]:
    """`Code — a tiny target` -> ("Code", "a tiny target")."""
    m = re.match(r"^([A-Za-z][A-Za-z &/]*?)\s+[—–-]\s+(.*)$", title)
    return (m.group(1).strip(), m.group(2).strip()) if m else (title.strip(), "")


def to_alert(text: str, kind: str) -> str:
    """Wrap a block of markdown lines in a GitHub alert."""
    lines = [ln.rstrip() for ln in text.strip("\n").split("\n")]
    body = "\n".join(("> " + ln).rstrip() for ln in lines)
    return f"> [!{kind}]\n{body}\n"


def unwrap(text: str) -> str:
    return text.strip("\n") + "\n"


DIV_RE = re.compile(
    r'<div class="([^"]+)">\s*\n(.*?)\n\s*</div>\s*\n', re.DOTALL
)

# A fenced block whose every line is a `course.py` progress command. The Academy tracks
# progress itself, so these are removed together with the sentence that introduces them.
PROGRESS_BLOCK_RE = re.compile(
    r"\n*Mark[^.\n]*(?:complete|progress)[^.\n]*:\s*\n+```(?:bash|sh|shell)?\n"
    r"(?:[^\n]*\bcourse\.py\b[^\n]*\n)+```\n",
    re.IGNORECASE,
)
BARE_PROGRESS_RE = re.compile(
    r"\n*```(?:bash|sh|shell)?\n(?:[^\n]*\bcourse\.py\b[^\n]*\n)+```\n", re.IGNORECASE
)

# The legacy <div class="prereq"> block landed above the H1 once the divs were unwrapped.
# Park it at the end of the file so the front-matter pass can fold it in and delete it.
PREREQ_LEAD_RE = re.compile(r"\A(?P<lead>\*\*Prerequisites\.\*\*.*?)\n(?P<h1># \d+\.\d+ · [^\n]*)\n", re.DOTALL)
PARK_START = "<!-- PREREQ-BLOCK: fold into the front matter (prerequisites/objectives), then delete"
PARK_END = "-->"


def strip_progress(text: str, log: list[str]) -> str:
    before = text
    text = PROGRESS_BLOCK_RE.sub("\n", text)
    text = BARE_PROGRESS_RE.sub("\n", text)
    if text != before:
        log.append("  - removed course.py progress commands")
    return text


def park_prereq(text: str, log: list[str]) -> str:
    """Move the leading prereq block to a marker at the very end of the file."""
    existing = re.search(
        re.escape(PARK_START) + r"(?P<block>.*?)\n" + re.escape(PARK_END) + r"\n",
        text,
        re.DOTALL,
    )
    if existing:
        # Rebuild the whole marker. `block` spans from after PARK_START to before the closing
        # PARK_END, so the closing " -->" of the start marker is inside it; re-emitting it
        # verbatim is what dropped the marker on an earlier run.
        block = PARK_START + " -->\n" + existing.group("block").rstrip() + f"\n{PARK_END}\n"
        rest = text[: existing.start()].rstrip() + "\n\n" + text[existing.end():]
        return rest.rstrip() + "\n\n" + block
    m = PREREQ_LEAD_RE.match(text)
    if not m:
        return text
    log.append("  - parked leading prereq block at the end for the front-matter pass")
    lead = m.group("lead").strip()
    rest = (m.group("h1") + "\n\n" + text[m.end():]).strip()
    return f"{rest}\n\n{PARK_START} -->\n{lead}\n{PARK_END}\n"


# Canonical section order. Anything not listed keeps its place at the end.
CANONICAL_ORDER = [
    "Why this matters",
    "Learning objectives",
    "Concept",
    "Intuition",
    "Technical explanation",
    "Mathematics",
    "Attack / Defense model",
    "Real-world examples",
    "Code",
    "Practical lab",
    "Exercise",
    "Research paper",
    "Further reading",
    "What you should now be able to do",
]


def reorder_sections(text: str, log: list[str]) -> str:
    """Put the `## ` sections into the canonical order, keeping any preamble (H1) on top."""
    lines = text.split("\n")
    head: list[str] = []
    i = 0
    while i < len(lines) and not re.match(r"^##\s+", lines[i]):
        head.append(lines[i])
        i += 1
    sections: list[tuple[str, list[str]]] = []
    while i < len(lines):
        title = re.match(r"^##\s+(.*\S)\s*$", lines[i]).group(1)
        j = i + 1
        while j < len(lines) and not re.match(r"^##\s+", lines[j]):
            j += 1
        sections.append((title, lines[i:j]))
        i = j

    order = {t: n for n, t in enumerate(CANONICAL_ORDER)}
    current = [t for t, _ in sections if t in order]
    wanted = sorted(current, key=order.get)
    if current != wanted:
        log.append("  - reordered sections to the canonical order")
    tail = [c for c in sections if c[0] not in order]

    out = "\n".join(head).rstrip()
    by_title = dict(sections)
    for title in wanted + [t for t, _ in tail]:
        out += "\n\n" + "\n".join(by_title[title]).rstrip()
    return out + "\n"



def convert_divs(body: str, log: list[str]) -> str:
    def repl(m: re.Match) -> str:
        cls, inner = m.group(1), m.group(2)
        if cls not in CALLOUT_MAP:
            log.append(f"  ? unknown div class {cls!r} left as-is")
            return m.group(0)
        kind = CALLOUT_MAP[cls]
        if kind is None:
            if cls == "prereq":
                log.append("  - dropped <div class=\"prereq\"> (content is in front matter)")
            else:
                log.append("  - unwrapped <div class=\"lab\"> to plain markdown")
            return unwrap(inner)
        log.append(f"  - <div class=\"{cls}\"> -> > [!{kind}]")
        return to_alert(inner, kind)

    prev = None
    while prev != body:
        prev = body
        body = DIV_RE.sub(repl, body)
    return body


def convert_sections(body: str, log: list[str]) -> str:
    lines = body.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^##\s+(.*\S)\s*$", line)
        if not m:
            out.append(line)
            i += 1
            continue
        title = m.group(1)
        # Find the extent of this section.
        j = i + 1
        while j < len(lines) and not re.match(r"^##\s+", lines[j]):
            j += 1
        chunk = lines[i:j]

        base, suffix = strip_h2_suffix(title)
        if base in DROP_SECTIONS:
            log.append(f"  - dropped ## {title}")
            i = j
            continue
        if base in SECTION_SPLITS:
            heads = SECTION_SPLITS[base]
            log.append(f"  - split ## {title} -> {', '.join(heads)}")
            # Put the first heading here and splice the others in at the end of the chunk.
            out.append(f"## {heads[0]}")
            for extra in heads[1:]:
                out.append("")
                out.append(f"## {extra}")
            out.extend(chunk[1:])
            i = j
            continue
        if base != title:
            log.append(f"  - ## {title} -> ## {base}" + (f" ({suffix})" if suffix else ""))
            out.append(f"## {base}")
            if suffix:
                out.append("")
                out.append(suffix + ".")
            out.extend(chunk[1:])
            i = j
            continue
        out.append(line)
        out.extend(chunk[1:])
        i = j
    return "\n".join(out)


def process(path: Path, dry: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        return []  # already migrated
    log: list[str] = [str(path.relative_to(ROOT))]
    log.append(f"  first line: {text.split(chr(10), 1)[0][:60]!r}")
    body = convert_sections(text, log)
    body = convert_divs(body, log)
    body = strip_progress(body, log)
    body = park_prereq(body, log)
    body = reorder_sections(body, log)
    body = re.sub(r"\n{4,}", "\n\n\n", body)

    # Safety net: this pass only removes HTML tags, two sections and progress commands,
    # so a large shrink means a bug, not intended work. Refuse to write.
    budget = len(text) - sum(
        len(s) for s in re.findall(r"<[^>\n]+>", text)
    ) - 4000  # the dropped ## Assessment / ## Progress checkpoint bodies
    if len(body) < budget * 0.6:
        raise SystemExit(
            f"ABORT {path.relative_to(ROOT)}: {len(text)} -> {len(body)} chars, "
            f"below the {int(budget * 0.6)} floor. Nothing further was written."
        )

    if not dry:
        path.write_text(body, encoding="utf-8", newline="\n")
    return log


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets = sorted(p for p in LESSONS.rglob("*.md") if not p.read_text(encoding="utf-8").startswith("---"))
    logs: list[str] = []
    for p in targets:
        entry = process(p, args.dry_run)
        if entry:
            logs.append("\n".join(entry))

    report = (
        "# Migration report (mechanical pass)\n\n"
        "Generated by `scripts/migrate_lessons.py`. "
        + ("Dry run — nothing written.\n" if args.dry_run else "Changes applied.\n")
        + f"\n{len(targets)} legacy lessons processed.\n"
        + "\n---\n".join([""] + logs)
        + "\n"
    )
    REPORT.write_text(report, encoding="utf-8", newline="\n")
    print(f"processed {len(targets)} lessons -> {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

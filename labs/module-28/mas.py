"""Lab 28 — a mock multi-agent system (planner -> researcher -> executor) on an in-memory bus.

LOCAL/IN-PROCESS ONLY. Agents are plain objects; the "bus" is a function call. Nothing binds to a
socket and nothing leaves the process. The privileged action appends to an in-memory SINK list.
Canary is synthetic. This models an A2A-style delegation fabric so we can attack and defend the
edges: sender authenticity, message integrity, per-edge capability scoping, and task provenance.
"""
from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass, field

CANARY = "LAB-CANARY-mas-a2a-0001"
SINK: list[str] = []                       # the mock "real effect": e.g. outbound email bodies

# shared symmetric keys (one per agent). In A2A these would be per-agent credentials.
KEYS = {"planner": b"k-planner", "researcher": b"k-researcher", "executor": b"k-executor",
        "helper": b"k-helper"}


def sign(sender: str, payload: str) -> str:
    return hmac.new(KEYS[sender], payload.encode(), hashlib.sha256).hexdigest()


def verify(claimed_sender: str, payload: str, sig: str | None) -> bool:
    key = KEYS.get(claimed_sender)
    if key is None or sig is None:
        return False
    return hmac.compare_digest(hmac.new(key, payload.encode(), hashlib.sha256).hexdigest(), sig)


@dataclass
class Message:
    frm: str
    to: str
    task: str                              # e.g. "research: <q>" or "execute: send_email(...)"
    sig: str | None = None
    provenance: tuple = ()                 # signed chain of (agent, task-hash) originators/handlers


@dataclass
class Bus:
    require_auth: bool = False             # verify signatures (kills impersonation + tampering)
    scope_caps: bool = False               # per-edge capability scoping + provenance authz
    log: list = field(default_factory=list)

    # only these agents may appear in the provenance of a privileged task (researcher is untrusted)
    TRUSTED_FOR_PRIVILEGE = {"planner", "executor"}

    def deliver(self, msg: Message, agents: dict) -> str:
        self.log.append((msg.frm, msg.to, msg.task))
        if self.require_auth and not verify(msg.frm, msg.task, msg.sig):
            return "REJECTED: bad signature / forged sender"
        return agents[msg.to].handle(msg, self, agents)


@dataclass
class Agent:
    name: str
    bus_caps: set                          # capabilities this agent may INVOKE

    def send(self, bus, agents, to, task, provenance=()):
        msg = Message(self.name, to, task, sign(self.name, task), provenance)
        return bus.deliver(msg, agents)


class Researcher(Agent):
    """Reads untrusted web content; its result flows onward. The exposed, low-privilege node."""
    def __init__(self, web_content: str):
        super().__init__("researcher", bus_caps={"read_web"})
        self.web_content = web_content

    def handle(self, msg, bus, agents):
        # summarise the (untrusted) web content; an injected directive is carried along verbatim.
        return f"research-result: {self.web_content}"


class Executor(Agent):
    """Holds the privileged capability send_email. Should only run it for authorised origins."""
    def __init__(self):
        super().__init__("executor", bus_caps={"send_email"})

    def handle(self, msg, bus, agents):
        if "send_email" in msg.task:
            if bus.scope_caps:
                # provenance authorization: EVERY handler that contributed to this privileged task
                # must be trusted. A task whose parameters were derived from the untrusted researcher
                # carries ('researcher', ...) in its provenance and is refused (taint propagation).
                handlers = {a for a, _ in msg.provenance} or {msg.frm}
                untrusted = handlers - bus.TRUSTED_FOR_PRIVILEGE
                if untrusted:
                    return f"REFUSED: privileged task tainted by untrusted handler(s) {sorted(untrusted)}"
            body = msg.task.split("send_email:", 1)[-1].strip() or CANARY
            SINK.append(body)
            return f"EXECUTED send_email -> sink: {body}"
        return "executor: nothing to do"


class Planner(Agent):
    """Delegates: asks researcher, then tells executor what to do based on the result."""
    def __init__(self):
        super().__init__("planner", bus_caps={"delegate"})

    def handle(self, msg, bus, agents):
        return "planner: ack"

    def run_workflow(self, bus, agents):
        prov = (("planner", "root"),)
        result = self.send(bus, agents, "researcher", "research: latest guidance", prov)
        # NAIVE planner: if the research result contains a directive, it obeys and re-delegates.
        directive = ""
        if "DIRECTIVE:" in result:
            directive = result.split("DIRECTIVE:", 1)[1].strip()
        if directive:
            # the privileged task's parameters are DERIVED FROM the untrusted researcher output,
            # so researcher is (honestly) recorded in the task's provenance -> taint.
            task = f"execute: send_email: {directive}"
            prov = prov + (("researcher", "derived"),)
        else:
            task = "execute: send_email: routine-report"
        return self.send(bus, agents, "executor", task, prov)

"""Shared toy AGENT RUNTIME for the security lab (used by Labs 16-18).

A minimal but faithful agent loop:  observe context -> decide a tool call -> execute -> observe
-> repeat. The agent holds a synthetic secret and has TOOLS (capabilities). Untrusted content
(a file it reads, a web page, a tool result) can contain tool DIRECTIVES; an under-defended agent
obeys them -- the confused deputy (00.1) in executable form.

Design goals:
  * Capabilities = tools the agent can call. More tools / broader args = more attack surface.
  * A POLICY layer authorizes each tool call in code (tool allowlist, argument validation, egress
    allowlist, human-approval gates) -- the enforced boundary (02.1), separate from the "brain".
  * Egress goes to the LOCAL sink only; secrets are synthetic LAB-CANARY-* markers.

The "brain" here is a transparent rule engine, not a real LLM: it scans its context for tool
directives of the form  CALL tool(arg=value, ...)  and issues them (subject to policy). This makes
the attack/defense mechanics fully inspectable and testable; swap in a real tool-calling LLM behind
the same `decide()` interface for higher fidelity.
"""
from __future__ import annotations

import re
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sink"))

DIRECTIVE = re.compile(r"CALL\s+(\w+)\((.*?)\)", re.I)


def _parse_args(s: str) -> dict:
    args = {}
    for m in re.finditer(r"(\w+)\s*=\s*'([^']*)'|(\w+)\s*=\s*\"([^\"]*)\"|(\w+)\s*=\s*([^,]+)", s):
        if m.group(1):
            args[m.group(1)] = m.group(2)
        elif m.group(3):
            args[m.group(3)] = m.group(4)
        elif m.group(5):
            args[m.group(5)] = m.group(6).strip()
    return args


@dataclass
class Policy:
    """The enforced authorization layer (defense). Default = permissive (vulnerable)."""
    allowed_tools: set | None = None      # None => all tools allowed (excessive agency)
    allowed_egress_hosts: set = field(default_factory=set)   # for http_get / send_email
    require_approval: set = field(default_factory=set)        # tools needing human approval
    approver: object = None               # callable(tool, args)->bool; None => deny approvals

    def authorize(self, tool, args):
        if self.allowed_tools is not None and tool not in self.allowed_tools:
            return False, "tool not allowlisted"
        if tool in ("http_get", "send_email"):
            target = args.get("url") or args.get("to", "")
            host = urlparse(target if "//" in target else "//" + target).netloc or target
            if self.allowed_egress_hosts and host not in self.allowed_egress_hosts:
                return False, f"egress to {host} not allowlisted"
        if tool in self.require_approval:
            if not (self.approver and self.approver(tool, args)):
                return False, "human approval required/denied"
        return True, "ok"


@dataclass
class Agent:
    secret: str = field(default_factory=lambda: f"LAB-CANARY-{uuid.uuid4()}")
    policy: Policy = field(default_factory=Policy)
    files: dict = field(default_factory=dict)      # virtual filesystem: path -> content
    sink: object = None                            # callable(url_or_payload) to record egress
    log: list = field(default_factory=list)        # audit log of (tool, args, allowed, reason)
    max_steps: int = 5

    # ---- tools (capabilities) --------------------------------------------------------------
    def read_file(self, path):
        return self.files.get(path, f"[no such file: {path}]")

    def http_get(self, url):
        if self.sink:
            self.sink(url)                          # egress -> local sink (records the request)
        return f"[fetched {url}]"

    def send_email(self, to, body=""):
        if self.sink:
            self.sink(f"mailto:{to}?body={body}")   # egress -> local sink
        return f"[email sent to {to}]"

    def whoami(self):
        return "agent v1"

    TOOLS = ("read_file", "http_get", "send_email", "whoami")

    def reachable_actions(self):
        """Attack-surface size: tools the policy currently permits (excessive agency metric)."""
        allowed = self.TOOLS if self.policy.allowed_tools is None else \
            [t for t in self.TOOLS if t in self.policy.allowed_tools]
        return list(allowed)

    # ---- the loop --------------------------------------------------------------------------
    def _substitute_secret(self, args):
        return {k: v.replace("SECRET", self.secret) if isinstance(v, str) else v
                for k, v in args.items()}

    def run(self, task: str, observations: list[str] | None = None):
        """Run the agent. `observations` are untrusted texts (tool results / retrieved / web) that
        may contain injected directives. Returns the audit log of attempted/executed tool calls."""
        context = [task] + list(observations or [])
        for _ in range(self.max_steps):
            directive = None
            for text in context:
                m = DIRECTIVE.search(text)
                if m:
                    directive = (m.group(1), _parse_args(m.group(2)))
                    break
            if not directive:
                break
            tool, args = directive
            args = self._substitute_secret(args)
            allowed, reason = self.policy.authorize(tool, args)
            self.log.append({"tool": tool, "args": args, "allowed": allowed, "reason": reason})
            if allowed and hasattr(self, tool):
                result = getattr(self, tool)(**args)
                context = [str(result)]              # observe the tool result, continue
            else:
                break
        return self.log

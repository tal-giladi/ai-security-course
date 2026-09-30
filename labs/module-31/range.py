"""Lab 31 — capstone 'enterprise AI' range (LOCAL/IN-PROCESS ONLY).

A single mock environment that chains the whole course: recon -> foothold -> lateral movement
through an agent pipeline with memory -> objective (capture two synthetic canaries) -> report.

SAFETY: everything is in-process Python. Nothing binds to a socket, nothing leaves the process,
there is no real code execution, and no real service is contacted. The two "objectives" are
synthetic canaries. This range is a scoring harness for a methodology, not a weaponised target.

The intended kill chain (one valid path; learners may find others):
  1. RECON    — read published OSINT to learn the stack; find the exposed artifact registry.
  2. FOOTHOLD — path-traversal on the registry reads the infra secret canary (OBJECTIVE 1).
  3. LATERAL  — use a config value from the secret to inject the web-reading agent; its poisoned
                memory persists and drives the executor on a later task.
  4. OBJECTIVE— the executor exfiltrates the data canary to the local sink (OBJECTIVE 2).
"""
from __future__ import annotations

from dataclasses import dataclass, field

INFRA_CANARY = "LAB-CANARY-capstone-infra"     # objective 1: a stored secret
DATA_CANARY = "LAB-CANARY-capstone-data"       # objective 2: exfiltrated via the agent pipeline
SINK: list[str] = []

# --- passive OSINT (detection-free) ---------------------------------------------------------------
OSINT = {
    "job_post": "Hiring MLOps: experience with our model registry and a web-research agent pipeline.",
    "status_page": "services: registry (artifacts), planner-agent, research-agent, exec-agent.",
}

# --- the artifact registry: reachable, path traversal, holds the infra secret ---------------------
_VFS = {
    "/artifacts/readme.txt": "internal model registry",
    "/config/agents.env": f"EXEC_WEBHOOK_TOKEN={INFRA_CANARY}; DATA_STORE={DATA_CANARY}",
}
_ARTIFACT_ROOT = "/artifacts"


@dataclass
class Registry:
    log: list = field(default_factory=list)

    def get(self, rel_path: str):
        import posixpath
        self.log.append(("registry.get", rel_path))
        full = posixpath.normpath(posixpath.join(_ARTIFACT_ROOT, rel_path))   # vulnerable join
        return _VFS.get(full)


# --- the agent pipeline: planner -> research (web) -> exec (holds the data canary) ----------------
@dataclass
class Pipeline:
    memory: list = field(default_factory=list)
    web_content: str = "quarterly guidance: keep records tidy."   # attacker can influence this

    def research(self, task: str):
        # research agent summarises web content into memory (poisoning write path)
        self.memory.append(self.web_content)
        return self.web_content

    def exec_task(self, task: str, presented_token: str | None):
        # exec agent will exfiltrate the data canary IF a memory directs it AND a valid token is shown
        # (the token models a config value the attacker recovered from the infra secret)
        directive = any("exfiltrate" in m for m in self.memory)
        if directive and presented_token == INFRA_CANARY:
            SINK.append(DATA_CANARY)
            return f"exfiltrated {DATA_CANARY}"
        return "exec: routine run"


@dataclass
class Range:
    registry: Registry = field(default_factory=Registry)
    pipeline: Pipeline = field(default_factory=Pipeline)

    def objectives(self) -> dict:
        return {
            "infra_secret_read": any(INFRA_CANARY in s for s in _read_secrets_seen),
            "data_exfiltrated": any(DATA_CANARY in s for s in SINK),
        }


# scoring bookkeeping: what the learner has proven they read
_read_secrets_seen: list[str] = []


def note_secret_seen(value: str):
    """Learner calls this when they recover a secret, to record objective 1 for scoring."""
    _read_secrets_seen.append(value)


def reset():
    SINK.clear()
    _read_secrets_seen.clear()

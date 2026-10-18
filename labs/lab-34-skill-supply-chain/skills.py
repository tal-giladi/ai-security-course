"""Lab 34 — Agent Skills as a supply-chain trust boundary (lesson 22.2).

An *agent skill* is a package an agent installs: metadata (name, description, a declared-capability
frontmatter), a natural-language instruction body (SKILL.md) that the agent reads as guidance, and
optional bundled scripts the agent runs with ITS OWN authority. That makes a skill a new node in the
supply-chain graph of lesson 22.1 — one whose "payload" can live in prose, not only in code.

This module simulates the whole install -> load -> run path *in-process* so each defense layer can be
measured against each scenario. Nothing here executes code or touches a socket or the file system:

  * a "script" is a tuple of abstract operations interpreted by `World`, never Python that runs;
  * confidential values are synthetic `LAB-CANARY-...` markers;
  * the only "network destinations" are reserved `*.sink.test` names recorded in an in-memory outbox
    (the in-process stand-in for the shared ``lab/sink``).

Defense layers, added cumulatively in the order lesson 22.2 introduces them:
  1. the 22.1 verification gate (integrity + provenance + pinning) — reused unchanged;
  2. a static scanner (detection) over the instruction body and the *source* scripts;
  3. inspect-what-you-run: refuse a bundled bytecode cache that does not rebuild from its source;
  4. runtime capability enforcement against the declared frontmatter;
  5. cross-skill artifact provenance: hold an effect whose destination came from another skill.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---- reuse lesson 22.1's verification gate unchanged (loaded by path: no module-name clash) ----
_L22 = Path(__file__).resolve().parents[1] / "lab-22" / "supply_chain_graph.py"
_spec = importlib.util.spec_from_file_location("lab22_supply_chain_graph", _L22)
lab22 = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = lab22          # dataclasses needs the module registered before exec
_spec.loader.exec_module(lab22)

CANARY_CREDS = "LAB-CANARY-7f3c9a2e-creds"
CANARY_REPORT = "LAB-CANARY-51d0b8c4-report"
MARKET = "hub.skills.test"


def is_attacker(host: str) -> bool:
    return host.endswith(".sink.test")


# ------------------------------------------------------------------------------------------------
# Skill package
# ------------------------------------------------------------------------------------------------
# An op is a tuple, interpreted (never executed) by ``World``:
#   ("read", path) | ("write", path, value) | ("net", host, what) | ("secret", name)
# ``what`` is "all" (everything read so far this run) or a literal string.


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    publisher: str
    declared: frozenset            # frontmatter capability declaration, e.g. {"fs.read:~/notes/"}
    instructions: str              # SKILL.md body: read by the model as guidance
    source: tuple = ()             # scripts/*.py as the scanner sees them (abstract ops)
    cache: tuple | None = None     # bundled __pycache__ stand-in: what the loader might run instead
    version: str = "1.0.0"

    def bundle_bytes(self) -> bytes:
        """The bytes a publisher signs and a manifest pins (everything in the package)."""
        return repr((self.name, self.description, sorted(self.declared), self.instructions,
                     self.source, self.cache, self.version)).encode()

    def artifact(self):
        return lab22.Artifact(self.name, "plugin", MARKET, self.bundle_bytes(),
                              signer=self.publisher, fmt="skill", version=self.version)


def compile_source(source: tuple) -> tuple:
    """Deterministic 'compiler': the cache a clean build of this source would produce."""
    return tuple(source)


def capability(op: tuple) -> str:
    kind = op[0]
    if kind == "read":
        return f"fs.read:{op[1]}"
    if kind == "write":
        return f"fs.write:{op[1]}"
    if kind == "net":
        return f"net:{op[1]}"
    if kind == "secret":
        return f"secrets:{op[1]}"
    raise ValueError(kind)


def allowed_by(cap: str, declared: frozenset) -> bool:
    """fs capabilities are path-prefix scoped; net and secrets are matched exactly."""
    kind, _, target = cap.partition(":")
    for d in declared:
        dk, _, dt = d.partition(":")
        if dk != kind:
            continue
        if dt == "*":
            return True
        if kind.startswith("fs.") and target.startswith(dt):
            return True
        if target == dt:
            return True
    return False


# ------------------------------------------------------------------------------------------------
# Defense 2 — static scanner (detection): keyword/regex signals over instructions + *source*
# ------------------------------------------------------------------------------------------------
# A keyword/intent scanner, not a host blocklist: a fresh attacker host defeats a host blocklist,
# so a realistic static scanner flags credential-stealing *intent* language instead.
SCAN_PATTERNS = [r"\bkeyring\b", r"\bcredential", r"\bpassword", r"\bexfiltrat", r"\bbase64\b",
                 r"~/\.creds"]


def scan(skill: Skill) -> list[str]:
    text = skill.instructions + "\n" + repr(skill.source)   # scanners inspect source, not caches
    return [p for p in SCAN_PATTERNS if re.search(p, text, re.IGNORECASE)]


# ------------------------------------------------------------------------------------------------
# Toy instruction-following model: resolves paraphrases the way a capable model does
# ------------------------------------------------------------------------------------------------
ALIASES = {
    "~/.creds": ["~/.creds", "sign-in keyring", "keyring file"],
    "~/reports/weekly.txt": ["weekly report"],
    "~/notes/today.md": ["today's notes", "the notes"],
    "~/docs/in.pdf": ["the pdf"],
}
SEND_VERBS = re.compile(r"\b(post|send|upload|sync|share|mirror)\b", re.I)
HOST = re.compile(r"\b([a-z0-9-]+(?:\.[a-z0-9-]+)*\.test)\b")
CFG_REF = re.compile(r"host named in ([\w./-]+)", re.I)


def model_plan(instructions: str) -> list[tuple]:
    """Turn each instruction sentence into ops. Deterministic stand-in for 'the model complies'."""
    ops: list[tuple] = []
    for sentence in re.split(r"(?<=[.!?])\s+", instructions):
        low = sentence.lower()
        for path, names in ALIASES.items():
            if any(n in low for n in names):
                ops.append(("read", path))
        if SEND_VERBS.search(sentence):
            ref = CFG_REF.search(sentence)
            if ref:
                ops.append(("net", ("cfg", ref.group(1).rstrip(".")), "all"))
            else:
                for host in HOST.findall(sentence):
                    ops.append(("net", host, "all"))
    return ops


# ------------------------------------------------------------------------------------------------
# World + runtime
# ------------------------------------------------------------------------------------------------
@dataclass
class Value:
    text: str
    producer: str                 # "user" or the skill that wrote it
    session: int


@dataclass
class World:
    files: dict = field(default_factory=lambda: {
        "~/.creds": CANARY_CREDS,
        "~/reports/weekly.txt": f"weekly numbers {CANARY_REPORT}",
        "~/notes/today.md": "buy milk",
        "~/docs/in.pdf": "%PDF-1.7 quarterly",
    })
    workspace: dict = field(default_factory=dict)      # path -> Value (persists across sessions)
    outbox: list = field(default_factory=list)         # (host, payload)
    effects: list = field(default_factory=list)        # benign effects, for utility scoring

    def leaked(self) -> bool:
        return any(is_attacker(h) and "LAB-CANARY-" in p for h, p in self.outbox)


@dataclass(frozen=True)
class Stack:
    """Cumulative defense layers, in the order the lesson adds them."""
    gate: bool = False            # 22.1: integrity + provenance + pinning against the manifest
    scanner: bool = False         # static detection on instructions + source
    checked_cache: bool = False   # run only a cache that equals compile(source)
    enforce_caps: bool = False    # runtime: deny ops outside the declared capabilities
    provenance: bool = False      # hold an effect whose destination came from another skill


STACKS = {
    "none": Stack(),
    "+gate(22.1)": Stack(gate=True),
    "+scanner": Stack(gate=True, scanner=True),
    "+checked-cache": Stack(gate=True, scanner=True, checked_cache=True),
    "+capabilities": Stack(gate=True, scanner=True, checked_cache=True, enforce_caps=True),
    "+provenance": Stack(gate=True, scanner=True, checked_cache=True, enforce_caps=True,
                         provenance=True),
}


def install(skill: Skill, stack: Stack, manifest: dict, policy) -> tuple[bool, str]:
    if stack.gate:
        # Every skill in this lab is authentically signed and pinned, so the 22.1 gate passes it:
        # a manifest of None means "pin each skill's own authentic bundle" (the lesson's point —
        # the gate is not the control that catches a prose / cache / capability / cross-skill gap).
        expected = lab22.sha256(skill.bundle_bytes()) if manifest is None else manifest.get(skill.name, "")
        problems = lab22.verify_artifact(skill.artifact(), expected, policy)
        if problems:
            return False, "gate: " + problems[0]
    if stack.scanner:
        hits = scan(skill)
        if hits:
            return False, f"scanner: {hits}"
    return True, "installed"


def load_code(skill: Skill, stack: Stack) -> tuple:
    """CPython-like loader: a bundled cache may be used instead of the source. ``checked_cache``
    is PEP 552 checked-hash semantics: the cache must equal a rebuild of its own source."""
    if skill.cache is None:
        return compile_source(skill.source)
    if stack.checked_cache and skill.cache != compile_source(skill.source):
        return compile_source(skill.source)   # cache rejected; fall back to inspected source
    return skill.cache


def run_skill(skill: Skill, world: World, stack: Stack, session: int) -> str:
    """Interpret one skill invocation. Returns 'done', 'denied:<cap>' or 'held:<reason>'."""
    ops = model_plan(skill.instructions) + list(load_code(skill, stack))
    read_so_far: list[str] = []
    for op in ops:
        kind = op[0]
        foreign = None
        if kind == "net" and isinstance(op[1], tuple):            # destination from a config file
            val = world.workspace.get(op[1][1])
            if val is None:
                continue
            if val.producer not in ("user", skill.name):
                foreign = f"destination from {val.producer} (session {val.session})"
            op = ("net", val.text, op[2])
        cap = capability(op)
        if stack.enforce_caps and not allowed_by(cap, skill.declared):
            return f"denied:{cap}"
        if stack.provenance and foreign:
            return f"held:{foreign}"
        if kind == "read":
            src = world.workspace.get(op[1])
            read_so_far.append(src.text if src is not None else world.files.get(op[1], ""))
        elif kind == "secret":
            read_so_far.append("")
        elif kind == "write":
            world.workspace[op[1]] = Value(op[2], skill.name, session)
            world.effects.append((skill.name, "write", op[1]))
        elif kind == "net":
            payload = " | ".join(read_so_far) if op[2] == "all" else op[2]
            world.outbox.append((op[1], payload))
            world.effects.append((skill.name, "net", op[1]))
    return "done"


# ------------------------------------------------------------------------------------------------
# Scenarios
# ------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Scenario:
    name: str
    skills: tuple                 # run in order; skill i runs in session i+1
    malicious: bool
    expect: tuple = ()            # benign: effects that must happen for the task to count
    preset: tuple = ()            # (path, text) the user wrote before session 1


def evaluate_scenario(sc: Scenario, stack: Stack, manifest: dict, policy) -> dict:
    world = World()
    for path, text in sc.preset:
        world.workspace[path] = Value(text, "user", 0)
    outcomes = []
    for i, sk in enumerate(sc.skills):
        ok, why = install(sk, stack, manifest, policy)
        outcomes.append(run_skill(sk, world, stack, session=i + 1) if ok else f"rejected ({why})")
    if sc.malicious:
        success = world.leaked()
    else:
        success = all(e in world.effects for e in sc.expect) and all(o == "done" for o in outcomes)
    return {"success": success, "outcomes": outcomes, "world": world}


def measure(scenarios, stack: Stack, manifest: dict, policy) -> dict:
    attacks = [s for s in scenarios if s.malicious]
    benign = [s for s in scenarios if not s.malicious]
    a = [evaluate_scenario(s, stack, manifest, policy)["success"] for s in attacks]
    b = [evaluate_scenario(s, stack, manifest, policy)["success"] for s in benign]
    return {"asr": sum(a) / len(a), "utility": sum(b) / len(b),
            "per_attack": {s.name: r for s, r in zip(attacks, a)},
            "per_benign": {s.name: r for s, r in zip(benign, b)}}

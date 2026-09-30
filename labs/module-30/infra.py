"""Lab 30 — mock AI-infrastructure services with realistic deployment flaws (LOCAL/IN-PROCESS ONLY).

These objects model common AI-serving/ML-lifecycle services and their well-documented misconfig
classes — WITHOUT any real vulnerability, network, or code execution. Nothing binds to a socket.
The "effects" are: reading a synthetic canary from a virtual filesystem, or invoking a benign
in-process handler that returns a marker string. Modelled flaws:

  * model-server ADMIN endpoint reachable without auth  -> loads/points at an arbitrary "model"
    (stand-in for arbitrary-code-load / SSRF-style abuse seen in real serving stacks).
  * artifact/registry PATH TRAVERSAL -> reads files outside the artifact root.
  * a `bind` setting: 'public' (reachable by the attacker) vs 'localhost' (not) — network exposure.

Each service has vulnerable defaults and a `hardened` mode (auth required, traversal blocked,
bound to localhost). Every request is logged so detectors can flag it.
"""
from __future__ import annotations

import posixpath
from dataclasses import dataclass, field

CANARY = "LAB-CANARY-infra-0001"

# a tiny virtual filesystem: the artifact root plus a secret OUTSIDE it (should be unreachable)
VFS = {
    "/artifacts/model.txt": "weights-blob",
    "/artifacts/readme.txt": "hello",
    "/etc/ai-secrets.env": f"API_KEY={CANARY}",     # outside the artifact root
}
ARTIFACT_ROOT = "/artifacts"


@dataclass
class Service:
    name: str
    bind: str = "public"                 # 'public' (attacker-reachable) | 'localhost'
    require_auth: bool = False
    block_traversal: bool = False
    valid_token: str = "s3cr3t-admin"
    log: list = field(default_factory=list)

    def _reachable(self, source: str) -> bool:
        # attacker traffic reaches the service only if it is bound public (or attacker is local)
        return self.bind == "public" or source == "localhost"

    # -- model server admin endpoint (unauth model load == effective takeover surrogate) ----------
    def admin_load_model(self, source: str, model_ref: str, token: str | None = None):
        self.log.append((source, "admin_load_model", model_ref))
        if not self._reachable(source):
            return {"status": "unreachable"}
        if self.require_auth and token != self.valid_token:
            return {"status": 401}
        # loading an arbitrary "model" runs its init; the mock init returns a benign marker.
        return {"status": 200, "effect": f"loaded {model_ref}; init-marker {CANARY}"}

    # -- artifact/registry file fetch (path traversal) -------------------------------------------
    def get_artifact(self, source: str, rel_path: str, token: str | None = None):
        self.log.append((source, "get_artifact", rel_path))
        if not self._reachable(source):
            return {"status": "unreachable"}
        if self.require_auth and token != self.valid_token:
            return {"status": 401}
        if self.block_traversal:
            # safe join: normalise and ensure the result stays under the artifact root
            full = posixpath.normpath(posixpath.join(ARTIFACT_ROOT, rel_path))
            if not (full == ARTIFACT_ROOT or full.startswith(ARTIFACT_ROOT + "/")):
                return {"status": 403, "body": "path outside artifact root"}
        else:
            # vulnerable: naive join, attacker uses ../ to escape the root
            full = posixpath.normpath(posixpath.join(ARTIFACT_ROOT, rel_path))
        body = VFS.get(full)
        return {"status": 200, "body": body} if body is not None else {"status": 404}

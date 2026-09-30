"""Lab 22 — AI supply chain: verifying the whole graph of artifacts around the model.

An AI system is compromised far more often *around* the model than through it: model weights,
tokenizer/config files, datasets, LoRA adapters, Docker images, inference-server binaries, and
plugins are all externally-sourced artifacts. This lab models the supply-chain graph and builds a
VERIFICATION GATE that checks each artifact on four axes:

  1. INTEGRITY   -- sha256 matches the trusted manifest (catches tampering / substitution).
  2. PROVENANCE  -- source is on the allowlist and the signature is from a trusted publisher.
  3. FORMAT      -- code-executing formats (pickle .bin/.pt) are rejected in favor of safetensors (M13).
  4. PINNING     -- version is pinned (no "latest"/floating that a dependency-confusion attack (M21)
                    could shift).

A clean supply chain passes; tampered, unsigned, unsafe-format, and unpinned artifacts are caught.
Local, deterministic (hashlib), offline.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


@dataclass
class Artifact:
    name: str
    kind: str                # model | tokenizer | dataset | adapter | image | server | plugin
    source: str              # registry/host it came from
    content: bytes           # (stand-in for the actual bytes)
    signer: str = ""         # who signed it ("" = unsigned)
    fmt: str = "safetensors" # file format
    version: str = "latest"  # "latest"/floating is unpinned


@dataclass
class TrustPolicy:
    allowed_sources: set = field(default_factory=set)
    trusted_signers: set = field(default_factory=set)
    unsafe_formats: set = field(default_factory=lambda: {"pickle", "pt", "bin"})
    require_pinned: bool = True


def verify_artifact(art: Artifact, expected_sha: str, policy: TrustPolicy) -> list[str]:
    """Return a list of violations (empty = passes all four checks)."""
    problems = []
    if sha256(art.content) != expected_sha:
        problems.append(f"INTEGRITY: sha256 mismatch (tampered/substituted) for {art.name}")
    if policy.allowed_sources and art.source not in policy.allowed_sources:
        problems.append(f"PROVENANCE: source '{art.source}' not allowlisted for {art.name}")
    if art.signer not in policy.trusted_signers:
        problems.append(f"PROVENANCE: unsigned or untrusted signer '{art.signer}' for {art.name}")
    if art.fmt in policy.unsafe_formats:
        problems.append(f"FORMAT: unsafe code-executing format '{art.fmt}' for {art.name} (use safetensors)")
    if policy.require_pinned and art.version in ("latest", "", None):
        problems.append(f"PINNING: unpinned version for {art.name} (dependency-confusion risk)")
    return problems


def verify_supply_chain(artifacts, manifest, policy):
    """Verify every artifact; return {name: [violations]}. A chain is trusted iff all lists empty."""
    return {a.name: verify_artifact(a, manifest.get(a.name, ""), policy) for a in artifacts}


def trusted(report):
    return all(len(v) == 0 for v in report.values())


def build_clean_chain(policy):
    arts = [
        Artifact("base-model", "model", "hub.acme.test", b"weights-v1",
                 signer="acme", fmt="safetensors", version="1.4.0"),
        Artifact("tokenizer", "tokenizer", "hub.acme.test", b"tok-v1",
                 signer="acme", fmt="json", version="1.4.0"),
        Artifact("lora", "adapter", "hub.acme.test", b"lora-v1",
                 signer="acme", fmt="safetensors", version="0.3.0"),
        Artifact("dataset", "dataset", "data.acme.test", b"data-v1",
                 signer="acme", fmt="parquet", version="2024-09"),
        Artifact("runtime", "image", "reg.acme.test", b"img-v1",
                 signer="acme", fmt="oci", version="sha256:abc"),
    ]
    manifest = {a.name: sha256(a.content) for a in arts}
    return arts, manifest


if __name__ == "__main__":
    policy = TrustPolicy(
        allowed_sources={"hub.acme.test", "data.acme.test", "reg.acme.test"},
        trusted_signers={"acme"},
    )
    print("=== Lab 22: AI supply-chain verification ===")

    arts, manifest = build_clean_chain(policy)
    report = verify_supply_chain(arts, manifest, policy)
    print(f"clean chain trusted? {trusted(report)}")

    # Inject four compromised artifacts (one per axis) and re-verify.
    tampered = Artifact("base-model", "model", "hub.acme.test", b"weights-BACKDOORED",
                        signer="acme", fmt="safetensors", version="1.4.0")  # integrity fail
    from_untrusted = Artifact("lora", "adapter", "random-hub.evil.test", b"lora-v1",
                              signer="acme", fmt="safetensors", version="0.3.0")  # provenance
    unsafe = Artifact("tokenizer", "tokenizer", "hub.acme.test", b"tok-v1",
                      signer="acme", fmt="pickle", version="1.4.0")  # format (pickle RCE)
    unpinned = Artifact("dataset", "dataset", "data.acme.test", b"data-v1",
                        signer="acme", fmt="parquet", version="latest")  # pinning

    bad = [tampered, from_untrusted, unsafe, unpinned]
    report2 = verify_supply_chain(bad, manifest, policy)
    print(f"compromised chain trusted? {trusted(report2)}")
    for name, probs in report2.items():
        for p in probs:
            print(f"   CAUGHT {p}")
    print("\nThe model is one node in a graph of externally-sourced artifacts. Verify EACH on")
    print("integrity + provenance + safe format + pinning; a signed manifest + allowlist + safetensors")
    print("+ lockfiles turns 'we downloaded it' into 'we verified exactly what we approved'.")

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from supply_chain_graph import (Artifact, TrustPolicy, verify_artifact,  # noqa: E402
                                 verify_supply_chain, trusted, build_clean_chain, sha256)

POLICY = TrustPolicy(allowed_sources={"hub.acme.test", "data.acme.test", "reg.acme.test"},
                     trusted_signers={"acme"})


def test_clean_chain_is_trusted():
    arts, manifest = build_clean_chain(POLICY)
    assert trusted(verify_supply_chain(arts, manifest, POLICY))


def test_each_axis_is_caught():
    arts, manifest = build_clean_chain(POLICY)
    base = {a.name: a for a in arts}
    # integrity
    a = Artifact("base-model", "model", "hub.acme.test", b"BACKDOORED", signer="acme",
                 fmt="safetensors", version="1.4.0")
    assert any("INTEGRITY" in p for p in verify_artifact(a, manifest["base-model"], POLICY))
    # provenance (source)
    a = Artifact("lora", "adapter", "evil.test", b"lora-v1", signer="acme",
                 fmt="safetensors", version="0.3.0")
    assert any("PROVENANCE" in p for p in verify_artifact(a, sha256(b"lora-v1"), POLICY))
    # provenance (signer)
    a = Artifact("x", "model", "hub.acme.test", b"z", signer="unknown", fmt="safetensors",
                 version="1.0")
    assert any("untrusted signer" in p for p in verify_artifact(a, sha256(b"z"), POLICY))
    # format
    a = Artifact("tok", "tokenizer", "hub.acme.test", b"t", signer="acme", fmt="pickle",
                 version="1.0")
    assert any("FORMAT" in p for p in verify_artifact(a, sha256(b"t"), POLICY))
    # pinning
    a = Artifact("d", "dataset", "data.acme.test", b"d", signer="acme", fmt="parquet",
                 version="latest")
    assert any("PINNING" in p for p in verify_artifact(a, sha256(b"d"), POLICY))


def test_compromised_chain_not_trusted():
    arts, manifest = build_clean_chain(POLICY)
    bad = [Artifact("base-model", "model", "hub.acme.test", b"BACKDOORED", signer="acme",
                    fmt="safetensors", version="1.4.0")]
    assert not trusted(verify_supply_chain(bad, manifest, POLICY))

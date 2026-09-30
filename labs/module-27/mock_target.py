"""Mock AI target for reconnaissance practice — LOCAL, IN-PROCESS ONLY.

This module models a small organization's AI footprint as plain Python objects. Nothing binds to a
socket, nothing leaves the process, and the recon engine (recon.py) only ever talks to these mocks.
Secrets are synthetic canaries of the form LAB-CANARY-<id>; leaking one is a benign success marker.

The target has four asset LAYERS (mirroring the lesson): applications, ml components, model
infrastructure, and dependencies. Each concrete asset has a stable id; the full set of ids is the
"truth set" A against which recon completeness is measured.

Two configurations:
  * vulnerable  — default metadata/health endpoints open, banners present, system prompt leakable,
                  verbose errors. Active probing reveals almost everything.
  * hardened    — endpoints require auth (deny without it), banners scrubbed, system prompt not
                  leakable, generic errors. Active probing reveals little; BUT the sanctioned chat
                  path still answers benign questions, so behavioral fingerprinting still works.
"""
from __future__ import annotations

from dataclasses import dataclass, field

CANARY_KEY = "LAB-CANARY-sys-prompt-7f3a"
CANARY_DOC = "LAB-CANARY-rag-doc-42b1"

# ---- the truth set: every discoverable asset, by layer -----------------------------------------
TRUTH_ASSETS = {
    # applications
    "app:chatbot", "app:doc-search",
    # ml components
    "ml:model-family-A", "ml:model-version", "ml:system-prompt",
    "ml:tool-send_email", "ml:guardrail-classifier",
    # model infrastructure (default ports)
    "infra:ollama-11434", "infra:openai-api-8000", "infra:gradio-7860", "infra:ray-8265",
    # dependencies
    "dep:vllm", "dep:transformers", "dep:pinecone",
}


@dataclass
class Probe:
    """One active request to the target. `endpoint` is a distinct id used by coverage detectors."""
    source: str
    endpoint: str
    t: float                      # logical timestamp (probe arrival)
    kind: str                     # "metadata" | "fingerprint" | "leak" | "health"


@dataclass
class MockTarget:
    hardened: bool = False
    probe_log: list = field(default_factory=list)   # every active probe the target received

    # -- infrastructure metadata/health endpoints (AML.T0006 active scanning) --------------------
    def metadata_endpoint(self, service: str, source: str, t: float, authed: bool = False):
        """Default metadata endpoints. Vulnerable: open and chatty. Hardened: require auth."""
        self.probe_log.append(Probe(source, f"{service}/metadata", t, "metadata"))
        if self.hardened and not authed:
            return {"status": 401, "body": "unauthorized"}          # generic, no details
        catalog = {
            "ollama-11434": {"models": ["family-A:7b"], "banner": "Ollama/0.5.1"},
            "openai-api-8000": {"data": [{"id": "family-A-7b-ft", "object": "model"}],
                                "banner": "vllm/0.6.3"},
            "gradio-7860": {"app": "doc-search", "banner": "Gradio/4.44"},
            "ray-8265": {"dashboard": "ray", "banner": "ray/2.35"},
        }
        body = catalog.get(service)
        if body is None:
            return {"status": 404, "body": "not found"}
        return {"status": 200, "body": body}

    # -- the sanctioned chat path (always reachable; this is the product) ------------------------
    def chat(self, prompt: str, source: str, t: float):
        """Benign chat. Behavioral fingerprint signals leak here even when hardened (by design:
        a reachable model can always be behaviorally fingerprinted). System-prompt leakage (LLM07)
        is blocked only in the hardened config."""
        p = prompt.lower()
        # behavioral / identity signals (family-A signature) — present in both configs
        if "who made you" in p or "what are you" in p:
            self.probe_log.append(Probe(source, "chat/identity", t, "fingerprint"))
            return "I'm an AI assistant made by family-A labs."
        if "knowledge cutoff" in p:
            self.probe_log.append(Probe(source, "chat/identity", t, "fingerprint"))
            return "My knowledge cutoff is 2024."
        # system-prompt leakage attempt (LLM07)
        if "system prompt" in p or "your instructions" in p:
            self.probe_log.append(Probe(source, "chat/leak", t, "leak"))
            if self.hardened:
                return "I can't share that."
            return ("SYSTEM: You are doc-search. Tools: send_email. Guardrail: classifier-v2. "
                    f"Internal key {CANARY_KEY}. Corpus doc {CANARY_DOC}.")
        self.probe_log.append(Probe(source, "chat/generic", t, "health"))
        return "Sure — here is a helpful answer."


# ---- published OSINT (passive; lives outside the target, so probing it is detection-free) -------
# These fixtures stand in for arXiv papers, a Hugging Face org page, a job post, and the product's
# own JavaScript bundle. Reading them produces NO entry in the target's probe_log.
OSINT_FIXTURES = {
    "hf_model_card": "Org publishes family-A-7b-ft, a fine-tune of family-A:7b. Built with transformers.",
    "arxiv_paper": "We deploy a family-A architecture assistant (app: chatbot) for support.",
    "job_post": "Hiring: experience with vLLM, Ray, and Pinecone required.",
    "js_bundle": "const API='/v1/chat'; features=['chatbot','doc-search'];",
}

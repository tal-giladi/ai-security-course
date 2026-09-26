<div class="prereq">

**Prerequisites.** [13.1 weights/adapter supply chain](../module-13/lesson-01.md),
[21.1 code-agent / dependency confusion](../module-21/lesson-01.md), [01.1 supply chain / deserialization](../module-01/lesson-01.md),
[11.1 poisoning](../module-11/lesson-01.md). Lab: hashlib, offline.

**You will learn.** The full **AI supply chain** as an attack surface — model hubs, datasets,
tokenizer/config files, LoRA adapters, Docker images, inference servers, plugins — and how to build a
**verification gate** (integrity, provenance, safe format, pinning) that turns "we downloaded it" into
"we verified exactly what we approved." This ties M13 and M21 into one discipline.

**Why this matters.** You can perfectly secure a model's behavior and still be compromised by a
poisoned dataset, a pickle tokenizer, an unpinned dependency, or a backdoored base image. Most AI
compromise happens *around* the model, through the graph of artifacts you assemble it from — and that
graph is defensible with the same structural controls (hashes, signatures, allowlists, safe formats,
lockfiles) that secure any software supply chain.

</div>

# 22.1 · AI supply-chain security

## Why this matters

An AI system is not a model; it's a *graph*: weights + tokenizer + config + datasets + adapters +
inference server + container image + plugins, each fetched from somewhere. Every node is a place an
attacker can substitute, poison, or backdoor. The lesson of this module is that securing the model's
outputs is necessary but nowhere near sufficient — you must verify the provenance and integrity of
the whole graph.

## Learning objectives

1. Enumerate the AI supply-chain graph and the compromise vector at each node.
2. Build a **verification gate** checking integrity, provenance, safe format, and pinning per artifact.
3. Explain why **verification** (structural) beats **detection** (probabilistic) for supply chain.
4. Map to frameworks (SLSA levels, signed manifests, SBOM) and the residual risk (signed-but-malicious).
5. Integrate the per-node defenses from M13 (safetensors/pickle) and M21 (lockfiles/pinning).

## Concept

### The graph and its compromise vectors

| Node | Compromise vector | Per-node defense (module) |
|---|---|---|
| Model weights | backdoor/poison; pickle RCE | behavioral vetting (M11), safetensors (M13) |
| Tokenizer/config | code paths, `trust_remote_code` | safe formats, no remote code (M13) |
| Dataset | poisoning (M11) | provenance, dedup, integrity hash |
| LoRA/adapter | stealthy backdoor (M13) | signing, behavioral vetting |
| Inference server | compromised binary/CVE | pinned+signed image, SBOM |
| Docker image | backdoored base layer | pinned digest, signed image, scan |
| Plugin/MCP server | tool poisoning, RCE (M17/M19) | allowlist/pin/sign, capability scoping |

Each node is externally sourced; a break at *any* node compromises the system (the M18 chain applied
to artifacts). So the defense is per-node **verification**, applied to the whole graph.

### Verification beats detection

You cannot reliably *detect* a backdoored model or a novel malicious payload (M11/M13 — detection has
false negatives). But you *can* **verify**: enforce that each artifact is (1) byte-identical to a
trusted manifest (**integrity**, sha256), (2) from an allowlisted source signed by a trusted publisher
(**provenance**), (3) in a non-code-executing format (**safe format**, safetensors not pickle), and
(4) pinned to an exact version (**pinning**, no `latest`). Verification is structural — it doesn't ask
"is this bad?" but "is this *exactly the approved thing*?" — sidestepping the base-rate problem of
scanners (M02.2). Lab: the gate catches tampering, untrusted source, pickle format, and unpinned
version, one per axis.

## Intuition

Assembling an AI system from hub downloads is like building a car from parts ordered off the internet.
Inspecting the finished car's *handling* (model behavior) won't reveal that the brake line is a
counterfeit or the ECU firmware was swapped. What keeps you safe is a **bill of materials with
tamper-evident seals**: each part has a part number (pin), a serial that matches the manufacturer's
manifest (integrity), a certificate from an approved supplier (provenance), and isn't a type known to
hide explosives (safe format). You verify the parts, not just test-drive the car.

## Technical explanation & Code

`labs/lab-22/supply_chain_graph.py`: `Artifact` (name/kind/source/content/signer/fmt/version), a
`TrustPolicy` (allowed sources, trusted signers, unsafe formats, require-pinned), and `verify_artifact`
returning violations across the four axes. `verify_supply_chain` verifies the whole graph; `trusted`
is true iff every node passes. A clean chain passes; four injected artifacts (one per axis) are each
caught with a specific reason.

## Mathematics

**Chain integrity (M18 again).** The system is trusted only if *all* $N$ nodes verify:
$P(\text{system safe}) = \prod_{i=1}^{N} \mathbb 1[\text{node }i\text{ verified}]$ — a single failed
node fails the system, so coverage must be complete (every artifact, including transitive ones). This
is why partial verification ("we check the model but not the tokenizer") is nearly worthless: the
attacker targets the unverified node.

**Verification vs detection, formally.** A detector has false-negative rate $\beta>0$ (a novel
backdoor slips through), so residual risk per node is $\ge \beta$. Verification against a trusted
manifest has *zero* false negatives for substitution/tampering (a changed byte changes the hash with
overwhelming probability — collision resistance), reducing that residual to the probability of a
*compromised trusted publisher/manifest* — a much smaller, auditable surface. You trade "detect all
bad things" (impossible) for "trust a small set of publishers/keys" (manageable). The residual is
exactly a **signed-but-malicious** publisher (M13) — hence defense-in-depth with behavioral vetting.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — supply-chain verification gate.**
- **Stops:** substitution/tampering (integrity), fetches from untrusted sources or unsigned/wrong
  signers (provenance), code-executing formats (safe format, structural), and version-shift/dependency
  confusion (pinning) — across every verified node. Structural, not detection-based.
- **Does NOT stop:** a **compromised or malicious trusted publisher** (signs real malware), a poisoned
  dataset/backdoored model that is *legitimately* the approved artifact (needs behavioral vetting,
  M11/M13), or **unverified/transitive** nodes you forgot to include.
- **Attacker adapts:** compromise/impersonate a trusted signer, poison an artifact *before* it's
  signed, or target a node outside the gate's coverage.
- **Cost:** manifest/signature/lockfile infrastructure and discipline; you must enumerate the *whole*
  graph (including transitive deps and base images).
- **Takeaway:** verification (integrity + provenance + safe format + pinning) is the structural
  backbone of AI supply-chain security — necessary and high-leverage — but it trusts publishers, so
  pair it with behavioral vetting (M11/M13) and complete coverage of the graph. "We downloaded it"
  must become "we verified exactly what we approved, everywhere."

</div>

## Practical lab

<div class="lab">

**Lab 22** ([`labs/lab-22/`](../../labs/lab-22/README.md)) — supply-chain graph + four-axis
verification gate. hashlib, offline.

```bash
py labs/lab-22/supply_chain_graph.py
py -m pytest labs/lab-22 -q
```

</div>

## Exercise

1. **Transitive coverage.** Add a plugin that pulls its own dependencies; show that verifying only
   top-level artifacts misses a compromised transitive node, then extend the gate to the full closure.
2. **Real signature verification.** Replace "signer present" with actual signature *verification*
   against a key store (sign the manifest, verify with a public key); show a forged signature fails and
   a valid one passes.
3. **Compromised-but-signed publisher (residual).** Model a trusted signer that signs a backdoored
   model; show the gate passes it (verification's residual), then add behavioral vetting (M11 trigger
   probing) as the complementary control.
4. **Integrate M13 + M21.** Wire in a pickle-format scan (M13) and a lockfile+integrity-hash check
   (M21); show the unified gate catches RCE-format and dependency-confusion together.
5. **SLSA mapping.** Map your gate to SLSA build/provenance levels and produce an SBOM for the graph;
   state which threats each level addresses. Write the guarantee box for a production model-deployment
   pipeline.

<details><summary>Hint (step 3)</summary>

Verification proves "this is the artifact the publisher signed", not "this artifact is safe". A
malicious/compromised publisher defeats it — the residual the guarantee box names. The only defense
for a signed-but-backdoored model is *behavioral* (M11: probe for triggers, evaluate on your own held
data), which is why supply-chain security layers verification (provenance) with vetting (behavior).

</details>

**Deliverable.** Transitive coverage, real signature verification, the compromised-publisher residual +
behavioral vetting, the integrated M13/M21 gate, and the SLSA/SBOM mapping + guarantee box.

## Research paper

**SLSA (Supply-chain Levels for Software Artifacts)** framework + **Sigstore/in-toto** (signing &
provenance) + a real **AI-artifact incident** (malicious models on a public hub; poisoned dataset).
*Why:* SLSA/Sigstore are the industry structure for exactly this gate; the incident shows the concrete
delivery. *Read:* SLSA's provenance/build-integrity levels; Sigstore's keyless signing model; the
incident's artifact path. *Reproduce:* the lab is the gate; add real signature verification (Exercise
2) toward SLSA provenance. *Limits:* SLSA addresses build/provenance integrity, not model *behavior* —
a genuinely-backdoored-but-properly-built model still passes, so behavioral vetting remains necessary.

## Further reading

- OWASP LLM03 (Supply Chain); MITRE ATLAS (ML supply-chain compromise); NIST SSDF;
  [`references/standards-map.md`](../../references/standards-map.md). Back-links M11, M13, M21.

## Assessment

<details><summary>Q1. Why is securing model behavior insufficient?</summary>

Because the system is a graph of externally-sourced artifacts (weights, tokenizer, dataset, adapter,
image, server, plugins), and a compromise at *any* node — a pickle tokenizer, a poisoned dataset, a
backdoored base image, an unpinned dependency — compromises the system regardless of how well the
model's outputs are vetted. You must verify the whole graph.

</details>

<details><summary>Q2. Why does verification beat detection for supply chain?</summary>

Detection has false negatives (a novel backdoor/payload slips past a scanner). Verification against a
trusted manifest has ~zero false negatives for substitution/tampering (a changed byte changes the
hash — collision resistance) and enforces "exactly the approved artifact from an approved signer in a
safe format at a pinned version." It trades the impossible "detect all bad things" for the manageable
"trust a small set of publishers/keys."

</details>

<details><summary>Q3. What is the residual risk of a verification gate, and how do you cover it?</summary>

A compromised or malicious *trusted publisher* that legitimately signs a backdoored/poisoned artifact —
verification passes it because it *is* the approved, signed artifact. Cover it with behavioral vetting
(M11 trigger probing, evaluation on your own data) and complete graph coverage (including transitive
deps and base images).

</details>

## What you should now be able to do

- Enumerate the AI supply-chain graph and the compromise vector at each node.
- Build a verification gate (integrity + provenance + safe format + pinning) covering the whole graph.
- Explain why verification is structural and where its residual (trusted-publisher compromise) lies.
- Integrate M13/M21 defenses and map to SLSA/SBOM, pairing verification with behavioral vetting.

## Progress checkpoint

```bash
py course.py complete 22.1
py course.py next
```

**Next:** Stage 9 — 23.1 · Defensive engineering: input filtering, output validation, structured
output, policy enforcement, isolation, monitoring — each with its guarantee analysis and limits.

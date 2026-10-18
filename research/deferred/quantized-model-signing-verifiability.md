# Quantized-artifact signing verifiability (what you sign is not what you run)

- **Topic ID:** quantized-model-signing-verifiability
- **Status:** WAIT
- **Next review:** 2026-11-22
- **Course change:** none
- **Candidates:** C-20261015-02

## Summary

Model signing authenticates full-precision release weights, but the artifact users actually run (a
quantized GGUF) is a different object whose production is not reproducible from what is signed or
documented. Defines an Independent Verifiability Rate (IVR); across the 200 most-downloaded Hugging
Face GGUF repos, no card records the build environment (IVR 0/198), but two extra disclosed
coordinates (fp-contraction setting; per-tensor quant recipe) re-derive 7/8 target files bit-for-bit
on x86. Directly extends M22's "signed-but-malicious / verify the whole graph" theme to the
quantization step. Adversarial-fp16 edits lie explicitly outside the protocol's guarantee.

## Evidence

- https://arxiv.org/abs/2610.19498 — Liu, Tsai; real-scale measurement; audit data + re-runnable harness stated as released (location unconfirmed from the abstract); single preprint, affiliations unconfirmed.

## What would change the decision

Confirmed public harness; independent reproduction of the 7/8 re-derivation; a CPU-feasible toy
(quantize → sign full-precision → attempt bit-exact re-derivation) for a M22.1 extension.

## History

- 2026-10-18 — WAIT — concrete real-scale finding that cleanly extends M22.1, with a stated fix and an explicit out-of-scope limit, but single preprint, unconfirmed code and affiliations; ADD budget used on skill-trust-boundary (a more mature M22 node) — weekly/2026-W42.md — candidates C-20261015-02

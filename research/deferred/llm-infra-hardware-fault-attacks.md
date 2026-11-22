# Rowhammer against LLM-serving JIT compilation (LLVMhammer)

- **Topic ID:** llm-infra-hardware-fault-attacks
- **Status:** WAIT
- **Next review:** 2027-01-17
- **Course change:** none
- **Candidates:** C-20261024-02, C-20261120-01

## Summary

A CPU-DRAM Rowhammer bit-flip corrupts an optimization pass in Triton's MLIR/LLVM pipeline, producing a slower (4–16%) or output-corrupting kernel that persists via the on-disk kernel cache; NVIDIA and AMD.

## Evidence

- https://arxiv.org/abs/2610.30798 — single preprint, no code, no mitigation.
- https://arxiv.org/abs/2611.25945 — BlockJack (C-20261120-01): Rowhammer on vLLM paged-KV block tables redirects one tenant's KV reads to another's blocks; vendor confirmation per the authors only; no advisory found; no code. Added 2026-11-22.

## What would change the decision

Replication plus a mitigation (e.g. kernel-cache integrity checks) with cost; a lab would need Rowhammer-capable hardware, so a simulated fault-injection lab is the only safe option.

## History

- 2026-10-25 — WAIT — novel but hardware-bound, attack-only, single preprint; low curriculum priority — weekly/2026-W43.md — candidates C-20261024-02
- 2026-11-22 — WAIT — a multi-tenant KV-cache fault attack with a mitigation, but single preprint and unverified vendor confirmation; date unchanged — next review 2027-01-17 — weekly/2026-W47.md — candidates C-20261120-01

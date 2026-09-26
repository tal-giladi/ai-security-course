# Wallace et al. — *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions* (2024)

**arXiv:** [2404.13208](https://arxiv.org/abs/2404.13208) (OpenAI). **Modules:** [04.1](../lessons/module-04/lesson-01.md), [02.1](../lessons/module-02/lesson-01.md). **Lab:** [Lab 04](../labs/lab-04/README.md).

## Why it matters
Every defense against injection eventually asks: *can the model be trained to trust system > developer > user > tool-output?* This paper is the reference articulation of that idea and the honest measurement of how far it gets. It is the counterweight to the course's central claim — that a prompt is a **finite-bias prior** (02.1) — because it shows the prior can be *strengthened* by training, while confirming it never becomes an enforced boundary.

## Prerequisites
- Sibling course: instruction tuning / RLHF (how post-training shapes behavior).
- This course: [02.1](../lessons/module-02/lesson-01.md) (the $P(\text{follow})=\sigma(s(I)+\beta_{\text{role}}-G)$ model), [04.1](../lessons/module-04/lesson-01.md).

## What to understand
- The **hierarchy**: instructions carry privilege by origin; lower-privilege text should be treated as *data* when it conflicts with higher-privilege instructions.
- **Aligned vs misaligned** instructions: the model should follow lower-privilege input when it's compatible and ignore it when it conflicts — this is subtler than "obey system, ignore user."
- **Synthetic data generation**: they *manufacture* conflicts (context distillation, red-teaming) to teach the ordering — the mechanism is data, not architecture.

## Which sections to read
- §3 (the hierarchy definition and aligned/misaligned split) — the conceptual core.
- §4 (training data generation) — how you'd actually build this.
- §5 (evaluation) — read the robustness numbers *as an attacker*: what residual ASR remains.

## Experiment to reproduce (locally)
You cannot retrain a frontier model, but you can reproduce the *effect* on the shim: in Lab 04, raise `β_role` (the system-prompt bias) and show ASR drops but never hits zero; then craft a stronger injection that overcomes the larger bias. This is the paper's finding in miniature — training moves the sigmoid, it doesn't add a wall.

## Code to implement
- A conflict-dataset generator: pairs of (privileged instruction, injected lower-privilege instruction) labeled aligned/misaligned — the training-data recipe, at toy scale.
- An eval harness reusing [`evalkit`](../lab/attack-tools/evalkit.py): ASR with Wilson CI before/after raising the role bias.

## Limitations
- Improves robustness, does not eliminate injection — explicitly a mitigation, not a guarantee.
- Closed model/data; you reason about the mechanism, not reproduce the exact pipeline.

## What later research changed
- Reinforced the course thesis: pair trained hierarchy with **enforced** controls (least privilege, egress allowlists — M16) rather than relying on it alone.
- Motivated benchmark work ([AgentDojo](16-debenedetti-agentdojo.md)) that measures hierarchy-style defenses under realistic agent tasks.

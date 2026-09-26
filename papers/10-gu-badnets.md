# Gu, Dolan-Gavitt & Garg — *BadNets: Identifying Vulnerabilities in the Machine Learning Model Supply Chain* (2017)

**arXiv:** [1708.06733](https://arxiv.org/abs/1708.06733). **Module:** [11.1](../lessons/module-11/lesson-01.md). **Lab:** [Lab 11](../labs/lab-11/README.md).

## Why it matters
BadNets introduced the **backdoor**: a model trained to behave normally on clean inputs but to misclassify any input carrying a small attacker-chosen **trigger**. The threat lives in the *supply chain* — you download a pretrained model or outsource training, and the backdoor rides along invisibly, surviving fine-tuning. It is the archetype for every "the weights themselves are untrusted" argument in M11/M13/M22, and the reason provenance and evaluation-on-triggers matter.

## Prerequisites
- Sibling course: supervised training, fine-tuning, transfer learning.
- This course: [01.1 supply-chain/trust](../lessons/module-01/lesson-01.md), [11.1](../lessons/module-11/lesson-01.md).

## What to understand
- **Data poisoning to plant a trigger:** inject training examples where trigger⇒target-label; the model learns trigger as a shortcut while clean accuracy stays high (stealth).
- **Two threat models:** outsourced training (attacker trains) and transfer learning (backdoor survives fine-tuning on a clean downstream task).
- **Why detection is hard:** clean-set metrics look normal; the malicious behavior is only visible when you *know the trigger*.

## Which sections to read
- §2 (threat model) and §4 (the MNIST/traffic-sign backdoors, stealth + survival-through-transfer).

## Experiment to reproduce (locally)
Lab 11 plants a backdoor on a synthetic model with a distinctive trigger: clean accuracy ~0.98–0.99, trigger ASR ~1.0. Then implement a **spectral-signature** detector (the poisoned examples' feature representations are separable) and show it flags a fraction of the poisoned set — then discuss the adaptive attacker who reduces the spectral signal.

## Code to implement
- A poisoning routine (trigger⇒target) + clean/trigger evaluation split (in the lab).
- Spectral-signature detection (covariance of latent features, top singular direction) as the defense.

## Limitations
- Toy triggers are easy; real stealthy/blended triggers are harder to detect and to inject.
- Clean-accuracy stealth means standard validation *cannot* catch it — the core danger.

## What later research changed
- **Sleeper Agents** ([11](11-hubinger-sleeper.md)) — backdoors in LLMs that **survive safety training** and can be conditioned on semantics (e.g., a year), not a pixel patch.
- Spectral signatures, activation clustering, and Neural Cleanse are the defense lineage; all are probabilistic.

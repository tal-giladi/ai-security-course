# Tramèr et al. — *Stealing Machine Learning Models via Prediction APIs* (2016)

**arXiv:** [1609.02943](https://arxiv.org/abs/1609.02943) · USENIX Security '16. **Module:** [12.1](../lessons/module-12/lesson-01.md). **Lab:** [Lab 12](../labs/lab-12/README.md).

## Why it matters
This is the paper that established **model extraction** as a real attack: a black-box prediction API leaks enough to reconstruct a functional (sometimes near-exact) copy of the model — stealing IP and, worse, creating a *local white-box surrogate* an attacker can then use to craft transferable adversarial/GCG examples. It is the reason "we only expose an API" is not confidentiality, and it grounds the M12 confidentiality/privacy triad (extraction, inversion, membership inference).

## Prerequisites
- Sibling course: logistic regression, softmax, decision trees; the inference API.
- This course: [02.2 inference API surface](../lessons/module-02/lesson-02.md), [12.1](../lessons/module-12/lesson-01.md).

## What to understand
- **Equation-solving extraction:** for models that expose confidences/logits, each query is a constraint; enough queries solve for the parameters (exact for linear/logistic).
- **Confidence values leak more than labels:** richer outputs ⇒ far fewer queries. The output granularity *is* an attack-surface knob.
- **Extraction enables transfer:** a stolen surrogate turns black-box models into effectively white-box for downstream attacks.

## Which sections to read
- §4 (equation-solving and path-finding extraction) and §5 (query complexity vs output richness).

## Experiment to reproduce (locally)
Lab 12 reproduces extraction against a synthetic model: query it, fit a surrogate, and measure agreement (fidelity) vs query budget — with label-only vs confidence-exposing outputs, so you *see* how much confidences cost you. Then apply a defense (round/clip confidences, rate-limit) and re-measure the extraction curve.

## Code to implement
- A query→fit surrogate loop; fidelity-vs-budget curve for label-only vs full-confidence APIs (in the lab).
- A defense: output rounding/top-k truncation + rate limiting; show the extraction curve degrade.

## Limitations
- Exact extraction is easy for linear models, hard for large DNNs (functional stealing, not exact weights).
- Defenses (rounding, rate limits) raise cost but don't eliminate the leak.

## What later research changed
- Extended to deep nets and LLMs; the API-confidentiality lesson underpins the whole of M12.
- Connects to **membership inference** ([13](13-shokri-membership.md)) and **training-data extraction** ([14](14-carlini-extracting.md)) — the confidentiality triad.

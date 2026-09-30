# Glossary inbox — module 27 (recon)

- **Reconnaissance (AI)** — mapping an AI target (apps, ML components, infrastructure, dependencies) before exploitation; MITRE ATLAS tactic AML.TA0002.
- **Passive recon** — learning from signals that already exist (OSINT, public bundles, manifests, scan indexes) without touching the target's AI path; detection-free.
- **Active recon** — sending inputs/probes and reading outputs; every probe is a loggable event.
- **Model fingerprinting** — inferring model family/provider/version from behavioural and protocol signals (refusal style, error envelope, tokenizer artefacts, latency).
- **Asset completeness** — fraction of a target's discoverable assets that recon has mapped.
- **Low-and-slow** — keeping the probe rate below a rate detector's threshold to evade volume-based detection.
- **Coverage/fan-out detector** — flags a source that touches many distinct endpoints in a session; defeats low-and-slow because slowing changes timing, not fan-out.
- **Information per noise** — the recon objective: maximise mutual information about the config subject to a detection-cost budget (a knapsack).

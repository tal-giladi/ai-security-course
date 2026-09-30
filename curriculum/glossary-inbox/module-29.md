# Glossary inbox — module 29 (embeddings)

- **Embedding inversion** — recovering (much of) the input text from its embedding vector, given the encoder or a surrogate.
- **Attribute extraction** — reading a private property (topic, author, presence of a sensitive term) off an embedding with a probe, without full inversion.
- **Surrogate encoder** — an imperfect copy/approximation of the target encoder; often enough to invert without exact weights.
- **vec2text** — method reconstructing fluent text from black-box embeddings (Morris et al. 2023).
- **Minimisation (privacy)** — not embedding/storing sensitive text (redact before embedding); removes the leak at the source.
- **Noise / DP on embeddings** — perturbing stored vectors to bound inference; trades recovery for retrieval utility (Pareto curve), defence-in-depth only.
- **Embeddings-are-content** — the principle that a vector store is a content store; exfiltrated embeddings ≈ exfiltrated text.

# The local security lab

Every offensive exercise in this course runs **here** — against intentionally vulnerable
applications in local Docker containers, never against a real system (`plan.md` §20, §22, §33).

## Layout

```text
lab/
├── models/          # small open-weights models (gitignored) + a deterministic local model shim
├── vulnerable-apps/ # intentionally vulnerable LLM/RAG/agent apps (targets)
├── agents/          # toy agent runtime with tools, fake creds, sandboxable
├── rag/             # ingestion → embed → vector-db → retriever → LLM pipeline
├── vector-db/       # local vector store for RAG labs
├── attack-tools/    # our minimal reimplementations + external-tool wrappers
├── defense-tools/   # filters, validators, policy engine, monitors
├── monitoring/      # logs, anomaly detection, the audit trail
├── sink/            # local egress sink — where "exfiltration" goes in labs (never the internet)
├── datasets/        # synthetic data + synthetic canary secrets
└── docker-compose.yml
```

## Safety model — read before running any lab

- **Targets are local only.** Compose binds to `127.0.0.1`. No lab reaches the public internet.
- **Secrets are synthetic.** Canaries look like `LAB-CANARY-<uuid>` and mean nothing outside the
  lab. Never put a real credential, key, or token into any lab.
- **Exfiltration goes to the local sink.** The `sink` container records what an attack *would*
  have sent, so you can measure exfiltration without any real data leaving your machine.
- **Payloads are inert.** Attack payloads demonstrate the *mechanism* with a benign success
  marker (e.g. the model emitting a canary, or a tool being invoked); they contain no working
  malware and no destructive effect.
- **Reset is one command.** Each lab ships a `reset` script (or `docker compose down -v`) that
  returns it to a clean state.

## Running

```bash
cd labs/lab-XX-slug
docker compose up          # start the target(s)
# run the attack script, observe, then apply the defense and retest
docker compose down -v     # clean up
```

Most labs also run **CPU-only** using the deterministic model shim in `lab/models`, so you can
complete the learning objective without a GPU or a model download. Labs that genuinely need a
real model or GPU say so in their own README and provide a reduced-fidelity fallback.

*Infrastructure (`docker-compose.yml`, the model shim, the sink, the first vulnerable app) lands
with the first prompt-injection lab; see `TODO_FOR_TAL.md`.*

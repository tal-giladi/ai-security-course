# Shared lab runtime

Everything in this folder is added to **every module's lab zip**. It is the same code the repo
uses at `lab/` (the `shim` model, the egress sink, the agent runtime, the defense toolkit and the
eval harness), flattened to one directory so that after you unzip a module's labs you can just run
the lab from that folder:

```bash
unzip module-16-labs.zip
cd module-16-labs
py excessive_agency.py
```

No install step and no network access are needed: the labs are pure-stdlib Python and the model
is a deterministic shim, so every run is reproducible.

| File | What it is | Used by |
|---|---|---|
| `shim.py` | Deterministic stand-in for an LLM. Same input → same output, so an ASR number means something. | modules 04-15, 32 |
| `sink.py` | Local egress sink. Lab "exfiltration" writes here instead of anywhere real. | modules 04, 05, 16, 18 |
| `agent.py` | Minimal observe → decide → act agent loop with tools, the harness for every agent lab. | modules 16-18, 28 |
| `defenses.py` | Defense pipeline: secret scrubbing, egress allowlist, authz, sandbox, rate limit, detector. | modules 23, 24 |
| `evalkit.py` | Attack success rate, precision/recall and cost measurement helpers. | modules 24, 25 |

## How a lab finds these files

Each lab puts this directory on `sys.path` before importing:

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
```

That works both in a clone of this repository and in an unzipped lab download, because
`parents[1]` is `labs/` in either layout.

## Safety

These labs only ever attack the intentionally vulnerable apps shipped alongside them, running
locally. Secrets are synthetic canaries (`LAB-CANARY-…`) and "exfiltration" goes to `sink.py` on
your own machine. See `lab/README.md` in the repository for the full safety boundary.

## Keeping this folder in sync

`lab/` is the source of truth; this folder is a copy for shipping. After changing anything under
`lab/`, run:

```bash
py scripts/sync_labs_common.py
```

which copies the five modules above and reports any drift.

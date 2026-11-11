#!/usr/bin/env bash
# Lab 34 — fetch the model weights and the benchmark datasets for the refusal-circumvention lab.
#
# Nothing downloaded here is committed to git. Everything lands in ./hf-cache, one directory per
# repo id with "/" replaced by "--", because that is exactly the layout refusal_harness.py looks
# for. Covered by the lab-local .gitignore and by the repo-wide *.safetensors / *.bin rules.
#
# Versions pinned below were checked on 2026-10-03. Re-check before trusting a run from another
# date: transformers 5.x in particular has moved the model-loading and chat-template APIs this lab
# depends on.
#
#   torch 2.14.1 (2026-09-30, BSD-3-Clause)   transformers 5.18.0 (2026-09-30, Apache-2.0)
#   datasets 5.0.1 (2026-07-28)              accelerate 1.15.0 (2026-09-09)
#   huggingface_hub 2.1.1 (2026-10-01)      safetensors 0.8.0 (2026-06-09)
#   pyarrow 22.0.0                           numpy 2.5.3 (2026-09-06)
#   pytest 9.1.1 (2026-06-19)
#
# pyarrow is pinned explicitly because refusal_harness.py imports it directly to read the
# downloaded parquet shards. `datasets` would pull it in anyway, but relying on a transitive
# dependency for a direct import is how labs break.
#
# Install the CUDA build of torch from the PyTorch index, not from PyPI:
#   https://pytorch.org/get-started/locally/   (pick your CUDA version; 12.1+ recommended)
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${LAB_DIR}/hf-cache"
mkdir -p "${CACHE_DIR}"

# ---------------------------------------------------------------------------------------------
# MODEL_ID — the model this lab measures.
#
# TIER C is the default, deliberately. It is a ~3.1 GB dense model that runs on one 24 GB card and
# teaches the same algebra as the replication target. Do not change this line casually.
# ---------------------------------------------------------------------------------------------
TIER="C"                       # C = free path (default) | A = full GLM-5.3 replication | S = skip model

case "${TIER}" in
  C)
    MODEL_ID="Qwen/Qwen2.5-1.5B-Instruct"
    # Alternatives, all ungated on the Hub:
    #   MODEL_ID="Qwen/Qwen2.5-7B-Instruct"                     # ~15 GB bf16; closer to the
    #                                                          # abliteration results in the paper
    #   MODEL_ID="HuggingFaceTB/SmolLM2-360M-Instruct"         # ~0.7 GB; what --dry-run uses
    ;;
  A)
    # TIER A — full replication of the published GLM-5.3 numbers.
    #
    # zai-org/GLM-5.3-Flash is a 320B-total / 18B-active MoE: 45 layers, 288 experts (8 routed
    # per token), hybrid attention (KDA linear attention + NoPE sparse MLA), 1,048,576-token
    # context. Budget against the 320B TOTAL, not the 18B active — every expert must be resident.
    # ~328 GB on disk at FP8; roughly double again at BF16. That is 8x80 GB or 4xH200 minimum.
    #
    # Before you provision anything, confirm these against the official model card: the Hub repo
    # id, the exact release, and the serving flags all move, and the figures above came from the
    # model card plus the zai-org/GLM-5 repository.
    #
    # Serving: Z.ai documents SGLang, vLLM, TokenSpeed and KTransformers. vLLM is the default here
    # (`--tensor-parallel-size 8`); treat the zai-org/GLM-5 cookbook as authoritative for the flag
    # set rather than guessing. The 1M context is aspirational on small hardware — start low and
    # raise it once the server actually comes up.
    #
    # There is NO `GLM-5.3-Flash` GitHub repository. The cookbooks live in zai-org/GLM-5. People
    # search for the former and waste an afternoon; that is what this line is for.
    MODEL_ID="zai-org/GLM-5.3-Flash"          # FP8, the reference release
    # MODEL_ID="zai-org/GLM-5.3-Flash-BF16"   # ~2x the disk
    echo "!! TIER A selected: ~328 GB download and a multi-GPU node. This costs real money."
    echo "!! Confirm the model id and hardware against the official model card first."
    ;;
  S)
    MODEL_ID=""
    ;;
  *)
    echo "unknown TIER '${TIER}' (expected C, A or S)" >&2
    exit 1
    ;;
esac

# ---------------------------------------------------------------------------------------------
# Datasets. Both defaults are UNGATED and load without a Hugging Face login.
#
#   longphann/harmful_harmless_instructions  harmful/harmful dialogue pairs, 512 rows
#       (published as justinphan3110/..., which now redirects here — use the canonical id)
#   tatsu-lab/alpaca                          benign instructions, 52k rows, CC-BY-NC-4.0
#
# Alternatives that need `hf auth login` first, because the Hub gates them:
#   walledai/AdvBench        (MIT, 520 harmful behaviours, column `prompt`)  <- the paper's corpus
#   allenai/wildjailbreak    (ODC-By; filter client-side on data_type, there is no `vanilla` split)
# ---------------------------------------------------------------------------------------------
HARMFUL_DATASET="longphann/harmful_harmless_instructions"
HARMLESS_DATASET="tatsu-lab/alpaca"

# ---------------------------------------------------------------------------------------------
# Python deps. Pinned; the comments say why the pin matters.
# ---------------------------------------------------------------------------------------------
echo "==> Python dependencies (pinned, checked 2026-10-03)"
# torch is intentionally NOT pinned here: the right build depends on your CUDA version, and a
# wrong pin silently installs a CPU-only wheel that makes every GPU flag a no-op. Install it first
# from https://pytorch.org/get-started/locally/ , then let the rest resolve around it.
python -m pip install \
  "transformers==5.18.0" \
  "datasets==5.0.1" \
  "accelerate==1.15.0" \
  "huggingface_hub==2.1.1" \
  "safetensors==0.8.0" \
  "pyarrow==22.0.0" \
  "numpy==2.5.3" \
  "pytest==9.1.1"

# `hf` is the CLI shipped by huggingface_hub >= 0.34 and the only one in 2.x; the old
# `huggingface-cli` name is deprecated and gone in some releases. If your install only has the
# old name, set HF_CLI=huggingface-cli before running this script.
HF_CLI="${HF_CLI:-hf}"

echo "==> Datasets -> ${CACHE_DIR}"
"${HF_CLI}" download "${HARMFUL_DATASET}" --repo-type dataset --local-dir "${CACHE_DIR}/${HARMFUL_DATASET//\//--}"
"${HF_CLI}" download "${HARMLESS_DATASET}" --repo-type dataset --local-dir "${CACHE_DIR}/${HARMLESS_DATASET//\//--}"

if [ -n "${MODEL_ID}" ]; then
  echo "==> Model ${MODEL_ID} -> ${CACHE_DIR}/${MODEL_ID//\//--}"
  echo "    (hundreds of MB for tier C; ~328 GB for tier A — the download is not the expensive part)"
  "${HF_CLI}" download "${MODEL_ID}" --local-dir "${CACHE_DIR}/${MODEL_ID//\//--}"
else
  echo "==> TIER S: skipping the model download."
fi

# Report the footprint rather than just "done". Disk is the constraint that actually bites: tier C
# is ~3 GB, tier B is ~90 GB, tier A is ~328 GB and you find out about it here rather than after
# the download. Assert the ignore rules while we are looking at the directories, instead of
# trusting that nobody ever ran `git add -A` in this folder.
echo "==> Downloaded into ${CACHE_DIR} (git-ignored):"
du -sh "${CACHE_DIR}" 2>/dev/null || echo "   (could not measure)"
if git -C "${LAB_DIR}/../.." rev-parse --git-dir >/dev/null 2>&1; then
  if git -C "${LAB_DIR}/../.." check-ignore -q "${CACHE_DIR}"; then
    echo "    git correctly ignores this directory."
  else
    echo "    WARNING: git is NOT ignoring ${CACHE_DIR}. Do not commit it."
  fi
fi

cat <<'EOF'

Done. Next:

  # free path: the full harness on one 24 GB GPU
  python labs/module-34/refusal_harness.py --model Qwen/Qwen2.5-1.5B-Instruct --limit 40

  # no GPU at all: the ablation code path on a tiny model
  python labs/module-34/ablate.py --dry-run --iterations 2

  # the acceptance tests need none of the above
  python -m pytest labs/module-34 -q

Reminder: the downloaded corpora contain harmful text. Do not commit them, do not paste them into
a chat window, and do not print them from a notebook. The lab never prints dataset text — only
counts and rates.
EOF
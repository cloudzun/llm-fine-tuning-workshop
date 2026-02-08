#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/chengzh/training-projects/llm-training-course"
cd "$ROOT/code_samples/quickstart"

if [ ! -d "$ROOT/.venv" ]; then
  echo "Please run: bash $ROOT/resources/configs/env_setup.sh"
  exit 1
fi

source "$ROOT/.venv/bin/activate"

python train.py

# Simulated quantize step (user must set MODEL_PATH)
# bash run_quantize.sh

echo "Quickstart complete. Review lora_out/ for adapter files."
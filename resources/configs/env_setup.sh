#!/usr/bin/env bash
set -euo pipefail

# Minimal environment setup for llm-training-course quickstart
# - Creates Python venv
# - Installs pip deps
# - Checks for Docker

VENV_DIR=".venv"
PYTHON=python3

if ! command -v $PYTHON >/dev/null 2>&1; then
  echo "Error: $PYTHON not found. Install Python 3.10+ and retry."
  exit 1
fi

$PYTHON -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r /home/chengzh/training-projects/llm-training-course/code_samples/quickstart/requirements.txt

if command -v docker >/dev/null 2>&1; then
  echo "Docker found"
else
  echo "Docker not found — install Docker if you plan to use containers for Ollama/One-API"
fi

echo "Environment setup complete. Activate with: source $VENV_DIR/bin/activate" }
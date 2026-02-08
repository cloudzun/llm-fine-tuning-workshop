Quickstart — Minimal demo to run a LoRA micro-fine-tune → quantize → local test

This quickstart provides a minimal, reproducible path to demonstrate the core flow used in the course:
- Prepare environment
- Run a tiny LoRA fine-tune on a few examples
- Convert / quantize the resulting model (example commands)
- Load into Ollama (Modelfile example) and test locally

Prerequisites
- Linux or macOS with Python 3.10+ and Git
- Docker (optional for One-API or Ollama if using containers)
- (Optional) GPU with CUDA if you want faster fine-tuning

Quick steps
1. Setup environment (recommended to use a venv):

   bash resources/configs/env_setup.sh

2. Run the quickstart micro-train (very small dataset):

   cd code_samples/quickstart
   bash run_quickstart.sh

What the script does
- Installs Python dependencies into the virtualenv
- Runs a tiny LoRA fine-tune (train.py) on sample_data.jsonl
- Runs a sample quantize command (run_quantize.sh) to demonstrate how to convert to GGUF-ish formats
- Writes an example Modelfile (resources/configs/Modelfile.example) you can adapt for Ollama

Notes
- This quickstart is intentionally tiny (dozens of examples) to be runnable on a developer laptop. It is NOT production training.
- Adjust model names and paths in code_samples/quickstart/train.py before running for larger experiments.

Further reading
- See docs/modules/01_Module1_LECTURE.md for environment and AutoDL notes
- See docs/modules/02_Module2_CONFIGS.md for fine-tuning config templates

#!/usr/bin/env bash
set -euo pipefail

# Simple throughput test for Ollama/OpenAI-compatible endpoint
URL=${1:-"http://localhost:11434/v1/completions"}
MODEL=${2:-"qwen2.5-7b-instruct-lora"}

for i in {1..10}; do
  start=$(date +%s%3N)
  curl -s -X POST "$URL" -H "Content-Type: application/json" -d '{"model":"'"$MODEL"'","messages":[{"role":"user","content":"Hello"}],"max_tokens":64}' >/dev/null
  end=$(date +%s%3N)
  echo "request $i: $((end-start)) ms"
done

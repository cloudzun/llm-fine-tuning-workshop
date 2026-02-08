#!/usr/bin/env bash
# labs/04_quantize_example.sh — 演示用的量化流程（伪命令，需根据具体工具调整）
set -e
if ! command -v ./llama.cpp/main >/dev/null 2>&1; then
  echo "llama.cpp binary not found; please build llama.cpp first or provide path"
  exit 2
fi

# 假设有 convert_to_gptq.py 脚本或工具
# python convert_to_gptq.py --model model.bin --out model.q4
# ./llama.cpp/main --model model.q4 --prompt "测试"

echo "QUANTIZE_SIM_DONE"

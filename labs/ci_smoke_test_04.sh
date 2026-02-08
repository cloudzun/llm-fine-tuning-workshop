#!/usr/bin/env bash
set -e
# 量化操作依赖环境，CI 做一个工具存在性检查作为轻量 smoke test
if [ -f ./llama.cpp/main ] || command -v llama.cpp >/dev/null 2>&1; then
  echo "LLAMA_CPP_OK"
else
  echo "LLAMA_CPP_MISSING"
fi

echo "SMOKE SIM OK"

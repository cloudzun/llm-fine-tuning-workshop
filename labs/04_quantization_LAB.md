---
title: "Chapter 4 Lab — 量化实操：使用 GPTQ / llama.cpp 导出 GGUF 模型"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","量化","实操","llama.cpp"]
categories: ["LLM","工程实践"]
---

# 第4章实验 — 量化实操：使用 GPTQ / llama.cpp 导出 GGUF 模型

## 实验目标
- 学会使用 GPTQ 或现有工具对小模型进行训练后量化；
- 将量化后的模型转换为 GGUF 或适合 llama.cpp 的格式并进行本地推理测试；
- 记录量化前后的性能差异（latency、memory、perplexity）。

## 预估时间
- 环境准备：30–60 分钟（含编译 llama.cpp）
- 运行量化（小模型）：10–30 分钟
- 评估与对比：20–40 分钟

## 快速安装（示例，参考具体工具链）
```bash
# 安装依赖（示例）
sudo apt install build-essential cmake
# clone llama.cpp 并编译
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
```

## 示例流程（high-level）
1. 下载小模型（或使用已有本地模型）
2. 使用 GPTQ 工具对模型执行量化（示例命令见工具文档）
3. 将量化模型转换为 GGUF 格式
4. 用 llama.cpp 的示例命令做推理测试并记录 tokens/s 与 latency

## CI Smoke test（说明）
- 由于量化与编译依赖较多，CI 可以只做“工具存在性检查”或使用模拟脚本断言 llama.cpp 可执行。

## 提交要求
- 量化流程脚本（quantize.sh / python）
- 测试脚本与结果对比记录（results.md）
- README.md（含依赖与编译步骤）

## 教学提示
- 课堂上可提前把编译好的二进制放到课堂镜像中以节省时间；
- 强调量化可能影响模型质量，展示如何选择校准数据。

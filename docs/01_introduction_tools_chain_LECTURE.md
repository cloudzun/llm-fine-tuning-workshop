---
title: "Chapter 1 — 导论与工具链"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","导论","工具链"]
categories: ["LLM","工程实践"]
---

# 第1章 — 导论与工具链

## 1. 学习目标（Learning Objectives）
- 理解课程定位、学习路线与交付物要求。
- 熟悉本课程使用的主要工具链（Python、Git、Docker、PyTorch/Transformers、量化/推理工具）。
- 能搭建并运行一个最小可复现的本地推理示例（CPU 可运行的微型 LLM 演示）。
- 掌握课程中“可复现性”“验证步骤”“Smoke test”概念与标准流程。

## 2. 背景与为什么要学这章
- LLM 工程不只是模型训练：工程化、部署、可复现与监控是实际交付的关键。
- 本章目标：让学员具备开始动手的最小开发环境，并理解后续模块为何按那样设计（微调→量化→部署→评估）。

## 3. 关键概念速览（必要原理，简短）
- Tokenization：子词（BPE/WordPiece/Unigram）概念与对模型输入长度的影响。
- 模型权重 vs 运行时引擎：PyTorch/TF 权重、ONNX/ORT、ggml/quantized runtime 的角色区分。
- 推理流水线：tokenize → model.forward → decode。理解推理延迟的主要来源（模型大小、硬件、attention 计算、I/O）。
- 可复现性要点：固定随机种子、记录依赖版本、提供小数据样例与验证指令。

## 4. 工具链概览（短清单 + 说明）
- Python 3.9/3.10、venv/conda
- Git、GitHub/GitLab（分支/PR 流程）
- Docker（可选，但推荐用于 CI/环境隔离）
- PyTorch（或 CPU-only fallback）、transformers (Hugging Face)
- Tokenizers、sentencepiece（按需）
- ONNX & onnxruntime、量化 工具（GPTQ、bitsandbytes）——后续模块详细
- 简易性能基准工具：time、python 脚本 + psutil/benchmarks

## 5. 本章演示说明（high-level）
- 我们先完成“最小可复现演示”：在虚拟环境中安装依赖，运行一个使用 distilgpt2（或指定小模型）的文本生成 demo，验证输出并记录版本信息。
- 该演示作为课程的 smoke test：所有后续模块的 CI 都应先能通过该 smoke test。

## 6. 参考与拓展阅读
- Hugging Face Transformers 文档（tokenizers、pipeline）
- PyTorch 快速入门
- 课程后续模块计划（简短列点，参见目录）

---

结束语：本章是全课程的工程起点，务必保证每位学员能顺利完成 Lab 的 smoke test —— 这是后续实验能否顺利开展的前提。

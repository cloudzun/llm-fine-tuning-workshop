---
title: "第1章 — 导论与工具链（教科书式重写）"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","导论","工具链","教科书"]
categories: ["LLM","工程实践"]
---

# 第1章 导论与工具链（教科书式）

## 学习目标
完成本章后，你应能：
1. 用连贯的认知框架解释大型语言模型（LLM）的输入—模型—输出流程；
2. 理解 tokenization、embedding、self-attention 与解码的基本直观机制；
3. 搭建最小可复现的实验环境并运行 smoke test；
4. 在小的 toy 示例上手算一层 attention 的输出并解释其含义；
5. 记录并报告环境信息以保证可复现性。

---

## 引言
在工程化场景下，LLM 不再是学术论文中的模型秀——它是需要被打包、部署和运营的工程组件。工程师要在模型能力、成本与风险之间权衡。为此，本章以工程实践优先的视角，把最必要的原理与可操作步骤结合起来：你既要知道内部机制“为什么”，也要知道如何把模型跑起来“怎么做”。

---

## 从字符串到生成：系统流程
典型推理流水线包含：分词 (tokenization) → embedding → Transformer 编码（自注意力 + 前馈）→ 解码（logits → softmax → 采样）。每个环节都会影响性能和输出质量：分词决定序列长度，embedding 决定维度，Transformer 决定计算密度，解码影响输出多样性。

---

## 关键概念精要
- Tokenization：选择 BPE/Unigram 等会影响子词切分与序列长度。中文多用 SentencePiece/Unigram；英文常用 BPE/WordPiece。  
- Self-Attention：查询-键-值机制决定上下文信息如何聚合。  
- 解码控制：temperature、top-k/top-p、beam 等控制生成质量与多样性。  
- 可复现性：固定随机种子、记录依赖版本、提供小样本与 smoke test。

---

## 手工 Worked Example（attention 手算，回顾）
（本例为简化说明，见 lab 的可运行 demo）
见章节手算示例：给定 X、Q=K=V=X，计算 S=QK^T，缩放、softmax 得到 A，最后 Y=AV，观察每个 token 表示如何混合上下文向量。

---

## 工程要点（环境与 smoke test）
- 环境：推荐 Python 3.10、venv、固定依赖（requirements.txt）或 Docker 镜像。  
- Smoke test：提供一个能在 CPU 上运行的小模型 demo（例如 distilgpt2），脚本需输出环境版本信息与生成文本，CI 根据输出断言通过。  
- 缓存与离线方案：课堂应准备模型缓存或离线包以避免网络问题。

---

## 练习（Exercises）
1. 手算 attention：按本章 worked example 手工计算一行 softmax 的近似概率并解释。  
2. 在本地运行 labs/01 的 demo.py，记录 transformers 与 torch 版本与生成文本。  
3. 修改 demo 中的 temperature 与 top_k，分别运行并记录生成差异（简短对比说明）。  
4. 编写一个小脚本记录当前虚拟环境中所有依赖的版本并输出为 json（README 中需说明如何运行）。

---

## 练习参考提示（简短答案提示）
1. softmax 会把映射变为概率分布，缩放因子 sqrt(d_k) 用于稳定数值范围，避免 softmax 进入极端。  
2. demo.py 输出中包含 transformers 和 torch 的版本字段，将其粘贴到报告中。  
3. 降低 temperature 值会使输出更保守，减少多样性；较高 temperature 增加随机性。top_k 限制候选集会提高生成稳定性但可能降低多样性。  
4. 可以用 pkg_resources 或 pip list --format=json 获取依赖并写入文件。

---

## 参考与延伸
- Vaswani et al., "Attention is All You Need"  
- Hugging Face Transformers 文档  
- labs/01_introduction_tools_chain_LAB.md（环境搭建与 smoke test）

结束语：本章为后续微调、量化与部署打基础，请务必完成 lab 的 smoke test 并在作业中提交环境信息与生成示例。

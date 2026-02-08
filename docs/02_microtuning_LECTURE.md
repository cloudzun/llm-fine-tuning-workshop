---
title: "第2章 — 微调与高效微调方法（LoRA / QLoRA）"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","微调","LoRA","QLoRA"]
categories: ["LLM","工程实践"]
---

# 第2章 微调与高效微调方法（LoRA / QLoRA）

## 学习目标
1. 理解微调的目的、适用情景与成本—效益权衡；
2. 掌握 Full fine-tuning、LoRA、QLoRA 的原理差异与实现要点；
3. 能根据显存与数据规模选择合适的微调方案并设计训练流程；
4. 通过一个简化数学示例理解 LoRA 的低秩近似思想。

---

## 1. 引言
微调（fine-tuning）是把通用预训练模型适配到特定任务或风格的关键手段。但在实际工程中，直接对全部参数微调常常受限于显存、时间与成本。于是出现了多种“参数高效”微调方法，如 LoRA（低秩适配）与 QLoRA（量化 + LoRA）。本章既讲清楚这些方法背后的直观与数学理由，也给出工程实践中的选型与实施建议。

---

## 2. 微调的类型与工程考量
- Full fine-tuning：更新模型所有参数；效果上限高，但显存与存储成本大，适合有大规模资源或需要深度适配的场景。
- Adapter / Prompt-tuning：插入小模块或只训练 prompt，参数少、轻量，但对复杂任务的适配能力有限。
- LoRA（Low-Rank Adaptation）：在权重更新上只训练低秩补丁矩阵 A,B，原模型权重冻结，训练参数显著减少。
- QLoRA：在量化后的基础模型上训练 LoRA，大幅降低显存需求，适合中小显存 GPU。

工程选型要点：
- 目标性能 vs 成本：是否必须达到最优效果？是否受显存限制？
- 数据量与多样性：数据少建议 LoRA/Adapter；数据多且任务复杂可考虑 Full FT。 
- 部署与维护：LoRA 权重小，便于版本管理和快速回滚。

---

## 3. LoRA 的数学直观与 worked example（简化）
核心思想：对某个线性层的权重矩阵 W ∈ R^{d×d}，不直接更新 W，而引入低秩补丁 ΔW = A B，其中 A ∈ R^{d×r}, B ∈ R^{r×d}，r ≪ d。

直观：A B 的参数量仅为 2dr，比原始 d^2 小得多，训练时只更新 A 和 B，推理时可按需合并成 W' = W + α A B。

Worked example（简化）：
设 d=4，r=1，原始权重 W 为常数矩阵（示意），A、B 为训练参数。相比更新 16 个参数，LoRA 只需更新 8 个（2×4），对资源消耗大减。

带入训练：forward 时计算 (W + A B) x = W x + A (B x)，训练只计算并反向传播到 A、B，显存与算力节约明显。

---

## 4. QLoRA 概述
QLoRA 把模型先量化（例如 4-bit），在量化后的权重上训练 LoRA。量化降低了模型基础内存占用，LoRA 保持训练参数在浮点数格式（FP16/FP32），二者结合能在单卡或小显存环境中实现可行的微调流程。

工程要点与风险：
- 量化可能引入精度损失，需评估量化策略与后处理（量化感知训练 vs 训练后量化）。
- QLoRA 常用工具链（比如 bitsandbytes、transformers 的量化支持、gptq 工具）需版本匹配。

---

## 5. 工程实践要点（Checklist）
- 选取 target_modules（例如 attention 的 q_proj、v_proj）以控制改动范围；
- 固定随机种子并记录训练超参（lr、batch、r、alpha、dropout）；
- 在小样例上先做快速验证（1 epoch）再全量训练；
- 训练输出应包含验证对比（原模型 vs LoRA），并保存可加载的 LoRA 权重文件。

---

## 6. 练习（Exercises）
1. （理解）说明 LoRA 为什么能在不更新 W 的前提下改变模型行为？提示：考虑 A B 对 Wx 的影响。
2. （实践）用 Hugging Face 的 peft/peft-trainer 在一个小数据集上训练一个 LoRA，并记录训练日志与显存占用（提交截图）。
3. （分析）给出 QLoRA 对比 LoRA 在显存、训练时间与可能精度损失上的三点优劣比较。
4. （设计）你有一张 16GB GPU，如何设计一个微调方案使得效果和成本之间达到平衡？写出关键超参与理由。

---

## 7. 参考资料
- Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models" 
- QLoRA 社区教程与 bitsandbytes 文档

---

链接到实操：请参阅 labs/02_llama_factory_lab.md（LLaMA Factory 微调实战）。

---
title: "第2章 — 微调与高效微调方法（LoRA / QLoRA）"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","微调","LoRA","QLoRA","教科书"]
categories: ["LLM","工程实践"]
---

# 第2章 微调与高效微调方法（LoRA / QLoRA）

## 学习目标
完成本章后，你应该：
1. 能解释为什么要微调以及不同微调方案的适用场景；
2. 理解 LoRA 的低秩近似原理和在训练/推理中的工程收益；
3. 理解 QLoRA（量化 + LoRA）的思路及其权衡；
4. 能根据硬件与数据条件设计一个可行的微调方案并做基本验证。

---

## 1. 引言与动机（工程视角）
微调的目标是把通用预训练模型适配到特定任务或风格。在工程环境下，微调常常受到显存、时间与维护成本的限制。传统的 Full fine-tuning 虽然直接、效果好，但对资源要求高；参数高效微调（PEFT）方法如 LoRA 则把成本大幅降低，使得团队在常见的单卡/小集群上也能完成任务适配。本章从原理出发，结合工程选型与实践建议，帮助你在不同场景下做出平衡决策。

---

## 2. 微调方法概览与工程决策树
常见方法：
- Full fine-tuning：更新全部参数；优点是灵活、效果上限高；缺点是显存和存储成本大、部署复杂。
- Adapter / Prompt-tuning：插入小模块或只训练 prompt；轻量但适用性有限。
- LoRA（Low-Rank Adaptation）：仅训练低秩补丁矩阵，参数极少，便于版本管理。
- QLoRA：先量化基础模型再训练 LoRA，在低显存上可行。

工程决策要点：
1. 显存可用？>32GB 考虑 Full FT；12–24GB 优先 LoRA/QLoRA；<12GB 用更小模型或云资源。 
2. 数据量：<10k 样本优先 LoRA；>100k 可考虑 Full FT（若资源允许）。
3. 部署频率：若频繁迭代或多任务，LoRA 权重小便于管理。

---

## 3. LoRA 的数学直观与工程实现
核心想法是用低秩矩阵近似权重更新：

设某线性层权重为 W ∈ R^{d×d}，LoRA 不直接更新 W，而是引入 ΔW = A B，A ∈ R^{d×r}, B ∈ R^{r×d}（r ≪ d）。训练时冻结 W，只更新 A 和 B；推理时可按需合并 W' = W + α A B。

参数量比较（示例）：d=4096，则 W 参数约 16M，而 r=8 时 A、B 参数总计约 65K，节省数百倍。

工程实现要点：
- 选择 target_modules（通常为 attention 的 q_proj/v_proj 或 MLP 层），控制改动范围；
- r 的选取根据任务复杂度与显存调整（常用 4/8/16）；
- lora_alpha、dropout 用于稳定训练；
- 保存与加载：只保存 LoRA 权重文件，保留原始模型不变，便于回滚与对比。

---

## 4. Worked Example 1：LoRA 对线性层的影响（手算示例）
假设 d=4, r=1，
W 为 4×4 矩阵，x 为输入向量。设 A 为列向量 a，B 为行向量 b^T，则 ΔW x = a (b^T x) = (b^T x) * a，即对 x 的响应被缩放到向量 a 的方向。若训练学会把 b 对特定语义模式响应较大，则该模式在输出表示中被“放大”。

步骤：
1. 给定 x, 计算 b^T x → 标量 s。
2. 输出增量为 s * a，加到 W x 上。

该示例直观展示 LoRA 如何通过少量参数改变权重输出的方向与幅度。

---

## 5. Worked Example 2：LoRA 在训练流程中的工程性（伪代码）
伪代码展示训练时只更新 A,B：
```
model = load_pretrained()
frozen(model)
attach_lora(model, r=8)
for batch in data:
  logits = model(batch)
  loss = loss_fn(logits, labels)
  loss.backward()
  optimizer.step()  # only updates A,B parameters
```
该流程说明显存占用比 Full FT 小，且 checkpoint 体积小。

---

## 6. QLoRA：量化 + LoRA（原理与权衡）
QLoRA 先将基础模型量化（常见为 4-bit），在量化后的模型上训练 LoRA 补丁。量化显著降低模型的内存占用，LoRA 保留浮点补丁以保证可训练性。权衡：量化可能带来微小精度下降，需要实验验证；工具链（bitsandbytes、GPTQ、transformers 的兼容性）需严格把控版本。

工程建议：
- 先在小样本上做 QLoRA 快速验证；
- 使用校准数据评估量化误差；
- 在可用的情况下对比 LoRA 与 QLoRA 的验证集表现与延迟/显存指标。

---

## 7. 练习（Exercises）
1. （理解）说明 LoRA 的 ΔW = A B 在改变层输出时如何与 W x 叠加，写出数学表达并解释。  
   提示：先写出 W x + A (B x)。
2. （实践）在 distilgpt2 上用 peft 框架做一次 r=8 的 LoRA 微调（小样本），记录训练日志与模型大小变化。  
   提示：只跑 1 个 epoch 或使用少量样本以节省时间。
3. （比较）设计一个小实验比较 LoRA(r=8) 与 Full FT 在同一小样本上的验证损失与显存峰值，报告结果并分析。  
   提示：可用 torch.cuda.max_memory_allocated() 监控显存。
4. （工程）你有一张 16GB GPU 和 5k 条数据，写出你的微调计划（选择方法、超参建议、验证策略）。  
   提示：考虑 batch size、accumulate steps、lr 与早停。

---

## 8. 参考与延伸阅读
- Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models"（论文）
- bitsandbytes、GPTQ、Hugging Face PEFT 教程

---

（本章同时指向 labs/02_microtuning_LAB.md 以获取可运行的 LoRA demo 与快速验证脚本。）

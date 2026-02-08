---
title: "Chapter 2 Lab — 微调与高效微调实操（LoRA 快速上手）"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","微调","LoRA","实操"]
categories: ["LLM","工程实践"]
---

# 第2章实验 — 微调与高效微调实操（LoRA 快速上手）

## 实验目标
- 了解 LoRA 微调流程与关键配置项（r、alpha、target_modules）。
- 在受控小数据集 / 小模型上完成一次参数高效微调的“可复现性验证”流程（以 demo 形式）。
- 产出可加载的 LoRA 权重文件与一份训练日志。

## 预估时间
- 准备环境：15–30 分钟
- 运行示例训练（小样本、快速验证）：10–30 分钟（取决于硬件）
- 结果验证与提交：10–20 分钟

## 所需环境
- Python 3.9/3.10
- Git
- 建议：一张有 12GB+ 显存的 GPU；若无 GPU，说明如何用 CPU 快速做验证（但训练时间会长）

## 快速安装（可复制命令）
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install torch transformers accelerate peft datasets
```
（注：在无 GPU 环境建议安装 CPU-only torch wheel）

## 示例脚本（train_lora.py）
将下面脚本保存为 labs/02_train_lora.py（简化版，仅作为教学 demo）

```python
# labs/02_train_lora.py — 最小 LoRA 训练示例（使用 Hugging Face + peft）
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset

MODEL = os.environ.get('MODEL','distilgpt2')
DATASET = os.environ.get('DATASET','wikitext')

def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL)

    # Demo: very small data sample
    ds = load_dataset('wikitext', 'wikitext-2-raw-v1', split='train[:0.01%]')

    # LoRA config (示例)
    lora_config = LoraConfig(r=8, lora_alpha=16, target_modules=['q_proj','v_proj'], lora_dropout=0.05)
    peft_model = get_peft_model(model, lora_config)

    # 这里省略完整训练 loop，以便课堂演示：
    print('MODEL:', MODEL)
    print('SAMPLE SIZE:', len(ds))
    print('PEFT MODEL READY')

if __name__ == '__main__':
    main()
```

## 运行与验证（Smoke test）
- 运行：
  ```bash
  source .venv/bin/activate
  python labs/02_train_lora.py
  ```
- 预期：脚本能完成模型与 tokenizer 加载并打印 PEFT MODEL READY（不必进行完整训练以节约课堂时间）。

## CI Smoke test（ci_smoke_test_02.sh）
保存为 labs/ci_smoke_test_02.sh：
```bash
#!/usr/bin/env bash
set -e
python - <<'PY'
try:
    import transformers, peft, datasets
    print('IMPORTS_OK')
except Exception as e:
    print('IMPORT_FAIL', e)
    raise
print('SMOKE TEST PASSED')
PY
```

## 提交要求
- labs/02_train_lora.py（脚本）
- labs/ci_smoke_test_02.sh（smoke test）
- README.md（运行说明，包含 MODEL/DATASET 环境变量说明）

## 教学提示
- 课堂演示时优先展示模型加载与 LoRA 模型结构，再展示如何在小样本上验证参数更新是否生效（Loss 曲线或打印梯度信息）。
- 如果课堂网络受限，提前缓存模型或使用 distilgpt2 的本地包。

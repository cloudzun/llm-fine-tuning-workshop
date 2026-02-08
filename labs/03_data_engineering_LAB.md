---
title: "Chapter 3 Lab — 数据工程实操：清洗、去重与质量检测"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","数据工程","实操"]
categories: ["LLM","工程实践"]
---

# 第3章实验 — 数据工程实操：清洗、去重与质量检测

## 实验目标
- 实现基本的数据清洗流水线（编码、去重、噪声过滤）。
- 使用脚本统计数据质量指标（重复率、长度分布、常见词频）。
- 能用 embedding-based 方法做简单的多样性抽样（可选）。

## 预估时间
- 环境准备与数据准备：15–30 分钟
- 运行清洗脚本与质量检测：20–40 分钟
- 多样性抽样（可选）：20–60 分钟

## 快速安装
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install datasets sentencepiece scikit-learn faiss-cpu numpy
```

## 示例脚本（clean_and_stats.py）
保存为 labs/03_clean_and_stats.py：
```python
# labs/03_clean_and_stats.py — 简单清洗与质量检测脚本
import sys, json
from collections import Counter

def load_sample(path):
    with open(path,'r',encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
    return lines

if __name__=='__main__':
    path = sys.argv[1]
    lines = load_sample(path)
    print('TOTAL', len(lines))
    # 简单去重
    uniq = list(dict.fromkeys(lines))
    print('UNIQ', len(uniq))
    lens = [len(l.split()) for l in uniq]
    print('AVG_LEN', sum(lens)/len(lens))
    # top tokens
    tokens = Counter()
    for l in uniq:
        tokens.update(l.split())
    print('TOP_20', tokens.most_common(20))
```

## 运行与验证
```bash
python labs/03_clean_and_stats.py data/sample.txt
```
预期输出包含 TOTAL、UNIQ、AVG_LEN 与 TOP_20。

## CI Smoke test（ci_smoke_test_03.sh）
```bash
#!/usr/bin/env bash
set -e
python - <<'PY'
from labs._ import __name__
print('SMOKE OK')
PY
```
（注：CI 脚本模板，请根据实际路径调整）

## 提交要求
- labs/03_clean_and_stats.py
- labs/sample.txt（小样本用于 CI）
- README.md（运行说明）

## 教学提示
- 演示时强调去重与采样对最终微调效果的影响；
- 用简单的可视化（length histogram）说明数据分布。

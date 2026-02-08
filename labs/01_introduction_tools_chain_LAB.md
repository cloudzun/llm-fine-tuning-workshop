---
title: "Chapter 1 Lab — 环境搭建与最小推理演示"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","实验","环境搭建"]
categories: ["LLM","工程实践"]
---

# 第1章实验 — 环境搭建与最小推理演示

## 1. 实验目标
- 在本地创建可复现的 Python 环境并运行一个最小 LLM 推理 demo（文本生成）。
- 提供 smoke test 脚本以便 CI 能快速验证环境与依赖是否正确。
- 学会记录环境信息（python 版本、依赖版本、模型名称、随机种子）。

## 2. 预估时间
- 准备（创建虚拟环境 + 安装依赖）：15–30 分钟（受网速影响）
- 运行 demo 与验证：10–20 分钟
- 故障排查：15–30 分钟（若遇问题）

总时长建议：45–90 分钟

## 3. 所需环境
- 操作系统：Linux / macOS / Windows Subsystem for Linux 推荐
- Python 3.9 或 3.10
- Git
- 若可用：一个带 CUDA 的 GPU（可选；本 lab 可在 CPU 上运行小模型）

## 4. 快速安装（步骤，可复制命令）
- 在课程代码根目录下创建实验目录（示例）
  mkdir -p llm_course/labs/chapter01 && cd llm_course/labs/chapter01
- 创建并激活虚拟环境（venv 示例）
  python3 -m venv .venv
  source .venv/bin/activate
- 更新 pip 并安装最小依赖
  pip install --upgrade pip
  pip install torch --index-url https://download.pytorch.org/whl/cpu  # CPU-only 示例（如有GPU改用官方CUDA wheel）
  pip install transformers==4.40.0 sentencepiece  # 固定版本以保证可复现
  pip install psutil requests

（备注：如果你用 conda 或 prefer GPU，请用对应安装命令。CI 可使用 CPU 版本以避免 GPU 依赖）

## 5. 示例代码（demo.py）
保存为 demo.py：
```
# demo.py — 最小文本生成 demo（distilgpt2）
import sys, json, random, platform
from transformers import pipeline, set_seed


def env_info():
    import pkg_resources
    reqs = ["torch","transformers"]
    versions = {p: pkg_resources.get_distribution(p).version for p in reqs}
    info = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "versions": versions
    }
    print(json.dumps(info, indent=2))


def main():
    set_seed(42)
    generator = pipeline("text-generation", model="distilgpt2", device=-1)  # device=-1 表示 CPU
    prompt = "在未来的人工智能实践中，工程师应优先考虑"
    res = generator(prompt, max_length=60, num_return_sequences=1)
    print("=== GENERATED ===")
    print(res[0]["generated_text"])


if __name__ == "__main__":
    env_info()
    main()
```

## 6. 运行与验证
- 运行：
  python demo.py
- 预期行为：
  - 终端先打印 JSON 格式的环境信息（包括 torch 与 transformers 版本）。
  - 随后打印 “=== GENERATED ===” 与一段生成文本（基于 distilgpt2 的短文本续写）。
- 验证要点（Smoke test）：
  - 脚本能运行完成（非异常退出）
  - 环境信息包含 torch 与 transformers 的版本
  - 生成文本非空且含 prompt 续写

## 7. Smoke test 自动化脚本（ci_smoke_test.sh）
保存为 ci_smoke_test.sh，可供 CI 使用（退出码表示结果）：
```
#!/usr/bin/env bash
set -e
python demo.py > demo_out.txt
grep -q "=== GENERATED ===" demo_out.txt
# 检查是否打印了 versions
grep -q "\"transformers\"" demo_out.txt
echo "SMOKE TEST PASSED"
```
- 在 CI 中运行：bash ci_smoke_test.sh
- 若某步失败，CI 返回非零退出码以阻止合并。

## 8. 常见失败与排查（FAQ）
- 问：pip 安装 torch 非常慢或失败
  - 答：在中国大陆可使用国内镜像或指定 CPU wheel；或使用 conda 的 prebuilt 包。
- 问：模型下载失败（网络/防火墙）
  - 答：提前在有网络的机器上用 transformers 下载并缓存模型（HF_HOME），或在课堂前准备离线模型包并提供链接。
- 问：生成报错 "no module named transformers"
  - 答：确认虚拟环境已激活，pip 安装成功，且 python 使用的是同一环境。
- 问：输出为空或模型行为异常
  - 答：检查是否使用了正确的 model 名称（distilgpt2），检查 transformers 版本兼容性，重试 set_seed 或降低 max_length。

## 9. 扩展任务（可选）
- 切换到小型 encoder-decoder 模型（如 t5-small），尝试做一个简单的摘要任务。
- 将示例改写成 Dockerfile，构建并运行容器化版本以体验容器化部署流程。
- 用 onnxruntime 导出并加载 ONNX 模型（简要流程留待后续模块）。

## 10. 记录与交付（提交要求）
- 学员提交内容：
  - llm_course/labs/chapter01/demo.py
  - llm_course/labs/chapter01/ci_smoke_test.sh
  - README.md：一句话说明如何运行（含 Python 版本与依赖）
- 教师/助教验收：
  - 在 Instructor CI（或本地）运行 ci_smoke_test.sh，确保通过
  - 验证 README 描述与 demo.py 一致

## 11. 教学提示（给助教的建议）
- 课堂演示时建议先在 projector 上运行 demo.py，让学员观察模型加载与生成耗时（便于讲解 I/O 与模型加载开销）。
- 若学员网络受限，预先准备好模型缓存或使用课堂内网镜像。
- 强调“记录版本”的重要性：让学员把 demo 输出的版本信息粘到作业提交中。

## 12. 参考资料与链接
- Hugging Face transformers — 文档与 pipeline 教程
- PyTorch 官方安装指南
- 课程规范（Course Development Specifications）链接

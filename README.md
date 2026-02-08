# LLM全流程实战培训课程

这是一个关于大型语言模型（LLM）从微调到部署的完整实战课程项目。

## 课程简介

**课程名称**: LLM 工程实践与必要原理  
**课程时长**: 2天（每天6小时，可扩展为多周课程以用于深度教学）  
**目标受众**: 有编程与工程背景（熟悉 Python、Git），对 LLM 只有基础概念的学习者  
**课程目标**: 学员将掌握从微调、量化到部署的工程化流程，并理解必要的支撑原理（tokenization、attention、量化策略、治理）。

### 技术栈
- **微调**: LLaMA Factory / Hugging Face + PEFT（LoRA）  
- **量化**: llama.cpp、GPTQ、bitsandbytes、GGUF  
- **部署**: Ollama / Docker + Flask（教学替代）  
- **API管理**: One-API（概念讲解）


## 项目结构（说明）
```
llm-training-course/
├── COURSE_OVERVIEW.md          # 课程大纲（已更新为课程指导规范）
├── README.md                   # 项目说明（本文件）
├── docs/                       # 教科书式讲义（第1–6章已完成草稿）
│   ├── 01_introduction_tools_chain_LECTURE.md
│   ├── 02_microtuning_LECTURE.md
│   ├── 03_data_engineering_LECTURE.md
│   ├── 04_quantization_LECTURE.md
│   ├── 05_deployment_LECTURE.md
│   └── 06_governance_LECTURE.md
├── labs/                       # 实验手册与示例脚本（第1–6章）
│   ├── 01_introduction_tools_chain_LAB.md
│   ├── 02_microtuning_LAB.md
│   ├── 03_data_engineering_LAB.md
│   ├── 04_quantization_LAB.md
│   ├── 05_deployment_LAB.md
│   ├── 06_governance_LAB.md
│   ├── 02_train_lora.py
│   ├── 03_clean_and_stats.py
│   ├── 04_quantize_example.sh
│   ├── 05_serve.py
│   └── 06_bias_check.py
├── .github/                    # CI 工作流（smoke-tests）
│   └── workflows/smoke-tests.yml
├── code_samples/               # 课堂代码示例
├── slides/                     # 幻灯片（占位）
└── resources/                  # 数据样例与脚本
```

## 当前状态（开发进度）
- 教科书式讲义：第1–第6章已完成草稿并按统一风格（每章 800–1,200 字，含 1–2 个 worked example 与练习题）。
- 实验手册（labs）：第1–第6章的 Lab 指南已编写，示例脚本与轻量 CI smoke tests 已加入仓库。
- CI：添加了 .github/workflows/smoke-tests.yml，用于运行轻量级 smoke tests 并上传日志。

## 如何在本地运行 smoke tests
1. 克隆仓库并进入目录：
   ```bash
   git clone <repo_url> && cd llm-training-course
   ```
2. 安装 Python 3.10，并创建虚拟环境：
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   ```
3. 安装部分依赖（若需要运行所有 demo 请安装完整依赖）：
   ```bash
   pip install transformers datasets peft flask detoxify
   ```
4. 运行某个 lab 的 smoke test（示例）：
   ```bash
   bash labs/ci_smoke_test_03.sh
   ```
   注意：部分 smoke test 为轻量化检查（仅验证工具可用或脚本导入），完整训练或量化需在具备 GPU/编译环境的机器上运行。

## 建议的下一步
- 为每个 Lab 补齐更完整的示例与数据（目前为教学演示精简版）。
- 如需在 CI 运行完整的 LoRA/量化测试，建议配置 self-hosted runner 或 GPU-enabled runner。
- 逐章校对并补充图表、伪代码与参考链接以提升教科书质量。

---

如需我把 README.md 的某段改为更正式的教学简介、或直接生成 PDF/教学包，请告诉我。
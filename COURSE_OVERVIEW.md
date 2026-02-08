# LLM 工程实践与必要原理 — 课程指导规范（已重写）

## 概述（Summary）
- 名称：LLM 工程实践与必要原理（实践为主，辅以原理）
- 语言：全部中文（文件名/URL 建议使用英文短名以保证 URL 友好）
- 目标学员：有编程与工程背景（熟悉 Python、Git），对 LLM 只有基础概念，需以工程可交付能力为导向
- 课程定位：以“能做”为首要目标；理论覆盖关键原理以支撑工程判断（比例建议 1:2 原理:实践，但模块内可微调）
- 交付物：每模块的 LECTURE.md + LAB.md + EXAMPLE 代码 + smoke-test 脚本；期末 Capstone 项目交付可部署服务与技术报告

---

## 一、总体原则（High-level Principles）
- 工程优先：所有实验都必须可执行、可验证、可复现（提供 smoke test）。
- 可复现性：固定依赖版本、固定随机种子、提供小样例数据与预期输出。
- 渐进设计：从“搭建环境与最小推理”→“微调/LoRA”→“量化/推理优化”→“部署/监控”。
- 文档与验收并重：每次变更必须包含运行/验证步骤与预期检查点。
- 学员体验：课堂演示短、小任务可在50–90分钟内完成并能在家复现。

## 二、文件命名与目录结构（Repo Layout）
- 顶层建议结构：
  - docs/ — 讲义（LECTURE.md）与模块说明
  - labs/ — 实验手册（LAB.md）与脚本
  - examples/ 或 code_samples/ — 可运行示例代码、Notebook
  - slides/ — 课堂幻灯片
  - resources/ — 数据样本、外部资源链接、模型缓存说明
  - tools/ — 部署与基准脚本、Dockerfile
- 命名规范：
  - Lecture: {NN}_{short_english_name}_LECTURE.md （例：01_introduction_LECTURE.md）
  - Lab: {NN}_{short_english_name}_LAB.md
  - Example code: {NN}_{short}_example.py 或 {NN}_{short}_example.ipynb
- Front Matter 模板（Hugo/静态站兼容）：
---
title: "短英文名 — 中文显示名"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","微调"]
categories: ["LLM","工程实践"]
---

## 三、每章/每讲模板（Lecture / Lab Template）
- Lecture（结构）：
  1. 学习目标（3–5 条可验证目标）
  2. 背景与动机（为什么学、在哪儿用）
  3. 必要原理（精炼，配图或 ASCII 流程图）
  4. 工程实践要点（典型配置、陷阱、衡量指标）
  5. 案例与类比
  6. 参考与拓展阅读
  7. 预习/作业
- Lab（结构）：
  1. 实验目标与预期学习成果
  2. 时间预算（总时长 + 步骤时长）
  3. 所需环境（最低配置 + 推荐配置）
  4. 一键准备脚本（venv/conda/Docker）
  5. 详细步骤（可复制命令）
  6. 预期输出与验证（smoke test）
  7. 常见错误与排查要点（FAQ）
  8. 扩展任务（挑战题）
  9. 提交要求（作业/PR 内容与格式）

## 四、实验/作业标准（Acceptance Criteria）
- 每个 Lab 必须包含：
  - demo.py 或 notebook 的最小可运行示例
  - ci_smoke_test.sh（或 pytest 脚本）返回明确退出码
  - README（如何运行、依赖、预期输出）
- 验收维度（示例权重）：
  - 功能性与可复现（40%）  
  - 工程质量（测试、文档、结构）（25%）  
  - 性能/效果（量化、推理延迟等）（20%）  
  - 报告与演示（阐述问题与解决方案）（15%）

## 五、课程模块（建议目录与关键点）
- Module 00：导论与工具链（环境搭建、smoke test）
- Module 01：Tokenizer 与 LLM 基本原理（短讲 + 工程注意点）
- Module 02：微调与高效微调（LoRA/QLoRA）—（含 LLaMA Factory 实操）
- Module 03：数据工程（数据清洗、质量、评估）
- Module 04：量化与推理优化（llama.cpp、GGUF、ONNX）
- Module 05：部署与服务化（Ollama、One-API、容器化、监控）
- Module 06：安全、合规与模型治理（偏差、隐私、滥用防护）
- Module 07：Capstone（端到端项目）

## 六、工程化规范（PR / 分支 / CI）
- 分支策略：
  - feature/NN-short 描述新模块或实验
  - fix/* 用于修复
  - release/* 可选
- PR 模板内容要点：
  - 变更概述、运行步骤、验证步骤（如何通过 smoke test）、影响范围、关联 issue
  - Review Checklist（命令可复制、预期输出、依赖固定、安全注意）
- CI 建议（GitHub Actions）：
  - job: smoke-test（在 ubuntu-latest CPU 环境跑 demo 的快速 smoke test）
  - job: lint（Markdown lint、pyflakes）
  - 对 GPU-only tests 提供“模拟/断言”或标注为 manual workflow
- 代码审查要点：运行脚本、依赖、是否包含大文件（模型）且有外部下载说明

## 七、环境与复现（Reproducibility）
- 每个 Lab 提供：
  - requirements.txt 或 environment.yml（固定版本）
  - Dockerfile（推荐）或简易一键脚本 setup.sh
  - 小样例数据（放在 resources/ 或外部链接），并提供 checksum
  - 随机种子示例与复现说明
- 缓存与离线方案：
  - 提供模型缓存导出流程（HF cache打包或模型离线包）
  - 课堂内网/镜像说明（若网络受限）

## 八、教学与评估（Teaching Notes）
- 课堂演示建议：先展示 smoke test（模型加载耗时、输出），再做分步讲解
- 实验室指导：助教优先解决环境/依赖问题，鼓励学员提交 issue 记录失败案例
- 评估形式：作业提交（Git repo + CI 通过） + 小型演示（录像或现场）
- 学员提交清单（必做）：代码、README、运行日志、实验报告（问题、解决思路、结果）

## 九、性能与基准（Benchmarking）
- 每个与推理性能相关的 Lab 提供基准脚本（tokens/s、latency、memory）
- 在 README 中列出参考硬件配置与基线数据
- 在量化实验中同时报告“质量（常用指标） vs 性能”对比图表

## 十、安全、合规与伦理（必包含单元）
- 在相关实验中标注数据隐私风险、脱敏流程、可复现性与泄露风险
- 增加模型滥用测试与应对建议（prompt 屏蔽、流水线过滤）
- 对使用真实/敏感数据的实验必须要求先做脱敏或使用合成数据

## 十一、样板 Front Matter 与文件示例
- Lecture 示例 Front Matter（见上节）
- Lab 最低提交：
  - {NN}_{name}_LAB.md
  - demo.py / notebook
  - ci_smoke_test.sh（可在 CI 下跑）
  - README.md（一句话运行说明 + 依赖）

## 十二、维护与迭代（Course Maintenance）
- 每次课程后收集反馈（GitHub issue + 简短问卷），在 labs/ 或 docs/ 下记录问题与修复（changelog）
- 每季度（或当关键工具链更新）做一次全面检视与更新（依赖、命令、示例）
- 指定负责人与合并策略（谁有权合并实验改动）

## 十三、交付模板（Checklist）—— 每个模块合并前必须满足
- [] Lecture.md 存在并通过基本拼写检查  
- [] Lab.md 存在并包含步骤 + 预期输出  
- [] demo.py / notebook 能在 venv 下运行（本地或 CI）  
- [] ci_smoke_test.sh 提供并可被 CI 执行（或说明为什么无法执行）  
- [] README 写明运行依赖与命令  
- [] Front Matter 完整（title/date/tags/categories）  
- [] 教学助教/Reviewers 已至少一人 review

## 十四、其它建议（快速参考）
- 小模型默认使用 distilgpt2 / t5-small 做课堂 demo；生产模块用 Qwen/DeepSeek 等指定模型并说明许可
- 把复杂的 GPU-only 实验拆分为“理论 + 本地小样例”两部分，避免课堂中断
- 保持讲义中“类比+流程图+命令”三要素：学员能看懂原理、看懂命令、复制结果

---

（本文件已按你的要求直接重写为课程指导规范，语言为中文，面向工程实践型学员，参考了 docs/02_llama_factory_lecture.md 与指定的课程开发规范样式。）

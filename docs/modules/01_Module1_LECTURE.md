# Module 1 — LLM 全景与实验环境准备

## 目标
- 让学员了解课程定位与技术栈
- 在训练环境中快速搭建并验证实验依赖

## 课程内容
1. LLM 发展简史与技术栈对比
2. 课程技术栈：LLaMA Factory、llama.cpp、Ollama、One-API
3. 实验环境选择：云端 vs 本地，GPU vs CPU
4. AutoDL/镜像选择与注意事项
5. 常见依赖与冲突处理（CUDA、PyTorch、bitsandbytes）

## 环境搭建（步骤）
1. 安装 Python 3.10+
2. 克隆仓库并进入目录：
   git clone <repo> && cd llm-training-course
3. 运行环境脚本：
   bash resources/configs/env_setup.sh
4. 激活虚拟环境：
   source .venv/bin/activate
5. （可选）安装 Docker：
   sudo apt install docker.io

## 验证脚本
- labs/Temp_02_Lab_Verification.md 包含基础验证步骤（Python/torch/transformers 可用性测试）

## 故障排查要点
- 检查 CUDA 与 PyTorch 版本匹配
- bitsandbytes 在某些平台需要特殊编译，建议使用官方 wheel 或 conda

## 参考
- COURSE_OVERVIEW.md

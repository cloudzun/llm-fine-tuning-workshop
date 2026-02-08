# Module 4 — Ollama 本地部署

## 目标
- 了解 Ollama 架构与 Modelfile 配置
- 演示如何导入量化模型并进行基本 API 调用

## 内容概要
1. Ollama 简介与对比（vs docker/其他本地部署）
2. Modelfile 字段详解（name、format、model_path、parameters）
3. 导入模型：从 GGUF 导入到 Ollama
4. 调用示例：本地 API 调用与参数调整

## 实验步骤（示例）
1. 安装 Ollama（参考官方文档）
2. 编写 Modelfile（参考 resources/configs/Modelfile.example）
3. 导入模型并测试对话

## 验证点
- Ollama 能识别并加载 Modelfile 指定的模型
- 通过 curl 或 Python 的 OpenAI 兼容客户端进行基本对话测试

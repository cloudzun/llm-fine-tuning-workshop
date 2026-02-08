# Module 3 — 模型量化原理与实践

## 目标
- 让学员理解量化的目的、常见方法与 trade-offs
- 演示 llama.cpp 与 GGUF 等工具链的基本用法

## 内容概要
1. 量化基础：INT8/INT4/INT3 概念，量化误差来源
2. GGUF 格式与 llama.cpp 支持的量化等级（Q4_Q8 等）
3. 量化前的准备：校准集、权重格式、导出策略
4. 实操：编译 llama.cpp、运行量化命令示例

## 实验步骤示例
1. 编译 llama.cpp：
   git clone https://github.com/ggerganov/llama.cpp && make
2. 使用转换脚本将模型转换为 GGUF
3. 对比量化等级的推理性能与输出差异

## 验证点
- 生成 GGUF 文件
- 记录 tokens/s 与显存占用
- 简单对比模型回答差异（自动化脚本）

# Module 8 — 综合实战：客服助手（课程综合实验）

目标：把微调、量化、部署串联成一个端到端流程，产出可调用的客服助手。

目录结构建议
- code_samples/projects/customer_assistant/
  - data/
  - train/
  - deploy/

主要步骤
1. 数据准备：收集或合成 100–500 条高质量对话
2. 使用 LoRA 微调模型（参考 Module2 配置）
3. 量化并导出 GGUF（参考 Module3）
4. 导入 Ollama 并配置 Modelfile（参考 Module4）
5. 通过 One-API 或直接 Ollama API 提供服务

验收标准
- 能对给定 10 个客服问题生成合理回答
- 提供部署说明与脚本

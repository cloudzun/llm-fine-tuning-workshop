# Module 2 — 微调配置模板与示例

包含 LoRA / QLoRA 的配置示例和说明，供 Module2 实验使用。

示例 LoRA 配置（Trainer / Transformers）：
```
per_device_train_batch_size: 1
num_train_epochs: 3
learning_rate: 1e-4
fp16: true
save_total_limit: 1
```

QLoRA 示例参考（使用 bitsandbytes + 4-bit 训练）：
- 使用适当的 quantization backend（bitsandbytes）
- 注意 adapter 保存策略

小样例数据建议放置在 resources/data/module2_examples/

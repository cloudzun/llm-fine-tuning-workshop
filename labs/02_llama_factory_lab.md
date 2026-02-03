# **LLaMA Factory微调实战 - 详细实验步骤**

---

## **实验1-1: LLaMA Factory环境搭建与界面熟悉** (15分钟)

### **步骤1: AutoDL环境准备** (5分钟)
```bash
# 1. 租用AutoDL机器（3090/4090，推荐PyTorch镜像）
# 2. 进入JupyterLab或SSH连接
# 3. 创建工作目录
mkdir -p ~/llm-course/day1
cd ~/llm-course/day1

# 4. 检查环境
nvidia-smi # 确认GPU可用
python --version # 确认Python 3.10+
```

### **步骤2: 安装LLaMA Factory** (5分钟)
```bash
# 克隆仓库
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory

# 安装依赖（使用清华镜像加速）
pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple

# 验证安装
llamafactory-cli version
```

### **步骤3: 启动WebUI** (5分钟)
```bash
# 启动WebUI
llamafactory-cli webui

# 如果是SSH连接，需要端口转发
# 在本地终端执行：
# ssh -L 7860:localhost:7860 root@your-autodl-ip

# 浏览器访问: http://localhost:7860
```

**界面熟悉要点**：
- **Language**: 切换到中文界面
- **Model name**: 模型选择区
- **Finetuning method**: 微调方法选择
- **Dataset**: 数据集选择
- **Training parameters**: 训练参数配置
- **Output dir**: 输出目录设置

---

## **实验1-2: 下载模型与数据准备** (20分钟)

### **步骤1: 下载Qwen2.5-7B模型** (10分钟)

**方法A: 使用ModelScope（推荐，国内快）**
```bash
# 安装modelscope
pip install modelscope -i https://pypi.tuna.tsinghua.edu.cn/simple

# 创建下载脚本
cat > download_model.py << 'EOF'
from modelscope import snapshot_download

model_dir = snapshot_download(
    'Qwen/Qwen2.5-7B-Instruct',
    cache_dir='./models'
)
print(f"模型下载到: {model_dir}")
EOF

# 执行下载
python download_model.py
```

**方法B: 使用HuggingFace（需要魔法）**
```bash
# 设置HF镜像
export HF_ENDPOINT=https://hf-mirror.com

# 下载
huggingface-cli download Qwen/Qwen2.5-7B-Instruct \
--local-dir ./models/Qwen2.5-7B-Instruct
```

### **步骤2: 准备训练数据** (10分钟)

**创建示例数据集 - 客服对话场景**
```bash
# 创建数据目录
mkdir -p data

# 创建训练数据文件
cat > data/customer_service.json << 'EOF'
[
  {
    "instruction": "如何查询订单物流信息？",
    "input": "",
    "output": "您可以通过以下方式查询订单物流： 1. 登录账户，进入"我的订单"页面 2. 找到对应订单，点击"查看物流" 3. 或者直接在首页搜索框输入订单号查询 如需帮助，请提供您的订单号，我来帮您查询。"
  },
  {
    "instruction": "退货流程是什么？",
    "input": "",
    "output": "退货流程如下： 1. 在订单详情页点击"申请退货" 2. 选择退货原因并上传凭证（如需要） 3. 等待审核通过（1-2个工作日） 4. 按照提供的地址寄回商品 5. 我们收到商品后3-5个工作日内退款 注意：商品需保持完好，带齐配件和发票。"
  },
  {
    "instruction": "支持哪些支付方式？",
    "input": "",
    "output": "我们支持以下支付方式： 1. 微信支付 2. 支付宝 3. 银联卡支付 4. 信用卡支付 5. 花呗分期 所有支付方式都是安全加密的，请放心使用。"
  },
  {
    "instruction": "会员有什么优惠？",
    "input": "",
    "output": "会员专享权益包括： 1. 全场商品9.5折优惠 2. 每月赠送优惠券礼包 3. 免册包邮（无门槛） 4. 优先客服支持 5. 生日月双倍积分 6. 新品提前购买权 现在注册即可获得30天免费会员体验！"
  },
  {
    "instruction": "如何联系人工客服？",
    "input": "",
    "output": "联系人工客服的方式： 1. 在线客服：工作日9:00-18:00，点击右下角客服图标 2. 客服电话：400-XXX-XXXX（工作日9:00-21:00） 3. 邮箱：service@example.com 4. 微信公众号：关注后发送"人工客服" 我会尽力帮您解决问题，如需人工协助请告诉我。"
  }
]
EOF
```

**注册数据集到LLaMA Factory**
```bash
# 编辑数据集配置文件
cat >> data/dataset_info.json << 'EOF'
{
  "customer_service": {
    "file_name": "customer_service.json",
    "columns": {
      "prompt": "instruction",
      "query": "input",
      "response": "output"
    }
  }
}
EOF

# 将配置文件复制到LLaMA Factory目录
cp data/dataset_info.json LLaMA-Factory/data/
cp data/customer_service.json LLaMA-Factory/data/
```

---

## **实验1-3: LoRA微调实战** (45分钟)

### **步骤1: WebUI配置微调参数** (10分钟)

在WebUI中进行以下配置：

**1. 模型设置**
```
Model name: Qwen2.5-7B-Instruct
Model path: ./models/Qwen2.5-7B-Instruct (或ModelScope下载路径)
Finetuning method: lora
```

**2. 数据集设置**
```
Dataset: customer_service (应该在下拉列表中看到)
Data format: alpaca
Cutoff length: 1024
```

**3. LoRA参数**
```
LoRA rank: 8
LoRA alpha: 16
LoRA dropout: 0.05
LoRA target modules: all (或选择 q_proj,v_proj)
```

**4. 训练参数**
```
Learning rate: 5e-5
Epochs: 3
Batch size: 2
Gradient accumulation: 4
Max samples: 1000
Learning rate scheduler: cosine
Warmup steps: 100
```

**5. 输出设置**
```
Output dir: ./output/qwen-customer-service
Logging steps: 10
Save steps: 100
```

### **步骤2: 启动训练** (20分钟)
```bash
# 方法A: 通过WebUI启动
# 点击"Start"按钮，观察训练日志

# 方法B: 通过命令行启动（推荐，便于调试）
llamafactory-cli train \
--stage sft \
--model_name_or_path ./models/Qwen2.5-7B-Instruct \
--dataset customer_service \
--template qwen \
--finetuning_type lora \
--lora_rank 8 \
--lora_alpha 16 \
--lora_dropout 0.05 \
--lora_target all \
--output_dir ./output/qwen-customer-service \
--per_device_train_batch_size 2 \
--gradient_accumulation_steps 4 \
--learning_rate 5e-5 \
--num_train_epochs 3 \
--lr_scheduler_type cosine \
--warmup_steps 100 \
--logging_steps 10 \
--save_steps 100 \
--plot_loss \
--fp16
```

**训练过程监控要点**：
```bash
# 另开一个终端，实时监控
watch -n 1 nvidia-smi # 监控GPU使用

# 查看训练日志
tail -f ./output/qwen-customer-service/trainer_log.jsonl

# 关键指标
# - loss: 应该逐步下降，最终在0.5-1.5之间
# - learning_rate: 观察学习率变化曲线
# - GPU memory: 应该在20-24GB（4090）
```

**预期训练时间**：
- 3090: 约15-20分钟
- 4090: 约10-15分钟

### **步骤3: 查看训练结果** (5分钟)
```bash
# 检查输出目录
ls -lh ./output/qwen-customer-service/

# 应该看到：
# - adapter_config.json (LoRA配置)
# - adapter_model.bin (LoRA权重)
# - training_loss.png (loss曲线图)
# - trainer_log.jsonl (训练日志)

# 查看loss曲线
# 可以在WebUI的"Evaluate"标签页查看
# 或者直接打开training_loss.png
```

### **步骤4: 模型合并（可选）** (10分钟)
```bash
# 方法A: 通过WebUI
# 切换到"Export"标签页
# - Model name: Qwen2.5-7B-Instruct
# - Checkpoint path: output/qwen-customer-service
# - Export dir: output/qwen-customer-service-merged
# 点击"Export"

# 方法B: 通过命令行
llamafactory-cli export \
--model_name_or_path ./models/Qwen2.5-7B-Instruct \
--adapter_name_or_path ./output/qwen-customer-service \
--template qwen \
--finetuning_type lora \
--export_dir ./output/qwen-customer-service-merged \
--export_size 2 \
--export_legacy_format False
```

---

## **实验1-4: 微调效果测试** (30分钟)

### **步骤1: WebUI交互测试** (10分钟)
```bash
# 切换到"Chat"标签页
# 配置：
# - Model name: Qwen2.5-7B-Instruct
# - Checkpoint path: output/qwen-customer-service (使用LoRA)
# - Template: qwen
# 点击"Load model"

# 测试对话：
```

**测试用例**：
| 测试问题 | 预期行为 |
|---------|---------|
| "如何查询订单？" | 应该给出详细的查询步骤 |
| "我要退货" | 应该说明退货流程 |
| "你们支持微信支付吗？" | 应该列出所有支付方式 |
| "天气怎么样？"（超出训练范围） | 观察模型如何处理 |

### **步骤2: 对比原模型与微调模型** (10分钟)

**创建对比测试脚本**：
```python
# test_comparison.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def test_model(model_path, adapter_path=None, question="如何查询订单物流信息？"):
    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    
    # 加载模型
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # 如果有adapter，加载LoRA权重
    if adapter_path:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter_path)
        print("✓ 已加载LoRA权重")
    
    # 构造prompt
    messages = [
        {"role": "system", "content": "你是一个专业的客服助手。"},
        {"role": "user", "content": question}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    # 生成回复
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        top_p=0.8,
        repetition_penalty=1.1
    )
    response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
    return response

# 测试原模型
print("=" * 50)
print("原始模型回答：")
print("=" * 50)
response_base = test_model("./models/Qwen2.5-7B-Instruct")
print(response_base)

# 测试微调模型
print(" " + "=" * 50)
print("微调模型回答：")
print("=" * 50)
response_finetuned = test_model(
    "./models/Qwen2.5-7B-Instruct",
    "./output/qwen-customer-service"
)
print(response_finetuned)
```

```bash
# 运行对比测试
python test_comparison.py
```

### **步骤3: 批量评估** (10分钟)

**创建评估脚本**：
```python
# evaluate.py
import json
from test_comparison import test_model

# 测试用例
test_cases = [
    "如何查询订单物流信息？",
    "我想退货，怎么操作？",
    "你们支持哪些支付方式？",
    "会员有什么优惠？",
    "怎么联系人工客服？"
]

results = []
for question in test_cases:
    print(f" 测试问题: {question}")
    print("-" * 50)
    
    # 测试微调模型
    response = test_model(
        "./models/Qwen2.5-7B-Instruct",
        "./output/qwen-customer-service",
        question
    )
    results.append({
        "question": question,
        "response": response
    })
    print(response)

# 保存结果
with open("evaluation_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(" 评估完成！结果已保存到 evaluation_results.json")
```

```bash
# 运行评估
python evaluate.py
```

---

## **常见问题排查**

### **问题1: CUDA Out of Memory**
```bash
# 解决方案A: 减小batch size
# 在训练参数中修改：
per_device_train_batch_size: 1
gradient_accumulation_steps: 8

# 解决方案B: 使用量化训练
# 添加参数： --quantization_bit 4
```

### **问题2: 模型下载失败**
```bash
# 使用断点续传
export HF_HUB_ENABLE_HF_TRANSFER=1
pip install hf-transfer

# 或手动下载后指定本地路径
```

### **问题3: Loss不下降**
```bash
# 检查点：
# 1. 数据格式是否正确
cat data/customer_service.json | python -m json.tool

# 2. 学习率是否合适（尝试调整）
learning_rate: 1e-4 # 增大
# 或 learning_rate: 1e-5 # 减小

# 3. 检查数据是否被正确加载
# 查看日志中的样本数量
```

### **问题4: 训练速度慢**
```bash
# 优化方案：
# 1. 使用flash attention（如果支持）
--use_flash_attention True

# 2. 减少logging频率
--logging_steps 50

# 3. 使用更高效的数据加载
--preprocessing_num_workers 4
```

---

## **实验检查清单**

完成实验后，确认以下文件存在：
```bash
# 检查脚本
cat > check_experiment.sh << 'EOF'
#!/bin/bash

echo "检查实验1完成情况..."

# 检查模型
if [ -d "./models/Qwen2.5-7B-Instruct" ]; then
    echo "✓ 模型已下载"
else
    echo "✗ 模型未找到"
fi

# 检查数据
if [ -f "./data/customer_service.json" ]; then
    echo "✓ 训练数据已准备"
else
    echo "✗ 训练数据未找到"
fi

# 检查训练输出
if [ -f "./output/qwen-customer-service/adapter_model.bin" ]; then
    echo "✓ LoRA权重已生成"
else
    echo "✗ LoRA权重未找到"
fi

# 检查loss曲线
if [ -f "./output/qwen-customer-service/training_loss.png" ]; then
    echo "✓ 训练曲线已生成"
else
    echo "✗ 训练曲线未找到"
fi

# 检查评估结果
if [ -f "./evaluation_results.json" ]; then
    echo "✓ 评估已完成"
else
    echo "✗ 评估未完成"
fi

echo "检查完成！"
EOF

chmod +x check_experiment.sh
./check_experiment.sh
```

---

## **扩展练习（课后）**

1. **尝试不同的LoRA参数**
   - rank: 4, 16, 32
   - 观察模型大小和效果的变化

2. **使用自己的数据**
   - 收集50-100条领域数据
   - 按照格式整理
   - 重新训练

3. **尝试QLoRA**
   - 添加 `--quantization_bit 4`
   - 对比训练速度和显存占用

4. **超参数调优**
   - 学习率: 1e-4, 5e-5, 1e-5
   - Epoch: 1, 3, 5
   - 找到最佳组合

---
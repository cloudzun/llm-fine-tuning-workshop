import json
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from peft import get_peft_config, get_peft_model, LoraConfig, TaskType

# Very small demo script for LoRA micro-finetune
MODEL_NAME = "qwen2.5-7b-instruct"  # replace with local path or smaller model for faster runs

with open("sample_data.jsonl","r") as f:
    lines = [json.loads(l) for l in f]

dataset = Dataset.from_list([{"text": l["text"]} for l in lines])

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, load_in_8bit=True, device_map="auto")

peft_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj","v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, peft_config)

# Tokenize

def preprocess(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=512)

dataset = dataset.map(preprocess, batched=False)

training_args = TrainingArguments(
    output_dir="./lora_out",
    per_device_train_batch_size=1,
    num_train_epochs=1,
    logging_steps=10,
    save_total_limit=1,
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

trainer.train()

# Save adapter only
model.save_pretrained("./lora_out")

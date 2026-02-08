"""
Minimal LoRA demo script for classroom use.
This script is intentionally small: it loads a small model and attaches LoRA (PEFT) for demonstration.
It is NOT intended for full training in the classroom environment — use it to show the pipeline and verify imports.
"""
import os
import sys

MODEL = os.environ.get('MODEL', 'distilgpt2')
SAMPLE_SIZE = int(os.environ.get('SAMPLE_SIZE', '16'))

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model
except Exception as e:
    print('MISSING_DEPENDENCY', e)
    print('Install with: pip install transformers datasets peft')
    sys.exit(1)


def main():
    print('MODEL:', MODEL)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL)

    # load tiny sample
    ds = load_dataset('wikitext', 'wikitext-2-raw-v1', split=f'train[:{SAMPLE_SIZE}]')
    print('SAMPLE SIZE:', len(ds))

    # LoRA config (demo)
    lora_config = LoraConfig(r=8, lora_alpha=16, target_modules=['q_proj', 'v_proj'], lora_dropout=0.05)
    try:
        peft_model = get_peft_model(model, lora_config)
        print('PEFT MODEL READY')
    except Exception as e:
        print('PEFT_SETUP_FAIL', e)

    # Print small debug info
    print('Tokenizer vocab size:', len(tokenizer))


if __name__ == '__main__':
    main()

#!/usr/bin/env bash
set -e
python labs/02_train_lora.py > /tmp/lora_demo_out.txt
grep -q "PEFT MODEL READY" /tmp/lora_demo_out.txt && echo "SMOKE OK" || (cat /tmp/lora_demo_out.txt && exit 1)

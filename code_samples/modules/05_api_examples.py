import requests

# Simple Ollama / OpenAI-compatible API example
OLLAMA_URL = "http://localhost:11434/v1/completions"

payload = {
    "model": "qwen2.5-7b-instruct-lora",
    "messages": [{"role":"user","content":"Tell me about LoRA in 2 sentences."}],
}

r = requests.post(OLLAMA_URL, json=payload)
print(r.status_code)
print(r.text)

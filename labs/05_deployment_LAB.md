---
title: "Chapter 5 Lab — 部署实操：容器化与 Ollama 快速部署"
date: 2026-02-08T00:00:00+08:00
draft: false
tags: ["llm","部署","Ollama","容器化"]
categories: ["LLM","工程实践"]
---

# 第5章实验 — 部署实操：容器化与 Ollama 快速部署

## 实验目标
- 把量化或微调后的模型封装为 Docker 镜像；
- 在本地用 Ollama 或简单的 Flask API 启动模型服务；
- 记录基本的监控数据（cpu/memory/latency）。

## 预估时间
- 准备与构建镜像：20–40 分钟
- 启动服务并验证：10–20 分钟
- 监控与记录：10–20 分钟

## 示例 Dockerfile（简化）
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python","serve.py"]
```

## 示例 serve.py（简化）
```python
from flask import Flask, request, jsonify
from transformers import pipeline
app = Flask(__name__)

generator = pipeline('text-generation', model='distilgpt2', device=-1)

@app.route('/generate', methods=['POST'])
def gen():
    prompt = request.json.get('prompt','')
    res = generator(prompt, max_length=50)
    return jsonify(res)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
```

## 运行与验证
```bash
docker build -t llm-demo:latest .
docker run -p 8080:8080 llm-demo:latest
# 然后 curl 调用 /generate
```

## 提交要求
- Dockerfile、serve.py、requirements.txt
- README.md（如何构建与运行）

## 教学提示
- 课堂演示应展示镜像构建时间与启动时间，强调冷启动成本；
- 对于 Ollama，如果可用，展示 Modelfile 与导入流程；否则用 Flask 做简易替代。 

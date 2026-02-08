#!/usr/bin/env python3
# labs/05_serve.py — 简单 Flask 服务示例
from flask import Flask, request, jsonify
try:
    from transformers import pipeline
except Exception:
    print('MISSING_TRANSFORMERS')
    raise

app = Flask(__name__)

generator = pipeline('text-generation', model='distilgpt2', device=-1)

@app.route('/generate', methods=['POST'])
def gen():
    prompt = request.json.get('prompt','')
    res = generator(prompt, max_length=50)
    return jsonify(res)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)

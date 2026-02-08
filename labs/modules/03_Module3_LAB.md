# Lab 03 — 模型量化实战

目标：使用 llama.cpp 流程将已训练模型转换并量化为 GGUF 并进行推理测试。

步骤：
1. 编译 llama.cpp：
   git clone https://github.com/ggerganov/llama.cpp && make
2. 准备模型文件并运行转换脚本（示例）：
   python convert_to_gguf.py --input ./model_dir --output ./model.gguf --bits 8
3. 使用 llama.cpp 的示例程序运行推理并记录性能：
   ./main -m ./model.gguf -p "Hello" -n 128

验收：生成 model.gguf 并能用 main 程序输出文本

注意：上述脚本为占位示例，请根据实际工具替换具体脚本和命令

# Lab 01 — 环境配置与验证

目标：在学员机器上完成实验环境搭建并通过基础验证。

步骤：
1. 运行环境搭建脚本：
   bash /home/chengzh/training-projects/llm-training-course/resources/configs/env_setup.sh
2. 激活虚拟环境：
   source /home/chengzh/training-projects/llm-training-course/.venv/bin/activate
3. 运行验证脚本：
   python -c "import torch; print(torch.__version__); print('cuda', torch.cuda.is_available())"
4. 安装 Docker（可选）并确认：
   docker version

常见问题与解决：
- Python 版本错误：安装合适版本并重试
- pip 依赖冲突：尝试 pip install --upgrade pip 或使用 --use-feature=2020-resolver

验收：输出显示 torch 版本与 cuda 可用性状态

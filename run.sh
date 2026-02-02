#!/bin/bash
# DreamWeaver AI 启动脚本

echo "🎨 绘梦精灵 (DreamWeaver AI) 启动脚本"
echo "========================================"

# 检查Python
echo "检查Python环境..."
python --version

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 检查配置
echo "检查配置..."
python check_setup.py

# 启动应用
echo ""
echo "🚀 启动应用..."
echo "应用将在 http://localhost:8501 打开"
echo "按 Ctrl+C 停止运行"
echo ""

streamlit run src/app.py

"""
DreamWeaver AI - 绘梦精灵
ModelScope 创空间入口文件
"""
import os
import sys

# 添加 src 目录到 Python 路径
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# 切换工作目录到 src
os.chdir(src_path)

# 导入并运行主应用
exec(open('app.py', encoding='utf-8').read())

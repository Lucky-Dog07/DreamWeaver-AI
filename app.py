"""
DreamWeaver AI - 绘梦精灵
ModelScope 创空间入口文件
"""
import os
import sys

# 添加 src 目录到 Python 路径
root_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 运行主应用
exec(open(os.path.join(src_path, 'app.py'), encoding='utf-8').read())

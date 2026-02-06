"""
DreamWeaver AI - 绘梦精灵
ModelScope 创空间入口文件
"""
import os
import sys
import subprocess

# 获取当前文件所在目录
root_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_dir, 'src')

# 添加 src 目录到 Python 路径
sys.path.insert(0, src_path)

# 切换工作目录到 src
os.chdir(src_path)

# 直接导入并运行
from app import *

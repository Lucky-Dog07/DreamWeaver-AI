#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DreamWeaver AI 配置检查脚本
检查所有必要的依赖和配置是否正确
"""

import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - 正常")
        return True
    else:
        print(f"❌ Python版本过低 (需要 3.8+)")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")

    required_packages = [
        'streamlit',
        'streamlit_drawable_canvas',
        'cozepy',
        'dashscope',
        'requests',
        'dotenv',
        'numpy',
        'PIL',
        'cv2',
        'scipy'
    ]

    all_ok = True
    for package in required_packages:
        try:
            if package == 'PIL':
                from PIL import Image
                print(f"✅ {package} - 已安装")
            elif package == 'dotenv':
                from dotenv import load_dotenv
                print(f"✅ {package} - 已安装")
            elif package == 'cv2':
                import cv2
                print(f"✅ {package} - 已安装")
            else:
                __import__(package)
                print(f"✅ {package} - 已安装")
        except ImportError:
            print(f"❌ {package} - 未安装")
            all_ok = False

    return all_ok

def check_env_file():
    """检查环境变量文件"""
    print("\n🔍 检查环境变量配置...")

    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ .env 文件存在")

        with open(env_file, 'r') as f:
            content = f.read()

        required_keys = [
            'DASHSCOPE_API_KEY',
            'COZE_API_TOKEN',
            'COZE_BOT_ID'
        ]

        all_configured = True
        for key in required_keys:
            if key in content:
                # 检查是否配置了值
                if f'{key}=' in content:
                    value = content.split(f'{key}=')[1].split('\n')[0].strip()
                    if value and not value.startswith('your_'):
                        print(f"✅ {key} - 已配置")
                    else:
                        print(f"⚠️  {key} - 未填写值")
                        all_configured = False
            else:
                print(f"❌ {key} - 未找到")
                all_configured = False

        return all_configured
    else:
        print(f"❌ .env 文件不存在")
        print(f"💡 请复制 .env.example 为 .env 并填入API密钥")
        return False

def check_directories():
    """检查必要的目录"""
    print("\n🔍 检查目录结构...")

    required_dirs = [
        'src',
        'src/pages',
        'src/services',
        'src/models',
        'src/utils',
        'data',
        'data/artworks',
    ]

    all_ok = True
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ {dir_path}/ - 存在")
        else:
            print(f"❌ {dir_path}/ - 不存在")
            all_ok = False

    return all_ok

def check_main_files():
    """检查主要文件"""
    print("\n🔍 检查核心文件...")

    required_files = [
        'src/app.py',
        'src/pages/1_🎬_应用首页.py',
        'src/pages/2_🎨_智能画板.py',
        'src/pages/3_🧚_加工工厂.py',
        'src/pages/5_⚙️_设置中心.py',
        'src/utils/session_manager.py',
        'src/utils/config_loader.py',
        'src/utils/file_handler.py',
        'src/services/multimodal_service.py',
        'src/services/voice_service.py',
        'src/services/coze_service.py',
        'src/services/video_service.py',
        'requirements.txt',
    ]

    all_ok = True
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"✅ {file_path} - 存在")
        else:
            print(f"❌ {file_path} - 不存在")
            all_ok = False

    return all_ok

def main():
    """主检查函数"""
    print("=" * 50)
    print("🎨 绘梦精灵 (DreamWeaver AI) - 配置检查")
    print("=" * 50)

    checks = [
        ("Python版本", check_python_version),
        ("依赖包", check_dependencies),
        ("目录结构", check_directories),
        ("核心文件", check_main_files),
        ("环境变量", check_env_file)
    ]

    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} - 检查失败: {str(e)}")
            results[check_name] = False

    print("\n" + "=" * 50)
    print("📋 检查总结")
    print("=" * 50)

    for check_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")

    all_passed = all(results.values())

    print("\n" + "=" * 50)
    if all_passed:
        print("✅ 所有检查通过！")
        print("\n🚀 你可以运行以下命令启动应用:")
        print("   streamlit run src/app.py")
    else:
        print("❌ 某些检查未通过")
        print("\n💡 请根据上方提示修复问题，然后重新运行此脚本")
    print("=" * 50)

    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

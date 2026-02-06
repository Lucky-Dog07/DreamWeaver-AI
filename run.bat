@echo off
REM DreamWeaver AI 启动脚本 (Windows)

echo.
echo 🎨 绘梦精灵 (DreamWeaver AI) 启动脚本
echo ========================================
echo.

REM 检查Python
echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)

REM 创建虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 检查配置
echo 检查配置...
python check_setup.py
if %errorlevel% neq 0 (
    echo ⚠️  配置检查失败，但继续启动...
)

REM 启动应用
echo.
echo 🚀 启动应用...
echo 应用将在 http://localhost:8501 打开
echo 按 Ctrl+C 停止运行
echo.

streamlit run src/app.py

pause

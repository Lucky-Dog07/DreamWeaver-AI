# 🎨 绘梦精灵 (DreamWeaver AI)

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/yourname/dreamweaver-ai)

**让每个孩子的画都能被看见、被听见、被记住**

> 🏆 2025"小有可为"公益黑客松参赛项目 | 🎯 AI For Good赋能教育公平

---

## 📖 项目简介

**绘梦精灵**是一个基于Streamlit和多模态大模型的儿童创造力启发与情感陪伴系统。通过"视觉-听觉-动态影像"全感官反馈，帮助孩子跨越表达障碍，实现从"被动绘画"到"主动创作故事"的转变。

### 核心价值

- **教育公平**：为乡村学校和特殊教育机构提供低成本、高质量的美术教育支持
- **情感陪伴**：AI小精灵实时陪伴，给予孩子积极的反馈和鼓励
- **创造力培养**：通过多维度分析，引导孩子发展艺术表达能力
- **成长记录**：自动生成儿童创造力发展档案，追踪成长轨迹

---

## ✨ 核心功能

### 🎨 智能画板系统

- **自由绘画**：HTML5 Canvas实现的高性能画板
- **笔刷工具**：多种颜色、粗细、类型选择
- **编辑工具**：撤销/重做/清空功能
- **小精灵陪伴**：实时语音反馈和创意建议

### 🧚 AI小精灵系统

- **实时交互**：根据绘画内容生成个性化反馈
- **语音合成**：使用Qwen-Omini-Flash生成儿童友好的语音
- **五维度分析**：
  - 🎯 主题分析 - 理解孩子在画什么
  - 🎨 色彩分析 - 色彩心理学解读
  - 📐 构图分析 - 艺术启蒙
  - 💭 情感分析 - 理解孩子内心
  - 📊 发展阶段评估 - 教育价值核心

### 🧚 作品工坊系统

- **音乐生成**：将画作转换为配乐（Coze工作流）
- **AI点评**：生成专业的语音评价
- **视频生成**：首尾帧魔法动画（火山引擎）
- **多格式导出**：支持图片、音乐、视频下载

### ⚙️ 设置中心

- 👤 个人信息管理
- 🎨 界面主题和显示设置
- 🔊 语音和音乐设置
- ♿ 无障碍设置
- 📊 数据管理和存储统计

---

## 🚀 快速开始

### 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.8+
- **内存**: 至少2GB RAM
- **网络**: 需要互联网连接（用于API调用）

### 一键启动（推荐）

#### Windows用户
```batch
# 双击运行
run.bat
```

#### macOS/Linux用户
```bash
# 运行启动脚本
bash run.sh
```

### 手动安装

#### 1. 安装Python依赖

```bash
# 创建虚拟环境（可选但推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 2. 配置API密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# 需要填入以下API密钥：

# 必需 - 阿里云DashScope (Qwen Omini)
DASHSCOPE_API_KEY=your_api_key_here

# 必需 - Coze (音乐生成)
COZE_API_TOKEN=your_token_here
COZE_BOT_ID=your_bot_id_here
COZE_WORKFLOW_ID=7601786439168229386

# 可选 - 火山引擎 (视频生成)
HUOSHAN_ACCESS_KEY=your_key_here
HUOSHAN_SECRET_KEY=your_secret_here
```

#### 3. 检查配置

```bash
python check_setup.py
```

应该看到所有检查都✅通过。

#### 4. 启动应用

```bash
streamlit run src/app.py
```

应用将自动在 `http://localhost:8501` 打开浏览器。

---

## 🔑 API密钥获取

### 1. 阿里云DashScope (Qwen Omini)

1. 访问 [阿里云百炼](https://bailian.console.aliyun.com/)
2. 注册/登录账号
3. 进入API密钥管理
4. 创建新的API Key
5. 复制密钥到 `.env` 中的 `DASHSCOPE_API_KEY`

### 2. Coze (音乐生成)

1. 访问 [Coze官网](https://coze.com/)
2. 注册/登录账号
3. 创建Bot或使用现有Bot
4. 在设置中获取API Token
5. 复制到 `.env` 中的 `COZE_API_TOKEN` 和 `COZE_BOT_ID`

### 3. 火山引擎 (视频生成 - 可选)

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 注册/登录账号
3. 在API密钥管理中创建新密钥
4. 复制到 `.env` 中的 `HUOSHAN_ACCESS_KEY` 和 `HUOSHAN_SECRET_KEY`

---

## 📁 项目结构

```
DreamWeaver/
├── src/
│   ├── app.py                          # 主应用入口
│   ├── __init__.py
│   │
│   ├── pages/                          # 多页面应用
│   │   ├── 1_🎬_应用首页.py            # 首页
│   │   ├── 2_🎨_智能画板.py            # 智能画板
│   │   ├── 3_🧚_加工工厂.py            # 作品工坊
│   │   └── 5_⚙️_设置中心.py            # 设置页面
│   │
│   ├── services/                       # 业务服务层
│   │   ├── multimodal_service.py       # 多模态分析
│   │   ├── voice_service.py            # 语音交互
│   │   ├── coze_service.py             # Coze工作流
│   │   └── video_service.py            # 视频生成
│   │
│   ├── models/                         # 数据模型
│   │   └── drawing_model.py            # 绘画/作品数据模型
│   │
│   ├── utils/                          # 工具函数
│   │   ├── session_manager.py          # 会话状态管理
│   │   ├── config_loader.py            # 配置加载
│   │   ├── file_handler.py             # 文件处理
│   │   ├── image_processor.py          # 图像处理
│   │   └── audio_processor.py          # 音频处理
│   │
│   ├── components/                     # 可复用组件
│   │   ├── drawing_canvas.py
│   │   ├── voice_interaction.py
│   │   ├── music_player.py
│   │   ├── video_player.py
│   │   └── progress_tracker.py
│   │
│   └── assets/                         # 静态资源
│       ├── css/
│       ├── js/
│       ├── images/
│       └── sounds/
│
├── data/                               # 数据存储
│   ├── artworks/                       # 作品存储
│   ├── analytics/                      # 分析数据
│   └── cache/                          # 缓存数据
│
├── .streamlit/                         # Streamlit配置
│   └── config.toml
│
├── docs/                               # 文档
│   └── presentations/
│
├── requirements.txt                    # Python依赖
├── .env.example                        # 环境变量模板
├── check_setup.py                      # 配置检查脚本
├── run.sh                              # Linux/macOS启动脚本
├── run.bat                             # Windows启动脚本
├── README.md                           # 项目说明（本文件）
├── DEVELOPMENT.md                      # 详细开发指南
├── QUICK_START.md                      # 快速安装使用指南
└── PROJECT_COMPLETION.md               # 项目完成总结
```

---

## 🛠️ 技术栈

### 前端
- **框架**: Streamlit 1.30+
- **绘画**: HTML5 Canvas
- **样式**: CSS3 + Streamlit内置主题

### AI/ML
- **视觉理解**: Qwen-VL-Chat (阿里云DashScope)
- **文本理解**: Qwen3-Omini-Flash
- **语音合成**: TTS (Qwen3-Omini-Flash)
- **音乐生成**: Coze工作流
- **视频生成**: 火山引擎Seedance

### 后端
- **语言**: Python 3.8+
- **数据处理**: NumPy, Pillow, OpenCV
- **音频处理**: Wave, SciPy
- **HTTP**: Requests

### 存储
- **本地存储**: 文件系统
- **数据格式**: JSON, PNG, WAV, MP3

---

## � 使用指南

### 🎨 智能画板

1. 在左侧菜单选择"🎨 智能画板"
2. 在画布上自由绘画
3. 使用左侧工具调整笔刷设置
4. 点击"✅ 完成作品"让小精灵分析
5. 查看分析结果和语音反馈

**功能**:
- 🖌️ 多色笔刷选择
- ↶↷ 撤销/重做
- 🗑️ 清空画板
- 🧚 小精灵语音反馈
- 📊 五维度AI分析

### 🧚 作品工坊

1. 在左侧菜单选择"🧚 作品工坊"
2. 上传已有的图片
3. 选择功能:
   - **📊 分析作品** - 多模态AI分析
   - **🎵 生成音乐** - AI创作配乐
   - **🎬 生成视频** - 首尾帧动画

**功能**:
- 📤 图片上传和预览
- 🎵 Coze音乐生成工作流
- 🎬 火山引擎视频生成
- 💾 结果下载

### ⚙️ 设置中心

- 👤 个人信息管理
- 🎨 主题和显示设置
- 🔊 语音和音乐设置
- ♿ 无障碍设置
- 📊 数据管理和存储统计

---

## 🚨 常见问题

### Q: 运行时出现"模块未找到"错误

**解决**:
```bash
# 重新安装依赖
pip install -r requirements.txt --upgrade

# 或者查看具体缺少哪个模块
pip list
```

### Q: 画板不显示或无法绘画

**解决**:
- 尝试使用不同浏览器（推荐Chrome/Edge）
- 清除浏览器缓存
- 检查JavaScript是否启用
- 检查浏览器控制台的错误信息

### Q: API调用超时

**解决**:
- 检查网络连接
- 验证API密钥是否正确
- 检查API配额是否用尽
- 尝试使用代理或VPN（如果有地理限制）

### Q: 内存占用过高

**解决**:
- 关闭其他程序释放内存
- 清除缓存目录: `data/cache/`
- 减少保存的作品数量

### Q: 生成的音乐/视频质量不好

**解决**:
- 确保上传的图片质量良好
- 图片大小在1-10MB之间
- 图片包含清晰的主题和元素

---

## 📊 部署选项

### 本地部署
```bash
streamlit run src/app.py
```

### Hugging Face Spaces部署
1. Fork项目到GitHub
2. 在Hugging Face Spaces创建新Space
3. 选择Streamlit SDK
4. 连接GitHub仓库
5. 在Settings中添加Secret（API密钥）

### Docker部署
```bash
docker build -t dreamweaver-ai .
docker run -p 8501:8501 -e DASHSCOPE_API_KEY=xxx dreamweaver-ai
```

---

## 📚 文档

- [快速安装和使用指南](QUICK_START.md) - 5分钟快速开始
- [详细开发指南](DEVELOPMENT.md) - 完整开发文档
- [项目完成总结](PROJECT_COMPLETION.md) - 交付清单和功能说明

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. **报告Bug**: 在Issues中提交
2. **功能建议**: 使用Feature Request模板
3. **代码贡献**: Fork后提交Pull Request
4. **文档改进**: 直接修改文档文件

---

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件

---

## 🙏 致谢

感谢以下支持：

- **阿里云DashScope** - 提供Qwen系列模型
- **Coze平台** - 工作流编排能力
- **火山引擎** - 视频生成API
- **Streamlit团队** - 优秀的前端框架
- **所有测试者和反馈者** - 帮助完善产品

---

## 📞 联系方式

- 📧 Email: contact@dreamweaver.ai
- 🐛 Bug Report: GitHub Issues
- 💡 Feature Request: GitHub Discussions

---

**让科技有温度，让教育更公平** ❤️

*绘梦精灵 v1.0.0 | © 2025 DreamWeaver Project*

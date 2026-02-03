# 🎨 绘梦精灵 (DreamWeaver AI) - 开发完成说明

## 📋 项目概况

**绘梦精灵**是一个基于Streamlit和多模态大模型的儿童创造力启发与情感陪伴系统。通过"视觉-听觉-动态影像"全感官反馈，帮助孩子跨越表达障碍，实现从"被动绘画"到"主动创作故事"的转变。

### ✨ 核心功能

#### 1️⃣ 智能画板系统
- **自由绘画**：HTML5 Canvas实现的高性能画板
- **笔刷工具**：多种颜色、粗细、类型选择
- **编辑工具**：撤销/重做/清空功能
- **小精灵陪伴**：实时语音反馈和创意建议

#### 2️⃣ AI小精灵系统
- **实时交互**：根据绘画内容生成个性化反馈
- **语音合成**：使用Qwen-Omini-Flash生成儿童友好的语音
- **五维度分析**：
  - 🎯 主题分析 - 理解孩子在画什么
  - 🎨 色彩分析 - 色彩心理学解读
  - 📐 构图分析 - 艺术启蒙
  - 💭 情感分析 - 理解孩子内心
  - 📊 发展阶段评估 - 教育价值核心

#### 3️⃣ 作品工坊系统
- **音乐生成**：将画作转换为配乐（Coze工作流）
- **AI点评**：生成专业的语音评价
- **视频生成**：首尾帧魔法动画（火山引擎）
- **多格式导出**：支持图片、音乐、视频下载

## 🚀 快速开始

### 1. 环境配置

```bash
# 克隆或进入项目目录
cd DreamWeaver

# 创建Python虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入以下API密钥：
```

需要的API配置：

```env
# 阿里云DashScope (Qwen Omini) - 必需
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Coze (音乐生成工作流) - 必需
COZE_API_TOKEN=your_coze_api_token_here
COZE_BOT_ID=your_bot_id_here
COZE_WORKFLOW_ID=7601786439168229386

# 火山引擎 (视频生成) - 可选
HUOSHAN_ACCESS_KEY=your_access_key_here
HUOSHAN_SECRET_KEY=your_secret_key_here
```

### 3. 运行应用

```bash
streamlit run src/app.py
```

应用将在 `http://localhost:8501` 打开

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
│   ├── components/                     # 可复用组件（预留）
│   │   ├── drawing_canvas.py
│   │   ├── voice_interaction.py
│   │   ├── music_player.py
│   │   ├── video_player.py
│   │   └── progress_tracker.py
│   │
│   └── assets/                         # 静态资源（预留）
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
├── README.md                           # 项目说明（本文件）
├── .env.example                        # 环境变量模板
└── 绘梦精灵.md                         # 完整PRD文档
```

## 🎯 主要功能使用说明

### 智能画板（2_🎨_智能画板.py）

1. **绘画**：在canvas上自由绘画
2. **工具**：
   - 调整笔刷颜色和粗细
   - 撤销/重做/清空
   - 查看统计数据
3. **完成作品**：点击"完成作品"，小精灵会：
   - 分析你的画作
   - 生成语音反馈
   - 显示详细的五维度分析

### 作品工坊（3_🧚_加工工厂.py）

1. **上传作品**：选择已有的图片
2. **功能选择**：
   - 📊 分析作品 - 多模态分析
   - 🎵 生成音乐 - Coze工作流
   - 🎬 生成视频 - 火山引擎
3. **下载结果**：导出音乐、视频或分析报告

### 设置中心（5_⚙️_设置中心.py）

- 👤 个人信息管理
- 🎨 界面主题和显示设置
- 📊 数据管理和存储统计
- ♿ 无障碍设置

## 🔌 API集成说明

### 1. Qwen-Omini-Flash (多模态分析 + 语音)

**文件**: `src/services/multimodal_service.py`, `src/services/voice_service.py`

```python
# 使用示例
service = MultimodalService()
analysis = service.analyze_drawing(image_bytes, drawing_info)
spirit_feedback = service.generate_spirit_feedback(image_bytes, drawing_info)

voice_service = VoiceService()
audio = voice_service.text_to_speech("你的反馈文本")
```

### 2. Coze工作流 (音乐生成)

**文件**: `src/services/coze_service.py`

```python
# 使用示例
coze_service = CozeService()
file_id = coze_service.upload_image_to_coze(image_bytes)
result = coze_service.generate_music_from_image(file_id)
# 返回: {'status': 'success', 'music_url': '...'}
```

### 3. 火山引擎 (视频生成)

**文件**: `src/services/video_service.py`

```python
# 使用示例
video_service = VideoService()
result = video_service.create_transition_video(first_frame_url, last_frame_url)
status = video_service.query_video_task(task_id)
```

## 💾 数据存储

### 目录结构

```
data/
├── artworks/
│   └── {user_id}/
│       ├── original/       # 原始图片
│       ├── uploaded/       # 上传的图片
│       ├── audio/          # 生成的音频
│       └── metadata/       # 作品元数据(JSON)
├── cache/                  # 临时缓存
└── temp/                   # 临时文件
```

## 🎨 UI/UX特点

### 儿童友好设计
- ✅ 简洁清晰的界面
- ✅ 大型按钮和易点击目标
- ✅ 鲜艳的颜色和图标
- ✅ 趣味提示和鼓励语言

### 无障碍支持
- ✅ 键盘导航
- ✅ 高对比度模式
- ✅ 简化界面选项
- ✅ 语音反馈

## 🧪 测试建议

### 功能测试清单

- [ ] 画板绘画功能
- [ ] 笔刷工具（颜色、粗细）
- [ ] 撤销/重做功能
- [ ] 作品分析功能
- [ ] 语音反馈生成
- [ ] 音乐生成
- [ ] 视频生成
- [ ] 文件保存和加载
- [ ] 设置保存
- [ ] 响应式设计

### 性能测试

- 大画布绘画流畅度
- API调用响应时间
- 文件加载速度
- 内存使用情况

## 🚨 常见问题

### Q: 画板没有显示
**A**: 确保浏览器支持HTML5 Canvas，尝试刷新页面或换浏览器

### Q: API调用超时
**A**: 检查网络连接和API密钥配置。大型文件处理可能需要更长时间。

### Q: 音乐/视频生成失败
**A**:
- 检查文件大小（推荐<10MB）
- 确认API配额未用尽
- 查看日志获取详细错误信息

### Q: 文件保存在哪里
**A**: 所有文件保存在`data/artworks/{user_id}/`目录下

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

## 📚 文档参考

- [完整PRD文档](绘梦精灵.md)
- [Coze工作流示例](coze工作流调用示例.md)
- [API文档](docs/api_docs.md)（待完成）

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License - 详见LICENSE文件

## 📞 联系方式

- 📧 Email: contact@dreamweaver.ai
- 🐛 Bug Report: GitHub Issues
- 💡 Feature Request: GitHub Discussions

---

**让科技有温度，让教育更公平** ❤️

Made with ❤️ for children everywhere

*绘梦精灵 v1.0.0 | © 2025 DreamWeaver Project*

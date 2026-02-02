# 🚀 快速安装和使用指南

## 一、系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.8+
- **内存**: 至少2GB RAM
- **网络**: 需要互联网连接（用于API调用）

## 二、安装步骤

### 方式一：一键启动（推荐）

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

### 方式二：手动安装

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

## 三、API密钥获取

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

## 四、使用指南

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

## 五、常见问题解决

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

## 六、故障排查

### 启动检查脚本

```bash
python check_setup.py
```

输出示例:
```
✅ Python 3.10 - 正常
✅ streamlit - 已安装
✅ dashscope - 已安装
✅ src/ - 存在
✅ .env 文件存在
✅ DASHSCOPE_API_KEY - 已配置
```

### 查看日志

Streamlit应用的日志显示在控制台。如遇到问题，请检查：

1. 控制台输出是否有错误信息
2. 浏览器开发者工具（F12）中的错误
3. `data/` 目录下是否有日志文件

### 联系支持

如遇到问题无法解决，请：

1. 检查 [GitHub Issues](https://github.com/your-repo/issues)
2. 提交新Issue，包含：
   - 操作系统和Python版本
   - 完整的错误信息
   - 复现步骤
   - 系统配置信息

## 七、性能优化建议

### 1. 缓存配置

Streamlit会自动缓存服务，首次加载可能较慢。

```python
# 查看缓存大小
du -sh ~/.streamlit/
```

### 2. 图片优化

- 推荐图片大小：800x600px
- 推荐文件大小：<5MB
- 格式：JPG或PNG

### 3. 并发控制

- 避免同时上传过多大文件
- 等待前一个操作完成后再进行下一个

## 八、升级和更新

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 重启应用
streamlit run src/app.py
```

## 九、卸载

```bash
# 删除虚拟环境
rm -rf venv

# 删除缓存数据
rm -rf data/
rm -rf .streamlit/cache/

# 删除项目目录（可选）
rm -rf DreamWeaver/
```

## 十、开发者信息

- **项目名称**: 绘梦精灵 (DreamWeaver AI)
- **版本**: v1.0.0
- **比赛**: 2025"小有可为"公益黑客松
- **开源许可**: MIT

---

**需要帮助？** 📞

- 📧 Email: contact@dreamweaver.ai
- 🐛 Bug Report: GitHub Issues
- 💡 Feature Request: GitHub Discussions

**让科技有温度，让教育更公平** ❤️

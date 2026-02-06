import streamlit as st
import os
import base64
from utils.session_manager import init_session_state, clear_session
from utils.file_handler import FileHandler

st.set_page_config(
    page_title="设置中心",
    page_icon="⚙️",
    layout="wide"
)

init_session_state()
file_handler = FileHandler()

# 添加背景图片
script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
bg_img_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "背景01.png"))

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if os.path.exists(bg_img_path):
    bg_base64 = get_base64_image(bg_img_path)
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 16px;
        padding: 2rem;
    }}
    """
else:
    bg_css = ""

# 按钮蓝色样式
button_css = """
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #357ABD;
        color: white;
    }
"""

st.markdown(f"<style>{bg_css}{button_css}</style>", unsafe_allow_html=True)

st.markdown("# ⚙️ 设置中心")

# 创建选项卡
tab1, tab2, tab3, tab4 = st.tabs(["👤 个人信息", "🎨 界面设置", "📊 数据管理", "ℹ️ 关于应用"])

with tab1:
    st.markdown("## 个人信息")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("用户ID", st.session_state.user_id[:12] + "...")
        created_at = st.text_input("用户名 (可选)", value="小画家", key="username")

    with col2:
        st.metric("创建时间", "2025-02-02")
        age_group = st.selectbox(
            "年龄段",
            ["4-6岁", "6-8岁", "8-10岁", "10岁以上"],
            key="age_group"
        )

    st.divider()

    st.markdown("### 个性化设置")

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.settings['voice_enabled'] = st.checkbox(
            "🔊 启用语音反馈",
            value=st.session_state.settings['voice_enabled']
        )

        voice_option = st.selectbox(
            "选择小精灵的声音",
            ["👧 豆豆(儿童女声)", "🧒 晓晓(儿童男声)", "🎤 青风(少年男声)"],
            key="spirit_voice"
        )

    with col2:
        st.session_state.settings['bgm_enabled'] = st.checkbox(
            "🎵 启用背景音乐",
            value=st.session_state.settings['bgm_enabled']
        )

        bgm_volume = st.slider(
            "背景音乐音量",
            min_value=0,
            max_value=100,
            value=50,
            key="bgm_volume"
        )

with tab2:
    st.markdown("## 界面设置")

    st.markdown("### 主题选择")

    theme = st.radio(
        "选择应用主题",
        ["🌞 亮色模式", "🌙 暗色模式", "🎨 自定义"],
        index=0 if st.session_state.settings['theme'] == 'light' else 1,
        key="theme_selection"
    )

    if "亮色" in theme:
        st.session_state.settings['theme'] = 'light'
    elif "暗色" in theme:
        st.session_state.settings['theme'] = 'dark'
    else:
        st.session_state.settings['theme'] = 'custom'

    st.divider()

    st.markdown("### 显示设置")

    col1, col2 = st.columns(2)

    with col1:
        font_size = st.slider(
            "文字大小",
            min_value=12,
            max_value=20,
            value=16,
            key="font_size"
        )

        animation_speed = st.selectbox(
            "动画速度",
            ["🐢 慢速", "⚡ 正常", "🚀 快速"],
            key="animation_speed"
        )

    with col2:
        contrast_level = st.selectbox(
            "对比度",
            ["正常", "高对比度", "色盲模式"],
            key="contrast"
        )

        simplify_ui = st.checkbox(
            "简化界面（特殊儿童适配）",
            key="simplify_ui",
            help="减少视觉干扰，简化交互"
        )

    st.divider()

    st.markdown("### 无障碍设置")

    col1, col2, col3 = st.columns(3)

    with col1:
        enable_keyboard = st.checkbox(
            "⌨️ 启用键盘导航",
            value=True,
            key="keyboard_nav"
        )

    with col2:
        enable_voice_control = st.checkbox(
            "🎤 启用语音控制",
            value=False,
            key="voice_control",
            help="使用语音指令控制应用"
        )

    with col3:
        enable_screen_reader = st.checkbox(
            "👂 启用屏幕阅读器",
            value=False,
            key="screen_reader"
        )

with tab3:
    st.markdown("## 📊 数据管理")

    # 存储统计
    st.markdown("### 存储使用情况")

    storage_size = file_handler.get_storage_size(st.session_state.user_id)
    storage_formatted = file_handler.format_file_size(storage_size)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("已使用空间", storage_formatted)

    with col2:
        st.metric("总配额", "1 GB")

    with col3:
        usage_percent = (storage_size / (1024 * 1024 * 1024)) * 100
        st.metric("使用率", f"{usage_percent:.1f}%")

    st.progress(min(usage_percent / 100, 1.0))

    st.divider()

    st.markdown("### 数据操作")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 导出所有数据", use_container_width=True):
            st.info("数据导出功能开发中...")

    with col2:
        if st.button("🔄 同步数据", use_container_width=True):
            st.success("数据已同步！")

    with col3:
        if st.button("🗑️ 清空缓存", use_container_width=True):
            st.success("缓存已清空！")

    st.divider()

    st.markdown("### 高级选项")

    if st.checkbox("显示高级选项", key="show_advanced"):
        st.warning("⚠️ 请谨慎操作以下功能")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 重置所有设置", use_container_width=True):
                if st.button("确认重置？", key="confirm_reset"):
                    clear_session()
                    st.success("所有设置已重置！")
                    st.rerun()

        with col2:
            if st.button("🗑️ 删除所有作品", use_container_width=True):
                if st.button("确认删除？", key="confirm_delete"):
                    st.warning("所有作品将被永久删除！此操作无法撤销。")

with tab4:
    st.markdown("## ℹ️ 关于应用")

    st.markdown("""
    ### 🎨 绘梦精灵 (DreamWeaver AI)
    **儿童多感官创造力启发系统**

    #### 项目信息
    - **版本**: v1.0.0
    - **发布日期**: 2025年2月
    - **比赛**: 2025"小有可为"公益黑客松
    - **主题**: AI For Good | 赋能教育公平

    #### 核心使命
    让每个孩子的画都能被看见、被听见、被记住。
    我们致力于：
    - 🌍 缩小城乡美育资源差距
    - ♿ 为特殊儿童提供表达出口
    - 🎨 激发每个孩子的创造力

    #### 技术栈
    - **前端**: Streamlit + HTML5 Canvas
    - **AI模型**: Qwen-Omini-Flash (阿里云)
    - **音乐生成**: Coze工作流
    - **视频生成**: 火山引擎Seedance
    - **后端**: Python 3.10+

    #### 支持的平台
    - 💻 Windows / macOS / Linux
    - 📱 iPad / Android平板
    - 🌐 在线Web版本

    #### 隐私政策
    - 我们不会收集个人隐私信息
    - 所有作品数据都存储在本地
    - 不会与第三方共享你的数据

    #### 开源许可
    本项目采用 **MIT License**
    """)

    st.divider()

    st.markdown("### 🔗 相关链接")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        [GitHub 项目](https://github.com)

        [提交问题](https://github.com/issues)

        [查看文档](https://docs)
        """)

    with col2:
        st.markdown("""
        [参赛方案](https://docs/proposal)

        [演示视频](https://video)

        [用户手册](https://manual)
        """)

    with col3:
        st.markdown("""
        [联系我们](mailto:contact@example.com)

        [意见反馈](https://feedback)

        [赞助支持](https://sponsor)
        """)

    st.divider()

    st.markdown("### 👥 致谢")

    st.markdown("""
    感谢以下组织和个人的支持：

    - 🤝 **ModelScope魔搭社区** - 提供优质国产模型
    - 🚀 **火山引擎** - 视频生成API支持
    - 🎵 **Coze平台** - 工作流编排能力
    - 💙 **Streamlit** - 优秀的前端框架
    - 👨‍👩‍👧‍👦 **所有参与测试的老师和学生**

    ---

    **让科技有温度，让教育更公平** ❤️

    Made with ❤️ for children everywhere
    """)

    st.divider()

    # 页脚
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📧 联系开发者", use_container_width=True):
            st.info("contact@dreamweaver.ai")

    with col2:
        if st.button("⭐ GitHub Stars", use_container_width=True):
            st.info("给我们一个Star吧！")

    with col3:
        if st.button("🐛 报告Bug", use_container_width=True):
            st.info("https://github.com/issues")

st.divider()

# 应用信息
st.caption("绘梦精灵 v1.0.0 | © 2025 DreamWeaver Project | 保留所有权利")

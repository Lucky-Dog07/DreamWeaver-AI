import streamlit as st
from utils.session_manager import init_session_state
from utils.config_loader import ConfigLoader

# 页面配置
st.set_page_config(
    page_title="绘梦精灵 - AI儿童创意启发系统",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
init_session_state()

# 自定义CSS样式
st.markdown("""
<style>
    /* 全局样式 */
    body {
        background-color: #F8F9FA;
        font-family: 'ZCOOL XiaoWei', 'Noto Sans SC', sans-serif;
    }

    /* 主容器 */
    .main {
        max-width: 1400px;
        margin: 0 auto;
    }

    /* 标题样式 */
    h1 {
        font-family: 'Ma Shan Zheng', cursive;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 30px;
    }

    /* 按钮样式 */
    .stButton > button {
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        background-color: #4A90E2;
        color: white;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #2E5C8A;
        transform: scale(1.05);
    }

    /* 卡片样式 */
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* 输入框样式 */
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #E0E0E0;
        padding: 10px;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border: 2px solid #4A90E2;
    }
</style>
""", unsafe_allow_html=True)

# 加载应用配置
config = ConfigLoader.get_app_settings()

# 侧边栏配置
with st.sidebar:
    st.markdown("## ⚙️ 应用设置")

    # 用户信息
    st.info(f"👤 用户ID: {st.session_state.user_id[:8]}...")

    # 主题设置
    theme = st.radio(
        "选择主题",
        ["🌞 亮色", "🌙 暗色"],
        help="选择您喜欢的界面主题"
    )
    st.session_state.settings['theme'] = 'light' if theme == "� 亮色" else 'dark'

    # 声音设置
    st.session_state.settings['voice_enabled'] = st.checkbox(
        "🔊 启用语音反馈",
        value=True,
        help="小精灵的语音提示"
    )

    # 背景音乐设置
    st.session_state.settings['bgm_enabled'] = st.checkbox(
        "🎵 启用背景音乐",
        value=True,
        help="轻松舒适的背景音乐"
    )

    st.divider()
    st.markdown("### 📚 帮助与反馈")

    if st.button("📖 使用指南", use_container_width=True):
        st.session_state.show_help = True

    if st.button("🐛 报告问题", use_container_width=True):
        st.session_state.show_bug_report = True

    st.divider()
    st.caption(f"版本: {config['version']}")

# 主页面内容
st.markdown("# 🎨 绘梦精灵")
st.markdown("*让每个孩子的画都能被看见、被听见、被记住*")

# 创建三列布局展示两种工作方式
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🎨 智能画板</h3>
        <p>在画板上自由绘画，小精灵会实时陪伴与反馈</p>
        <ul>
            <li>🖌️ 自由创作</li>
            <li>🧚 AI小精灵实时陪伴</li>
            <li>💬 语音互动反馈</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("进入智能画板 →", use_container_width=True, key="btn_canvas"):
        st.switch_page("pages/2_🎨_智能画板.py")

with col2:
    st.markdown("""
    <div class="card">
        <h3>🧚 作品工坊</h3>
        <p>上传已有图片，AI为您生成音乐、点评和视频</p>
        <ul>
            <li>🎵 AI音乐生成</li>
            <li>📝 智能点评</li>
            <li>🎬 魔法视频变身</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("进入作品工坊 →", use_container_width=True, key="btn_workshop"):
        st.switch_page("pages/3_🧚_加工工厂.py")

st.divider()

# 功能介绍区域
st.markdown("## ✨ 功能特色")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    ### � 精准陪伴
    小精灵会根据孩子的绘画内容实时反馈，
    用有趣的语言猜测和鼓励创作。
    """)

with feature_col2:
    st.markdown("""
    ### 🎵 多模态体验
    将画作转换为音乐、视频和文字点评，
    让创意用多种方式绽放。
    """)

with feature_col3:
    st.markdown("""
    ### 📊 成长记录
    记录每个孩子的创意之旅，
    形成专属的成长档案。
    """)

st.divider()

# 页脚
st.markdown("""
---
<div style="text-align: center; color: #666;">
    <p>💝 为乡村和特殊儿童赋能 | 🏆 2025"小有可为"公益黑客松参赛项目</p>
    <p style="font-size: 12px;">让科技有温度，让教育更公平 ❤️</p>
</div>
""", unsafe_allow_html=True)

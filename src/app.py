import os
import sys

# 确保模块路径正确
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import streamlit as st
import base64
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

# 获取背景图片路径并转换为base64
script_dir = os.path.dirname(__file__)
bg_img_path = os.path.normpath(os.path.join(script_dir, "..", "assets", "背景.png"))

def get_base64_image(image_path):
    """将图片转换为base64编码"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

bg_base64 = get_base64_image(bg_img_path)

# 自定义CSS样式（含背景图片）
if bg_base64:
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* 让内容区域有半透明白色背景，提高可读性 */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 0 2rem 2rem 2rem;
        margin-top: -12rem;
    }}
    
    /* 侧边栏半透明效果 */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.9);
    }}
    """
else:
    bg_css = ""

st.markdown(f"""
<style>
    {bg_css}
    
    /* 全局样式 */
    body {{
        font-family: 'ZCOOL XiaoWei', 'Noto Sans SC', sans-serif;
    }}

    /* 主容器 */
    .main {{
        max-width: 1400px;
        margin: 0 auto;
    }}

    /* 标题样式 */
    h1 {{
        font-family: 'Ma Shan Zheng', cursive;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 30px;
    }}

    /* 按钮样式 */
    .stButton > button {{
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        background-color: #4A90E2;
        color: white;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #2E5C8A;
        transform: scale(1.05);
    }}

    /* 卡片样式 */
    .card {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}

    /* 首页功能卡片：固定宽高比 + 最小高度，放大页面时高度不缩水 */
    .card-img-wrap {{
        aspect-ratio: 4/3;
        min-height: 220px;
        width: 100%;
        overflow: hidden;
        border-radius: 12px;
    }}
    .card-img-wrap img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }}

    /* 输入框样式 */
    .stTextInput input, .stTextArea textarea {{
        border-radius: 8px;
        border: 2px solid #E0E0E0;
        padding: 10px;
    }}

    .stTextInput input:focus, .stTextArea textarea:focus {{
        border: 2px solid #4A90E2;
    }}
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
    st.session_state.settings['theme'] = 'light' if theme == "🌞 亮色" else 'dark'

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
# 获取角色图片路径
script_dir = os.path.dirname(__file__)
img_path = os.path.normpath(os.path.join(script_dir, "..", "assets", "球球角色透明背景.png"))
title_img_path = os.path.normpath(os.path.join(script_dir, "..", "assets", "绘梦精灵.png"))

# 读取角色图片并转为base64
char_base64 = get_base64_image(img_path) if os.path.exists(img_path) else None
title_img_base64 = get_base64_image(title_img_path) if os.path.exists(title_img_path) else None

# 标题区域 - 文字居中，图片在右侧
if char_base64 and title_img_base64:
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; gap: 8px;">
        <div style="text-align: center; display: flex; flex-direction: column; align-items: center; margin-left: 280px;">
            <img src="data:image/png;base64,{title_img_base64}" style="height: 360px; width: auto; margin: 0 auto 10px auto;">
            <p style="color: #666; font-size: 1.2em;">让每个孩子的画都能被看见、被听见、被记住</p>
        </div>
        <img src="data:image/png;base64,{char_base64}" style="width: 300px; height: auto;">
    </div>
    """, unsafe_allow_html=True)
elif title_img_base64:
    st.markdown(f"""
    <div style="text-align: center; display: flex; flex-direction: column; align-items: center; margin-left: 280px;">
        <img src="data:image/png;base64,{title_img_base64}" style="height: 360px; width: auto; margin: 0 auto 10px auto;">
        <p style="color: #666; font-size: 1.2em;">让每个孩子的画都能被看见、被听见、被记住</p>
    </div>
    """, unsafe_allow_html=True)
elif char_base64:
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; gap: 8px;">
        <div style="text-align: center; display: flex; flex-direction: column; align-items: center;">
            <h1 style="margin-bottom: 10px; font-size: 3em;">绘梦精灵</h1>
            <p style="color: #666; font-size: 1.2em;">让每个孩子的画都能被看见、被听见、被记住</p>
        </div>
        <img src="data:image/png;base64,{char_base64}" style="width: 300px; height: auto;">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="margin-bottom: 10px; font-size: 3em;">绘梦精灵</h1>
        <p style="color: #666; font-size: 1.2em;">让每个孩子的画都能被看见、被听见、被记住</p>
    </div>
    """, unsafe_allow_html=True)

# 创建三列布局展示两种工作方式
col1, col2 = st.columns(2)

with col1:
    card1_img_path = os.path.normpath(os.path.join(script_dir, "..", "assets", "背景1.png"))
    card1_base64 = get_base64_image(card1_img_path)
    if card1_base64:
        st.markdown(f"""
        <div class="card" style="padding: 0;">
            <div class="card-img-wrap" style="border: 3px solid #FFD700;">
                <img src="data:image/png;base64,{card1_base64}" alt="智能画板">
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="card"></div>', unsafe_allow_html=True)

    if st.button("进入智能画板 →", use_container_width=True, key="btn_canvas"):
        try:
            st.switch_page("pages/2_🎨_智能画板.py")
        except Exception:
            st.info("👈 请从左侧边栏选择「智能画板」进入")

with col2:
    card2_img_path = os.path.normpath(os.path.join(script_dir, "..", "assets", "背景2.png"))
    card2_base64 = get_base64_image(card2_img_path)
    if card2_base64:
        st.markdown(f"""
        <div class="card" style="padding: 0;">
            <div class="card-img-wrap" style="border: 3px solid #4A90E2;">
                <img src="data:image/png;base64,{card2_base64}" alt="作品工坊">
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="card"></div>', unsafe_allow_html=True)

    if st.button("进入作品工坊 →", use_container_width=True, key="btn_workshop"):
        try:
            st.switch_page("pages/3_🧚_加工工厂.py")
        except Exception:
            st.info("👈 请从左侧边栏选择「加工工厂」进入")

st.divider()

# 功能介绍区域
st.markdown("## ✨ 功能特色")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    ### 🤖 精准陪伴
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

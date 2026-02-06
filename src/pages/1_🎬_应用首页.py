import streamlit as st
from utils.session_manager import init_session_state
import os
import base64

init_session_state()

def get_base64_image(image_path):
    """将图片转换为 base64 编码"""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

st.set_page_config(page_title="首页", page_icon="🎬", layout="wide")

# 构建背景图片路径（用于本页底层背景）
script_dir = os.path.dirname(__file__)
bg_img_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "背景01.png"))
bg_base64 = get_base64_image(bg_img_path) if os.path.exists(bg_img_path) else None

if bg_base64:
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
        border-radius: 20px;
        padding: 2rem;
    }}
    """
else:
    bg_css = """
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    """

# 自定义 CSS 样式，打造童趣感
st.markdown(f"""
<style>
    /* 引入圆润字体 */
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

    {bg_css}

    /* 标题样式 */
    .hero-title {{
        font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 3.5rem !important;
        color: #FF6B6B;
        text-align: center;
        margin-top: -2rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}

    .hero-subtitle {{
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }}

    /* 卡片容器 */
    .feature-container {{
        display: flex;
        justify-content: space-around;
        gap: 2rem;
        margin-bottom: 3rem;
    }}

    /* 功能卡片样式 */
    .feature-card {{
        background: white;
        border-radius: 30px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 4px solid transparent;
        flex: 1;
        cursor: pointer;
    }}

    .feature-card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }}

    .card-canvas:hover {{ border-color: #FFD93D; }}
    .card-workshop:hover {{ border-color: #6BCB77; }}

    .card-icon {{
        font-size: 4rem;
        margin-bottom: 1rem;
    }}

    .card-title {{
        font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 1.8rem;
        color: #333;
        margin-bottom: 1rem;
    }}

    .card-desc {{
        color: #666;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        min-height: 80px;
    }}

    /* 亮点网格 */
    .highlight-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}

    .highlight-item {{
        background: rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 2px dashed #DDD;
    }}

    .highlight-emoji {{ font-size: 2rem; margin-bottom: 0.5rem; }}
    .highlight-text {{ font-weight: bold; color: #444; }}

    /* 隐藏 Streamlit 默认按钮样式，自定义按钮容器 */
    div.stButton > button {{
        width: 100%;
        border-radius: 20px !important;
        border: none !important;
        padding: 0.8rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.2s !important;
        background-color: #4A90E2 !important;
        color: white !important;
    }}

    div.stButton > button:hover {{
        opacity: 0.9;
        transform: scale(1.02);
    }}

</style>
""", unsafe_allow_html=True)

# 顶部欢迎区
# 构建角色图片和标题图片路径
img_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "球球角色透明背景.png"))
welcome_title_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "欢迎来到绘梦精灵.png"))
welcome_title_base64 = get_base64_image(welcome_title_path) if os.path.exists(welcome_title_path) else None

# 功能卡片 / 装饰图片路径
canvas_card_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "背景1.png"))
canvas_card_base64 = get_base64_image(canvas_card_path) if os.path.exists(canvas_card_path) else None
workshop_card_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "背景2.png"))
workshop_card_base64 = get_base64_image(workshop_card_path) if os.path.exists(workshop_card_path) else None
artist_bg_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "艺术家背景.png"))
artist_bg_base64 = get_base64_image(artist_bg_path) if os.path.exists(artist_bg_path) else None
zero_bg_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "0门槛背景.png"))
zero_bg_base64 = get_base64_image(zero_bg_path) if os.path.exists(zero_bg_path) else None
vis_bg_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "视听背景.png"))
vis_bg_base64 = get_base64_image(vis_bg_path) if os.path.exists(vis_bg_path) else None
companion_bg_path = os.path.normpath(os.path.join(script_dir, "..", "..", "assets", "陪伴背景.png"))
companion_bg_base64 = get_base64_image(companion_bg_path) if os.path.exists(companion_bg_path) else None

# 使用列布局显示标题和角色图片
col_title, col_img = st.columns([3, 1])

with col_title:
    if welcome_title_base64:
        st.markdown(
            f'<div style="text-align: center;"><img src="data:image/png;base64,{welcome_title_base64}" style="height: 600px; width: auto; display: inline-block; margin-left: 80px;" alt="欢迎来到绘梦精灵" /></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<h1 class="hero-title">欢迎来到绘梦精灵</h1>', unsafe_allow_html=True)

with col_img:
    if os.path.exists(img_path):
        st.image(img_path, width=380)

st.markdown('<p class="hero-subtitle">在这里，每一片云朵都能变成你的画笔，每一颗星星都能讲述你的故事</p>', unsafe_allow_html=True)

# 功能展示区
col1, col2 = st.columns(2)

with col1:
    if canvas_card_base64:
        st.markdown(f"""
        <div class="feature-card card-canvas" style="padding: 0; overflow: hidden;">
            <img src="data:image/png;base64,{canvas_card_base64}" style="width: 100%; height: auto; display: block; border-radius: 26px;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="feature-card card-canvas">
            <div class="card-icon">🎨</div>
            <div class="card-title">智能画板</div>
            <div class="card-desc">
                在画板上自由涂鸦，小精灵球球会陪你聊天，<br>
                给你创意建议，还能把你的画变魔法哦！
            </div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("开始绘画", use_container_width=True, key="home_canvas"):
        st.switch_page("pages/2_🎨_智能画板.py")

with col2:
    if workshop_card_base64:
        st.markdown(f"""
        <div class="feature-card card-workshop" style="padding: 0; overflow: hidden;">
            <img src="data:image/png;base64,{workshop_card_base64}" style="width: 100%; height: auto; display: block; border-radius: 26px;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="feature-card card-workshop">
            <div class="card-icon">🧚</div>
            <div class="card-title">作品工坊</div>
            <div class="card-desc">
                上传你画好的大作，AI工坊为你创作配乐、<br>
                专业点评，还能生成超酷的魔法视频！
            </div>
        </div>
        """, unsafe_allow_html=True)
    if st.button("开启工坊", use_container_width=True, key="home_workshop"):
        st.switch_page("pages/3_🧚_加工工厂.py")

st.markdown("---")

# 项目亮点
st.markdown('### 🌟 绘梦精灵的小秘密')
if artist_bg_base64 and zero_bg_base64 and vis_bg_base64 and companion_bg_base64:
    st.markdown(
        f"""
<div class="highlight-grid">
    <div class="highlight-item" style="padding: 0; border: none; background: transparent;">
        <img src="data:image/png;base64,{companion_bg_base64}" style="width: 100%; height: auto; display: block; border-radius: 20px;" alt="AI 伙伴全程陪伴" />
    </div>
    <div class="highlight-item" style="padding: 0; border: none; background: transparent;">
        <img src="data:image/png;base64,{vis_bg_base64}" style="width: 100%; height: auto; display: block; border-radius: 20px;" alt="视听动全方位体验" />
    </div>
    <div class="highlight-item" style="padding: 0; border: none; background: transparent;">
        <img src="data:image/png;base64,{zero_bg_base64}" style="width: 100%; height: auto; display: block; border-radius: 20px;" alt="零门槛释放想象力" />
    </div>
    <div class="highlight-item" style="padding: 0; border: none; background: transparent;">
        <img src="data:image/png;base64,{artist_bg_base64}" style="width: 100%; height: auto; display: block; border-radius: 20px;" alt="每个孩子都是艺术家" />
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
<div class="highlight-grid">
    <div class="highlight-item">
        <div class="highlight-emoji">🤖</div>
        <div class="highlight-text">AI 伙伴全程陪伴</div>
    </div>
    <div class="highlight-item">
        <div class="highlight-emoji">🎵</div>
        <div class="highlight-text">视听动全方位体验</div>
    </div>
    <div class="highlight-item">
        <div class="highlight-emoji">💝</div>
        <div class="highlight-text">零门槛释放想象力</div>
    </div>
    <div class="highlight-item">
        <div class="highlight-emoji">🏆</div>
        <div class="highlight-text">每个孩子都是艺术家</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

st.divider()

# 底部辅助信息
col_a, col_b = st.columns(2)

with col_a:
    with st.expander("❓ 常见问题"):
        st.markdown("""
        **Q: 我的作品会被保存吗？**
        A: 是的，所有作品都会被安全保存。你可以随时查看、下载或分享你的创意成果。

        **Q: 小精灵会什么？**
        A: 小精灵叫"球球"，它懂艺术、懂故事、懂鼓励。它会用5-8岁孩子能理解的语言和你交流。

        **Q: 生成音乐和视频需要多久？**
        A: 通常需要10-60秒，等待期间球球会给你有趣的提示。
        """)

with col_b:
    with st.expander("📚 学习更多"):
        st.markdown("""
        - [项目GitHub](https://github.com/yourname/dreamweaver-ai)
        - [完整PRD文档](../绘梦精灵.md)
        - [使用教程](../docs/user_manual.md)
        """)

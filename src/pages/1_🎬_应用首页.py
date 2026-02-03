import streamlit as st
from utils.session_manager import init_session_state

init_session_state()

st.set_page_config(page_title="首页", page_icon="🎬", layout="wide")

# 自定义 CSS 样式，打造童趣感
st.markdown("""
<style>
    /* 引入圆润字体 */
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

    .main {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* 标题样式 */
    .hero-title {
        font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 3.5rem !important;
        color: #FF6B6B;
        text-align: center;
        margin-top: -2rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }

    /* 卡片容器 */
    .feature-container {
        display: flex;
        justify-content: space-around;
        gap: 2rem;
        margin-bottom: 3rem;
    }

    /* 功能卡片样式 */
    .feature-card {
        background: white;
        border-radius: 30px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 4px solid transparent;
        flex: 1;
        cursor: pointer;
    }

    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }

    .card-canvas:hover { border-color: #FFD93D; }
    .card-workshop:hover { border-color: #6BCB77; }

    .card-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .card-title {
        font-family: 'ZCOOL KuaiLe', cursive;
        font-size: 1.8rem;
        color: #333;
        margin-bottom: 1rem;
    }

    .card-desc {
        color: #666;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        min-height: 80px;
    }

    /* 亮点网格 */
    .highlight-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .highlight-item {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 2px dashed #DDD;
    }

    .highlight-emoji { font-size: 2rem; margin-bottom: 0.5rem; }
    .highlight-text { font-weight: bold; color: #444; }

    /* 隐藏 Streamlit 默认按钮样式，自定义按钮容器 */
    div.stButton > button {
        width: 100%;
        border-radius: 20px !important;
        border: none !important;
        padding: 0.8rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.2s !important;
    }

    /* 针对特定按钮容器的样式 */
    .btn-container-canvas div.stButton > button {
        background-color: #FFD93D !important;
        color: #555 !important;
    }
    .btn-container-workshop div.stButton > button {
        background-color: #6BCB77 !important;
        color: white !important;
    }

    div.stButton > button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }

</style>
""", unsafe_allow_html=True)

# 顶部欢迎区
st.markdown('<h1 class="hero-title">� 欢迎来到绘梦精灵</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">在这里，每一片云朵都能变成你的画笔，每一颗星星都能讲述你的故事！🌟</p>', unsafe_allow_html=True)

# 功能展示区
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card card-canvas">
        <div class="card-icon">🎨</div>
        <div class="card-title">智能画板</div>
        <div class="card-desc">
            在画板上自由涂鸦，小精灵球球会陪你聊天，<br>
            给你创意建议，还能把你的画变魔法哦！
        </div>
        <div class="btn-container-canvas">
    """, unsafe_allow_html=True)
    if st.button("开始绘画 ✨", use_container_width=True, key="home_canvas"):
        st.switch_page("pages/2_🎨_智能画板.py")
    st.markdown('</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card card-workshop">
        <div class="card-icon">🧚</div>
        <div class="card-title">作品工坊</div>
        <div class="card-desc">
            上传你画好的大作，AI工坊为你创作配乐、<br>
            专业点评，还能生成超酷的魔法视频！
        </div>
        <div class="btn-container-workshop">
    """, unsafe_allow_html=True)
    if st.button("开启工坊 🚀", use_container_width=True, key="home_workshop"):
        st.switch_page("pages/3_🧚_加工工厂.py")
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("---")

# 项目亮点
st.markdown('### 🌟 绘梦精灵的小秘密')
st.markdown("""
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
""", unsafe_allow_html=True)

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

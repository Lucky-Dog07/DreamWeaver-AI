import os, sys
_src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _src not in sys.path: sys.path.insert(0, _src)
import streamlit as st
import uuid
import os
import base64
from datetime import datetime
from utils.session_manager import init_session_state
from utils.file_handler import FileHandler
from models.drawing_model import Artwork
from services.multimodal_service import MultimodalService
from services.voice_service import VoiceService
from services.coze_service import CozeService
from services.video_service import VideoService

st.set_page_config(
    page_title="作品工坊",
    page_icon="🧚",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()

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
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #357ABD;
        color: white;
    }
"""

st.markdown(f"<style>{bg_css}{button_css}</style>", unsafe_allow_html=True)

# 初始化服务
@st.cache_resource
def get_services():
    return {
        'multimodal': MultimodalService(),
        'voice': VoiceService(),
        'coze': CozeService(),
        'video': VideoService()
    }

services = get_services()
file_handler = FileHandler()

st.markdown("# 🧚 作品工坊")
st.markdown("*上传已有的图片，让AI为你创作音乐、点评和视频*")

# 选项卡
tab1, tab2, tab3 = st.tabs(["📤 上传作品", "🎵 音乐生成", "🎬 视频生成"])

with tab1:
    st.markdown("## 上传你的作品")

    uploaded_file = st.file_uploader(
        "选择一张图片（JPG、PNG）",
        type=["jpg", "jpeg", "png"],
        help="选择你想要处理的儿童画作"
    )

    if uploaded_file:
        st.image(uploaded_file, caption="预览", use_container_width=True)

        # 上传后的操作
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 分析作品", use_container_width=True):
                st.session_state.analyze_uploaded = True

        with col2:
            if st.button("🎵 生成音乐", use_container_width=True):
                st.session_state.generate_music_direct = True

        with col3:
            if st.button("🎬 生成视频", use_container_width=True):
                st.session_state.generate_video_direct = True

        # 处理上传的文件
        if st.session_state.get('analyze_uploaded'):
            with st.spinner("🤖 小精灵正在分析你的作品..."):
                try:
                    # 读取文件
                    image_data = uploaded_file.getvalue()

                    # 1. 上传图片到 Coze 获取 file_id
                    file_id = services['coze'].upload_image_to_coze(image_data)
                    
                    if not file_id:
                        st.error("图片上传失败")
                    else:
                        # 2. 调用 Coze 点评工作流
                        comment_result = services['coze'].generate_voice_comment(file_id)
                        
                        if comment_result.get('status') == 'success':
                            # 保存图片到本地以便展示
                            artwork_id = str(uuid.uuid4())[:8]
                            image_path = file_handler.save_image(
                                image_data,
                                st.session_state.user_id,
                                artwork_id,
                                subfolder="uploaded"
                            )

                            # 创建作品对象
                            artwork = Artwork(
                                artwork_id=artwork_id,
                                user_id=st.session_state.user_id,
                                image_path=image_path,
                                theme_analysis={'title': 'AI点评作品'},
                                color_analysis={},
                                composition_analysis={},
                                emotional_analysis={},
                                development_analysis={},
                                voice_feedback=comment_result.get('comment_text', '小精灵很喜欢你的画！')
                            )

                            st.session_state.current_artwork = artwork
                            st.session_state.show_analysis = True
                            
                            # 显示点评音频
                            if comment_result.get('comment_url'):
                                st.audio(comment_result['comment_url'])
                                
                            st.success("✅ 分析完成！")
                        else:
                            st.error(f"分析失败: {comment_result.get('error')}")

                    st.session_state.analyze_uploaded = False

                except Exception as e:
                    st.error(f"分析失败: {str(e)}")
                    st.session_state.analyze_uploaded = False

        # 处理直接生成音乐
        if st.session_state.get('generate_music_direct'):
            with st.spinner("🎵 正在为你的画生成音乐..."):
                try:
                    image_data = uploaded_file.getvalue()

                    # 上传到Coze
                    file_id = services['coze'].upload_image_to_coze(image_data)

                    if file_id:
                        result = services['coze'].generate_music_from_image(file_id)
                        if result.get('status') == 'success':
                            st.success("🎵 音乐生成成功！")
                            if result.get('emotion'):
                                st.info(f"🎨 **画作情感分析**：{result['emotion']}")
                            if result.get('music_url'):
                                st.audio(result['music_url'])
                                st.download_button(
                                    label="⬇️ 下载音乐",
                                    data=result['music_url'],
                                    file_name=f"music_{uuid.uuid4().hex[:8]}.mp3"
                                )
                        else:
                            st.error(f"音乐生成失败: {result.get('error')}")
                    else:
                        st.error("图片上传失败")
                except Exception as e:
                    st.error(f"生成音乐出错: {str(e)}")
                st.session_state.generate_music_direct = False

        # 处理直接生成视频
        if st.session_state.get('generate_video_direct'):
            with st.spinner("🎬 魔法变身中..."):
                try:
                    image_data = uploaded_file.getvalue()
                    
                    # 1. 上传到Coze
                    file_id = services['coze'].upload_image_to_coze(image_data)
                    
                    if file_id:
                        # 2. 调用 Coze 视频生成工作流
                        video_result = services['coze'].generate_video_from_image(file_id)
                        
                        if video_result.get('status') == 'success':
                            st.success("✨ 视频生成完成！")
                            if video_result.get('video_url'):
                                st.video(video_result['video_url'])
                        else:
                            st.error(f"视频生成失败: {video_result.get('error')}")
                    else:
                        st.error("图片上传失败")

                except Exception as e:
                    st.error(f"生成视频出错: {str(e)}")
                st.session_state.generate_video_direct = False

with tab2:
    st.markdown("## 🎵 音乐生成引擎")

    st.info("""
    上传你的画，AI将：
    - 分析画作的主题、色彩和情感
    - 根据分析结果创作配乐
    - 生成能够匹配画作氛围的音乐
    """)

    # 上传文件区域
    music_file = st.file_uploader(
        "上传图片生成音乐",
        type=["jpg", "jpeg", "png"],
        key="music_uploader"
    )

    if music_file:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.image(music_file, use_container_width=True)

        with col2:
            st.markdown("### 音乐风格选择")
            music_style = st.selectbox(
                "选择音乐风格",
                ["🎹 古典", "🎸 民谣", "🎹 钢琴", "🎺 爵士", "🎼 电子"],
                key="music_style"
            )

            if st.button("生成音乐", use_container_width=True, key="btn_gen_music"):
                with st.spinner("🎵 正在创作音乐..."):
                    try:
                        image_data = music_file.getvalue()
                        file_id = services['coze'].upload_image_to_coze(image_data)

                        if file_id:
                            result = services['coze'].generate_music_from_image(file_id)
                            if result.get('status') == 'success':
                                st.success("✨ 音乐生成成功！")
                                if result.get('emotion'):
                                    st.info(f"🎨 **画作情感分析**：{result['emotion']}")
                                if result.get('music_url'):
                                    st.audio(result['music_url'])

                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        st.download_button(
                                            label="⬇️ 下载音乐",
                                            data=result['music_url'],
                                            file_name=f"music_{uuid.uuid4().hex[:8]}.mp3",
                                            use_container_width=True
                                        )
                                    with col_b:
                                        if st.button("❤️ 喜欢这首音乐", use_container_width=True):
                                            st.success("已收藏！")
                            else:
                                st.error(f"生成失败: {result.get('error')}")
                        else:
                            st.error("图片上传失败")
                    except Exception as e:
                        st.error(f"出错: {str(e)}")

with tab3:
    st.markdown("## 🎬 视频生成引擎")

    st.info("""
    将你的静态画作变成魔法视频：
    - 添加动画效果
    - 配合音乐和音效
    - 生成精美的动画片段
    """)

    video_file = st.file_uploader(
        "上传图片生成视频",
        type=["jpg", "jpeg", "png"],
        key="video_uploader"
    )

    if video_file:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.image(video_file, use_container_width=True)

        with col2:
            st.markdown("### 视频设置")

            animation_style = st.selectbox(
                "选择动画风格",
                services['video'].get_animation_styles().items(),
                format_func=lambda x: x[1],
                key="anim_style"
            )

            video_duration = st.slider(
                "视频时长（秒）",
                min_value=3,
                max_value=12,
                value=8,
                key="video_duration"
            )

            video_quality = st.selectbox(
                "视频质量",
                services['video'].get_video_quality_options().items(),
                format_func=lambda x: x[1],
                key="video_quality"
            )

            if st.button("生成视频", use_container_width=True, key="btn_gen_video"):
                with st.spinner("🎬 魔法变身中..."):
                    try:
                        image_data = video_file.getvalue()
                        
                        # 1. 上传到Coze
                        file_id = services['coze'].upload_image_to_coze(image_data)
                        
                        if file_id:
                            # 2. 调用 Coze 视频生成工作流
                            video_result = services['coze'].generate_video_from_image(file_id)
                            
                            if video_result.get('status') == 'success':
                                st.success("✨ 视频生成完成！")
                                if video_result.get('video_url'):
                                    st.video(video_result['video_url'])

                                    col_x, col_y = st.columns(2)
                                    with col_x:
                                        st.download_button(
                                            label="⬇️ 下载视频",
                                            data=video_result['video_url'],
                                            file_name=f"video_{uuid.uuid4().hex[:8]}.mp4",
                                            use_container_width=True
                                        )
                                    with col_y:
                                        if st.button("❤️ 分享作品", use_container_width=True):
                                            st.success("已分享！")
                            else:
                                st.error(f"视频生成失败: {video_result.get('error')}")
                        else:
                            st.error("图片上传失败")

                    except Exception as e:
                        st.error(f"出错: {str(e)}")

st.divider()

# 显示已保存的作品
with st.expander("📚 我的作品库"):
    user_artworks = file_handler.get_user_artworks(st.session_state.user_id)

    if user_artworks:
        cols = st.columns(3)
        for idx, artwork_path in enumerate(user_artworks[:9]):
            with cols[idx % 3]:
                st.image(str(artwork_path), use_container_width=True)
                st.caption(artwork_path.stem)
    else:
        st.info("还没有保存任何作品。")

st.divider()

# 常见问题
with st.expander("❓ 常见问题"):
    st.markdown("""
    **Q: 生成音乐需要多久？**
    A: 通常需要10-30秒，取决于服务器负载。

    **Q: 生成视频需要多久？**
    A: 通常需要30-60秒。你可以在等待期间继续其他操作。

    **Q: 音乐和视频有版权问题吗？**
    A: 生成的内容是你创作的一部分，你可以自由使用和分享。

    **Q: 支持哪些图片格式？**
    A: 支持JPG和PNG格式，建议文件大小不超过10MB。
    """)

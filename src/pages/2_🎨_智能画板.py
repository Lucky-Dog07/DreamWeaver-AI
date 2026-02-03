import streamlit as st
import json
import time
import uuid
import requests
from datetime import datetime
from PIL import Image
import io
import base64
import numpy as np
from streamlit_drawable_canvas import st_canvas

from utils.session_manager import init_session_state
from utils.file_handler import FileHandler
from utils.image_processor import ImageProcessor
from models.drawing_model import DrawingData, Artwork, Stroke
from services.multimodal_service import MultimodalService
from services.voice_service import VoiceService
from services.coze_service import CozeService

st.set_page_config(
    page_title="智能画板",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_session_state()

# 初始化服务
def get_services():
    return {
        'multimodal': MultimodalService(),
        'voice': VoiceService(),
        'coze': CozeService()
    }

services = get_services()
file_handler = FileHandler()

st.markdown("# 🎨 智能画板")
st.markdown("*在画板上自由绘画，小精灵球球会实时陪伴与反馈*")

# 初始化触发计数器和互动历史
if 'last_trigger_count' not in st.session_state:
    st.session_state.last_trigger_count = 0
if 'interaction_history' not in st.session_state:
    st.session_state.interaction_history = []

# 侧边栏设置
with st.sidebar:
    st.markdown("## 🎨 画笔设置")

    # 笔刷设置
    stroke_color = st.color_picker(
        "选择笔刷颜色",
        value=st.session_state.drawing_data.get('stroke_color', '#000000'),
        key="color_picker"
    )
    st.session_state.drawing_data['stroke_color'] = stroke_color

    stroke_width = st.slider(
        "笔刷粗细",
        min_value=1,
        max_value=40,
        value=st.session_state.drawing_data.get('stroke_width', 5),
        key="stroke_width"
    )
    st.session_state.drawing_data['stroke_width'] = stroke_width

    st.markdown("### 🖼️ 背景设置")
    bg_color = st.color_picker(
        "背景颜色",
        value=st.session_state.drawing_data.get('background_color', '#FFFFFF'),
        key="bg_color"
    )
    st.session_state.drawing_data['background_color'] = bg_color

    st.divider()
    st.markdown("### 🛠️ 工具")
    st.info("💡 撤销/重做/清空功能已集成在画板左侧工具栏中")

    st.divider()

    # 统计信息占位符
    st.markdown("### 📊 统计")
    stats_placeholder = st.empty()
    
    # 默认显示
    with stats_placeholder.container():
        col1, col2 = st.columns(2)
        with col1:
            st.metric("笔画数", 0)
        with col2:
            st.metric("互动次数", 0)

# 创建画板和互动区域
st.markdown("## 画布区域")

# 使用两栏布局
canvas_col, feedback_col = st.columns([3, 1])

# 计算画布参数
canvas_width = 750 # 略微减小宽度以适应双栏
canvas_height = 550

with canvas_col:
    # 使用 streamlit-drawable-canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # 填充颜色（如果需要）
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=None,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="freedraw",
        key="canvas",
        display_toolbar=True,
    )

with feedback_col:
    st.markdown("### 🧚 球球的反馈")
    feedback_container = st.container(height=canvas_height - 50)
    with feedback_container:
        if not st.session_state.interaction_history:
            st.write("还没有互动哦，快画几笔吧！")
        
        # 获取最新的一条互动
        history = st.session_state.interaction_history
        for i, chat in enumerate(reversed(history)):
            with st.chat_message("assistant", avatar="🧚"):
                st.write(chat['text'])
                if chat.get('audio'):
                    # 只有最新的一条反馈且未播放过才自动播放
                    autoplay = (i == 0 and not chat.get('played', False))
                    st.audio(chat['audio'], format='audio/wav', autoplay=autoplay)
                    if autoplay:
                        chat['played'] = True

# 实时处理逻辑
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    current_count = len(objects)
    
    # 更新侧边栏统计（在画布渲染后更新）
    with stats_placeholder.container():
        c1, c2 = st.columns(2)
        with c1:
            st.metric("笔画数", current_count)
        with c2:
            st.metric("互动次数", st.session_state.last_trigger_count // 8)
    
    # 如果画布被清空，重置触发计数
    if current_count == 0 and st.session_state.last_trigger_count > 0:
        st.session_state.last_trigger_count = 0
        st.session_state.interaction_history = []
        st.rerun()
    
    # 更新session state中的笔画数据（简化存储）
    st.session_state.drawing_data['strokes'] = objects
    
    # 逻辑：每8笔触发一次语音互动
    # 修复：使用更稳健的触发逻辑，防止快速绘画时跳过
    trigger_threshold = 8
    if current_count >= st.session_state.last_trigger_count + trigger_threshold:
        # 获取图像数据并转换为字节
        if canvas_result.image_data is not None:
            try:
                # 将 numpy 数组转换为 PNG 字节流
                import numpy as np
                from PIL import Image
                import io
                
                img_data = canvas_result.image_data.astype(np.uint8)
                img = Image.fromarray(img_data)
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                image_bytes = buffered.getvalue()
                
                with st.spinner("🧚 球球正在看你的画..."):
                    # 只有在成功获取反馈后才更新 last_trigger_count
                    drawing_info = {
                        "stroke_count": current_count,
                        "timestamp": "realtime"
                    }
                    
                    # 准备对话上下文
                    history = []
                    # 取最近3轮对话作为上下文，避免上下文过长
                    for chat in st.session_state.interaction_history[-3:]:
                        if chat.get('prompt'):
                            history.append({"role": "user", "content": chat['prompt']})
                        history.append({"role": "assistant", "content": chat['text']})
                    
                    # 生成反馈
                    feedback_data = services['multimodal'].generate_spirit_feedback(
                        image_bytes, 
                        drawing_info,
                        history=history
                    )
                    
                    # 兼容性处理
                    if isinstance(feedback_data, str):
                        feedback_text = feedback_data
                        feedback_audio = None
                    else:
                        feedback_text = feedback_data.get('text', '')
                        feedback_audio = feedback_data.get('audio')
                    
                    # 更新状态
                    if feedback_text:
                        st.session_state.last_trigger_count = current_count
                        st.session_state.interaction_history.append({
                            "prompt": services['multimodal']._build_spirit_feedback_prompt(drawing_info),
                            "text": feedback_text,
                            "audio": feedback_audio,
                            "played": False # 新增播放状态标记
                        })
                        st.toast(f"🧚 球球说：{feedback_text}")
                        st.rerun()
                    
            except Exception as e:
                st.error(f"互动出错: {str(e)}")

st.info("""
💡 **使用提示：**
- 左侧工具栏可调整颜色、粗细，并支持撤销/重做/清空
- 每画8笔，小精灵球球会来看你的画并说话哦
- 完成后点击下方"完成作品"进行深度分析
""")

# 操作区域
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📸 截图预览", use_container_width=True):
        if canvas_result.image_data is not None:
             st.image(canvas_result.image_data, caption="当前画布预览")

with col2:
    if st.button("🎵 查看之前作品", use_container_width=True):
        if not canvas_result.json_data or not canvas_result.json_data["objects"]:
            st.error("请先在画板上绘画！")
        else:
            st.session_state.generate_music = True

with col3:
    if st.button("✅ 完成作品", use_container_width=True):
        if not canvas_result.json_data or not canvas_result.json_data["objects"]:
            st.error("请先在画板上绘画！")
        else:
            st.session_state.finish_artwork = True

# 处理完成作品
if st.session_state.get('finish_artwork'):
    with st.spinner("🤖 正在进行深度分析..."):
        try:
            if canvas_result.image_data is not None:
                # 获取图片
                img_data = canvas_result.image_data.astype(np.uint8)
                img = Image.fromarray(img_data)
                
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                image_data = img_bytes.getvalue()
                
                # 保存图片
                artwork_id = str(uuid.uuid4())[:8]
                image_path = file_handler.save_image(
                    image_data,
                    st.session_state.user_id,
                    artwork_id
                )
                
                # 1. 使用 ImageProcessor 进行视觉分析 (用户要求)
                st.write("🔍 正在进行视觉计算...")
                dominant_colors = ImageProcessor.extract_dominant_colors(image_data)
                balance_score = ImageProcessor.calculate_balance_score(image_data)
                focus_point = ImageProcessor.detect_focus_point(image_data)
                scene_type = ImageProcessor.detect_scene_type(image_data)
                palette_info = ImageProcessor.generate_palette(image_data)
                
                # 2. 多模态分析 (整合视觉分析数据)
                drawing_info = {
                    'duration': 120,  # 示例
                    'stroke_count': len(canvas_result.json_data["objects"]),
                    'revision_count': 0,
                    'visual_stats': {
                        'balance_score': balance_score,
                        'scene_type': scene_type,
                        'focus_point': focus_point
                    }
                }
                
                analysis = services['multimodal'].analyze_drawing(image_data, drawing_info)
                
                # 3. 生成小精灵最终点评
                spirit_feedback_data = services['multimodal'].generate_spirit_feedback(image_data, drawing_info)
                spirit_text = spirit_feedback_data.get('text', '')
                spirit_audio = spirit_feedback_data.get('audio')
                
                # 保存作品数据
                artwork = Artwork(
                    artwork_id=artwork_id,
                    user_id=st.session_state.user_id,
                    drawing_data=DrawingData(
                        user_id=st.session_state.user_id,
                        stroke_count=drawing_info['stroke_count']
                    ),
                    image_path=image_path,
                    theme_analysis=analysis.get('theme_analysis', {}),
                    color_analysis=analysis.get('color_analysis', {}),
                    composition_analysis=analysis.get('composition_analysis', {}),
                    emotional_analysis=analysis.get('emotional_analysis', {}),
                    development_analysis=analysis.get('development_analysis', {}),
                    voice_feedback=spirit_text  # 只存储文字
                )
                
                # 将音频存入 session_state 以供显示
                st.session_state.last_analysis_audio = spirit_audio
                
                # 补充视觉分析数据到 artwork (如果模型支持，这里暂存到 analysis 字段中展示)
                artwork.color_analysis['palette'] = palette_info.get('palette', [])
                artwork.composition_analysis['calculated_balance'] = balance_score
                
                # 保存到session
                st.session_state.current_artwork = artwork
                
                # 自动持久化保存元数据
                try:
                    artwork_dict = artwork.to_dict()
                    file_handler.save_json(
                        artwork_dict,
                        st.session_state.user_id,
                        f"{artwork.artwork_id}.json"
                    )
                except Exception as e:
                    print(f"自动保存元数据失败: {str(e)}")

                st.success("✨ 分析完成！")
                st.session_state.finish_artwork = False
                st.session_state.show_analysis = True
                st.rerun()

        except Exception as e:
            st.error(f"分析失败: {str(e)}")
            st.session_state.finish_artwork = False

# 显示分析结果
if st.session_state.get('show_analysis') and st.session_state.current_artwork:
    artwork = st.session_state.current_artwork

    st.divider()
    st.markdown("## 📊 AI分析结果")

    # 显示作品图片
    if artwork.image_path:
        st.image(artwork.image_path, caption="你的作品", use_column_width=True)

    # 显示小精灵反馈
    st.markdown("### 🧚 小精灵的话")
    if artwork.voice_feedback:
        st.info(artwork.voice_feedback)

    # 显示音频
    if st.session_state.get('last_analysis_audio'):
        st.audio(st.session_state.last_analysis_audio, format='audio/wav')
    elif artwork.voice_feedback:
        # 如果没有缓存的音频（比如是从历史记录加载的），则调用 TTS
        try:
            voice_audio = services['voice'].text_to_speech(artwork.voice_feedback)
            if voice_audio:
                st.audio(voice_audio, format='audio/wav')
        except:
            pass

    # 显示生成的视频
    if artwork.video_url:
        st.markdown("### 🎬 魔法视频")
        st.video(artwork.video_url)

    # 显示生成的音乐
    if artwork.music_url:
        st.markdown("### 🎵 背景音乐")
        st.audio(artwork.music_url)

    # 显示分析详情
    with st.expander("📈 详细分析", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 主题分析")
            theme = artwork.theme_analysis
            st.write(f"**主题:** {theme.get('main_theme', 'N/A')}")
            st.write(f"**元素:** {', '.join(theme.get('elements', []))}")

            st.markdown("#### 情感分析")
            emotion = artwork.emotional_analysis
            st.write(f"**主要情感:** {', '.join(emotion.get('primary_emotions', []))}")
            st.write(f"**表达风格:** {emotion.get('expression_style', 'N/A')}")

        with col2:
            st.markdown("#### 色彩分析")
            color = artwork.color_analysis
            st.write(f"**主要颜色:** {', '.join(color.get('dominant_colors', []))}")
            st.write(f"**情感基调:** {color.get('emotional_tone', 'N/A')}")

            st.markdown("#### 发展阶段")
            dev = artwork.development_analysis
            st.write(f"**阶段:** {dev.get('stage', 'N/A')}")
            st.write(f"**年龄范围:** {dev.get('age_range', 'N/A')}")

    # 操作按钮
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎵 生成音乐", use_container_width=True, key="btn_music_analysis"):
            st.session_state.generate_music_for_artwork = True

    with col2:
        if st.button("🎬 生成视频", use_container_width=True):
            st.session_state.generate_video = True

    with col3:
        if st.button("💾 保存作品", use_container_width=True):
            st.session_state.save_artwork = True

    # 处理生成音乐
    if st.session_state.get('generate_music_for_artwork'):
        with st.spinner("🎵 正在为你的画生成音乐..."):
            try:
                # 上传到Coze
                if artwork.image_path:
                    image_data = file_handler.load_image(artwork.image_path)
                    file_id = services['coze'].upload_image_to_coze(image_data)

                    if file_id:
                        result = services['coze'].generate_music_from_image(file_id)
                        if result.get('status') == 'success':
                            artwork.music_url = result.get('music_url')
                            emotion = result.get('emotion')
                            
                            # 保存emotion到情感分析中
                            if emotion:
                                if not artwork.emotional_analysis:
                                    artwork.emotional_analysis = {}
                                artwork.emotional_analysis['primary_emotions'] = [emotion]
                            
                            # 自动持久化保存音乐
                            if artwork.music_url:
                                try:
                                    music_response = requests.get(artwork.music_url)
                                    if music_response.status_code == 200:
                                        music_path = file_handler.save_audio(
                                            music_response.content,
                                            st.session_state.user_id,
                                            artwork.artwork_id,
                                            audio_type="music"
                                        )
                                        artwork.music_path = music_path
                                except:
                                    pass
                            
                            # 更新元数据
                            try:
                                file_handler.save_json(
                                    artwork.to_dict(),
                                    st.session_state.user_id,
                                    f"{artwork.artwork_id}.json"
                                )
                            except:
                                pass

                            st.session_state.current_artwork = artwork
                            st.success("🎵 音乐生成成功！")
                            
                            # 展示emotion文案
                            if emotion:
                                st.info(f"🎭 音乐情感标签：{emotion}")
                            
                            if artwork.music_url:
                                st.audio(artwork.music_url)
                        else:
                            st.error(f"音乐生成失败: {result.get('error')}")
                    else:
                        st.error("图片上传失败")
            except Exception as e:
                st.error(f"生成音乐出错: {str(e)}")
            st.session_state.generate_music_for_artwork = False

    # 处理生成视频
    if st.session_state.get('generate_video'):
        with st.spinner("🎬 正在为你的画生成魔法视频..."):
            try:
                # 上传到Coze
                if artwork.image_path:
                    image_data = file_handler.load_image(artwork.image_path)
                    file_id = services['coze'].upload_image_to_coze(image_data)

                    if file_id:
                        result = services['coze'].generate_video_from_image(file_id)
                        if result.get('status') == 'success':
                            artwork.video_url = result.get('video_url')
                            
                            # 自动持久化保存视频
                            if artwork.video_url:
                                try:
                                    video_response = requests.get(artwork.video_url)
                                    if video_response.status_code == 200:
                                        video_path = file_handler.save_video(
                                            video_response.content,
                                            st.session_state.user_id,
                                            artwork.artwork_id,
                                            video_type="magic"
                                        )
                                        artwork.video_path = video_path
                                except:
                                    pass

                            # 更新元数据
                            try:
                                file_handler.save_json(
                                    artwork.to_dict(),
                                    st.session_state.user_id,
                                    f"{artwork.artwork_id}.json"
                                )
                            except:
                                pass

                            st.session_state.current_artwork = artwork
                            st.success("🎬 视频生成成功！")
                            if artwork.video_url:
                                st.video(artwork.video_url)
                        else:
                            st.error(f"视频生成失败: {result.get('error')}")
                    else:
                        st.error("图片上传失败")
            except Exception as e:
                st.error(f"生成视频出错: {str(e)}")
            st.session_state.generate_video = False

    # 处理保存作品
    if st.session_state.get('save_artwork'):
        try:
            artwork_dict = artwork.to_dict()
            file_handler.save_json(
                artwork_dict,
                st.session_state.user_id,
                f"{artwork.artwork_id}.json"
            )
            st.success("✅ 作品已保存！")
            st.session_state.save_artwork = False
        except Exception as e:
            st.error(f"保存失败: {str(e)}")

st.divider()

# 快速帮助
with st.expander("❓ 如何使用"):
    st.markdown("""
    ### 画板操作
    1. **绘画**: 用鼠标或触摸笔在画布上绘画
    2. **调整设置**: 在左侧调整笔刷颜色和粗细
    3. **编辑**: 使用撤销/重做来修改
    4. **完成**: 点击"完成作品"让小精灵分析

    ### 作品工坊
    1. **生成音乐**: 让AI为你的画创作背景音乐
    2. **生成视频**: 让AI创建魔法视频变身效果
    3. **保存作品**: 将作品保存到本地
    4. **获得点评**: 小精灵会给出语音评价

    ### 小贴士
    - 大胆创作！没有对错之分
    - 小精灵喜欢有故事的画
    - 尝试不同的颜色组合
    - 继续修改完善你的作品
    """)

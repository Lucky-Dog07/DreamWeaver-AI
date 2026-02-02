import streamlit as st
import json
import time
import uuid
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
@st.cache_resource
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

# 初始化触发计数器
if 'last_trigger_count' not in st.session_state:
    st.session_state.last_trigger_count = 0

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
        max_value=20,
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

    # 统计信息
    st.markdown("### 📊 统计")
    current_strokes = 0
    if 'canvas_result' in st.session_state and st.session_state.canvas_result and st.session_state.canvas_result.json_data:
         if "objects" in st.session_state.canvas_result.json_data:
            current_strokes = len(st.session_state.canvas_result.json_data["objects"])
            
    col1, col2 = st.columns(2)
    with col1:
        st.metric("笔画数", current_strokes)
    with col2:
        # 这里的修改次数在使用st_canvas时较难精确统计，暂用触发次数代替或其他
        st.metric("互动次数", st.session_state.last_trigger_count // 8)

# 创建画板
st.markdown("## 画布区域")

# 计算画布参数
canvas_width = 800
canvas_height = 600

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

# 实时处理逻辑
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    current_count = len(objects)
    
    # 更新session state中的笔画数据（简化存储）
    st.session_state.drawing_data['strokes'] = objects
    
    # 逻辑：每8笔触发一次语音互动
    if current_count > 0 and current_count >= st.session_state.last_trigger_count + 8:
        st.session_state.last_trigger_count = current_count
        
        with st.spinner("🧚 球球正在看你的画..."):
            try:
                # 获取图片数据
                if canvas_result.image_data is not None:
                    img_data = canvas_result.image_data.astype(np.uint8)
                    img = Image.fromarray(img_data)
                    
                    # 转为bytes
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    image_bytes = img_bytes.getvalue()
                    
                    # 准备绘画信息
                    drawing_info = {
                        'duration': 0, # 暂未实现精确计时
                        'stroke_count': current_count,
                        'revision_count': 0
                    }
                    
                    # 生成反馈
                    feedback = services['multimodal'].generate_spirit_feedback(image_bytes, drawing_info)
                    
                    # 生成语音
                    voice_audio = services['voice'].text_to_speech(feedback)
                    
                    # 播放语音
                    if voice_audio:
                        st.audio(voice_audio, format='audio/wav', autoplay=True)
                    
                    st.toast(f"🧚 球球说：{feedback}")
                    
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
    if st.button("🎵 生成音乐", use_container_width=True):
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
                spirit_feedback = services['multimodal'].generate_spirit_feedback(image_data, drawing_info)
                voice_audio = services['voice'].text_to_speech(spirit_feedback)
                
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
                    voice_feedback=spirit_feedback
                )
                
                # 补充视觉分析数据到 artwork (如果模型支持，这里暂存到 analysis 字段中展示)
                artwork.color_analysis['palette'] = palette_info.get('palette', [])
                artwork.composition_analysis['calculated_balance'] = balance_score
                
                # 保存到session
                st.session_state.current_artwork = artwork
                
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
    st.info(artwork.voice_feedback)

    # 显示语音
    if artwork.voice_feedback:
        try:
            voice_audio = services['voice'].text_to_speech(artwork.voice_feedback)
            if voice_audio:
                st.audio(voice_audio, format='audio/wav')
        except:
            pass

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
                            st.session_state.current_artwork = artwork
                            st.success("🎵 音乐生成成功！")
                            if artwork.music_url:
                                st.audio(artwork.music_url)
                        else:
                            st.error(f"音乐生成失败: {result.get('error')}")
                    else:
                        st.error("图片上传失败")
            except Exception as e:
                st.error(f"生成音乐出错: {str(e)}")
            st.session_state.generate_music_for_artwork = False

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
    3. **获得点评**: 小精灵会给出语音评价

    ### 小贴士
    - 大胆创作！没有对错之分
    - 小精灵喜欢有故事的画
    - 尝试不同的颜色组合
    - 继续修改完善你的作品
    """)

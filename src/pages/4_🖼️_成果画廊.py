import streamlit as st
import os
from pathlib import Path
from utils.file_handler import FileHandler
from utils.session_manager import init_session_state

st.set_page_config(
    page_title="艺术画廊",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_session_state()
file_handler = FileHandler()

st.markdown("# 🖼️ 艺术画廊")
st.markdown("*在这里欣赏你创作的所有艺术作品*")

st.divider()

# 获取用户作品
user_id = st.session_state.user_id
artworks_paths = file_handler.get_user_artworks(user_id)

# 侧边栏显示存储信息
with st.sidebar:
    st.markdown("### 📁 存储信息")
    st.info(f"当前用户: {user_id}")
    
    # 获取存储路径
    user_dir = file_handler.artworks_dir / user_id
    if user_dir.exists():
        st.code(str(user_dir.absolute()), language="text")
        
        # 统计信息
        file_count = len(list(user_dir.rglob("*.*")))
        total_size = file_handler.get_storage_size(user_id)
        st.text(f"文件数量: {file_count}")
        st.text(f"占用空间: {file_handler.format_file_size(total_size)}")
    else:
        st.warning("暂无存储数据")

if not artworks_paths:
    st.info("画廊空空如也，快去创作你的第一幅作品吧！")
    # 尝试检测是否有其他用户的数据（可能是之前的会话产生的）
    all_users = [d.name for d in file_handler.artworks_dir.iterdir() if d.is_dir() and d.name != user_id]
    if all_users:
        with st.expander("检测到历史数据"):
            st.write("发现其他会话产生的数据，可能属于之前的操作：")
            for old_user in all_users:
                st.text(f"- {old_user}")
            st.info("提示：由于系统更新了持久化机制，旧数据位于不同文件夹。您可以手动迁移数据到当前用户目录。")
    st.stop()

# 分页设置
items_per_page = 12
if 'gallery_page' not in st.session_state:
    st.session_state.gallery_page = 0

total_pages = (len(artworks_paths) - 1) // items_per_page + 1
current_page = st.session_state.gallery_page

# 翻页控件
if total_pages > 1:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ 上一页", disabled=current_page == 0):
            st.session_state.gallery_page -= 1
            st.rerun()
    with col3:
        if st.button("下一页 ➡️", disabled=current_page == total_pages - 1):
            st.session_state.gallery_page += 1
            st.rerun()

# 显示当前页作品
start_idx = current_page * items_per_page
end_idx = start_idx + items_per_page
current_batch = artworks_paths[start_idx:end_idx]

# 使用网格布局显示
cols = st.columns(4) # 4列布局
for idx, artwork_path in enumerate(current_batch):
    with cols[idx % 4]:
        # 获取作品ID (文件名格式: {artwork_id}_{timestamp}.png)
        filename = artwork_path.name
        artwork_id = filename.split('_')[0]
        
        # 加载元数据
        metadata = file_handler.get_artwork_metadata(user_id, artwork_id)
        
        # 显示图片容器
        with st.container(border=True):
            st.image(str(artwork_path), use_column_width=True)
            
            # 显示标题或日期
            if metadata and 'theme_analysis' in metadata:
                 title = metadata['theme_analysis'].get('title', '无题')
            else:
                title = "未命名作品"
            st.markdown(f"**{title}**")
            
            # 详情按钮
            if st.button("👀 查看详情", key=f"btn_view_{artwork_id}"):
                st.session_state.selected_artwork_id = artwork_id
                st.session_state.selected_artwork_path = str(artwork_path)
                st.session_state.selected_artwork_metadata = metadata
                st.rerun()

# 显示详情弹窗 (使用 expander 模拟或直接在下方显示)
if 'selected_artwork_id' in st.session_state and st.session_state.selected_artwork_id:
    st.divider()
    st.markdown("## 🎨 作品详情")
    
    col_img, col_info = st.columns([1, 1])
    
    with col_img:
        st.image(st.session_state.selected_artwork_path, caption="作品原图")
        if st.button("❌ 关闭详情"):
            del st.session_state.selected_artwork_id
            st.rerun()
            
    with col_info:
        metadata = st.session_state.selected_artwork_metadata
        if metadata:
            st.markdown(f"### {metadata.get('theme_analysis', {}).get('title', '无题')}")
            
            # 播放语音点评
            if metadata.get('voice_feedback'):
                st.info(f"🧚 **小精灵点评**: {metadata['voice_feedback']}")
            
            # 播放音乐
            music_file = None
            if metadata.get('music_url'):
                st.markdown("### 🎵 背景音乐")
                st.audio(metadata['music_url'])
            elif metadata.get('music_path'): # 本地存储路径
                st.markdown("### 🎵 背景音乐")
                st.audio(metadata['music_path'])
                music_file = metadata['music_path']

            # 播放视频
            video_file = None
            if metadata.get('video_url'):
                st.markdown("### 🎬 魔法视频")
                st.video(metadata['video_url'])
            elif metadata.get('video_path'): # 本地存储路径
                st.markdown("### 🎬 魔法视频")
                st.video(metadata['video_path'])
                video_file = metadata['video_path']
                
            # 下载区域
            st.divider()
            st.markdown("#### 📥 下载资源")
            d_col1, d_col2, d_col3 = st.columns(3)
            
            with d_col1:
                # 图片下载
                with open(st.session_state.selected_artwork_path, "rb") as f:
                    st.download_button(
                        label="🖼️ 下载原画",
                        data=f,
                        file_name=Path(st.session_state.selected_artwork_path).name,
                        mime="image/png"
                    )
            
            with d_col2:
                # 音乐下载
                if music_file and os.path.exists(music_file):
                    with open(music_file, "rb") as f:
                        st.download_button(
                            label="🎵 下载音乐",
                            data=f,
                            file_name=Path(music_file).name,
                            mime="audio/wav"
                        )
            
            with d_col3:
                # 视频下载
                if video_file and os.path.exists(video_file):
                    with open(video_file, "rb") as f:
                        st.download_button(
                            label="🎬 下载视频",
                            data=f,
                            file_name=Path(video_file).name,
                            mime="video/mp4"
                        )

            # 显示分析
            with st.expander("📊 详细分析数据"):
                st.json(metadata)
        else:
            st.warning("暂无详细元数据")


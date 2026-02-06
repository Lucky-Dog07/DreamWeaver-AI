import os, sys
_src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if _src not in sys.path: sys.path.insert(0, _src)
import streamlit as st
import os
import base64
from pathlib import Path
from datetime import datetime
from utils.file_handler import FileHandler
from utils.session_manager import init_session_state

st.set_page_config(
    page_title="艺术画廊",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# 强制注入稳定性 CSS
st.markdown(f"""
<style>
    {bg_css}
    
    /* 按钮蓝色样式 */
    .stButton > button {{
        background-color: #4A90E2;
        color: white;
        border: none;
        border-radius: 8px;
    }}
    .stButton > button:hover {{
        background-color: #357ABD;
        color: white;
    }}
    
    /* 强制显示垂直滚动条，防止布局跳动 */
    html {{
        overflow-y: scroll;
    }}
    
    /* 画廊图片容器固定比例，防止加载时高度塌陷导致跳动 */
    .stImage > img {{
        object-fit: cover;
        height: 200px; /* 固定高度确保整齐 */
        border-radius: 8px;
        transition: transform 0.3s ease;
    }}
    
    .stImage:hover img {{
        transform: scale(1.02);
    }}
    
    /* 优化卡片容器稳定性 */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {{
        gap: 1rem;
    }}
    
    /* 翻页按钮稳定性 */
    .stButton button {{
        width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

init_session_state()
file_handler = FileHandler()

st.markdown("# 🖼️ 艺术画廊")
st.markdown("*在这里欣赏你创作的所有艺术作品*")

st.divider()

# 获取所有作品（包括历史会话的）
artworks_paths = file_handler.get_all_artworks()

# 侧边栏显示存储信息
with st.sidebar:
    st.markdown("### 📁 存储信息")
    st.code(str(file_handler.artworks_dir.absolute()), language="text")
    
    # 统计信息
    all_users = [d.name for d in file_handler.artworks_dir.iterdir() if d.is_dir()]
    st.text(f"作品数量: {len(artworks_paths)}")
    st.text(f"会话数量: {len(all_users)}")

if not artworks_paths:
    st.info("画廊空空如也，快去创作你的第一幅作品吧！")
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
        
        # 从文件修改时间获取创建日期
        mtime = artwork_path.stat().st_mtime
        create_date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        
        # 显示图片容器
        with st.container(border=True):
            st.image(str(artwork_path), use_container_width=True)
            
            # 显示创建日期
            st.markdown(f"**{create_date}**")
            
            # 详情按钮
            if st.button("👀 查看详情", key=f"btn_view_{idx}_{artwork_id}"):
                st.session_state.selected_artwork_id = artwork_id
                st.session_state.selected_artwork_path = str(artwork_path)
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
        # 显示文件信息
        artwork_path = Path(st.session_state.selected_artwork_path)
        mtime = artwork_path.stat().st_mtime
        create_date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        file_size = artwork_path.stat().st_size / 1024  # KB
        
        st.markdown(f"### 📋 作品信息")
        st.text(f"创建时间: {create_date}")
        st.text(f"文件大小: {file_size:.1f} KB")
        st.text(f"文件名: {artwork_path.name}")
                
        # 下载区域
        st.divider()
        st.markdown("#### 📥 下载资源")
        
        # 图片下载
        with open(st.session_state.selected_artwork_path, "rb") as f:
            st.download_button(
                label="🖼️ 下载原画",
                data=f,
                file_name=artwork_path.name,
                mime="image/png",
                use_container_width=True
            )

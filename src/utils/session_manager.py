import streamlit as st
import uuid

def init_session_state():
    """初始化会话状态"""
    
    # 基础配置
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
    # 画板相关
    if 'drawing_data' not in st.session_state:
        st.session_state.drawing_data = {
            'strokes': [],
            'current_canvas': None,
            'undo_stack': [],
            'redo_stack': [],
            'background_color': '#FFFFFF',
            'stroke_width': 5,
            'stroke_color': '#000000',
            'revision_count': 0,
        }
    
    # AI交互相关
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    # 作品工坊相关
    if 'current_artwork' not in st.session_state:
        st.session_state.current_artwork = None
        
    if 'generated_music' not in st.session_state:
        st.session_state.generated_music = None
        
    if 'generated_video' not in st.session_state:
        st.session_state.generated_video = None

    # 设置相关
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'voice_enabled': True,
            'bgm_enabled': True,
            'theme': 'light'
        }

def get_state(key, default=None):
    """获取session状态"""
    return st.session_state.get(key, default)

def set_state(key, value):
    """设置session状态"""
    st.session_state[key] = value

def clear_session():
    """清除会话状态"""
    # 保留user_id等核心信息，重置其他
    user_id = st.session_state.get('user_id')
    st.session_state.clear()
    st.session_state.user_id = user_id
    init_session_state()

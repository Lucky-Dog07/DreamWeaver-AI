import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ConfigLoader:
    """配置加载器"""
    
    @staticmethod
    def get_dashscope_api_key():
        return os.getenv("DASHSCOPE_API_KEY")
    
    @staticmethod
    def get_coze_config():
        return {
            "api_token": os.getenv("COZE_API_TOKEN"),
            "bot_id": os.getenv("COZE_BOT_ID"),
            "workflow_id": os.getenv("COZE_WORKFLOW_ID", "7601786439168229386"),
            "comment_workflow_id": os.getenv("COZE_COMMENT_WORKFLOW_ID", "7601786024813445158"),
            "video_workflow_id": os.getenv("COZE_VIDEO_WORKFLOW_ID", "7602166946105556998")
        }
    
    @staticmethod
    def get_huoshan_config():
        return {
            "access_key": os.getenv("HUOSHAN_ACCESS_KEY"),
            "secret_key": os.getenv("HUOSHAN_SECRET_KEY")
        }
    
    @staticmethod
    def get_app_settings():
        """获取应用基础设置"""
        return {
            "app_name": "绘梦精灵 (DreamWeaver AI)",
            "version": "v1.0.0",
            "debug": False
        }

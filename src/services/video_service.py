import requests
import json
import time
from typing import Optional, Dict, Any
from utils.config_loader import ConfigLoader

class VideoService:
    """视频生成服务 - 火山引擎Seedance集成"""

    def __init__(self):
        config = ConfigLoader.get_huoshan_config()
        self.access_key = config.get("access_key")
        self.secret_key = config.get("secret_key")
        self.base_url = "https://api.volcengine.com/video"
        self.default_model = "doubao-seedance-1-0-pro-fast-251015"
        self.fallback_model = "doubao-seedance-1-0-lite-t2v-250428"

    def create_transition_video(
        self,
        first_frame_url: str,
        last_frame_url: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        创建首尾帧过渡视频

        Args:
            first_frame_url: 首帧图片URL或Base64
            last_frame_url: 尾帧图片URL或Base64
            config: 视频配置参数

        Returns:
            包含task_id和status的字典
        """
        if config is None:
            config = self._default_config()

        try:
            # 准备请求数据
            payload = {
                "model": self.default_model,
                "images": [
                    {
                        "url": first_frame_url,
                        "role": "first_frame"
                    },
                    {
                        "url": last_frame_url,
                        "role": "last_frame"
                    }
                ],
                "prompt": config.get("prompt", "平滑过渡动画，添加魔法光效效果"),
                "duration": config.get("duration", 8),
                "resolution": config.get("resolution", "720p"),
                "ratio": config.get("ratio", "4:3"),
                "generate_audio": False,  # 单独处理音频
                "watermark": False,
                "service_tier": config.get("service_tier", "flex")  # 离线推理降成本
            }

            # 调用API
            response = self._call_video_api("/v1/video-generation/submit", payload)

            if response and response.get("code") == 0:
                data = response.get("data", {})
                return {
                    "task_id": data.get("task_id"),
                    "status": "processing",
                    "estimated_time": 60,
                    "model": self.default_model
                }
            else:
                error_msg = response.get("message") if response else "未知错误"
                print(f"视频生成失败: {error_msg}")
                return {
                    "status": "failed",
                    "error": error_msg,
                    "fallback": True
                }

        except Exception as e:
            print(f"视频生成异常: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "fallback": True
            }

    def query_video_task(self, task_id: str) -> Dict[str, Any]:
        """
        查询视频生成任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态信息
        """
        try:
            response = self._call_video_api(
                "/v1/video-generation/query",
                {"task_id": task_id}
            )

            if response and response.get("code") == 0:
                data = response.get("data", {})
                status = data.get("status")

                result = {
                    "task_id": task_id,
                    "status": self._map_status(status),
                    "progress": data.get("progress", 0),
                    "cost": data.get("cost")
                }

                # 如果完成，添加视频URL
                if status == "success":
                    result["video_url"] = data.get("output", {}).get("video_url")
                elif status == "failed":
                    result["error"] = data.get("error_msg")

                return result
            else:
                return {
                    "status": "unknown",
                    "error": response.get("message") if response else "未知错误"
                }

        except Exception as e:
            print(f"状态查询失败: {str(e)}")
            return {
                "status": "unknown",
                "error": str(e)
            }

    def create_simple_transition(
        self,
        first_frame_url: str,
        last_frame_url: str
    ) -> Dict[str, Any]:
        """
        创建简单过渡效果（降级方案）

        Args:
            first_frame_url: 首帧URL
            last_frame_url: 尾帧URL

        Returns:
            包含过渡信息的字典
        """
        try:
            # 这是一个简化的实现
            # 实际应该使用OpenCV或PIL创建帧过渡
            return {
                "status": "fallback",
                "message": "使用简化过渡效果",
                "first_frame": first_frame_url,
                "last_frame": last_frame_url,
                "duration": 5
            }

        except Exception as e:
            print(f"简单过渡创建失败: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def _call_video_api(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """调用火山引擎视频API"""
        try:
            url = f"{self.base_url}{endpoint}"

            headers = {
                "Authorization": f"Bearer {self.access_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"API调用失败: {response.status_code}")
                print(f"响应: {response.text}")
                return None

        except Exception as e:
            print(f"API调用异常: {str(e)}")
            return None

    def _map_status(self, api_status: str) -> str:
        """映射API状态到统一状态"""
        status_map = {
            "processing": "processing",
            "running": "processing",
            "success": "completed",
            "failed": "failed",
            "error": "failed"
        }
        return status_map.get(api_status, "unknown")

    def _default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "duration": 8,
            "resolution": "720p",
            "ratio": "4:3",
            "prompt": "平滑过渡动画，添加魔法光效效果",
            "service_tier": "flex"
        }

    def get_video_quality_options(self) -> Dict[str, str]:
        """获取可用的视频质量选项"""
        return {
            "480p": "标清（480p）",
            "720p": "高清（720p）",
            "1080p": "超清（1080p）"
        }

    def get_video_ratio_options(self) -> Dict[str, str]:
        """获取可用的视频比例选项"""
        return {
            "4:3": "标准（4:3）- 适合绘画",
            "16:9": "宽屏（16:9）",
            "9:16": "竖屏（9:16）",
            "1:1": "正方形（1:1）"
        }

    def get_animation_styles(self) -> Dict[str, str]:
        """获取可用的动画风格"""
        return {
            "fantasy": "魔法✨ - 星星点点，梦幻过渡",
            "cartoon": "卡通🎨 - 弹性效果，活泼过渡",
            "watercolor": "水彩🌊 - 晕染效果，艺术过渡",
            "smooth": "平滑💫 - 简单优雅，顺畅过渡"
        }

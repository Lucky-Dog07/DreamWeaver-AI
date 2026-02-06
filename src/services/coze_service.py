import requests
import json
import time
from typing import Optional, Dict, Any
from utils.config_loader import ConfigLoader
from cozepy import Coze, TokenAuth, WorkflowEvent, WorkflowEventType, Stream, COZE_CN_BASE_URL

class CozeService:
    """Coze工作流集成服务 - 用于音乐生成和AI点评"""

    def __init__(self):
        config = ConfigLoader.get_coze_config()
        self.api_token = config.get("api_token") or ""
        self.api_token = self.api_token.strip() if isinstance(self.api_token, str) else ""
        self.bot_id = config.get("bot_id") or ""
        self.music_workflow_id = config.get("workflow_id", "7601786439168229386")
        self.comment_workflow_id = config.get("comment_workflow_id", "7601786024813445158")
        self.video_workflow_id = config.get("video_workflow_id", "7602166946105556998")
        self.base_url = "https://api.coze.cn/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        # 未配置 Token 时不创建 Coze 客户端，相关功能会提示“请配置 COZE_API_TOKEN”
        self.coze = None
        if self.api_token:
            self.coze = Coze(auth=TokenAuth(self.api_token), base_url=COZE_CN_BASE_URL)

    def _not_configured_result(self, feature: str) -> Dict[str, Any]:
        return {"status": "failed", "error": f"请先在 .env 中配置 COZE_API_TOKEN 和 COZE_BOT_ID 后再使用{feature}"}

    def generate_music_from_image(self, image_file_id: str) -> Optional[Dict[str, Any]]:
        """
        通过Coze工作流从图片生成音乐

        Args:
            image_file_id: 上传到Coze的图片文件ID

        Returns:
            包含music_url和其他信息的字典
        """
        if not self.coze:
            return self._not_configured_result("音乐生成")
        try:
            workflow_input = {
                "img": {"file_id": image_file_id}
            }

            result = self._execute_workflow_stream(
                self.music_workflow_id,
                workflow_input
            )

            if result and result.get("status") == "success":
                return {
                    "music_url": result.get("music_url"),
                    "emotion": result.get("emotion"),
                    "status": "success",
                    "workflow_id": self.music_workflow_id
                }
            else:
                return {
                    "status": "failed",
                    "error": result.get("error") if result else "未知错误"
                }

        except Exception as e:
            print(f"音乐生成失败: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def generate_voice_comment(self, image_file_id: str) -> Optional[Dict[str, Any]]:
        """
        通过Coze工作流生成AI点评语音

        Args:
            image_file_id: 上传的图片文件ID

        Returns:
            包含点评文案和音频链接的字典
        """
        if not self.coze:
            return self._not_configured_result("点评")
        try:
            workflow_input = {
                "img": {"file_id": image_file_id}
            }

            result = self._execute_workflow_stream(
                self.comment_workflow_id,
                workflow_input
            )

            if result and result.get("status") == "success":
                return {
                    "comment_url": result.get("comment_url"),
                    "comment_text": result.get("comment_text"),
                    "status": "success"
                }
            else:
                return {
                    "status": "failed",
                    "error": result.get("error") if result else "未知错误"
                }

        except Exception as e:
            print(f"点评生成失败: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def generate_video_from_image(self, image_file_id: str) -> Optional[Dict[str, Any]]:
        """
        通过Coze工作流从图片生成视频

        Args:
            image_file_id: 上传到Coze的图片文件ID

        Returns:
            包含video_url的字典
        """
        if not self.coze:
            return self._not_configured_result("视频生成")
        try:
            workflow_input = {
                "img": {"file_id": image_file_id}
            }

            result = self._execute_workflow_stream(
                self.video_workflow_id,
                workflow_input
            )

            if result and result.get("status") == "success":
                return {
                    "video_url": result.get("video_url"),
                    "status": "success"
                }
            else:
                return {
                    "status": "failed",
                    "error": result.get("error") if result else "未知错误"
                }

        except Exception as e:
            print(f"视频生成失败: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def upload_image_to_coze(self, image_bytes: bytes, filename: str = "drawing.png") -> Optional[str]:
        """
        上传图片到Coze（用于工作流输入）

        Args:
            image_bytes: 图片字节数据
            filename: 文件名

        Returns:
            文件ID
        """
        if not self.coze:
            return None
        try:
            from io import BytesIO

            file = self.coze.files.upload(file=BytesIO(image_bytes))
            return file.id

        except Exception as e:
            print(f"图片上传失败: {str(e)}")
            return None

    def _execute_workflow_stream(self, workflow_id: str, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        使用流式API执行Coze工作流

        Args:
            workflow_id: 工作流ID
            input_data: 输入数据

        Returns:
            工作流执行结果
        """
        if not self.coze:
            return {"status": "failed", "error": "请配置 COZE_API_TOKEN"}
        try:
            result = {
                "status": "pending",
                "data": None,
                "error": None
            }

            stream = self.coze.workflows.runs.stream(
                workflow_id=workflow_id,
                parameters=input_data
            )

            for event in stream:
                if event.event == WorkflowEventType.MESSAGE:
                    content = event.message.content
                    if content:
                        try:
                            data = json.loads(content)
                            result["data"] = data
                            result["status"] = "success"
                        except json.JSONDecodeError:
                            pass
                elif event.event == WorkflowEventType.ERROR:
                    result["status"] = "failed"
                    result["error"] = str(event.error)

            if result["data"]:
                data = result["data"]
                return {
                    "status": "success",
                    "music_url": data.get("AudioUrl") or data.get("music_url"),
                    "emotion": data.get("emotion"),
                    "comment_url": data.get("comment_audio") or data.get("comment_url"),
                    "comment_text": data.get("comment_text"),
                    "video_url": data.get("video_url") or data.get("VideoUrl"),
                    "raw_data": data
                }
            else:
                return {
                    "status": "failed",
                    "error": result.get("error") or "工作流执行完成但未返回数据"
                }

        except Exception as e:
            print(f"工作流执行异常: {str(e)}")
            return {
                "status": "failed",
                "error": str(e)
            }

    def _execute_workflow(self, workflow_id: str, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        执行Coze工作流（非流式，保留用于兼容性）

        Args:
            workflow_id: 工作流ID
            input_data: 输入数据

        Returns:
            工作流执行结果
        """
        if not self.coze:
            return None
        try:
            url = f"{self.base_url}/workflows/run"

            payload = {
                "workflow_id": workflow_id,
                "parameters": input_data
            }

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"工作流执行失败: {response.status_code}")
                print(f"响应: {response.text}")
                return None

        except Exception as e:
            print(f"工作流执行异常: {str(e)}")
            return None

    def query_workflow_status(self, workflow_run_id: str) -> Optional[Dict[str, Any]]:
        """
        查询工作流执行状态

        Args:
            workflow_run_id: 工作流运行ID

        Returns:
            执行状态信息
        """
        try:
            url = f"{self.base_url}/workflows/get_run"

            params = {
                "workflow_run_id": workflow_run_id
            }

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            print(f"状态查询失败: {str(e)}")
            return None

    def get_workflow_info(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """获取工作流信息"""
        try:
            url = f"{self.base_url}/workflows/get"

            params = {
                "workflow_id": workflow_id
            }

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            print(f"获取工作流信息失败: {str(e)}")
            return None

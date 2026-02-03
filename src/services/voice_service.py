import os
import base64
from typing import Optional, Tuple
import requests
from io import BytesIO
import wave
from utils.config_loader import ConfigLoader

class VoiceService:
    """语音交互服务 - 使用Qwen-Omini-Flash进行文本转语音"""

    def __init__(self):
        self.api_key = ConfigLoader.get_dashscope_api_key()
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model = "qwen3-omni-flash"

    def text_to_speech(self, text: str, voice: str = "Bilibili-DouDou") -> Optional[bytes]:
        """
        将文本转换为语音

        Args:
            text: 要转换的文本
            voice: 语音角色 (Bilibili-DouDou儿童声音)

        Returns:
            音频字节数据（WAV格式）
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                # 设置输出为文本+音频
                "modalities": ["text", "audio"],
                "audio": {
                    "voice": voice,
                    "format": "wav"
                },
                "stream": False
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                # 提取音频内容
                if 'choices' in data and len(data['choices']) > 0:
                    choice = data['choices'][0]
                    if 'message' in choice:
                        message = choice['message']
                        if 'audio' in message:
                            # 音频已经是base64编码
                            audio_base64 = message['audio']
                            audio_bytes = base64.b64decode(audio_base64)
                            return audio_bytes

            return None

        except Exception as e:
            print(f"语音生成失败: {str(e)}")
            return None

    def stream_text_to_speech(self, text: str, voice: str = "Bilibili-DouDou"):
        """
        流式生成语音（用于实时反馈）

        Args:
            text: 要转换的文本
            voice: 语音角色

        Yields:
            音频数据块
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "modalities": ["text", "audio"],
                "audio": {
                    "voice": voice,
                    "format": "wav"
                },
                "stream": True
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
                stream=True
            )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data:'):
                            data_str = line[5:].strip()
                            if data_str:
                                try:
                                    import json
                                    data = json.loads(data_str)

                                    if 'choices' in data and len(data['choices']) > 0:
                                        choice = data['choices'][0]
                                        if 'delta' in choice:
                                            delta = choice['delta']
                                            if 'audio' in delta:
                                                audio_base64 = delta['audio']
                                                audio_chunk = base64.b64decode(audio_base64)
                                                yield audio_chunk
                                except:
                                    pass

        except Exception as e:
            print(f"流式语音生成失败: {str(e)}")

    def create_wav_file(self, audio_chunks: list) -> bytes:
        """
        将音频块组合成WAV文件

        Args:
            audio_chunks: 音频数据块列表

        Returns:
            完整的WAV文件字节数据
        """
        try:
            # 合并所有音频块
            combined_audio = b''.join(audio_chunks)

            # 创建BytesIO对象
            buffer = BytesIO()

            # 写入WAV头
            with wave.open(buffer, 'wb') as wav_file:
                # 假设是16bit单声道WAV, 采样率16000Hz
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes(combined_audio)

            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            print(f"WAV文件创建失败: {str(e)}")
            return None

    def get_voice_options(self) -> dict:
        """获取可用的语音选项"""
        return {
            "Bilibili-DouDou": "👧 豆豆(儿童女声)",
            "Bilibili-XiaoXiao": "🧒 晓晓(儿童男声)",
            "Bilibili-Qingfeng": "🎤 青风(少年男声)",
            "Bilibili-Yuanzhao": "👦 元昭(小朋友声音)"
        }

    def validate_text(self, text: str) -> Tuple[bool, str]:
        """验证输入文本"""
        if not text:
            return False, "文本不能为空"
        if len(text) > 500:
            return False, "文本长度不能超过500字"
        return True, ""

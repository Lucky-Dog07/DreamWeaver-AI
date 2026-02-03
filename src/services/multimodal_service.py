import os
import base64
import json
import wave
from typing import Optional, Dict, Any, Tuple, List
from io import BytesIO
from PIL import Image
import requests
from openai import OpenAI
from utils.config_loader import ConfigLoader

class MultimodalService:
    """多模态分析服务 - 使用Qwen-Omini-Flash"""

    def __init__(self):
        self.api_key = ConfigLoader.get_dashscope_api_key()
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model = "qwen3-omni-flash"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def analyze_drawing(self, image_data: bytes, drawing_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        五维度分析绘画作品
        """
        try:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            analysis_prompt = self._build_analysis_prompt(drawing_info)
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                        {"type": "text", "text": analysis_prompt}
                    ]
                }
            ]

            text_content, _ = self._call_qwen_omini(messages, include_audio=False)
            return self._parse_analysis_response(text_content)
        except Exception as e:
            print(f"分析失败: {str(e)}")
            return self._get_default_analysis()

    def generate_spirit_feedback(self, image_data: bytes, drawing_info: Dict[str, Any], history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        生成小精灵的反馈结果（包含文字和音频）

        Args:
            image_data: 图片字节数据
            drawing_info: 绘画信息
            history: 历史对话记录，格式为 [{'role': 'user'|'assistant', 'content': '...'}]

        Returns:
            包含 'text' 和 'audio' (bytes) 的字典
        """
        try:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            feedback_prompt = self._build_spirit_feedback_prompt(drawing_info)

            messages = []
            
            # 添加历史记录
            if history:
                for item in history:
                    role = item.get('role')
                    content = item.get('content')
                    if role and content:
                        messages.append({
                            "role": role,
                            "content": [{"type": "text", "text": content}]
                        })

            # 添加当前轮次的输入
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": feedback_prompt
                    }
                ]
            })

            text_content, audio_data = self._call_qwen_omini(messages, include_audio=True)

            return {
                "text": text_content.strip(),
                "audio": audio_data
            }

        except Exception as e:
            print(f"生成反馈失败: {str(e)}")
            return {
                "text": "哇！你的画真有趣！继续加油！",
                "audio": None
            }

    def _build_analysis_prompt(self, drawing_info: Dict[str, Any]) -> str:
        """构建分析prompt"""
        prompt = f"""
你是一个专业的儿童艺术教育专家。请对这幅儿童画进行深度五维度分析。

绘画信息：
- 绘画时长: {drawing_info.get('duration', 0)}秒
- 笔画数: {drawing_info.get('stroke_count', 0)}
- 修改次数: {drawing_info.get('revision_count', 0)}

请返回JSON格式的分析结果，包含以下5个维度：

1. theme_analysis - 主题分析
   {{
     "main_theme": "主题描述",
     "elements": ["元素列表"],
     "story_hint": "可能的故事线索"
   }}

2. color_analysis - 色彩分析
   {{
     "dominant_colors": ["主要颜色"],
     "emotional_tone": "情感基调",
     "color_psychology": "色彩心理学解读"
   }}

3. composition_analysis - 构图分析
   {{
     "composition_type": "构图类型",
     "balance_score": 0-100,
     "focus_point": "视觉焦点描述"
   }}

4. emotional_analysis - 情感分析
   {{
     "primary_emotions": ["主要情感"],
     "expression_style": "表达风格",
     "confidence_level": "创作信心评估"
   }}

5. development_analysis - 发展阶段分析
   {{
     "stage": "发展阶段",
     "age_range": "适用年龄范围",
     "milestones": ["达成的里程碑"],
     "suggestions": ["发展建议"]
   }}

请确保返回有效的JSON格式。
"""
        return prompt

    def _build_spirit_feedback_prompt(self, drawing_info: Dict[str, Any]) -> str:
        """构建小精灵反馈prompt"""
        prompt = f"""
你是一个5-8岁孩子的绘画陪伴小精灵，名字叫"球球"。你调皮但博学，喜欢用孩子能理解的语言和他们聊天。

绘画过程特征：
- 绘画时长: {drawing_info.get('duration', 0)}秒
- 笔画数: {drawing_info.get('stroke_count', 0)}
- 修改次数: {drawing_info.get('revision_count', 0)}

请生成一条反馈，要求：
1. 使用5-8岁儿童能理解的语言
2. 长度不超过25字
3. 包含一个观察 + 一个开放式问题或鼓励
4. 语气亲切自然，像朋友聊天
5. 可以适当使用感叹号和问号增加趣味感

只返回反馈文本，不要返回其他内容。
"""
        return prompt

    def _call_qwen_omini(self, messages: List[Dict[str, Any]], include_audio: bool = False) -> Tuple[str, Optional[bytes]]:
        """调用Qwen-Omini-Flash API"""
        try:
            modalities = ["text", "audio"] if include_audio else ["text"]
            
            print(f"DEBUG: Calling {self.model} with modalities={modalities}")
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                modalities=modalities,
                audio={"voice": "Cherry", "format": "wav"} if include_audio else None,
                stream=True,
                stream_options={"include_usage": True}
            )

            full_text = ""
            audio_base64_chunks = []

            for chunk in completion:
                if not chunk.choices:
                    continue
                    
                delta = chunk.choices[0].delta
                
                # 处理文字
                content = getattr(delta, 'content', None)
                if content:
                    full_text += content
                
                # 处理音频
                if include_audio:
                    audio = getattr(delta, 'audio', None)
                    if audio:
                        # 兼容性：有些版本可能是 dict，有些是 object
                        data = None
                        if isinstance(audio, dict):
                            data = audio.get('data')
                        else:
                            data = getattr(audio, 'data', None)
                            
                        if data:
                            audio_base64_chunks.append(data)
                        
                        transcript = None
                        if isinstance(audio, dict):
                            transcript = audio.get('transcript')
                        else:
                            transcript = getattr(audio, 'transcript', None)
                            
                        if transcript and not full_text:
                            full_text += transcript

            print(f"DEBUG: Received text length: {len(full_text)}")
            if include_audio:
                print(f"DEBUG: Received audio chunks: {len(audio_base64_chunks)}")

            audio_data = None
            if include_audio and audio_base64_chunks:
                full_audio_base64 = "".join(audio_base64_chunks)
                pcm_data = base64.b64decode(full_audio_base64)
                # 将 PCM 转换为 WAV
                audio_data = self._pcm_to_wav(pcm_data)

            if not full_text and not audio_data:
                print("DEBUG: API returned empty response")

            return full_text, audio_data

        except Exception as e:
            import traceback
            print(f"API调用失败: {str(e)}")
            traceback.print_exc()
            return "", None

    def _pcm_to_wav(self, pcm_data: bytes, sample_rate: int = 24000, channels: int = 1, sample_width: int = 2) -> bytes:
        """将原始PCM数据转换为WAV格式"""
        try:
            from io import BytesIO
            with BytesIO() as wav_io:
                with wave.open(wav_io, 'wb') as wav_file:
                    wav_file.setnchannels(channels)
                    wav_file.setsampwidth(sample_width)
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(pcm_data)
                return wav_io.getvalue()
        except Exception as e:
            print(f"PCM转WAV失败: {e}")
            return pcm_data

    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """解析分析响应"""
        try:
            # 尝试提取JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                analysis = json.loads(json_str)
                return analysis
            else:
                return self._get_default_analysis()

        except Exception as e:
            print(f"解析失败: {str(e)}")
            return self._get_default_analysis()

    def _get_default_analysis(self) -> Dict[str, Any]:
        """获取默认分析结果"""
        return {
            "theme_analysis": {
                "main_theme": "创意作品",
                "elements": ["色彩", "形状"],
                "story_hint": "等待发现..."
            },
            "color_analysis": {
                "dominant_colors": ["未检测"],
                "emotional_tone": "正面",
                "color_psychology": "色彩丰富"
            },
            "composition_analysis": {
                "composition_type": "自由构图",
                "balance_score": 70,
                "focus_point": "整体作品"
            },
            "emotional_analysis": {
                "primary_emotions": ["快乐", "创意"],
                "expression_style": "自由表达",
                "confidence_level": "有信心"
            },
            "development_analysis": {
                "stage": "创意期",
                "age_range": "4-8岁",
                "milestones": ["大胆创作"],
                "suggestions": ["继续探索", "尝试新元素"]
            }
        }

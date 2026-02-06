import os
import base64
import json
from typing import Optional, Dict, Any
from io import BytesIO
from PIL import Image
import requests
from utils.config_loader import ConfigLoader

class MultimodalService:
    """多模态分析服务 - 使用Qwen-Omini-Flash"""

    def __init__(self):
        self.api_key = ConfigLoader.get_dashscope_api_key()
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model = "qwen3-omni-flash"

    def analyze_drawing(self, image_data: bytes, drawing_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        五维度分析绘画作品

        Args:
            image_data: 图片字节数据
            drawing_info: 绘画信息（时长、笔数等）

        Returns:
            分析结果字典
        """
        try:
            # 转换为base64
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # 构建分析prompt
            analysis_prompt = self._build_analysis_prompt(drawing_info)

            # 调用API
            response = self._call_qwen_omini(base64_image, analysis_prompt)

            # 解析结果
            return self._parse_analysis_response(response)

        except Exception as e:
            print(f"分析失败: {str(e)}")
            return self._get_default_analysis()

    def generate_spirit_feedback(self, image_data: bytes, drawing_info: Dict[str, Any]) -> str:
        """
        生成小精灵的反馈语音文本

        Args:
            image_data: 图片字节数据
            drawing_info: 绘画信息

        Returns:
            反馈文本
        """
        try:
            base64_image = base64.b64encode(image_data).decode('utf-8')

            feedback_prompt = self._build_spirit_feedback_prompt(drawing_info)

            response = self._call_qwen_omini(base64_image, feedback_prompt)

            return response.strip()

        except Exception as e:
            print(f"生成反馈失败: {str(e)}")
            return "哇！你的画真有趣！继续加油！"

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

    def _call_qwen_omini(self, base64_image: str, prompt: str) -> str:
        """调用Qwen-Omini-Flash API"""
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
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"API错误: {response.status_code}")
                return ""

        except Exception as e:
            print(f"API调用失败: {str(e)}")
            return ""

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

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json

@dataclass
class Stroke:
    """单笔笔触数据"""
    x: List[float]
    y: List[float]
    color: str
    width: float
    timestamp: float
    tool: str = "pen"  # pen, eraser, etc.

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'color': self.color,
            'width': self.width,
            'timestamp': self.timestamp,
            'tool': self.tool
        }

@dataclass
class DrawingData:
    """完整的绘画数据"""
    user_id: str
    strokes: List[Stroke] = field(default_factory=list)
    background_color: str = "#FFFFFF"
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = None
    duration: float = 0.0  # 绘画时长（秒）
    revision_count: int = 0  # 修改次数
    stroke_count: int = 0  # 笔画数
    canvas_width: int = 800
    canvas_height: int = 600

    def add_stroke(self, stroke: Stroke):
        """添加笔触"""
        self.strokes.append(stroke)
        self.stroke_count += 1

    def get_duration(self):
        """获取绘画时长"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'strokes': [s.to_dict() for s in self.strokes],
            'background_color': self.background_color,
            'start_time': self.start_time.isoformat(),
            'duration': self.get_duration(),
            'revision_count': self.revision_count,
            'stroke_count': self.stroke_count,
            'canvas_width': self.canvas_width,
            'canvas_height': self.canvas_height
        }

@dataclass
class Artwork:
    """完整的作品数据"""
    artwork_id: str
    user_id: str
    title: str = "未命名作品"
    description: str = ""
    drawing_data: DrawingData = None
    image_path: str = None  # 保存的图片路径
    created_at: datetime = field(default_factory=datetime.now)

    # AI分析结果
    theme_analysis: Dict[str, Any] = field(default_factory=dict)
    color_analysis: Dict[str, Any] = field(default_factory=dict)
    composition_analysis: Dict[str, Any] = field(default_factory=dict)
    emotional_analysis: Dict[str, Any] = field(default_factory=dict)
    development_analysis: Dict[str, Any] = field(default_factory=dict)

    # 生成的内容
    music_url: str = None
    music_path: str = None  # 本地音乐路径
    music_file_id: str = None
    voice_feedback: str = None
    voice_feedback_url: str = None
    video_url: str = None
    video_path: str = None  # 本地视频路径
    video_task_id: str = None

    # 元数据
    tags: List[str] = field(default_factory=list)
    is_public: bool = False

    def to_dict(self):
        return {
            'artwork_id': self.artwork_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'drawing_data': self.drawing_data.to_dict() if self.drawing_data else None,
            'image_path': self.image_path,
            'created_at': self.created_at.isoformat(),
            'theme_analysis': self.theme_analysis,
            'color_analysis': self.color_analysis,
            'composition_analysis': self.composition_analysis,
            'emotional_analysis': self.emotional_analysis,
            'development_analysis': self.development_analysis,
            'music_url': self.music_url,
            'music_path': self.music_path,
            'voice_feedback': self.voice_feedback,
            'voice_feedback_url': self.voice_feedback_url,
            'video_url': self.video_url,
            'video_path': self.video_path,
            'tags': self.tags,
            'is_public': self.is_public
        }

@dataclass
class AnalysisResult:
    """AI分析结果"""
    theme_analysis: Dict[str, Any]
    color_analysis: Dict[str, Any]
    composition_analysis: Dict[str, Any]
    emotional_analysis: Dict[str, Any]
    development_analysis: Dict[str, Any]

    def to_dict(self):
        return {
            'theme_analysis': self.theme_analysis,
            'color_analysis': self.color_analysis,
            'composition_analysis': self.composition_analysis,
            'emotional_analysis': self.emotional_analysis,
            'development_analysis': self.development_analysis
        }

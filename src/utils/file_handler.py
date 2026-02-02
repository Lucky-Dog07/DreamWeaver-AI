import os
import io
import base64
from datetime import datetime
from pathlib import Path
from PIL import Image
import streamlit as st

class FileHandler:
    """文件处理工具"""

    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.artworks_dir = self.base_dir / "artworks"
        self.cache_dir = self.base_dir / "cache"
        self.temp_dir = self.base_dir / "temp"

        # 创建必要的目录
        self._create_directories()

    def _create_directories(self):
        """创建必要的目录"""
        for dir_path in [self.artworks_dir, self.cache_dir, self.temp_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def save_image(
        self,
        image_data: bytes,
        user_id: str,
        artwork_id: str,
        subfolder: str = "original"
    ) -> str:
        """
        保存图片文件

        Args:
            image_data: 图片字节数据
            user_id: 用户ID
            artwork_id: 作品ID
            subfolder: 子文件夹名称

        Returns:
            保存路径
        """
        try:
            # 创建用户目录
            user_dir = self.artworks_dir / user_id / subfolder
            user_dir.mkdir(parents=True, exist_ok=True)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{artwork_id}_{timestamp}.png"
            filepath = user_dir / filename

            # 保存文件
            with open(filepath, 'wb') as f:
                f.write(image_data)

            return str(filepath)

        except Exception as e:
            print(f"图片保存失败: {str(e)}")
            return None

    def load_image(self, filepath: str) -> bytes:
        """加载图片文件"""
        try:
            with open(filepath, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"图片加载失败: {str(e)}")
            return None

    def image_to_base64(self, image_data: bytes) -> str:
        """将图片转换为Base64"""
        try:
            return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            print(f"Base64转换失败: {str(e)}")
            return None

    def base64_to_image(self, base64_str: str) -> bytes:
        """将Base64转换为图片"""
        try:
            return base64.b64decode(base64_str)
        except Exception as e:
            print(f"Base64解码失败: {str(e)}")
            return None

    def resize_image(self, image_data: bytes, max_width: int = 800, max_height: int = 600) -> bytes:
        """调整图片大小"""
        try:
            image = Image.open(io.BytesIO(image_data))

            # 计算缩放比例
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # 保存为字节
            output = io.BytesIO()
            image.save(output, format='PNG')
            return output.getvalue()

        except Exception as e:
            print(f"图片调整失败: {str(e)}")
            return image_data

    def optimize_image(self, image_data: bytes, quality: int = 85) -> bytes:
        """优化图片（压缩）"""
        try:
            image = Image.open(io.BytesIO(image_data))

            # 转换为RGB（如果有透明度）
            if image.mode in ('RGBA', 'LA', 'P'):
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = rgb_image

            # 保存为JPEG
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality, optimize=True)
            return output.getvalue()

        except Exception as e:
            print(f"图片优化失败: {str(e)}")
            return image_data

    def save_audio(
        self,
        audio_data: bytes,
        user_id: str,
        artwork_id: str,
        audio_type: str = "feedback"
    ) -> str:
        """
        保存音频文件

        Args:
            audio_data: 音频字节数据
            user_id: 用户ID
            artwork_id: 作品ID
            audio_type: 音频类型 (feedback, music)

        Returns:
            保存路径
        """
        try:
            user_dir = self.artworks_dir / user_id / "audio"
            user_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{artwork_id}_{audio_type}_{timestamp}.wav"
            filepath = user_dir / filename

            with open(filepath, 'wb') as f:
                f.write(audio_data)

            return str(filepath)

        except Exception as e:
            print(f"音频保存失败: {str(e)}")
            return None

    def load_audio(self, filepath: str) -> bytes:
        """加载音频文件"""
        try:
            with open(filepath, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"音频加载失败: {str(e)}")
            return None

    def save_json(self, data: dict, user_id: str, filename: str) -> str:
        """保存JSON文件"""
        try:
            import json
            user_dir = self.artworks_dir / user_id / "metadata"
            user_dir.mkdir(parents=True, exist_ok=True)

            filepath = user_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return str(filepath)

        except Exception as e:
            print(f"JSON保存失败: {str(e)}")
            return None

    def load_json(self, filepath: str) -> dict:
        """加载JSON文件"""
        try:
            import json
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"JSON加载失败: {str(e)}")
            return None

    def get_user_artworks(self, user_id: str) -> list:
        """获取用户所有作品"""
        try:
            user_dir = self.artworks_dir / user_id / "original"
            if not user_dir.exists():
                return []

            images = list(user_dir.glob("*.png"))
            return sorted(images, key=lambda x: x.stat().st_mtime, reverse=True)

        except Exception as e:
            print(f"获取作品列表失败: {str(e)}")
            return []

    def delete_artwork(self, user_id: str, artwork_id: str) -> bool:
        """删除作品"""
        try:
            import shutil
            artwork_dir = self.artworks_dir / user_id / "original"

            for file in artwork_dir.glob(f"{artwork_id}_*"):
                file.unlink()

            return True

        except Exception as e:
            print(f"删除作品失败: {str(e)}")
            return False

    def get_cache_file(self, key: str) -> bytes:
        """获取缓存文件"""
        try:
            filepath = self.cache_dir / f"{key}.cache"
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    return f.read()
            return None
        except Exception as e:
            print(f"缓存读取失败: {str(e)}")
            return None

    def set_cache_file(self, key: str, data: bytes) -> bool:
        """设置缓存文件"""
        try:
            filepath = self.cache_dir / f"{key}.cache"
            with open(filepath, 'wb') as f:
                f.write(data)
            return True
        except Exception as e:
            print(f"缓存保存失败: {str(e)}")
            return False

    def get_storage_size(self, user_id: str) -> int:
        """获取用户存储使用量（字节）"""
        try:
            user_dir = self.artworks_dir / user_id
            if not user_dir.exists():
                return 0

            total_size = sum(f.stat().st_size for f in user_dir.rglob('*') if f.is_file())
            return total_size

        except Exception as e:
            print(f"获取存储大小失败: {str(e)}")
            return 0

    def format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f}TB"

    def download_file(self, filepath: str, filename: str = None):
        """下载文件"""
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()

            if not filename:
                filename = Path(filepath).name

            st.download_button(
                label=f"📥 下载 {filename}",
                data=file_data,
                file_name=filename,
                mime="application/octet-stream"
            )

        except Exception as e:
            print(f"文件下载失败: {str(e)}")

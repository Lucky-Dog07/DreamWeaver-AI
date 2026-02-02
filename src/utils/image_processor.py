import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import io
from typing import Tuple, List

class ImageProcessor:
    """图像处理工具"""

    @staticmethod
    def extract_dominant_colors(image_data: bytes, num_colors: int = 5) -> List[Tuple[int, int, int]]:
        """
        提取图片的主要颜色

        Args:
            image_data: 图片字节数据
            num_colors: 要提取的颜色数量

        Returns:
            颜色列表 (RGB元组)
        """
        try:
            # 读取图片
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('RGB')

            # 调整大小以加快处理
            image.thumbnail((150, 150))

            # 将图片转换为numpy数组
            img_array = np.array(image)
            pixels = img_array.reshape((-1, 3))

            # 使用K-means聚类提取主要颜色
            pixels_float = np.float32(pixels)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv2.kmeans(pixels_float, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # 转换颜色为RGB
            colors = [(int(c[0]), int(c[1]), int(c[2])) for c in centers]
            return colors

        except Exception as e:
            print(f"提取颜色失败: {str(e)}")
            return [(128, 128, 128)]  # 返回默认灰色

    @staticmethod
    def detect_focus_point(image_data: bytes) -> Tuple[float, float]:
        """
        检测图片的视觉焦点

        Args:
            image_data: 图片字节数据

        Returns:
            焦点坐标 (x, y) 0-1之间的相对坐标
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('L')  # 转为灰度图

            img_array = np.array(image)

            # 使用Sobel边缘检测找出焦点
            sx = cv2.Sobel(img_array, cv2.CV_64F, 1, 0, ksize=3)
            sy = cv2.Sobel(img_array, cv2.CV_64F, 0, 1, ksize=3)
            edge_magnitude = np.sqrt(sx**2 + sy**2)

            # 找出最大边缘强度的位置
            y, x = np.unravel_index(np.argmax(edge_magnitude), edge_magnitude.shape)

            # 转换为相对坐标
            height, width = img_array.shape
            return (x / width, y / height)

        except Exception as e:
            print(f"焦点检测失败: {str(e)}")
            return (0.5, 0.5)  # 返回中心点

    @staticmethod
    def calculate_balance_score(image_data: bytes) -> float:
        """
        计算图片的构图平衡分数

        Args:
            image_data: 图片字节数据

        Returns:
            0-100的平衡分数
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('L')

            img_array = np.array(image)
            height, width = img_array.shape

            # 计算左右和上下的色彩分布
            left_half = img_array[:, :width//2].sum()
            right_half = img_array[:, width//2:].sum()
            top_half = img_array[:height//2, :].sum()
            bottom_half = img_array[height//2:, :].sum()

            # 计算平衡度
            horizontal_balance = 1 - abs(left_half - right_half) / max(left_half + right_half, 1)
            vertical_balance = 1 - abs(top_half - bottom_half) / max(top_half + bottom_half, 1)

            balance_score = (horizontal_balance + vertical_balance) / 2 * 100

            return min(balance_score, 100)

        except Exception as e:
            print(f"平衡分数计算失败: {str(e)}")
            return 50

    @staticmethod
    def create_thumbnail(image_data: bytes, size: Tuple[int, int] = (200, 200)) -> bytes:
        """
        创建缩略图

        Args:
            image_data: 图片字节数据
            size: 缩略图大小

        Returns:
            缩略图字节数据
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail(size, Image.Resampling.LANCZOS)

            output = io.BytesIO()
            image.save(output, format='PNG')
            return output.getvalue()

        except Exception as e:
            print(f"缩略图创建失败: {str(e)}")
            return image_data

    @staticmethod
    def add_watermark(image_data: bytes, text: str = "DreamWeaver") -> bytes:
        """
        添加水印

        Args:
            image_data: 图片字节数据
            text: 水印文本

        Returns:
            添加水印后的图片字节数据
        """
        try:
            image = Image.open(io.BytesIO(image_data))

            # 创建透明图层用于水印
            watermark = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark)

            # 在右下角添加水印
            width, height = image.size
            text_x = width - 150
            text_y = height - 40

            draw.text((text_x, text_y), text, fill=(200, 200, 200, 100))

            # 合并图片
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            watermarked = Image.alpha_composite(image, watermark)

            output = io.BytesIO()
            watermarked.save(output, format='PNG')
            return output.getvalue()

        except Exception as e:
            print(f"水印添加失败: {str(e)}")
            return image_data

    @staticmethod
    def apply_artistic_effect(image_data: bytes, effect_type: str = "oil_painting") -> bytes:
        """
        应用艺术效果

        Args:
            image_data: 图片字节数据
            effect_type: 效果类型 (oil_painting, cartoon, pencil_sketch)

        Returns:
            处理后的图片字节数据
        """
        try:
            # 读取图片
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if effect_type == "oil_painting":
                # 油画效果
                result = cv2.xphoto.oilPainting(img, 7, 1)

            elif effect_type == "cartoon":
                # 卡通效果
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                result = cv2.bitwise_and(img, img, mask=edges)

            elif effect_type == "pencil_sketch":
                # 铅笔素描效果
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                inv_gray = cv2.bitwise_not(gray)
                result = cv2.GaussianBlur(inv_gray, (21, 21), 0)
                result = cv2.divide(gray, 255 - result, scale=256)

            else:
                result = img

            # 转换为字节数据
            _, buffer = cv2.imencode('.png', result)
            return buffer.tobytes()

        except Exception as e:
            print(f"艺术效果应用失败: {str(e)}")
            return image_data

    @staticmethod
    def detect_scene_type(image_data: bytes) -> str:
        """
        检测图片场景类型

        Args:
            image_data: 图片字节数据

        Returns:
            场景类型字符串
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            image = image.convert('L')
            img_array = np.array(image)

            # 简单的场景检测
            mean_brightness = np.mean(img_array)
            std_brightness = np.std(img_array)

            if std_brightness < 20:
                return "uniform"  # 单调场景
            elif mean_brightness > 200:
                return "bright"  # 明亮场景
            elif mean_brightness < 50:
                return "dark"  # 暗色场景
            else:
                return "normal"  # 正常场景

        except Exception as e:
            print(f"场景检测失败: {str(e)}")
            return "unknown"

    @staticmethod
    def generate_palette(image_data: bytes, num_colors: int = 8) -> dict:
        """
        生成图片的调色板

        Args:
            image_data: 图片字节数据
            num_colors: 调色板颜色数

        Returns:
            包含颜色和名称的字典
        """
        try:
            colors = ImageProcessor.extract_dominant_colors(image_data, num_colors)

            # 颜色名称映射
            color_names = {
                (255, 0, 0): "红色",
                (0, 255, 0): "绿色",
                (0, 0, 255): "蓝色",
                (255, 255, 0): "黄色",
                (255, 0, 255): "紫色",
                (0, 255, 255): "青色",
                (255, 165, 0): "橙色",
                (128, 0, 0): "深红",
                (0, 128, 0): "深绿",
                (0, 0, 128): "深蓝"
            }

            palette = []
            for color in colors:
                # 找最接近的颜色名称
                nearest_color = min(color_names.keys(),
                                  key=lambda x: sum((a-b)**2 for a, b in zip(color, x))**0.5)
                palette.append({
                    "rgb": color,
                    "hex": "#{:02x}{:02x}{:02x}".format(*color),
                    "name": color_names.get(nearest_color, "自定义色")
                })

            return {"palette": palette, "dominant_color": palette[0] if palette else None}

        except Exception as e:
            print(f"调色板生成失败: {str(e)}")
            return {"palette": [], "dominant_color": None}

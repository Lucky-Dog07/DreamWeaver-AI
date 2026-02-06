import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.coze_service import CozeService

def test_generate_video_from_image():
    coze_service = CozeService()
    
    image_path = os.path.join(os.path.dirname(__file__), "test.png")
    
    print(f"读取图片: {image_path}")
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    print("上传图片到 Coze...")
    file_id = coze_service.upload_image_to_coze(image_bytes, "test.png")
    
    if not file_id:
        print("图片上传失败")
        return
    
    print(f"图片上传成功，文件ID: {file_id}")
    
    print("开始生成视频...")
    result = coze_service.generate_video_from_image(file_id)
    
    print("\n生成结果:")
    print(f"状态: {result.get('status')}")
    
    if result.get('status') == 'success':
        print(f"视频URL: {result.get('video_url')}")
    else:
        print(f"错误: {result.get('error')}")

if __name__ == "__main__":
    test_generate_video_from_image()

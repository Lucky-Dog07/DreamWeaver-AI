import os
import sys

# 将 src 目录添加到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from services.multimodal_service import MultimodalService

def test_spirit_feedback():
    print("开始测试 generate_spirit_feedback...")
    
    # 1. 初始化服务
    try:
        service = MultimodalService()
    except Exception as e:
        print(f"初始化服务失败: {e}")
        return
    
    # 2. 读取测试图片
    image_path = os.path.join(current_dir, "test.png")
    if not os.path.exists(image_path):
        print(f"错误: 找不到测试图片 {image_path}")
        return
    
    print(f"读取图片: {image_path}")
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    # 3. 准备绘画信息
    drawing_info = {
        "duration": 120,
        "stroke_count": 50,
        "revision_count": 5
    }
    
    # 4. 调用生成反馈
    print("正在生成反馈内容（包含文字和音频）...")
    result = service.generate_spirit_feedback(image_data, drawing_info)
    
    # 5. 解析并验证结果
    text = result.get("text")
    audio = result.get("audio")
    
    print("\n" + "="*20)
    print("测试结果")
    print("="*20)
    print(f"反馈文字: {text}")
    
    if audio:
        audio_size = len(audio)
        print(f"音频数据已接收，大小: {audio_size} 字节")
        
        # 保存音频文件以供验证
        output_path = os.path.join(current_dir, "test_feedback_output.wav")
        with open(output_path, "wb") as f:
            f.write(audio)
        print(f"音频已成功保存至: {output_path}")
        
        # 简单的解析测试：检查是否为有效的 wav (前4字节为 RIFF)
        if audio.startswith(b'RIFF'):
            print("解析验证: 音频格式确认为 WAV (RIFF header)")
        else:
            print("解析验证: 音频格式可能不是标准的 WAV")
    else:
        print("警告: 未收到音频数据")
    print("="*20)

if __name__ == "__main__":
    test_spirit_feedback()

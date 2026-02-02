import sys
import os

# 将项目根目录和 src 目录添加到 python 路径
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, "src"))

from services.coze_service import CozeService

def test_generate_voice_comment():
    service = CozeService()
    
    # 用户提供的 File ID
    image_file_id = "7602131782314115081"
    
    print(f"正在测试 generate_voice_comment, File ID: {image_file_id}...")
    print(f"使用的工作流 ID: {service.comment_workflow_id}")
    
    result = service.generate_voice_comment(image_file_id)
    
    if result and result.get("status") == "success":
        print("\n✅ 测试成功！")
        print(f"点评音频 URL: {result.get('comment_url')}")
        print(f"点评文本: {result.get('comment_text')}")
        print(f"完整响应数据: {result.get('raw_data')}")
    else:
        print("\n❌ 测试失败！")
        print(f"错误信息: {result.get('error') if result else '未知错误'}")

if __name__ == "__main__":
    test_generate_voice_comment()

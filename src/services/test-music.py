import sys
import os

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_dir)

from services.coze_service import CozeService


def test_generate_music_from_image():
    """测试从图片生成音乐功能"""
    
    print("=" * 60)
    print("测试 CozeService.generate_music_from_image")
    print("=" * 60)
    
    try:
        coze_service = CozeService()
        
        image_file_id = "7602131782314115081"
        
        print(f"\n输入参数:")
        print(f"  - Image File ID: {image_file_id}")
        print(f"  - Workflow ID: {coze_service.music_workflow_id}")
        
        print("\n开始调用工作流...")
        result = coze_service.generate_music_from_image(image_file_id)
        
        print("\n" + "=" * 60)
        print("执行结果:")
        print("=" * 60)
        
        if result:
            print(f"状态: {result.get('status')}")
            
            if result.get('status') == 'success':
                print(f"音乐URL: {result.get('music_url')}")
                print(f"情感: {result.get('emotion')}")
                print(f"工作流ID: {result.get('workflow_id')}")
            else:
                print(f"错误信息: {result.get('error')}")
        else:
            print("返回结果为空")
        
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"\n测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_generate_music_from_image()

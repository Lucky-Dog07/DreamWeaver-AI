import shutil
from pathlib import Path
import json

def migrate_artworks():
    """将旧UUID用户文件夹的内容迁移到default_user文件夹"""
    
    artworks_dir = Path("data/artworks")
    target_user = "default_user"
    target_dir = artworks_dir / target_user
    
    # 确保目标目录存在
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取所有旧用户文件夹（排除default_user）
    old_users = [d for d in artworks_dir.iterdir() 
                 if d.is_dir() and d.name != target_user]
    
    if not old_users:
        print("没有发现需要迁移的旧用户数据")
        return
    
    print(f"发现 {len(old_users)} 个旧用户文件夹需要迁移")
    
    # 统计信息
    total_files = 0
    migrated_files = 0
    skipped_files = 0
    
    for old_user_dir in old_users:
        print(f"\n正在处理用户: {old_user_dir.name}")
        
        # 遍历旧用户目录下的所有文件
        for old_file in old_user_dir.rglob("*"):
            if not old_file.is_file():
                continue
            
            total_files += 1
            
            # 计算相对路径
            rel_path = old_file.relative_to(old_user_dir)
            
            # 目标文件路径
            target_file = target_dir / rel_path
            
            # 检查文件是否已存在
            if target_file.exists():
                # 如果是JSON文件，尝试合并
                if old_file.suffix == '.json':
                    try:
                        with open(old_file, 'r', encoding='utf-8') as f:
                            old_data = json.load(f)
                        with open(target_file, 'r', encoding='utf-8') as f:
                            target_data = json.load(f)
                        
                        # 合并数据（以旧数据为主，保留target中可能更新的字段）
                        merged_data = {**target_data, **old_data}
                        
                        with open(target_file, 'w', encoding='utf-8') as f:
                            json.dump(merged_data, f, ensure_ascii=False, indent=2)
                        
                        print(f"  合并JSON: {rel_path}")
                        migrated_files += 1
                    except Exception as e:
                        print(f"  跳过JSON合并失败: {rel_path} - {e}")
                        skipped_files += 1
                else:
                    # 对于非JSON文件，如果已存在则跳过
                    print(f"  跳过已存在: {rel_path}")
                    skipped_files += 1
            else:
                # 创建目标目录
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制文件
                shutil.copy2(old_file, target_file)
                print(f"  迁移: {rel_path}")
                migrated_files += 1
    
    print(f"\n迁移完成！")
    print(f"总文件数: {total_files}")
    print(f"已迁移: {migrated_files}")
    print(f"已跳过: {skipped_files}")
    
    # 询问是否删除旧文件夹
    print(f"\n旧用户文件夹仍然保留在: {artworks_dir}")
    print(f"如需删除旧文件夹，请手动删除以下目录:")
    for old_user in old_users:
        print(f"  - {old_user.name}")

if __name__ == "__main__":
    migrate_artworks()

import json
import os
from pathlib import Path

class SaveManager:
    def __init__(self):
        """初始化存档管理器"""
        # 确保存档目录存在
        save_dir = Path('saves')
        save_dir.mkdir(exist_ok=True)
        
        # 设置存档文件路径
        self.save_path = save_dir / 'game_save.json'
        print(f"[SaveManager] 初始化 - 存档路径: {self.save_path}")
    
    def has_save(self) -> bool:
        """检查是否存在存档"""
        exists = self.save_path.exists()
        print(f"[SaveManager] 检查存档状态: {'存在' if exists else '不存在'}")
        return exists
    
    def save_game(self, data: dict) -> bool:
        """保存游戏数据
        
        Args:
            data: 包含游戏状态的字典
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 添加版本信息
            save_data = {
                "version": "1.0",
                "data": data
            }
            
            # 确保存档目录存在
            self.save_path.parent.mkdir(exist_ok=True)
            
            # 保存数据
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print("[SaveManager] 保存游戏成功")
            return True
            
        except Exception as e:
            print(f"[SaveManager] 保存游戏失败: {str(e)}")
            return False
    
    def load_game(self) -> dict:
        """加载游戏数据
        
        Returns:
            dict: 游戏数据，如果加载失败返回None
        """
        try:
            if not self.has_save():
                print("[SaveManager] 没有找到存档文件")
                return None
            
            with open(self.save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            # 检查版本
            if save_data.get("version") != "1.0":
                print("[SaveManager] 存档版本不兼容")
                return None
            
            print("[SaveManager] 加载游戏成功")
            return save_data["data"]
            
        except Exception as e:
            print(f"[SaveManager] 加载游戏失败: {str(e)}")
            return None
    
    def delete_save(self) -> bool:
        """删除存档
        
        Returns:
            bool: 删除是否成功
        """
        try:
            if self.has_save():
                os.remove(self.save_path)
                print("[SaveManager] 删除存档成功")
                return True
            return False
        except Exception as e:
            print(f"[SaveManager] 删除存档失败: {str(e)}")
            return False 
import pygame
import os
from pathlib import Path

class FontManager:
    _instance = None
    _fonts = {}

    @staticmethod
    def get_instance():
        if FontManager._instance is None:
            FontManager._instance = FontManager()
        return FontManager._instance

    def __init__(self):
        if FontManager._instance is not None:
            raise Exception("FontManager 是单例类，请使用 get_instance() 方法获取实例")
        FontManager._instance = self

    def get_font(self, size: int = 24) -> pygame.font.Font:
        """获取指定大小的字体
        
        Args:
            size: 字体大小，默认24
            
        Returns:
            pygame.font.Font: 字体对象
        """
        if size not in self._fonts:
            try:
                # 使用 Path 对象处理路径
                font_path = Path(__file__).parent.parent.parent / "assets" / "fonts" / "SourceHanSans-Bold.ttc"
                if not font_path.exists():
                    print(f"[FontManager] 警告: 字体文件不存在: {font_path}")
                    # 尝试使用系统默认字体
                    self._fonts[size] = pygame.font.SysFont("simhei", size)
                else:
                    print(f"[FontManager] 加载字体文件: {font_path}")
                    self._fonts[size] = pygame.font.Font(str(font_path), size)
            except Exception as e:
                print(f"[FontManager] 字体加载错误: {e}")
                # 出错时使用系统默认字体
                self._fonts[size] = pygame.font.SysFont("simhei", size)
        
        return self._fonts[size] 
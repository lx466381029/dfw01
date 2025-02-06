import pygame
import math
from typing import List, Tuple
import os
from pathlib import Path
from utils.font_manager import FontManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, cell_size: int):
        super().__init__()
        # 加载角色图片
        image_path = os.path.join("assets", "images", "characters", "character.png")
        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.cell_size = cell_size
        self.border_width = 5  # 添加边框宽度属性
        
        # 名称相关
        self.name = "冒险者"
        self.name_font = FontManager.get_instance().get_font(24)
        self.name_color = (33, 33, 33)  # 深灰色
        self.name_editing = False
        self.name_surface = None
        self.name_underline = None  # 添加下划线表面
        self._update_name_surface()
        
        # 位置信息
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.current_cell = 0  # 当前所在格子索引
        
        # 移动动画参数
        self.is_moving = False
        self.move_progress = 0
        self.move_duration = 300  # 300ms
        self.move_start_time = 0
        self.move_path: List[Tuple[int, int]] = []
        
        # 初始化位置
        self._update_rect_position()
        
    def _update_name_surface(self):
        """更新名称的渲染表面"""
        # 渲染名称文本
        self.name_surface = self.name_font.render(self.name, True, self.name_color)
        
        # 创建下划线
        underline_height = 2
        underline_surface = pygame.Surface((self.name_surface.get_width(), underline_height))
        underline_surface.fill(self.name_color)
        self.name_underline = underline_surface

    def set_name(self, name: str):
        """设置角色名称"""
        if name.strip():  # 确保名称不是空白
            self.name = name.strip()
            self._update_name_surface()

    def toggle_name_editing(self):
        """切换名称编辑状态"""
        self.name_editing = not self.name_editing
        self._update_name_surface()

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """处理点击事件"""
        # 计算名称显示区域
        name_rect = self.name_surface.get_rect()
        name_rect.topleft = (self.rect.x, self.rect.y - 30)  # 在角色上方显示
        return name_rect.collidepoint(pos)

    def update(self, current_time: int):
        if not self.is_moving:
            return
            
        # 计算动画进度
        elapsed = current_time - self.move_start_time
        progress = min(1.0, elapsed / self.move_duration)
        
        if progress >= 1.0:
            # 移动完成
            if self.move_path:
                self.start_next_move(current_time)
            else:
                print("[Player] 移动完成")
                self.is_moving = False
                self.x = self.target_x
                self.y = self.target_y
        else:
            # 使用缓动函数使移动更平滑
            smoothed_progress = self._ease_out_quad(progress)
            self.x = self._lerp(self.x, self.target_x, smoothed_progress)
            self.y = self._lerp(self.y, self.target_y, smoothed_progress)
        
        # 更新矩形位置
        self._update_rect_position()
        
    def move_to(self, path: List[Tuple[int, int]], current_time: int):
        """开始沿着路径移动"""
        if not path:
            print("[Player] 错误: 收到空路径")
            return
            
        print(f"[Player] 开始移动 - {len(path)}步")
        self.move_path = path[1:]  # 第一个点是当前位置
        self.start_next_move(current_time)
        
    def start_next_move(self, current_time: int):
        """开始移动到路径中的下一个点"""
        if not self.move_path:
            print("[Player] 警告: 没有更多的移动点")
            return
            
        next_pos = self.move_path.pop(0)
        self.target_x = next_pos[0]  # 已经在GameBoard中计算好的实际像素坐标
        self.target_y = next_pos[1]
        self.is_moving = True
        self.move_start_time = current_time
        print(f"[Player] 移动到新位置 - 目标: ({self.target_x}, {self.target_y})")
        
    def _update_rect_position(self):
        """更新精灵的矩形位置，确保居中
        
        计算方式：
        1. 使用给定的x,y坐标作为中心点
        2. 直接设置精灵的中心点位置
        """
        # 直接使用给定的坐标作为中心点
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
    def _ease_out_quad(self, t: float) -> float:
        """缓动函数：渐出二次方"""
        return -t * (t - 2)
        
    def _lerp(self, start: float, end: float, t: float) -> float:
        """线性插值"""
        return start + (end - start) * t
        
    def draw(self, screen: pygame.Surface):
        """绘制英雄"""
        # 绘制角色
        screen.blit(self.image, self.rect) 
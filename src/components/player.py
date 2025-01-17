import pygame
import math
from typing import List, Tuple

class Player:
    def __init__(self, x: int, y: int, cell_size: int):
        # 加载英雄图片
        self.image = pygame.image.load('assets/images/role/baby.png')
        # 缩放图片以适应格子大小（格子大小的80%）
        self.image_size = int(cell_size * 0.8)
        self.image = pygame.transform.scale(self.image, (self.image_size, self.image_size))
        self.rect = self.image.get_rect()
        self.cell_size = cell_size
        
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
        """更新精灵的矩形位置，确保居中"""
        # 计算图片在格子中的偏移量，使其居中
        offset = (self.cell_size - self.image_size) // 2
        self.rect.x = self.x + offset
        self.rect.y = self.y + offset
        
    def _ease_out_quad(self, t: float) -> float:
        """缓动函数：渐出二次方"""
        return -t * (t - 2)
        
    def _lerp(self, start: float, end: float, t: float) -> float:
        """线性插值"""
        return start + (end - start) * t
        
    def draw(self, screen: pygame.Surface):
        """绘制英雄"""
        screen.blit(self.image, self.rect) 
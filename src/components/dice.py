import pygame
import random
import math
import time

class Dice:
    def __init__(self, x, y):
        # 基础属性
        self.x = x
        self.y = y
        self.size = 80  # 骰子大小
        self.click_area = 180  # 点击响应区域
        
        # 颜色定义
        self.colors = {
            'dice': pygame.Color('#FFFFFF'),
            'border': pygame.Color('#424242'),
            'dots': pygame.Color('#1976D2'),
            'shadow': pygame.Color(0, 0, 0, 50),
            'click_area': pygame.Color(0, 0, 0, 80),  # 半透明黑色
            'click_area_hover': pygame.Color(0, 0, 0, 90)  # 鼠标悬停时的颜色
        }
        
        # 动画状态
        self.is_rolling = False
        self.roll_start_time = 0
        self.roll_duration = 1.5  # 秒
        self.current_value = 1
        self.target_value = 1
        self.rotation_angle = 0
        self.scale = 1.0
        
        # 交互状态
        self.is_hovered = False
        self.click_feedback_time = 0
        self.click_feedback_duration = 0.1  # 点击反馈持续时间
        
        # 点数位置配置
        self.dot_positions = {
            1: [(0.5, 0.5)],
            2: [(0.3, 0.3), (0.7, 0.7)],
            3: [(0.3, 0.3), (0.5, 0.5), (0.7, 0.7)],
            4: [(0.3, 0.3), (0.3, 0.7), (0.7, 0.3), (0.7, 0.7)],
            5: [(0.3, 0.3), (0.3, 0.7), (0.5, 0.5), (0.7, 0.3), (0.7, 0.7)],
            6: [(0.3, 0.3), (0.3, 0.5), (0.3, 0.7), (0.7, 0.3), (0.7, 0.5), (0.7, 0.7)]
        }
    
    def _ease_in_out_quad(self, t):
        """二次方缓动函数"""
        if t < 0.5:
            return 2 * t * t
        return -1 + (4 - 2 * t) * t
    
    def roll(self):
        """开始骰子投掷动画"""
        if not self.is_rolling:
            self.is_rolling = True
            self.roll_start_time = time.time()
            self.target_value = random.randint(1, 6)
            self.rotation_angle = 0
            # 添加点击反馈
            self.click_feedback_time = time.time()
    
    def update(self):
        """更新骰子状态"""
        if self.is_rolling:
            current_time = time.time()
            elapsed = current_time - self.roll_start_time
            progress = min(elapsed / self.roll_duration, 1.0)
            
            # 使用缓动函数计算动画进度
            eased_progress = self._ease_in_out_quad(progress)
            
            # 更新旋转角度
            self.rotation_angle = eased_progress * 720  # 旋转两圈
            
            # 更新缩放
            self.scale = 1.0 - 0.1 * math.sin(progress * math.pi)
            
            # 检查动画是否结束
            if progress >= 1.0:
                self.is_rolling = False
                self.current_value = self.target_value
                self.rotation_angle = 0
                self.scale = 1.0
    
    def draw(self, screen):
        """绘制骰子"""
        # 绘制点击响应区域
        click_area_rect = pygame.Rect(self.x, self.y, self.click_area, self.click_area)
        
        # 根据状态选择颜色
        if self.is_rolling:
            area_color = self.colors['click_area_hover']
        elif self.is_hovered:
            area_color = self.colors['click_area_hover']
        else:
            area_color = self.colors['click_area']
        
        # 绘制点击区域背景
        pygame.draw.rect(screen, area_color, click_area_rect, border_radius=10)
        pygame.draw.rect(screen, self.colors['border'], click_area_rect, width=2, border_radius=10)
        
        # 计算骰子的实际位置（考虑缩放）
        actual_size = int(self.size * self.scale)
        center_x = self.x + self.click_area // 2
        center_y = self.y + self.click_area // 2
        
        # 创建一个临时surface来绘制骰子
        dice_surface = pygame.Surface((actual_size, actual_size), pygame.SRCALPHA)
        
        # 绘制阴影
        shadow_rect = pygame.Rect(2, 2, actual_size, actual_size)
        pygame.draw.rect(dice_surface, self.colors['shadow'], shadow_rect, border_radius=8)
        
        # 绘制骰子主体
        dice_rect = pygame.Rect(0, 0, actual_size, actual_size)
        pygame.draw.rect(dice_surface, self.colors['dice'], dice_rect, border_radius=8)
        pygame.draw.rect(dice_surface, self.colors['border'], dice_rect, width=2, border_radius=8)
        
        # 绘制点数
        dot_radius = actual_size // 10
        for pos in self.dot_positions[self.current_value]:
            x = int(pos[0] * actual_size)
            y = int(pos[1] * actual_size)
            pygame.draw.circle(dice_surface, self.colors['dots'], (x, y), dot_radius)
        
        # 旋转骰子
        if self.is_rolling:
            rotated_surface = pygame.transform.rotate(dice_surface, self.rotation_angle)
            rot_rect = rotated_surface.get_rect(center=(center_x, center_y))
            screen.blit(rotated_surface, rot_rect)
        else:
            dice_rect = dice_surface.get_rect(center=(center_x, center_y))
            screen.blit(dice_surface, dice_rect)
    
    def handle_click(self, pos):
        """处理点击事件"""
        click_rect = pygame.Rect(self.x, self.y, self.click_area, self.click_area)
        if click_rect.collidepoint(pos):
            if not self.is_rolling:
                self.roll()
                return True
        return False
    
    def handle_motion(self, pos):
        """处理鼠标移动事件"""
        click_rect = pygame.Rect(self.x, self.y, self.click_area, self.click_area)
        self.is_hovered = click_rect.collidepoint(pos)
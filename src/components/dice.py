import pygame
import random
from typing import Optional, Callable, Tuple
import time

class Dice:
    """骰子系统类
    
    实现1-6点数的骰子功能，包含投掷动画
    """
    def __init__(self, x: int, y: int):
        # 基础属性
        self.x = x
        self.y = y
        self.size = 80  # 骰子大小
        self.click_area = 180  # 点击响应区域
        
        # 动画状态
        self.is_rolling = False
        self.roll_frames = 0
        self.max_roll_frames = 60  # 1.5秒 * 60帧 = 90帧
        self.value = 1
        self.rotation_angle = 0.0
        self.rotation_speed = 0.0
        self.last_update_time = 0
        
        # 回调函数
        self.roll_callback: Optional[Callable[[int], None]] = None
        
        # 预渲染骰子图像
        self.dice_images = []
        self._create_dice_images()
        
        # 交互状态
        self.is_hovered = False
        self.click_scale = 1.0
        
        print("骰子初始化完成")
    
    def _create_dice_images(self):
        """预渲染所有骰子状态的图像"""
        for value in range(1, 7):
            # 创建骰子表面
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            
            # 绘制骰子主体（白色带圆角的矩形）
            pygame.draw.rect(surface, (255, 255, 255), (0, 0, self.size, self.size), border_radius=8)
            
            # 绘制边框
            pygame.draw.rect(surface, (66, 66, 66), (0, 0, self.size, self.size), width=2, border_radius=8)
            
            # 绘制点数
            self._draw_dots(surface, value)
            
            self.dice_images.append(surface)
        #print(f"预渲染完成: 生成了 {len(self.dice_images)} 个骰子图像")
    
    def _draw_dots(self, surface: pygame.Surface, value: int):
        """在骰子表面绘制点数"""
        dot_positions = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
            6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5), (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)]
        }
        
        dot_radius = self.size // 10
        
        # 根据点数选择颜色
        if value in [1, 4]:
            dot_color = (220, 20, 20)  # 红色
        else:
            dot_color = (25, 118, 210)  # 蓝色
        
        for px, py in dot_positions[value]:
            x = int(px * self.size)
            y = int(py * self.size)
            # 绘制点的阴影
            pygame.draw.circle(surface, (0, 0, 0, 30), (x+1, y+1), dot_radius)
            # 绘制点
            pygame.draw.circle(surface, dot_color, (x, y), dot_radius)
    
    def roll(self, callback: Optional[Callable[[int], None]] = None):
        """开始骰子投掷动画"""
        if not self.is_rolling:
            print("[Dice] 开始投掷动画")
            self.is_rolling = True
            self.roll_frames = 0
            self.rotation_angle = 0.0
            self.rotation_speed = 720.0  # 初始旋转速度（每秒720度，即每秒2圈）
            self.last_update_time = time.time()
            self.roll_callback = callback
            self.click_scale = 0.95
    
    def update(self):
        """更新骰子状态"""
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # 更新点击缩放效果
        if self.click_scale < 1.0:
            self.click_scale += 0.01
            if self.click_scale > 1.0:
                self.click_scale = 1.0
        
        # 更新投掷动画
        if self.is_rolling:
            self.roll_frames += 1
            
            # 计算动画进度（0到1之间）
            progress = min(self.roll_frames / self.max_roll_frames, 1.0)
            
            # 更新旋转速度（使用缓动函数使其平滑减速）
            self.rotation_speed = 720.0 * (1.0 - progress * progress)  # 使用平方函数实现更自然的减速
            
            # 更新旋转角度，确保最终角度是90的倍数
            rotation_delta = self.rotation_speed * dt
            self.rotation_angle = (self.rotation_angle + rotation_delta)
            
            # 如果接近结束，确保最终角度是90的倍数
            if progress > 0.9:
                target_angle = round(self.rotation_angle / 90) * 90
                self.rotation_angle = self.rotation_angle * 0.8 + target_angle * 0.2
            
            # 保持角度在0-360度之间
            self.rotation_angle = self.rotation_angle % 360
            
            if self.roll_frames < self.max_roll_frames:
                # 骰子滚动时随机显示点数
                if self.roll_frames % 3 == 0:  # 每3帧改变一次点数
                    self.value = random.randint(1, 6)
            else:
                # 停止滚动，确定最终点数
                final_value = random.randint(1, 6)
                print(f"[Dice] 动画结束 - 最终点数: {final_value}")
                self.value = final_value
                self.is_rolling = False
                self.rotation_speed = 0
                # 确保最终角度是90的倍数
                self.rotation_angle = round(self.rotation_angle / 90) * 90
                if self.roll_callback:
                    self.roll_callback(final_value)  # 使用final_value而不是self.value
    
    def draw(self, screen: pygame.Surface):
        """绘制骰子"""
        # 绘制点击响应区域
        click_area_rect = pygame.Rect(self.x, self.y, self.click_area, self.click_area)
        
        # 根据状态选择颜色
        if self.is_rolling:
            area_color = (0, 0, 0, 40)
        elif self.is_hovered:
            area_color = (0, 0, 0, 30)
        else:
            area_color = (0, 0, 0, 20)
        
        # 绘制点击区域背景
        pygame.draw.rect(screen, area_color, click_area_rect, border_radius=10)
        pygame.draw.rect(screen, (66, 66, 66), click_area_rect, width=2, border_radius=10)
        
        # 计算骰子的实际位置和大小
        actual_size = int(self.size * self.click_scale)
        center_x = self.x + self.click_area // 2
        center_y = self.y + self.click_area // 2
        
        try:
            # 获取当前点数的骰子图像并缩放
            dice_surface = pygame.transform.scale(
                self.dice_images[self.value - 1],
                (actual_size, actual_size)
            )
            
            # 如果正在滚动，添加旋转效果
            if self.is_rolling or self.rotation_angle != 0:
                dice_surface = pygame.transform.rotate(dice_surface, self.rotation_angle)
            
            # 绘制骰子
            dice_rect = dice_surface.get_rect(center=(center_x, center_y))
            screen.blit(dice_surface, dice_rect)
            
        except Exception as e:
            print(f"绘制骰子时出错: {str(e)}")
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """处理点击事件"""
        click_rect = pygame.Rect(self.x, self.y, self.click_area, self.click_area)
        if click_rect.collidepoint(pos) and not self.is_rolling:
            print("[Dice] 开始投掷")
            return True
        return False
    
    def handle_motion(self, pos: Tuple[int, int]):
        """处理鼠标移动事件"""
        click_rect = pygame.Rect(self.x, self.y, self.click_area, self.click_area)
        was_hovered = self.is_hovered
        self.is_hovered = click_rect.collidepoint(pos)
        if self.is_hovered != was_hovered:
            pass  # 状态已在上面更新，这里不需要额外操作 
import pygame
from enum import Enum

class TimeOfDay(Enum):
    DAY = "昼"
    NIGHT = "夜"

class GameTime:
    def __init__(self):
        # 初始化时间
        self.year = 1
        self.month = 1
        self.day = 1
        self.time_of_day = TimeOfDay.DAY
        
        # 字体设置
        self.font = pygame.font.SysFont('simhei', 24)  # 使用系统黑体
        self.color = (66, 66, 66)  # 深灰色
        
    def advance(self):
        """推进时间"""
        if self.time_of_day == TimeOfDay.DAY:
            self.time_of_day = TimeOfDay.NIGHT
        else:
            self.time_of_day = TimeOfDay.DAY
            self._advance_day()
            
    def _advance_day(self):
        """增加一天"""
        self.day += 1
        # 简单的月份处理（每月30天）
        if self.day > 30:
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
                
    def draw(self, screen: pygame.Surface, x: int, y: int):
        """绘制时间显示"""
        # 创建时间文本
        text = f"{self.year}年{self.month}月{self.day}日 {self.time_of_day.value}"
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.bottom = y - 10  # 在指定位置上方10像素
        
        # 绘制背景
        padding = 10
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), bg_rect, width=1, border_radius=5)
        
        # 绘制文本
        screen.blit(text_surface, text_rect) 
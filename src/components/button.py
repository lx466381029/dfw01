import pygame
import os

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, action: str, enabled: bool = True, button_type: str = "primary"):
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
        self.text = text
        self.action = action
        self.enabled = enabled
        self.is_hovered = False
        self.button_type = button_type
        
        # 加载字体
        font_path = os.path.join('assets', 'fonts', 'SourceHanSans-Bold.ttc')
        try:
            self.font = pygame.font.Font(font_path, 32)
        except:
            self.font = pygame.font.Font(None, 32)
        
        # 颜色方案
        self.colors = {
            'primary': {
                'normal': pygame.Color('#4CAF50'),  # 绿色
                'hover': pygame.Color('#388E3C'),
                'disabled': pygame.Color('#BDBDBD')
            },
            'secondary': {
                'normal': pygame.Color('#2196F3'),  # 蓝色
                'hover': pygame.Color('#1976D2'),
                'disabled': pygame.Color('#BDBDBD')
            },
            'danger': {
                'normal': pygame.Color('#F44336'),  # 红色
                'hover': pygame.Color('#D32F2F'),
                'disabled': pygame.Color('#BDBDBD')
            }
        }
        
        # 文字颜色
        self.text_colors = {
            'normal': pygame.Color('#FFFFFF'),  # 白色
            'disabled': pygame.Color('#757575')  # 深灰色
        }
    
    def update(self):
        """更新按钮状态"""
        pass  # 目前没有需要更新的状态
    
    def draw(self, screen: pygame.Surface):
        """绘制按钮"""
        # 选择颜色
        if not self.enabled:
            color = self.colors[self.button_type]['disabled']
            text_color = self.text_colors['disabled']
        else:
            if self.is_hovered:
                color = self.colors[self.button_type]['hover']
            else:
                color = self.colors[self.button_type]['normal']
            text_color = self.text_colors['normal']
        
        # 绘制按钮阴影
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(screen, (0, 0, 0, 30), shadow_rect, border_radius=8)
        
        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        # 绘制文本
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        if self.is_hovered and self.enabled:
            text_rect.y -= 1  # 悬停时文字略微上移
        screen.blit(text_surface, text_rect)
    
    def handle_hover(self, mouse_pos: tuple):
        """处理鼠标悬停"""
        self.is_hovered = self.enabled and self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos: tuple) -> bool:
        """检查按钮是否被点击"""
        return self.enabled and self.rect.collidepoint(mouse_pos) 
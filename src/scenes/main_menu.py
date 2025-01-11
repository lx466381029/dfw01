import pygame
import os
import json
from pathlib import Path

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # 加载字体
        font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),    'assets', 'fonts', 'SourceHanSans-Bold.ttc')
        try:
            # 检查文件是否存在
            if not os.path.exists(font_path):
                print(f"错误：字体文件不存在于路径: {os.path.abspath(font_path)}")
                raise FileNotFoundError(f"字体文件不存在: {font_path}")
            
            # 尝试加载字体
            print(f"正在加载字体文件: {os.path.abspath(font_path)}")
            self.font = pygame.font.Font(font_path, 96)
            self.button_font = pygame.font.Font(font_path, 36)
            print("字体加载成功！")
            
        except (FileNotFoundError, pygame.error) as e:
            print(f"字体加载错误: {str(e)}")
            print("当前工作目录:", os.getcwd())
            print("尝试使用系统默认字体")
            self.font = pygame.font.Font(None, 96)
            self.button_font = pygame.font.Font(None, 36)
        
        # 按钮颜色
        self.button_colors = {
            'normal': pygame.Color('#2196F3'),
            'hover': pygame.Color('#1976D2'),
            'disabled': pygame.Color('#BDBDBD')
        }
        
        # 按钮状态
        self.buttons = {
            '开始新游戏': pygame.Rect(0, 0, 200, 50),
            '继续游戏': pygame.Rect(0, 0, 200, 50),
            '退出游戏': pygame.Rect(0, 0, 200, 50)
        }
        
        # 居中按钮
        self._center_buttons()
        
        # 存档检查
        self.has_save = self._check_save_exists()
    
    def _center_buttons(self):
        start_y = self.screen_height // 2 + 100
        for i, button in enumerate(self.buttons.values()):
            button.centerx = self.screen_width // 2
            button.y = start_y + i * 75
    
    def _check_save_exists(self):
        save_path = Path('saves/game_save.json')
        return save_path.exists()
    
    def draw(self):
        # 绘制背景
        self.screen.fill((240, 240, 240))
        
        # 绘制标题
        title = self.font.render("冒险大富翁", True, (33, 33, 33))
        title_rect = title.get_rect(centerx=self.screen_width//2, y=240)
        self.screen.blit(title, title_rect)
        
        # 绘制按钮
        mouse_pos = pygame.mouse.get_pos()
        for text, rect in self.buttons.items():
            color = self.button_colors['normal']
            if text == '继续游戏' and not self.has_save:
                color = self.button_colors['disabled']
            elif rect.collidepoint(mouse_pos):
                color = self.button_colors['hover']
            
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            text_surface = self.button_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for text, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    if text == '继续游戏' and not self.has_save:
                        return None
                    return self._handle_button_click(text)
        return None
    
    def _handle_button_click(self, button_text):
        if button_text == '开始新游戏':
            if self.has_save:
                return 'confirm_new_game'
            return 'new_game'
        elif button_text == '继续游戏':
            return 'continue_game'
        elif button_text == '退出游戏':
            return 'quit'
        return None 
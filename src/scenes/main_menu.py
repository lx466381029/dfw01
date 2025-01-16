import pygame
import os
from components.button import Button

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # 加载字体
        font_path = os.path.join('assets', 'fonts', 'SourceHanSans-Bold.ttc')
        print(f"正在加载字体文件: {os.path.abspath(font_path)}")
        try:
            self.font = pygame.font.Font(font_path, 96)
            print("字体加载成功！")
        except Exception as e:
            print(f"字体加载失败: {str(e)}")
            # 使用系统默认字体作为后备方案
            self.font = pygame.font.Font(None, 96)
        
        # 创建按钮
        button_y = self.screen_height // 2 + 50  # 将按钮整体下移
        button_spacing = 100  # 增加按钮间距
        button_width = 240  # 增加按钮宽度
        button_height = 60  # 增加按钮高度
        
        self.buttons = {
            'new_game': Button(
                self.screen_width // 2,
                button_y,
                button_width, button_height,
                "新游戏",
                action="new_game",
                button_type="primary"  # 主要按钮
            ),
            'continue_game': Button(
                self.screen_width // 2,
                button_y + button_spacing,
                button_width, button_height,
                "继续游戏",
                action="continue_game",
                enabled=False,  # 暂时禁用
                button_type="secondary"  # 次要按钮
            ),
            'quit': Button(
                self.screen_width // 2,
                button_y + button_spacing * 2,
                button_width, button_height,
                "退出游戏",
                action="quit",
                button_type="danger"  # 危险按钮
            )
        }
    
    def update(self):
        """更新主菜单状态"""
        # 更新按钮状态
        for button in self.buttons.values():
            button.update()
    
    def draw(self):
        # 绘制背景
        self.screen.fill((245, 245, 245))  # 更浅的灰色背景
        
        # 绘制标题
        title_text = self.font.render("冒险棋", True, (33, 33, 33))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(title_text, title_rect)
        
        # 绘制所有按钮
        for button in self.buttons.values():
            button.draw(self.screen)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 检查是否点击了任何按钮
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons.values():
                if button.is_clicked(mouse_pos):
                    return button.action
        
        elif event.type == pygame.MOUSEMOTION:
            # 更新按钮的悬停状态
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons.values():
                button.handle_hover(mouse_pos)
        
        return None
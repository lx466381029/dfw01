import pygame
import os
from components.button import Button
from components.save_manager import SaveManager

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # 初始化存档管理器
        self.save_manager = SaveManager()
        
        # 加载字体
        font_path = os.path.join('assets', 'fonts', 'SourceHanSans-Bold.ttc')
        print(f"正在加载字体文件: {os.path.abspath(font_path)}")
        try:
            self.font = pygame.font.Font(font_path, 96)
            self.warning_font = pygame.font.Font(font_path, 36)
            print("字体加载成功！")
        except Exception as e:
            print(f"字体加载失败: {str(e)}")
            self.font = pygame.font.Font(None, 96)
            self.warning_font = pygame.font.Font(None, 36)
        
        self._initialize_buttons()
        
    def _initialize_buttons(self):
        """初始化或重新初始化按钮"""
        button_y = self.screen_height // 2 + 50
        button_spacing = 100
        button_width = 240
        button_height = 60
        
        # 检查是否有存档
        has_save = self.save_manager.has_save()
        print(f"[MainMenu] 检查存档状态: {'有存档' if has_save else '无存档'}")
        
        self.buttons = {
            'new_game': Button(
                self.screen_width // 2,
                button_y,
                button_width, button_height,
                "新游戏",
                action="new_game",
                button_type="primary"
            ),
            'continue_game': Button(
                self.screen_width // 2,
                button_y + button_spacing,
                button_width, button_height,
                "继续游戏",
                action="continue_game",
                enabled=has_save,
                button_type="secondary"
            ),
            'quit': Button(
                self.screen_width // 2,
                button_y + button_spacing * 2,
                button_width, button_height,
                "退出游戏",
                action="quit",
                button_type="danger"
            )
        }
        
        # 确认对话框状态
        self.show_confirm_dialog = False
        self.confirm_dialog_buttons = {
            'yes': Button(
                self.screen_width // 2 - 120,
                self.screen_height // 2 + 50,
                200, 50,
                "确认删除",
                action="confirm_delete",
                button_type="danger"
            ),
            'no': Button(
                self.screen_width // 2 + 120,
                self.screen_height // 2 + 50,
                200, 50,
                "取消",
                action="cancel_delete",
                button_type="secondary"
            )
        }
        
    def refresh(self):
        """刷新主菜单状态"""
        print("[MainMenu] 刷新菜单状态")
        self.save_manager = SaveManager()  # 重新初始化存档管理器
        self._initialize_buttons()  # 重新初始化按钮
    
    def update(self):
        """更新主菜单状态"""
        # 更新按钮状态
        for button in self.buttons.values():
            button.update()
        if self.show_confirm_dialog:
            for button in self.confirm_dialog_buttons.values():
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
            
        # 如果显示确认对话框，绘制对话框
        if self.show_confirm_dialog:
            # 绘制半透明背景
            dialog_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            pygame.draw.rect(dialog_surface, (0, 0, 0, 128), dialog_surface.get_rect())
            self.screen.blit(dialog_surface, (0, 0))
            
            # 绘制对话框
            dialog_width = 500
            dialog_height = 200
            dialog_rect = pygame.Rect(
                (self.screen_width - dialog_width) // 2,
                (self.screen_height - dialog_height) // 2,
                dialog_width,
                dialog_height
            )
            pygame.draw.rect(self.screen, (245, 245, 245), dialog_rect, border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 200), dialog_rect, width=2, border_radius=10)
            
            # 绘制提示文本
            warning_text = self.warning_font.render("检测到已有存档，是否删除？", True, (33, 33, 33))
            warning_rect = warning_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 20))
            self.screen.blit(warning_text, warning_rect)
            
            # 绘制确认按钮
            for button in self.confirm_dialog_buttons.values():
                button.draw(self.screen)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 获取鼠标位置
            mouse_pos = pygame.mouse.get_pos()
            
            if self.show_confirm_dialog:
                # 处理确认对话框的按钮点击
                for button in self.confirm_dialog_buttons.values():
                    if button.is_clicked(mouse_pos):
                        if button.action == "confirm_delete":
                            print("[MainMenu] 确认删除存档")
                            # 删除存档并开始新游戏
                            if self.save_manager.delete_save():
                                self.show_confirm_dialog = False
                                print("[MainMenu] 开始新游戏")
                                return "new_game"
                            else:
                                print("[MainMenu] 删除存档失败")
                                self.show_confirm_dialog = False
                        elif button.action == "cancel_delete":
                            print("[MainMenu] 取消删除存档")
                            self.show_confirm_dialog = False
                return None
            else:
                # 检查是否点击了任何按钮
                for button in self.buttons.values():
                    if button.is_clicked(mouse_pos):
                        if button.action == "new_game":
                            if self.save_manager.has_save():
                                # 如果有存档，显示确认对话框
                                print("[MainMenu] 显示删除存档确认框")
                                self.show_confirm_dialog = True
                                return None
                            else:
                                # 如果没有存档，直接开始新游戏
                                print("[MainMenu] 开始新游戏")
                                return "new_game"
                        elif button.action == "continue_game":
                            # 检查存档是否存在
                            if self.save_manager.has_save():
                                print("[MainMenu] 继续游戏")
                                return "continue_game"
                            else:
                                print("[MainMenu] 错误：没有找到存档")
                        elif button.action == "quit":
                            print("[MainMenu] 退出游戏")
                            return "quit"
        
        elif event.type == pygame.MOUSEMOTION:
            # 更新按钮的悬停状态
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons.values():
                button.handle_hover(mouse_pos)
            if self.show_confirm_dialog:
                for button in self.confirm_dialog_buttons.values():
                    button.handle_hover(mouse_pos)
        
        return None
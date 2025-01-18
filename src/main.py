import pygame
import sys
import os
from pathlib import Path
from scenes.main_menu import MainMenu
from scenes.game_board import GameBoard

class Game:
    def __init__(self):
        # 确保在正确的工作目录
        self._setup_working_directory()
        
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("冒险棋")
        self.clock = pygame.time.Clock()
        
        # 初始化场景
        self.scenes = {
            'main_menu': MainMenu(self.screen),
            'game_board': GameBoard(self.screen)
        }
        self.current_scene = 'main_menu'  # 使用字符串键
        self.running = True
    
    def _setup_working_directory(self):
        """确保工作目录是项目根目录"""
        current_dir = Path(os.getcwd())
        src_dir = Path(__file__).parent
        
        if current_dir.name == 'src':
            # 如果在src目录中，移动到父目录
            os.chdir(src_dir.parent)
        elif not (current_dir / 'src').exists():
            # 如果不在项目根目录，尝试移动到正确位置
            os.chdir(src_dir.parent)
        
        print(f"工作目录设置为: {os.getcwd()}")
    
    def handle_scene_action(self, action):
        """处理场景返回的动作"""
        if action == "quit":
            self.running = False
        elif action == "new_game":
            print("[Game] 切换到游戏场景（新游戏）")
            self.current_scene = "game_board"
            # 重置游戏状态
            self.scenes["game_board"].reset()
        elif action == "continue_game":
            print("[Game] 切换到游戏场景（继续游戏）")
            self.current_scene = "game_board"
        elif action == "main_menu":
            print("[Game] 返回主菜单")
            self.current_scene = "main_menu"
            # 刷新主菜单状态
            self.scenes["main_menu"].refresh()
            
    def run(self):
        """运行游戏主循环"""
        while self.running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.current_scene == "game_board":
                        # 保存游戏状态
                        self.scenes["game_board"]._save_game_state()
                        # 返回主菜单
                        self.handle_scene_action("main_menu")
                        continue
                
                # 处理当前场景的事件
                action = self.scenes[self.current_scene].handle_event(event)
                if action:
                    self.handle_scene_action(action)
            
            # 更新当前场景
            self.scenes[self.current_scene].update()
            
            # 绘制当前场景
            self.scenes[self.current_scene].draw()
            
            # 更新显示
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run() 
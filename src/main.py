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
        pygame.display.set_caption("冒险大富翁")
        self.clock = pygame.time.Clock()
        self.current_scene = None
        self.running = True
        
        # 初始化场景
        self.scenes = {
            'main_menu': MainMenu(self.screen),
            'game_board': GameBoard(self.screen)
        }
        self.current_scene = self.scenes['main_menu']
    
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
    
    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if isinstance(self.current_scene, GameBoard):
                    self.current_scene = self.scenes['main_menu']
            
            if self.current_scene:
                result = self.current_scene.handle_event(event)
                if result:
                    self._handle_scene_result(result)
    
    def _handle_scene_result(self, result):
        if result == 'quit':
            self.running = False
        elif result == 'new_game':
            self.current_scene = self.scenes['game_board']
        elif result == 'continue_game':
            self.current_scene = self.scenes['game_board']
        elif result == 'confirm_new_game':
            # TODO: 实现确认新游戏对话框
            self.current_scene = self.scenes['game_board']
    
    def _update(self):
        pass
    
    def _draw(self):
        if self.current_scene:
            self.current_scene.draw()
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run() 
import pygame
import os
from pathlib import Path
from components.dice import Dice
from components.player import Player
from components.board import Board
from components.game_time import GameTime

class GameBoard:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # 棋盘配置
        self.cell_size = 110
        self.board_width = 16
        self.board_height = 9
        self.border_width = 5
        
        # 计算棋盘位置使其居中
        self.board_pixel_width = self.cell_size * self.board_width
        self.board_pixel_height = self.cell_size * self.board_height
        self.board_x = (self.screen_width - self.board_pixel_width) // 2
        self.board_y = (self.screen_height - self.board_pixel_height) // 2
        
        # 颜色定义
        self.colors = {
            'background': pygame.Color('#F5F5F5'),
            'cell': pygame.Color('#FFFFFF'),
            'border': pygame.Color('#424242'),
            'highlight': pygame.Color('#E3F2FD')
        }
        
        # 创建棋盘管理器
        self.board = Board()
        
        # 生成轨道格子位置
        self.cells = self.board.path
        
        # 当前高亮的格子
        self.highlighted_cell = None
        
        # 创建骰子
        dice_x = self.board_x + self.board_pixel_width - 300  # 右侧偏移
        dice_y = self.board_y + self.board_pixel_height - 300  # 下方偏移
        self.dice = Dice(dice_x, dice_y)
        
        # 创建玩家
        start_x = self.board_x
        start_y = self.board_y
        self.player = Player(start_x, start_y, self.cell_size)
        self.player_cell_index = 0
        
        # 注册骰子回调
        self.dice_result = None
        self.can_roll = True
        
        # 创建时间系统
        self.game_time = GameTime()
    
    def _on_dice_roll_complete(self, value):
        """骰子投掷完成的回调函数"""
        self.dice_result = value
        print(f"[GameBoard] 骰子点数: {value}")
        
        # 获取移动路径
        path = self.board.get_move_path(self.player_cell_index, value)
        
        # 转换路径坐标为实际像素坐标
        pixel_path = []
        for x, y in path:
            pixel_x = self.board_x + x * self.cell_size
            pixel_y = self.board_y + y * self.cell_size
            pixel_path.append((pixel_x, pixel_y))
        
        # 更新玩家位置
        self.player.move_to(pixel_path, pygame.time.get_ticks())
        
        # 更新玩家当前格子索引
        self.player_cell_index = (self.player_cell_index + value) % len(self.cells)
        
        # 推进时间
        self.game_time.advance()
        print(f"[GameBoard] 时间推进 - {self.game_time.year}年{self.game_time.month}月{self.game_time.day}日 {self.game_time.time_of_day.value}")
        
        # 禁用骰子直到移动完成
        self.can_roll = False
    
    def _generate_track_cells(self):
        """生成闭环轨道的所有格子位置"""
        cells = []
        
        # 外圈
        # 上边
        for x in range(self.board_width):
            cells.append((x, 0))
        # 右边
        for y in range(1, self.board_height):
            cells.append((self.board_width-1, y))
        # 下边
        for x in range(self.board_width-2, -1, -1):
            cells.append((x, self.board_height-1))
        # 左边
        for y in range(self.board_height-2, 0, -1):
            cells.append((0, y))
        
        return cells
    
    def _get_cell_rect(self, cell_pos):
        """获取指定格子的矩形区域"""
        x, y = cell_pos
        return pygame.Rect(
            self.board_x + x * self.cell_size,
            self.board_y + y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
    
    def update(self):
        """更新游戏状态"""
        current_time = pygame.time.get_ticks()
        self.dice.update()
        
        # 更新玩家
        self.player.update(current_time)
        
        # 如果玩家不在移动中，允许投骰子
        if not self.player.is_moving:
            self.can_roll = True
    
    def draw(self):
        # 绘制背景
        self.screen.fill(self.colors['background'])
        
        # 绘制所有格子
        for cell in self.cells:
            rect = self._get_cell_rect(cell)
            
            # 判断是否是高亮格子
            if cell == self.highlighted_cell:
                pygame.draw.rect(self.screen, self.colors['highlight'], rect)
            else:
                pygame.draw.rect(self.screen, self.colors['cell'], rect)
            
            # 绘制边框
            pygame.draw.rect(self.screen, self.colors['border'], rect, self.border_width)
        
        # 绘制骰子
        self.dice.draw(self.screen)
        
        # 绘制时间（在骰子上方）
        time_x = self.dice.x + self.dice.click_area // 2
        time_y = self.dice.y
        self.game_time.draw(self.screen, time_x, time_y)
        
        # 绘制玩家
        self.player.draw(self.screen)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 只有在允许投骰子时才处理点击
            if self.can_roll and self.dice.handle_click(event.pos):
                self.dice.roll(callback=self._on_dice_roll_complete)
                return None
        
        elif event.type == pygame.MOUSEMOTION:
            # 处理骰子悬停
            self.dice.handle_motion(event.pos)
            
            # 检测格子悬停
            mouse_pos = pygame.mouse.get_pos()
            self.highlighted_cell = None
            
            for cell in self.cells:
                rect = self._get_cell_rect(cell)
                if rect.collidepoint(mouse_pos):
                    self.highlighted_cell = cell
                    break
        
        return None 
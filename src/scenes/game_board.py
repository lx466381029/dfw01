import pygame
import os
from pathlib import Path
from components.dice import Dice
from components.player import Player
from components.board import Board
from components.game_time import GameTime
from components.save_manager import SaveManager

class GameBoard:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        self._initialize_game_state()
        
    def _initialize_game_state(self):
        """初始化或重置游戏状态"""
        print("[GameBoard] 初始化游戏状态")
        
        # 棋盘配置
        self.cell_size = 115
        self.board_width = 16
        self.board_height = 9
        self.border_width = 5
        
        # 计算棋盘位置
        self.board_pixel_width = self.cell_size * self.board_width
        self.board_pixel_height = self.cell_size * self.board_height
        
        # 添加右下方偏移量
        right_offset = 50
        down_offset = 20
        
        self.board_x = (self.screen_width - self.board_pixel_width) // 2 + right_offset
        self.board_y = (self.screen_height - self.board_pixel_height) // 2 + down_offset
        
        # 颜色定义
        self.colors = {
            'background': pygame.Color('#F5F5F5'),
            'cell': pygame.Color('#FFFFFF'),
            'border': pygame.Color('#AAAAAA'),
            'highlight': pygame.Color('#E3F2FD')
        }
        
        # 创建棋盘管理器
        self.board = Board()
        self.cells = self.board.path
        self.highlighted_cell = None
        
        # 创建骰子
        dice_x = self.board_x + self.board_pixel_width - 375
        dice_y = self.board_y + self.board_pixel_height - 340
        self.dice = Dice(dice_x, dice_y)
        
        # 创建玩家
        start_cell = self.cells[0]
        start_x = self.board_x + start_cell[0] * (self.cell_size - self.border_width)
        start_y = self.board_y + start_cell[1] * (self.cell_size - self.border_width)
        start_x += self.cell_size / 2
        start_y += self.cell_size / 2
        self.player = Player(start_x, start_y, self.cell_size)
        self.player_cell_index = 0
        
        # 游戏状态
        self.dice_result = None
        self.can_roll = True
        
        # 创建时间系统
        self.game_time = GameTime()
        
        # 创建存档管理器
        self.save_manager = SaveManager()
        
    def reset(self):
        """重置游戏状态"""
        print("[GameBoard] 重置游戏状态")
        self._initialize_game_state()
    
    def _on_dice_roll_complete(self, value):
        """骰子投掷完成的回调函数"""
        self.dice_result = value
        print(f"[GameBoard] 骰子点数: {value}")
        
        # 获取移动路径
        path = self.board.get_move_path(self.player_cell_index, value)
        
        # 转换路径坐标为实际像素坐标
        pixel_path = []
        for x, y in path:
            # 计算格子的实际像素位置，考虑边框重叠
            pixel_x = self.board_x + x * (self.cell_size - self.border_width)
            pixel_y = self.board_y + y * (self.cell_size - self.border_width)
            # 加上半个格子大小得到中心点
            pixel_x += self.cell_size / 2
            pixel_y += self.cell_size / 2
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
        """获取指定格子的矩形区域
        
        Args:
            cell_pos: 格子的(x, y)坐标
            
        Returns:
            pygame.Rect: 格子的矩形区域，包括位置和大小。
                       格子之间会重叠border_width像素，以实现边框的视觉统一。
        """
        x, y = cell_pos
        # 计算格子位置时减去border_width，使相邻格子重叠
        return pygame.Rect(
            self.board_x + x * (self.cell_size - self.border_width),
            self.board_y + y * (self.cell_size - self.border_width),
            self.cell_size,
            self.cell_size
        )
    
    def _load_game_state(self):
        """加载游戏状态"""
        save_data = self.save_manager.load_game()
        if save_data:
            # 恢复玩家位置
            self.player_cell_index = save_data["player_position"]
            cell_pos = self.cells[self.player_cell_index]
            # 计算格子的实际像素位置，考虑边框重叠
            player_x = self.board_x + cell_pos[0] * (self.cell_size - self.border_width)
            player_y = self.board_y + cell_pos[1] * (self.cell_size - self.border_width)
            # 加上半个格子大小得到中心点
            player_x += self.cell_size / 2
            player_y += self.cell_size / 2
            self.player.x = player_x
            self.player.y = player_y
            self.player._update_rect_position()
            
            # 恢复时间状态
            self.game_time.year = save_data["year"]
            self.game_time.month = save_data["month"]
            self.game_time.day = save_data["day"]
            self.game_time.time_of_day = save_data["time_of_day"]
            
            print(f"[GameBoard] 已加载存档 - 位置: {self.player_cell_index}, "
                  f"时间: {self.game_time.year}年{self.game_time.month}月{self.game_time.day}日 "
                  f"{self.game_time.time_of_day.value}")
    
    def _save_game_state(self):
        """保存游戏状态"""
        game_data = {
            "player_position": self.player_cell_index,
            "year": self.game_time.year,
            "month": self.game_time.month,
            "day": self.game_time.day,
            "time_of_day": self.game_time.time_of_day
        }
        
        if self.save_manager.save_game(game_data):
            print("[GameBoard] 游戏状态已保存")
    
    def update(self):
        """更新游戏状态"""
        current_time = pygame.time.get_ticks()
        self.dice.update()
        
        # 更新玩家
        self.player.update(current_time)
        
        # 如果玩家不在移动中，允许投骰子并保存游戏
        if not self.player.is_moving:
            if not self.can_roll:  # 移动刚结束
                self._save_game_state()
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # 按S键保存
                self._save_game_state()
                return None
        
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
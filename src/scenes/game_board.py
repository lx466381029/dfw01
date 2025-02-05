import pygame
import os
from pathlib import Path
from components.dice import Dice
from components.player import Player
from components.board import Board
from components.game_time import GameTime
from components.save_manager import SaveManager
from utils.font_manager import FontManager

class GameBoard:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        self._initialize_game_state()
        
        # 修改时间显示文本的渲染方式
        self.time_font = FontManager.get_instance().get_font(24)
        
        # 名称编辑弹窗相关
        self.editing_name = False
        self.edit_text = ""
        self.edit_surface = None
        self.edit_rect = None
        self.edit_bg_color = pygame.Color('#FFFFFF')
        self.edit_border_color = pygame.Color('#AAAAAA')
        self.edit_text_color = pygame.Color('#212121')
        
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
        self.game_time.advance_month()
        print(f"[GameBoard] 时间推进 - {self.game_time.year}年{self.game_time.month}月 {self.game_time.current_season}")
        
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
    
    def _save_game_state(self):
        """保存游戏状态"""
        game_data = {
            "player_position": self.player_cell_index,
            "year": self.game_time.year,
            "month": self.game_time.month,
            "player_name": self.player.name  # 添加玩家名称
        }
        
        if self.save_manager.save_game(game_data):
            print("[GameBoard] 游戏状态已保存")
    
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
            
            # 恢复玩家名称
            if "player_name" in save_data:
                self.player.set_name(save_data["player_name"])
            
            # 恢复时间状态
            self.game_time.year = save_data["year"]
            self.game_time.month = save_data["month"]
            
            print(f"[GameBoard] 已加载存档 - 位置: {self.player_cell_index}, "
                  f"时间: {self.game_time.year}年{self.game_time.month}月 {self.game_time.current_season}")
    
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
        self._draw_time_system()
        
        # 绘制玩家
        self.player.draw(self.screen)
        
        # 绘制玩家名称（在轨道中间的左上角）
        self._draw_player_name()
    
    def _draw_player_name(self):
        """绘制玩家名称"""
        if self.player.name_surface:
            # 计算名称位置（在骰子左侧）
            name_x = self.dice.x - 400  # 在骰子左侧400像素
            name_y = self.dice.y  # 与骰子同一水平线
            
            # 绘制名称
            self.screen.blit(self.player.name_surface, (name_x, name_y))
            
            # 绘制下划线
            if self.player.name_underline:
                underline_y = name_y + self.player.name_surface.get_height() + 2
                self.screen.blit(self.player.name_underline, (name_x, underline_y))
            
            # 如果正在编辑名称，绘制编辑弹窗
            if self.editing_name:
                self._draw_name_edit_popup()

    def _draw_name_edit_popup(self):
        """绘制名称编辑弹窗"""
        # 创建弹窗背景
        popup_width = 300
        popup_height = 120
        popup_x = (self.screen_width - popup_width) // 2
        popup_y = (self.screen_height - popup_height) // 2
        
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明黑色
        self.screen.blit(overlay, (0, 0))
        
        # 绘制弹窗主体
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.screen, self.edit_bg_color, popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.edit_border_color, popup_rect, 2, border_radius=10)
        
        # 绘制标题
        title_text = self.time_font.render("编辑名称", True, self.edit_text_color)
        title_x = popup_x + (popup_width - title_text.get_width()) // 2
        self.screen.blit(title_text, (title_x, popup_y + 15))
        
        # 绘制输入框
        input_width = 260
        input_height = 36
        input_x = popup_x + (popup_width - input_width) // 2
        input_y = popup_y + 50
        
        # 保存输入框位置供点击检测使用
        self.edit_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        
        # 绘制输入框背景
        pygame.draw.rect(self.screen, pygame.Color('#F5F5F5'), self.edit_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.edit_border_color, self.edit_rect, 1, border_radius=5)
        
        # 绘制输入的文本
        if self.edit_text:
            text = self.edit_text
        else:
            text = self.player.name
        text_surface = self.time_font.render(text + ("_" if pygame.time.get_ticks() // 500 % 2 else ""), True, self.edit_text_color)
        text_x = input_x + 10
        text_y = input_y + (input_height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # 按S键保存
                self._save_game_state()
                return None
            elif self.editing_name:  # 处理名称编辑
                if event.key == pygame.K_RETURN:  # 回车确认
                    if self.edit_text.strip():
                        self.player.set_name(self.edit_text)
                        self._save_game_state()  # 保存新名称
                    self.editing_name = False
                    self.edit_text = ""
                elif event.key == pygame.K_ESCAPE:  # ESC取消
                    self.editing_name = False
                    self.edit_text = ""
                elif event.key == pygame.K_BACKSPACE:  # 退格删除
                    self.edit_text = self.edit_text[:-1]
                elif event.unicode and len(self.edit_text) < 10:  # 限制名称长度
                    self.edit_text += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 检查是否点击了玩家名称
            mouse_pos = event.pos
            name_x = self.dice.x - 400
            name_y = self.dice.y
            name_rect = self.player.name_surface.get_rect(topleft=(name_x, name_y))
            if name_rect.collidepoint(mouse_pos):
                if not self.editing_name:
                    self.editing_name = True
                    self.edit_text = self.player.name
                return None
            
            # 如果正在编辑名称，检查点击是否在编辑区域外
            if self.editing_name and not (self.edit_rect and self.edit_rect.collidepoint(mouse_pos)):
                self.editing_name = False
                self.edit_text = ""
                return None
            
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
    
    def _draw_time_system(self):
        """绘制时间系统"""
        time_text = self.game_time.get_time_string()
        text_surface = self.time_font.render(time_text, True, self.game_time.current_season_color)
        
        # 创建背景框
        bg_rect = pygame.Rect(0, 0, text_surface.get_width()+20, text_surface.get_height()+10)
        
        # 调整位置到骰子区域上方
        # 使用骰子的x, y位置
        dice_x = self.dice.x  # 骰子的x坐标
        dice_y = self.dice.y  # 骰子的y坐标
        
        # 将时间显示放在骰子上方
        bg_rect.centerx = dice_x + 90
        bg_rect.bottom = dice_y -1
        
        # 绘制背景和文字
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect, 1, border_radius=5)
        self.screen.blit(text_surface, (bg_rect.x+10, bg_rect.y+5)) 
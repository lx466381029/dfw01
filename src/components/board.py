from typing import List, Tuple
import pygame

class Board:
    def __init__(self):
        """初始化棋盘
        设置基本属性，包括棋盘大小、格子大小等
        生成游戏路径
        """
        # 棋盘网格大小（格子数量）
        self.width = 16  # 横向16个格子
        self.height = 9  # 纵向9个格子
        
        # 单个格子的大小（像素）
        self.cell_size = 100  # 每个格子100x100像素
        
        # 生成游戏路径（外圈闭环）
        self.path = self._generate_path()
        print(f"[Board] 初始化完成 - 路径点数: {len(self.path)}")
        
    def _generate_path(self) -> List[Tuple[int, int]]:
        """生成闭环路径的坐标列表
        按照顺时针方向生成外圈路径：上→右→下→左
        
        Returns:
            List[Tuple[int, int]]: 路径坐标列表，每个元素为(x, y)格子坐标
        """
        path = []
        
        # 添加外圈坐标（顺时针）
        # 上边：从左到右
        for x in range(self.width):
            path.append((x, 0))
            
        # 右边：从上到下
        for y in range(1, self.height):
            path.append((self.width-1, y))
            
        # 下边：从右到左
        for x in range(self.width-2, -1, -1):
            path.append((x, self.height-1))
            
        # 左边：从下到上
        for y in range(self.height-2, 0, -1):
            path.append((0, y))
            
        print(f"[Board] 生成路径 - 总格子数: {len(path)}")
        return path
        
    def get_move_path(self, current_index: int, steps: int) -> List[Tuple[int, int]]:
        """计算从当前位置移动指定步数后的路径
        
        Args:
            current_index (int): 当前位置的索引
            steps (int): 需要移动的步数
            
        Returns:
            List[Tuple[int, int]]: 移动路径的坐标列表，包含起点和终点
        """
        path = []
        total_cells = len(self.path)
        
        print(f"[Board] 计算移动路径 - 当前位置: {current_index}, 步数: {steps}, 总格子数: {total_cells}")
        
        # 添加起始位置
        path.append(self.path[current_index])
        
        # 计算移动路径（考虑循环）
        for i in range(steps):
            next_index = (current_index + i + 1) % total_cells  # 使用取模运算处理循环
            next_pos = self.path[next_index]
            path.append(next_pos)
            print(f"[Board] 添加路径点 {i+1}/{steps} - 索引: {next_index}, 位置: {next_pos}")
            
        print(f"[Board] 路径计算完成 - 路径点数: {len(path)}")
        return path
        
    def get_cell_position(self, index: int) -> Tuple[int, int]:
        """获取指定索引格子的坐标
        
        Args:
            index (int): 格子的索引值
            
        Returns:
            Tuple[int, int]: 格子的(x, y)坐标，如果索引无效则返回(0, 0)
        """
        if 0 <= index < len(self.path):
            pos = self.path[index]
            print(f"[Board] 获取格子位置 - 索引: {index}, 位置: {pos}")
            return pos
        print(f"[Board] 警告: 无效的格子索引 {index}")
        return (0, 0)
        
    def draw(self, screen: pygame.Surface):
        """绘制棋盘
        
        绘制所有格子，包括：
        1. 普通格子（白色背景+灰色边框）
        2. 路径格子（浅蓝色背景+深灰色边框）
        
        相邻格子的边框会重叠，以保持视觉统一性。
        
        Args:
            screen (pygame.Surface): 游戏窗口表面
        """
        # 绘制所有格子（底层）
        for y in range(self.height):
            for x in range(self.width):
                # 计算格子的像素位置和大小
                rect = pygame.Rect(
                    x * self.cell_size,  # 不减1，让边框重叠
                    y * self.cell_size,  # 不减1，让边框重叠
                    self.cell_size + 1,  # 加1确保边框完全重叠
                    self.cell_size + 1   # 加1确保边框完全重叠
                )
                # 绘制格子背景（白色）
                pygame.draw.rect(screen, (255, 255, 255), rect)
                # 绘制格子边框（浅灰色）
                pygame.draw.rect(screen, (200, 200, 200), rect, width=1)
                
        # 高亮路径格子（上层）
        for x, y in self.path:
            rect = pygame.Rect(
                x * self.cell_size,  # 不减1，让边框重叠
                y * self.cell_size,  # 不减1，让边框重叠
                self.cell_size + 1,  # 加1确保边框完全重叠
                self.cell_size + 1   # 加1确保边框完全重叠
            )
            # 绘制路径格子背景（浅蓝色）
            pygame.draw.rect(screen, (235, 245, 255), rect)
            # 绘制路径格子边框（深灰色）
            pygame.draw.rect(screen, (150, 150, 150), rect, width=1)
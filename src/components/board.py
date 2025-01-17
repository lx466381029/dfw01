from typing import List, Tuple

class Board:
    def __init__(self):
        self.width = 16
        self.height = 9
        self.cell_size = 100
        self.path = self._generate_path()
        print(f"[Board] 初始化完成 - 路径点数: {len(self.path)}")
        
    def _generate_path(self) -> List[Tuple[int, int]]:
        """生成闭环路径的坐标列表"""
        path = []
        
        # 添加外圈坐标（顺时针）
        # 上边
        for x in range(self.width):
            path.append((x, 0))
        # 右边
        for y in range(1, self.height):
            path.append((self.width-1, y))
        # 下边
        for x in range(self.width-2, -1, -1):
            path.append((x, self.height-1))
        # 左边
        for y in range(self.height-2, 0, -1):
            path.append((0, y))
            
        print(f"[Board] 生成路径 - 总格子数: {len(path)}")
        return path
        
    def get_move_path(self, current_index: int, steps: int) -> List[Tuple[int, int]]:
        """计算从当前位置移动指定步数后的路径"""
        path = []
        total_cells = len(self.path)
        
        print(f"[Board] 计算移动路径 - 当前位置: {current_index}, 步数: {steps}, 总格子数: {total_cells}")
        
        # 添加起始位置
        path.append(self.path[current_index])
        
        # 计算移动路径
        for i in range(steps):
            next_index = (current_index + i + 1) % total_cells
            next_pos = self.path[next_index]
            path.append(next_pos)
            print(f"[Board] 添加路径点 {i+1}/{steps} - 索引: {next_index}, 位置: {next_pos}")
            
        print(f"[Board] 路径计算完成 - 路径点数: {len(path)}")
        return path
        
    def get_cell_position(self, index: int) -> Tuple[int, int]:
        """获取指定索引格子的坐标"""
        if 0 <= index < len(self.path):
            pos = self.path[index]
            print(f"[Board] 获取格子位置 - 索引: {index}, 位置: {pos}")
            return pos
        print(f"[Board] 警告: 无效的格子索引 {index}")
        return (0, 0) 
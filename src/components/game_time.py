import pygame

class GameTime:
    def __init__(self):
        # 修改时间单位为年和月
        self.year = 1
        self.month = 1  # 1-12个月
        self._season_mapping = {
            1: "冬", 2: "冬",
            3: "春", 4: "春", 5: "春",
            6: "夏", 7: "夏", 8: "夏",
            9: "秋", 10: "秋", 11: "秋",
            12: "冬"
        }
        
        # 季节对应的颜色
        self._season_colors = {
            "春": (129, 199, 132),  # #81C784
            "夏": (229, 115, 115),  # #E57373
            "秋": (255, 183, 77),   # #FFB74D
            "冬": (79, 195, 247)    # #4FC3F7
        }
        
    @property
    def current_season(self):
        return self._season_mapping[self.month]
    
    @property
    def current_season_color(self):
        return self._season_colors[self.current_season]
    
    def advance_month(self):
        """每月推进"""
        self.month += 1
        if self.month > 12:
            self.year += 1
            self.month = 1
            
    def get_time_string(self):
        """获取时间显示字符串"""
        return f"{self.year}年{self.month}月 {self.current_season}季"
    
    def serialize(self):
        """序列化时间数据"""
        return {
            "year": self.year,
            "month": self.month
        }
    
    def deserialize(self, data):
        """反序列化时间数据"""
        self.year = data["year"]
        self.month = data["month"]
        
    def advance(self):
        """推进时间"""
        if self.time_of_day == TimeOfDay.DAY:
            self.time_of_day = TimeOfDay.NIGHT
        else:
            self.time_of_day = TimeOfDay.DAY
            self._advance_day()
            
    def _advance_day(self):
        """增加一天"""
        self.day += 1
        # 简单的月份处理（每月30天）
        if self.day > 30:
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
                
    def draw(self, screen: pygame.Surface, x: int, y: int):
        """绘制时间显示"""
        # 创建时间文本
        text = f"{self.year}年{self.month}月 {self.current_season}季"
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.bottom = y - 10  # 在指定位置上方10像素
        
        # 绘制背景
        padding = 10
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), bg_rect, width=1, border_radius=5)
        
        # 绘制文本
        screen.blit(text_surface, text_rect) 
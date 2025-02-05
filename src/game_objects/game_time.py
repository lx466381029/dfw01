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
    
    @property
    def current_season(self):
        return self._season_mapping[self.month]
    
    def advance_month(self):
        """每月推进"""
        self.month += 1
        if self.month > 12:
            self.year += 1
            self.month = 1
            
    def get_time_string(self):
        """获取时间显示字符串"""
        return f"{self.year}年{self.month}月 {self._season_mapping[self.month]}季"
    
    def serialize(self):
        return {"year": self.year, "month": self.month}
    
    def deserialize(self, data):
        self.year = data["year"]
        self.month = data["month"] 
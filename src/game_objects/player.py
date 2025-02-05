class Player(pygame.sprite.Sprite):
    def __init__(self, cell_size=100):
        super().__init__()
        # 修改图片加载路径
        self.original_image = pygame.image.load(
            "assets/images/characters/character.png"  # 修改文件名
        ).convert_alpha()
        # 保持原有缩放逻辑不变
        self.image = pygame.transform.scale(
            self.original_image, 
            (int(cell_size * 0.8), int(cell_size * 0.8))
        )
        # 其余代码保持不变... 
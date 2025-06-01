# game_objects/base.py

import pygame
from resources import ResourceManager # 導入資源管理器
from game_config import GameConfig # 導入遊戲配置，用於佔位圖片大小

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name):
        super().__init__()
        # 使用 ResourceManager 載入圖片，如果失敗會有預設佔位圖
        self.image = ResourceManager.load_image(image_name)
        
        # 獲取圖片的矩形區域，並設置其左上角位置
        self.rect = self.image.get_rect(topleft=(x, y))
        self.live = True # 表示物件是否存活 (例如，血量歸零時設為 False)

    def draw(self, surface):
        """在指定的 Pygame surface 上繪製物件。"""
        if self.live: # 只有活著的物件才繪製
            surface.blit(self.image, self.rect)

    def update(self, game_state):
        """
        更新物件的狀態 (例如移動、攻擊、生成陽光等)。
        這是虛擬方法，子類需要覆寫此方法來實現各自的邏輯。
        """
        pass
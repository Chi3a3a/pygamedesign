# game_objects/map_tile.py

import pygame
from game_objects.base import GameObject # 導入基礎遊戲物件
from resources import ResourceManager # 導入資源管理器

class MapTile(GameObject):
    # 兩種不同顏色的地圖圖片名稱列表
    map_image_names = ['map1.png', 'map2.png']

    def __init__(self, x, y, img_index):
        # 根據 img_index 選擇圖片名稱
        image_name = MapTile.map_image_names[img_index]
        super().__init__(x, y, image_name) # 調用父類 GameObject 的初始化
        self.can_grow = True # 這個地圖塊是否可以種植植物
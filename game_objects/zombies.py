# game_objects/zombies.py

import pygame
from game_objects.base import GameObject
from game_config import GameConfig

class Zombie(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 'zombie.png')
        self.hp = GameConfig.ZOMBIE_HP_START # 殭屍生命值
        self.damage = GameConfig.ZOMBIE_DAMAGE # 殭屍攻擊力 (每幀對植物造成的傷害)
        self.speed = GameConfig.ZOMBIE_SPEED   # 殭屍移動速度
        self.stop = False # 標誌，表示殭屍是否因攻擊植物而停止移動

    def update(self, game_state):
        """殭屍的更新邏輯：移動並檢查是否與植物碰撞。"""
        if self.live:
            if not self.stop: # 如果沒有停止，就移動
                self.rect.x -= self.speed # 殭屍向左移動
                # 如果殭屍走出螢幕左邊界，遊戲結束
                if self.rect.x < -GameConfig.TILE_SIZE: 
                    game_state.game_over = True # 設定遊戲結束狀態
            self._check_plant_collision(game_state) # 檢查是否與植物碰撞

    def _check_plant_collision(self, game_state):
        """檢查殭屍是否與植物發生碰撞，如果碰撞則攻擊植物。"""
        collided = False
        for plant in game_state.plants:
            # 只有活著的植物才參與碰撞檢測
            if plant.live and pygame.sprite.collide_rect(self, plant):
                collided = True
                self.stop = True # 殭屍停止移動，開始攻擊植物
                plant.hp -= self.damage # 植物掉血

                if plant.hp <= 0: # 如果植物血量歸零
                    plant.live = False # 植物死亡
                    self.stop = False # 植物死了，殭屍可以繼續移動

                    # 找到對應的地圖塊，將其 'can_grow' 狀態設回 True
                    # 需要根據植物的位置計算出它位於哪個地圖格
                    grid_x = plant.rect.x // GameConfig.TILE_SIZE
                    grid_y = plant.rect.y // GameConfig.TILE_SIZE
                    
                    # 確保索引在範圍內 (因為地圖從 y=1 開始，所以 map_tiles 的行索引是 y-1)
                    if 0 <= grid_y - 1 < len(game_state.game_map_tiles) and \
                       0 <= grid_x < len(game_state.game_map_tiles[0]):
                        game_state.game_map_tiles[grid_y - 1][grid_x].can_grow = True
                break # 殭屍一次只攻擊一個植物

        # 如果殭屍沒有碰撞到任何活著的植物，則恢復移動狀態
        if not collided:
            self.stop = False
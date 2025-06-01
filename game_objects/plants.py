# game_objects/plants.py

from game_objects.base import GameObject
from game_config import GameConfig
# 豌豆射手需要生成豌豆子彈，所以需要導入 PeaBullet
from game_objects.bullets import PeaBullet 

class Plant(GameObject):
    def __init__(self, x, y, image_name, price, hp):
        super().__init__(x, y, image_name)
        self.price = price # 種植所需金錢
        self.hp = hp       # 生命值

class Sunflower(Plant):
    def __init__(self, x, y):
        # 調用父類 Plant 的初始化，傳入向日葵特有的圖片、價格、生命值
        super().__init__(x, y, 'sunflower.png', GameConfig.PLANT_PRICES["sunflower"], 100)
        self.time_to_produce_sun = 0 # 用於計時生成陽光

    def update(self, game_state):
        """向日葵的更新邏輯：計時並生成陽光金錢。"""
        if self.live:
            self.time_to_produce_sun += 1
            if self.time_to_produce_sun >= GameConfig.SUNFLOWER_MONEY_INTERVAL:
                game_state.money += GameConfig.SUNFLOWER_MONEY_PER_TICK
                self.time_to_produce_sun = 0

class PeaShooter(Plant):
    def __init__(self, x, y):
        # 調用父類 Plant 的初始化，傳入豌豆射手特有的圖片、價格、生命值
        super().__init__(x, y, 'peashooter.png', GameConfig.PLANT_PRICES["peashooter"], 200)
        self.shot_timer = 0 # 用於計時射擊

    def update(self, game_state):
        """豌豆射手的更新邏輯：檢查是否有殭屍在射程內並射擊。"""
        if self.live:
            should_fire = False
            # 遍歷所有殭屍，檢查是否有殭屍在同一行且在射擊範圍內
            for zombie in game_state.zombies: 
                # 判斷條件: 殭屍在同一行 (y 座標相同), 殭屍在螢幕內, 殭屍在豌豆射手右邊
                if zombie.live and zombie.rect.y == self.rect.y and \
                   zombie.rect.x < GameConfig.SCREEN_WIDTH and zombie.rect.x > self.rect.x:
                    should_fire = True
                    break # 只要找到一隻目標就足夠了

            if should_fire:
                self.shot_timer += 1
                if self.shot_timer >= GameConfig.PEASHOOTER_SHOT_INTERVAL:
                    # 在豌豆射手位置創建一顆豌豆子彈
                    peabullet = PeaBullet(self.rect.x + 60, self.rect.y + 15)
                    game_state.bullets.append(peabullet) # 將子彈加入到遊戲狀態的子彈列表中
                    self.shot_timer = 0 # 重置射擊計時器
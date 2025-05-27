# game_config.py

class GameConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 560
    TILE_SIZE = 80 # 地圖上每個格子的大小

    # 植物相關設定
    PLANT_PRICES = {"sunflower": 30, "peashooter": 50}
    SUNFLOWER_MONEY_PER_TICK = 5
    SUNFLOWER_MONEY_INTERVAL = 25 # 向日葵產錢間隔 (遊戲更新次數)
    PEASHOOTER_SHOT_INTERVAL = 25 # 豌豆射手射擊間隔 (遊戲更新次數)

    # 子彈相關設定
    BULLET_DAMAGE = 50
    BULLET_SPEED = 5
    BULLET_LIFE_SPAN = 100 # 子彈生命週期 (遊戲更新次數)

    # 殭屍相關設定
    ZOMBIE_HP_START = 1000
    ZOMBIE_DAMAGE = 2
    ZOMBIE_SPEED = 1
    ZOMBIE_SPAWN_INTERVAL_BASE = 100 # 基礎殭屍生成間隔
    ZOMBIE_SPAWN_INTERVAL_DECREMENT = 10 # 每關殭屍生成間隔減少量

    # 遊戲狀態與分數
    INITIAL_MONEY = 200
    INITIAL_REMNANT_SCORE = 100 # 達到下一關所需的分數起始值
    SCORE_PER_ZOMBIE = 20
    NEXT_LEVEL_SCORE_MULTIPLIER = 100 # 每關所需分數的乘數 (例如: 100 * 關卡數)
    MAX_LEVEL = 5 # 新增：遊戲的最高關卡數
    
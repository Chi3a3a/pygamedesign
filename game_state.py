# game_state.py

from game_config import GameConfig

class GameState:
    def __init__(self):
        self.game_over = False
        self.current_level = 1
        self.score = 0
        self.remnant_score = GameConfig.INITIAL_REMNANT_SCORE # 距離下一關還差的分數
        self.money = GameConfig.INITIAL_MONEY
        
        # 儲存遊戲中所有活動物件的列表
        self.plant_grid_points = [] # 地圖網格的邏輯坐標點列表 (用於初始化地圖)
        self.game_map_tiles = []    # 實際的 MapTile 物件的二維列表
        self.plants = []            # 所有的植物物件
        self.bullets = []           # 所有的子彈物件
        self.zombies = []           # 所有的殭屍物件

        # 殭屍生成計時器
        self.zombie_spawn_timer = 0
        # 殭屍生成閾值會根據關卡改變
        self.zombie_spawn_threshold = GameConfig.ZOMBIE_SPAWN_INTERVAL_BASE 

        self.screen = None # Pygame 視窗物件，在 GameManager 中設定
        self.first_zombie_wave_sound_played = False 

    def reset_game_state(self):
        """將所有遊戲狀態重置為初始值，用於重新開始遊戲。"""
        self.game_over = False
        self.current_level = 1
        self.score = 0
        self.remnant_score = GameConfig.INITIAL_REMNANT_SCORE
        self.money = GameConfig.INITIAL_MONEY
        
        self.plants.clear()
        self.bullets.clear()
        self.zombies.clear()
        
        # 地圖相關列表也需要清空，然後在 GameManager 中重新初始化
        self.plant_grid_points.clear()
        self.game_map_tiles.clear()
        
        self.zombie_spawn_timer = 0
        self.zombie_spawn_threshold = GameConfig.ZOMBIE_SPAWN_INTERVAL_BASE
        self.first_zombie_wave_sound_played = False 

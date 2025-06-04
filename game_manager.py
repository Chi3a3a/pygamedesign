# game_manager.py

import pygame
import random
from game_config import GameConfig
from game_state import GameState
from resources import ResourceManager # 導入資源管理器
# 從 game_objects 套件導入所有需要的遊戲物件類別
from game_objects import MapTile, Sunflower, PeaShooter, PeaBullet, Zombie 

class GameManager:
    def __init__(self):
        pygame.init() # 初始化 Pygame
        self.game_state = GameState() # 創建遊戲狀態物件
        # 設定 Pygame 視窗
        self.game_state.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("植物大戰殭屍") # 設定視窗標題
        self.clock = pygame.time.Clock() # 創建時鐘物件，用於控制幀率

        # 字體路徑，使用 ResourceManager 載入字體
        self.font_path = "fonts/fontsmsjh.ttf" 
        
        # 載入音效 (可以在這裡一次性載入，也可以在需要時載入)
        self.zombie_horde_sound = ResourceManager.load_sound("zombie_horde.mp3")
        self.win_sound = ResourceManager.load_sound("win_sound.mp3")
        self.lose_sound = ResourceManager.load_sound("lose_sound.mp3")

        # 定義一個旗標來控制殭屍來襲音效的播放頻率
        self.zombie_sound_played = False
        # 用於判斷是否是第一次進入遊戲，第一次才會播開場音樂
        self.first_game_start = True 

    def _draw_text(self, content, size, color):
        """輔助方法：繪製文字。"""
        font = ResourceManager.load_font(self.font_path, size) # 透過 ResourceManager 載入字體
        text_surface = font.render(content, True, color)
        return text_surface

    def _init_map_grid(self):
        """初始化地圖的邏輯網格點和實際地圖塊物件。"""
        # 創建地圖的邏輯網格點 (例如：(0,1), (1,1)...)
        # 遊戲區域從 y=1 行開始，共 6 行 (1-6)
        for y_idx in range(1, 7): 
            row_points = []
            # 每行 10 列 (0-9)
            for x_idx in range(10): 
                row_points.append((x_idx, y_idx))
            self.game_state.plant_grid_points.append(row_points)

        # 根據邏輯網格點，創建實際的 MapTile 物件
        for r_idx, row_points in enumerate(self.game_state.plant_grid_points):
            temp_map_row = []
            for c_idx, point in enumerate(row_points):
                # 交替使用兩種地圖圖片 (map1.png 和 map2.png)
                img_index = (point[0] + point[1]) % 2 
                # 創建 MapTile 物件，並設定其在螢幕上的位置
                map_tile = MapTile(point[0] * GameConfig.TILE_SIZE, point[1] * GameConfig.TILE_SIZE, img_index)
                temp_map_row.append(map_tile)
            self.game_state.game_map_tiles.append(temp_map_row)

    def _init_zombies(self):
        """初始化一批殭屍。"""
        # 決定這次要生成多少隻殭屍
        # 您可以根據關卡數來調整，例如：
        # num_zombies_to_spawn = min(5, self.game_state.current_level + 1)
        
        # 為了演示您提供的邏輯，我們讓它一次生成多隻殭屍，但可以調整
        # 如果您希望一次生成1隻，就設為1
        # 如果希望每行都生成，就維持 for loop 的範圍
        
        # 這裡我們結合兩種策略：每次生成隨機數量的殭屍，並使用您提供的水平間距邏輯
        num_zombies_this_wave = random.randint(1, 3) # 每次生成 1 到 3 隻

        # 為了確保不會在同一列生成，可以記錄已選的列
        spawned_rows = set() 

        for _ in range(num_zombies_this_wave):
            # 隨機選擇一行 (y 座標)，確保不會重複選到同一行
            while True:
                row_index = random.randint(1, 6) # 地圖行索引 1 到 6
                if row_index not in spawned_rows:
                    spawned_rows.add(row_index)
                    break
                # 如果所有行都已被選中，但 still_to_spawn > 0，則跳出循環避免無限循環
                if len(spawned_rows) == 6: 
                    break

            if len(spawned_rows) == 6 and _ < num_zombies_this_wave: # 防止在所有行都填滿後還試圖生成更多殭屍
                break

            # 根據您提供的邏輯計算水平間距
            # random.randint(1, 5) * 200 讓殭屍在螢幕外 200, 400, 600, 800, 1000 像素處生成
            # 這樣間距會比較大，不會擠在一起
            dis_offset = random.randint(1, 5) * 100 
            
            # 使用 GameConfig 中的常數
            initial_x = GameConfig.SCREEN_WIDTH + dis_offset 
            zombie = Zombie(initial_x, row_index * GameConfig.TILE_SIZE)
            self.game_state.zombies.append(zombie)


    def _handle_input(self):
        """處理所有 Pygame 事件 (鍵盤、滑鼠等)。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.game_over = True # 設定遊戲結束標誌
                pygame.quit() # 退出 Pygame
                exit()        # 終止程式
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # 如果按下了 'Q' 鍵
                    self.game_state.game_over = True # 設定遊戲結束標誌
                    print("按下 'Q' 鍵，遊戲結束。") # 可以在控制台輸出提示
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos # 獲取滑鼠點擊座標
                
                # 將滑鼠座標轉換為地圖網格的邏輯座標
                grid_x = mouse_x // GameConfig.TILE_SIZE
                grid_y = mouse_y // GameConfig.TILE_SIZE
                
                # 檢查點擊是否在有效的種植區域 (地圖網格內)
                if 1 <= grid_y <= 6 and 0 <= grid_x < 10:
                    # 獲取對應的地圖塊物件 (注意索引，因為地圖行是從 1 開始)
                    map_tile = self.game_state.game_map_tiles[grid_y - 1][grid_x]
                    
                    if map_tile.can_grow: # 如果該地圖塊可以種植
                        if event.button == 1: # 左鍵放置向日葵
                            if self.game_state.money >= GameConfig.PLANT_PRICES["sunflower"]:
                                sunflower = Sunflower(map_tile.rect.x, map_tile.rect.y)
                                self.game_state.plants.append(sunflower)
                                map_tile.can_grow = False # 設為不可種植
                                self.game_state.money -= GameConfig.PLANT_PRICES["sunflower"]
                        elif event.button == 3: # 右鍵放置豌豆射手
                            if self.game_state.money >= GameConfig.PLANT_PRICES["peashooter"]:
                                peashooter = PeaShooter(map_tile.rect.x, map_tile.rect.y)
                                self.game_state.plants.append(peashooter)
                                map_tile.can_grow = False # 設為不可種植
                                self.game_state.money -= GameConfig.PLANT_PRICES["peashooter"]

    def _update_game_state(self):
        """更新所有遊戲物件的狀態和遊戲邏輯。"""
        # 更新植物 (使用 list() 拷貝列表，以避免在迭代時修改列表導致的錯誤)
        for plant in list(self.game_state.plants): 
            if plant.live:
                plant.update(self.game_state) # 呼叫植物自己的 update 方法
            else:
                self.game_state.plants.remove(plant) # 如果植物死亡，從列表中移除

        # 更新子彈
        for bullet in list(self.game_state.bullets):
            if bullet.live:
                bullet.update(self.game_state) # 呼叫子彈自己的 update 方法
            else:
                self.game_state.bullets.remove(bullet) # 如果子彈死亡，從列表中移除

        # 更新殭屍
        for zombie in list(self.game_state.zombies):
            if zombie.live:
                zombie.update(self.game_state) # 呼叫殭屍自己的 update 方法
            else:
                self.game_state.zombies.remove(zombie) # 如果殭屍死亡，從列表中移除
        
        # 殭屍生成計時器
        self.game_state.zombie_spawn_timer += 1
        # 如果達到生成閾值，就生成一批新的殭屍
        if self.game_state.zombie_spawn_timer >= self.game_state.zombie_spawn_threshold:
            self._init_zombies() 
            self.game_state.zombie_spawn_timer = 0 # 重置計時器
            if not self.game_state.first_zombie_wave_sound_played:
                if self.zombie_horde_sound:
                    self.zombie_horde_sound.play()
                self.game_state.first_zombie_wave_sound_played = True
                
    def _draw_game_elements(self):
        """繪製遊戲畫面上的所有元素。"""
        self.game_state.screen.fill((255, 255, 255)) # 填充白色背景

        # 繪製地圖塊
        for row in self.game_state.game_map_tiles:
            for tile in row:
                tile.draw(self.game_state.screen) # 呼叫 MapTile 的 draw 方法

        # 繪製植物
        for plant in self.game_state.plants:
            plant.draw(self.game_state.screen) # 呼叫 Plant 的 draw 方法

        # 繪製子彈
        for bullet in self.game_state.bullets:
            bullet.draw(self.game_state.screen) # 呼叫 PeaBullet 的 draw 方法

        # 繪製殭屍
        for zombie in self.game_state.zombies:
            zombie.draw(self.game_state.screen) # 呼叫 Zombie 的 draw 方法

        # 繪製 UI (使用者介面)
        self.game_state.screen.blit(self._draw_text(f'當前錢數$: {self.game_state.money}', 26, (255, 0, 0)), (500, 40))
        self.game_state.screen.blit(self._draw_text(
            f'當前關數{self.game_state.current_level}，得分{self.game_state.score}, 距離下關還差{self.game_state.remnant_score}分', 26,
            (255, 0, 0)), (5, 40))
        self.game_state.screen.blit(self._draw_text('1.按左鍵放置向日葵 2.按右鍵放置豌豆射手', 26, (255, 0, 0)), (5, 5))

        pygame.display.update() # 更新整個螢幕顯示

    def show_start_screen(self):
        if self.first_game_start:
            ResourceManager.play_music("background_music.mp3", loops=-1) # 開場音樂循環播放
            self.first_game_start = False
        
        """顯示遊戲開始畫面。"""
        start_image = ResourceManager.load_image("start.png")
        start_image = pygame.transform.scale(start_image, (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        self.game_state.screen.blit(start_image, (0, 0))

        # 繪製「點擊任意處開始遊戲」的提示文字
        tip_text = self._draw_text("點擊任意處開始遊戲", 25, (0, 0, 0))
        # 計算文字位置，使其居中偏上一些
        tip_rect = tip_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2 + 75, GameConfig.SCREEN_HEIGHT // 2 - 15))
        self.game_state.screen.blit(tip_text, tip_rect)

        # --- 新增的「規則說明」文字 ---
        role_text = self._draw_text("規則說明", 25, (255, 255, 255)) # 白色文字
        # 計算文字位置，使其在「開始遊戲」文字下方
        role_rect = role_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2 - 67, GameConfig.SCREEN_HEIGHT // 2 + 127))
        self.game_state.screen.blit(role_text, role_rect)
        # --- 新增的「規則說明」文字結束 ---

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ResourceManager.stop_music() # 退出時停止音樂
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos # 獲取滑鼠點擊座標
                    
                    # 判斷是否點擊了「規則說明」區域
                    if role_rect.collidepoint(mouse_x, mouse_y):
                        self._show_rules_screen() # 呼叫顯示規則的方法
                        # 顯示完規則後，需要重新繪製開始畫面，因為規則畫面會覆蓋掉它
                        self.game_state.screen.blit(start_image, (0, 0))
                        self.game_state.screen.blit(tip_text, tip_rect)
                        self.game_state.screen.blit(role_text, role_rect)
                        pygame.display.update()
                    else:
                        # 如果沒有點擊「規則說明」區域，則開始遊戲
                        waiting = False # 結束等待迴圈，讓遊戲主迴圈開始

    def _show_rules_screen(self):
        """顯示遊戲規則說明畫面。"""
        rules_background = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        rules_background.fill((0, 0, 50)) # 深藍色背景

        # 規則內容 (您可以根據需要添加更多行)
        rules_lines = [
            "遊戲規則:",
            "1. 左鍵點擊空地種植向日葵($30)，向日葵會產錢。",
            "2. 右鍵點擊空地種植豌豆射手($50)，豌豆射手會攻擊殭屍。",
            "3. 殭屍會從右邊出現，向左移動。",
            "4. 如果殭屍突破防線，遊戲結束。",
            "5. 消滅殭屍可得分，達到一定分數進入下一關。",
            "6. 按 'Q' 鍵隨時結束遊戲。",
            "",
            "點擊任意處返回主畫面..."
        ]

        # 繪製規則文字
        y_offset = 150
        for line in rules_lines:
            rule_text = self._draw_text(line, 22, (255, 255, 255)) # 白色文字
            rule_rect = rule_text.get_rect(center=(GameConfig.SCREEN_WIDTH // 2, y_offset))
            rules_background.blit(rule_text, rule_rect)
            y_offset += 30 # 每行間距

        self.game_state.screen.blit(rules_background, (0, 0))
        pygame.display.update()

        # 等待玩家點擊返回
        waiting_for_return = True
        while waiting_for_return:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_return = False # 玩家點擊後返回

    def game_over_screen(self):
        ResourceManager.stop_music() # 停止當前播放的背景音樂
        win_image = ResourceManager.load_image("CLEAR.png")
        lose_image = ResourceManager.load_image("GAMEOVER.png")

        if self.game_state.current_level >= GameConfig.MAX_LEVEL:
            self.game_state.screen.blit(win_image, (0, 0))
            # 這裡需要更精確的勝利判斷，例如：所有殭屍被消滅，且達到最高關卡
            # 假設達到 MAX_LEVEL 且沒有殭屍殘留就算勝利
            if self.win_sound:
                self.win_sound.play()
            self.game_state.screen.blit(self._draw_text('回主頁', 25, (0, 0, 0)), (360, 410))
            self.game_state.screen.blit(self._draw_text(f'你的分數: {self.game_state.score}', 30, (255, 255, 255)), (300, 320))

        else:
            self.game_state.screen.blit(lose_image, (0, 0))
            if self.lose_sound:
                self.lose_sound.play()
            self.game_state.screen.blit(self._draw_text('重新', 50, (255, 255, 255)), (525, 360))
            self.game_state.screen.blit(self._draw_text(f'你的分數: {self.game_state.score}', 30, (255, 255, 255)), (500, 270))

        pygame.display.update()
        pygame.time.wait(1000)

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ResourceManager.stop_music() # 退出時停止音樂
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_restart = False
        
        # 重置遊戲狀態，並準備下一次開始時播放開場音樂
        self.game_state.reset_game_state()
        self.first_game_start = True # 重置為 True，下次 show_start_screen 會再播放音樂

    def run_game(self):
        """遊戲的主迴圈。"""
        # 遊戲開始前，如果還在背景播放開場音樂，可以選擇停止
        # 或者，如果遊戲中要用同一首音樂，這裡就不用特別處理
        # 如果遊戲中要播放另一首遊戲音樂，可以在這裡 ResourceManager.play_music("game_music.mp3", loops=-1)

        if not self.game_state.game_map_tiles:
             self._init_map_grid()
        if not self.game_state.zombies:
             self._init_zombies()

        while not self.game_state.game_over:
            self._handle_input()
            self._update_game_state()
            self._draw_game_elements()

            if self.game_state.game_over:
                self.game_over_screen()
                break
                
            self.clock.tick(60)

        if self.game_state.game_over:
            print("遊戲徹底結束。")

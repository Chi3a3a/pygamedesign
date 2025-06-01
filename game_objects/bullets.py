# game_objects/bullets.py

import pygame
from game_objects.base import GameObject
from game_config import GameConfig

class PeaBullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 'peabullet.png')
        self.damage = GameConfig.BULLET_DAMAGE
        self.speed = GameConfig.BULLET_SPEED

    def update(self, game_state):
        if self.live:
            self.rect.x += self.speed
            if self.rect.x > GameConfig.SCREEN_WIDTH:
                self.live = False
            self._check_collision(game_state)

    def _check_collision(self, game_state):
        for zombie in game_state.zombies:
            if zombie.live and pygame.sprite.collide_rect(self, zombie):
                self.live = False
                zombie.hp -= self.damage

                if zombie.hp <= 0:
                    zombie.live = False
                    game_state.score += GameConfig.SCORE_PER_ZOMBIE
                    game_state.remnant_score -= GameConfig.SCORE_PER_ZOMBIE

                    # 檢查是否達到進入下一關的分數
                    if game_state.remnant_score <= 0:
                        # --- 新增的關卡上限檢查 ---
                        if game_state.current_level >= GameConfig.MAX_LEVEL:
                            # 達到最高關卡，遊戲勝利結束
                            print(f"恭喜！您已達到最高關卡 {GameConfig.MAX_LEVEL}！遊戲結束。")
                            game_state.game_over = True # 設定遊戲結束
                            # 這裡可以考慮設置一個勝利標誌，讓 game_over_screen 顯示不同的訊息
                            # 例如：game_state.victory = True
                        else:
                            # 尚未達到最高關卡，正常升級
                            game_state.current_level += 1
                            print(f"升級！進入第 {game_state.current_level} 關。")
                            # 計算下一關所需分數
                            game_state.remnant_score = game_state.current_level * GameConfig.NEXT_LEVEL_SCORE_MULTIPLIER
                            # 隨著關卡推進，殭屍生成間隔會縮短（速度加快）
                            # 確保閾值不會變成負數或太小
                            game_state.zombie_spawn_threshold = max(50, GameConfig.ZOMBIE_SPAWN_INTERVAL_BASE -
                                                                     (game_state.current_level - 1) * GameConfig.ZOMBIE_SPAWN_INTERVAL_DECREMENT)
                break
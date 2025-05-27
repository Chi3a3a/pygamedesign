# main.py

from game_manager import GameManager

if __name__ == '__main__':
    game = GameManager()
    while True: # 增加一個無限迴圈來處理遊戲的多次開始和結束
        game.show_start_screen() # 顯示開始畫面，等待玩家點擊開始
        # 當 show_start_screen 結束後，表示玩家已點擊開始，接著運行遊戲
        game.run_game()
        # 當 run_game 結束後，表示遊戲結束 (game_state.game_over 為 True)，
        # run_game 內部會呼叫 game_over_screen，而 game_over_screen 會重置狀態並等待用戶點擊回到主畫面。
        # 之後迴圈會再次回到 game.show_start_screen()
# resources.py

import pygame
import os

class ResourceManager:
    _images = {} # 用於快取已載入的圖片
    _fonts = {}  # 用於快取已載入的字體
    _sounds = {} # 新增：用於快取已載入的音效


    @staticmethod
    def load_image(image_name):
        """
        載入圖片並將其快取。
        image_name: 圖片檔案名 (例如 'sunflower.png')。圖片應放在 'imgs/' 資料夾內。
        """
        if image_name not in ResourceManager._images:
            full_path = os.path.join("imgs", image_name) # 圖片路徑
            try:
                # .convert_alpha() 讓圖片背景透明度正確顯示
                image = pygame.image.load(full_path).convert_alpha() 
                ResourceManager._images[image_name] = image
                return image
            except pygame.error as e:
                print(f"錯誤: 無法載入圖片 {full_path}: {e}")
                # 如果圖片載入失敗，返回一個洋紅色的方塊作為佔位符
                placeholder_image = pygame.Surface((80, 80)) # 假設標準尺寸
                placeholder_image.fill((255, 0, 255)) 
                ResourceManager._images[image_name] = placeholder_image
                return placeholder_image
        return ResourceManager._images[image_name]

    @staticmethod
    def load_font(font_path, size):
        """
        載入字體並將其快取。
        font_path: 字體檔案路徑 (例如 'fonts/fontsmsjh.ttf')。
        size: 字體大小。
        """
        key = (font_path, size) # 用路徑和大小作為快取鍵
        if key not in ResourceManager._fonts:
            try:
                font = pygame.font.Font(font_path, size)
                ResourceManager._fonts[key] = font
                return font
            except FileNotFoundError:
                print(f"錯誤: 無法載入字體 {font_path}，將使用系統預設字體。")
                # 如果字體檔案找不到，使用系統預設字體
                font = pygame.font.SysFont("Arial", size)
                ResourceManager._fonts[key] = font
                return font
        return ResourceManager._fonts[key]
    
    @staticmethod
    def load_sound(sound_name):
        """
        載入音效並將其快取。
        sound_name: 音效檔案名 (例如 'zombie_horde.mp3')。音效應放在 'sounds/' 資料夾內。
        """
        if sound_name not in ResourceManager._sounds:
            full_path = os.path.join("sounds", sound_name) # 音效路徑
            try:
                sound = pygame.mixer.Sound(full_path)
                ResourceManager._sounds[sound_name] = sound
                return sound
            except pygame.error as e:
                print(f"錯誤: 無法載入音效 {full_path}: {e}")
                return None # 載入失敗返回 None
        return ResourceManager._sounds[sound_name]

    @staticmethod
    def play_music(music_name, loops=-1):
        """
        播放背景音樂 (使用 pygame.mixer.music)。
        music_name: 音樂檔案名 (例如 'background_music.mp3')。
        loops: 播放次數，-1 為無限循環。
        """
        full_path = os.path.join("sounds", music_name)
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(loops)
        except pygame.error as e:
            print(f"錯誤: 無法播放音樂 {full_path}: {e}")

    @staticmethod
    def stop_music():
        """停止當前播放的背景音樂。"""
        pygame.mixer.music.stop()
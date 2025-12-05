"""Конфигурация игры"""
import pygame

# Пути к ресурсам
ASSETS_PATH = "assets/"
BACKGROUNDS_PATH = "assets/backgrounds/"
TOWERS_PATH = "assets/towers/"
AUDIO_PATH = "assets/audio/"

# Настройки по умолчанию
DEFAULT_SETTINGS = {
    "music_volume": 0.5,
    "sound_volume": 0.7,
    "selected_background": 0,
}

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# FPS
FPS = 60

# Размеры блоков – под tower_x_*.png (96x48)
BLOCK_WIDTH = 96
BLOCK_HEIGHT = 48

# Для совместимости с resource_manager (ДОЛЖНО ИДТИ ПОСЛЕ BLOCK_WIDTH/HEIGHT)
TOWER_PART_WIDTH = BLOCK_WIDTH
TOWER_PART_HEIGHT = BLOCK_HEIGHT
TOWER_MID_PARTS_COUNT = 4

# Физика блока
GRAVITY = 0.5
ROPE_LENGTH = 150
ORIGIN = (400, 3)

# Настройки башни
SCROLL_SPEED = 5
MAX_LIVES = 3

# Скины башен
TOWER_SKINS = {
    "tower_1": {"name": "Classic Tower", "price": 0, "unlocked": True},
    "tower_2": {"name": "Modern Tower", "price": 100, "unlocked": False},
    "tower_3": {"name": "Ancient Tower", "price": 150, "unlocked": False},
    "tower_4": {"name": "Future Tower", "price": 200, "unlocked": False},
    "tower_5": {"name": "Crystal Tower", "price": 250, "unlocked": False},
    "tower_6": {"name": "Dark Tower", "price": 300, "unlocked": False},
    "tower_7": {"name": "Golden Tower", "price": 400, "unlocked": False},
    "tower_8": {"name": "Rainbow Tower", "price": 500, "unlocked": False},
}

# Фоны
BACKGROUND_COUNT = 3
BACKGROUND_SCROLL_HEIGHT = 600
BACKGROUND_NAMES = ["City Day", "City Night", "City Sunset"]

# Сила раскачивания
INITIAL_FORCE = -0.001
FORCE_MULTIPLIER = 1.02

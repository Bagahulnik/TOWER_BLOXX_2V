"""Константы и настройки игры"""

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)

# Физика
GRAVITY = 0.5
ROPE_LENGTH = 120
INITIAL_FORCE = -0.001
FORCE_MULTIPLIER = 1.02
ORIGIN = (400, 3)

# Геймплей
FPS = 120
BLINK_INTERVAL = 800
SCROLL_SPEED = 5

# Размеры блоков
BLOCK_WIDTH = 64
BLOCK_HEIGHT = 64

# Фоны
BACKGROUND_COUNT = 5
BACKGROUND_SCROLL_HEIGHT = 600

# Магазин
TOWER_SKINS = {
    'tower_1': {'name': 'Classic', 'price': 0, 'unlocked': True},
    'tower_2': {'name': 'Stone', 'price': 50, 'unlocked': False},
    'tower_3': {'name': 'Ice', 'price': 100, 'unlocked': False},
    'tower_4': {'name': 'Desert', 'price': 150, 'unlocked': False},
    'tower_5': {'name': 'Neon', 'price': 200, 'unlocked': False},
    'tower_6': {'name': 'Pink', 'price': 250, 'unlocked': False},
    'tower_7': {'name': 'Gothic', 'price': 300, 'unlocked': False},
    'tower_8': {'name': 'Golden', 'price': 500, 'unlocked': False},
}

# Пути к ресурсам
ASSETS_PATH = "assets/"
BACKGROUNDS_PATH = "assets/backgrounds/"
TOWERS_PATH = "assets/towers/"
AUDIO_PATH = "assets/audio/"

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
MAX_LIVES = 3

# Размеры блоков
BLOCK_WIDTH = 96
BLOCK_HEIGHT = 64

# Фоны
BACKGROUND_COUNT = 5
BACKGROUND_SCROLL_HEIGHT = 600

# Магазин (НАЗВАНИЯ ПО МАТЕРИАЛАМ)
TOWER_SKINS = {
    'tower_1': {'name': 'Wood', 'price': 0, 'unlocked': True},        # Деревянная
    'tower_2': {'name': 'Ice', 'price': 50, 'unlocked': False},       # Ледяная
    'tower_3': {'name': 'Steel', 'price': 100, 'unlocked': False},    # Стальная
    'tower_4': {'name': 'Stone', 'price': 150, 'unlocked': False},    # Каменная
    'tower_5': {'name': 'Brick', 'price': 200, 'unlocked': False},    # Кирпичная
    'tower_6': {'name': 'Gold', 'price': 250, 'unlocked': False},     # Золотая
    'tower_7': {'name': 'Marble', 'price': 300, 'unlocked': False},   # Мраморная
    'tower_8': {'name': 'Crystal', 'price': 500, 'unlocked': False},  # Хрустальная
}

# Названия фонов для меню
BACKGROUND_NAMES = {
    0: 'Day Sky',      # bg1
    1: 'Sunset',       # bg2
    2: 'Night',        # bg3
    3: 'Storm',        # bg4
    4: 'Space'         # bg5
}

# Пути к ресурсам
ASSETS_PATH = "assets/"
BACKGROUNDS_PATH = "assets/backgrounds/"
TOWERS_PATH = "assets/towers/"
AUDIO_PATH = "assets/audio/"

# Настройки по умолчанию
DEFAULT_SETTINGS = {
    'music_volume': 0.5,  # 0.0 - 1.0
    'sound_volume': 0.7,
    'selected_background': 0  # Индекс фона (0-4)
}

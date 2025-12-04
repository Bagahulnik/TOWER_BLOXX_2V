"""Управление загрузкой ресурсов с автоматическим разделением спрайтов"""
import pygame
import os
from config import *
from managers.sprite_splitter import SpriteSplitter

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.tower_sprites = {}
        self.sprite_splitter = SpriteSplitter(TOWERS_PATH, BLOCK_WIDTH)
        
    def load_image(self, name, path):
        """Загрузка изображения"""
        # Пробуем разные варианты путей
        possible_paths = [
            os.path.join(ASSETS_PATH, path),
            path,
            os.path.join(ASSETS_PATH, os.path.basename(path))
        ]
        
        for full_path in possible_paths:
            if os.path.exists(full_path):
                try:
                    self.images[name] = pygame.image.load(full_path).convert_alpha()
                    return self.images[name]
                except Exception as e:
                    print(f"Error loading image {full_path}: {e}")
        
        print(f"Warning: Image '{name}' not found at: {path}")
        return None
    
    def load_sound(self, name, path):
        """Загрузка звука (принимает полный путь)"""
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            return self.sounds[name]
        except Exception as e:
            print(f"Error loading sound '{name}' from {path}: {e}")
            return None
    
    def prepare_tower_sprites(self):
        """
        Подготовка спрайтов башен
        Автоматически разделяет полные спрайты на части если нужно
        """
        print("\n=== Preparing tower sprites ===")
        self.sprite_splitter.split_all_towers()
        print("=== Tower sprites ready ===\n")
    
    def load_tower_parts(self, tower_id):
        """Загрузка частей башни"""
        tower_path = os.path.join(TOWERS_PATH, tower_id)
        parts = {}
        
        # Проверяем существование папки
        if not os.path.exists(tower_path):
            os.makedirs(tower_path, exist_ok=True)
            print(f"Created directory: {tower_path}")
            return self.get_fallback_parts()
        
        # Загружаем части
        for part_name in ['base', 'middle', 'top']:
            part_path = os.path.join(tower_path, f"{part_name}.png")
            if os.path.exists(part_path):
                try:
                    parts[part_name] = pygame.image.load(part_path).convert_alpha()
                except Exception as e:
                    print(f"Error loading {part_name} for {tower_id}: {e}")
        
        # Если нет всех частей, пробуем загрузить full.png и разделить
        if len(parts) < 3:
            full_path = os.path.join(tower_path, "full.png")
            if os.path.exists(full_path):
                print(f"Using full.png for {tower_id}")
                try:
                    full_sprite = pygame.image.load(full_path).convert_alpha()
                    parts = self.split_pygame_surface(full_sprite)
                except Exception as e:
                    print(f"Error splitting full sprite for {tower_id}: {e}")
        
        # Если все еще нет частей, используем запасной вариант
        if not parts or len(parts) < 3:
            parts = self.get_fallback_parts()
        
        self.tower_sprites[tower_id] = parts
        return parts
    
    def split_pygame_surface(self, surface):
        """Разделение pygame surface на части"""
        width = surface.get_width()
        height = surface.get_height()
        block_height = BLOCK_HEIGHT
        
        parts = {}
        
        try:
            # Верхний блок
            top = pygame.Surface((width, block_height), pygame.SRCALPHA)
            top.blit(surface, (0, 0), (0, 0, width, block_height))
            parts['top'] = top
            
            # Средний блок
            if height > block_height * 2:
                middle = pygame.Surface((width, block_height), pygame.SRCALPHA)
                middle.blit(surface, (0, 0), (0, block_height, width, block_height))
                parts['middle'] = middle
            else:
                parts['middle'] = parts['top'].copy()
            
            # Нижний блок
            if height > block_height:
                base_y = height - block_height
                base = pygame.Surface((width, block_height), pygame.SRCALPHA)
                base.blit(surface, (0, 0), (0, base_y, width, block_height))
                parts['base'] = base
            else:
                parts['base'] = parts['top'].copy()
        except Exception as e:
            print(f"Error in split_pygame_surface: {e}")
            return self.get_fallback_parts()
        
        return parts
    
    def get_fallback_parts(self):
        """Создание запасных блоков если нет спрайтов"""
        fallback = {}
        colors = {
            'top': (200, 100, 100),
            'middle': (100, 150, 200),
            'base': (150, 150, 100)
        }
        
        for part, color in colors.items():
            surf = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
            surf.fill((*color, 255))
            pygame.draw.rect(surf, (255, 255, 255), (2, 2, BLOCK_WIDTH-4, BLOCK_HEIGHT-4), 2)
            # Добавляем текст для отладки
            font = pygame.font.Font(None, 20)
            text = font.render(part[:3].upper(), True, (255, 255, 255))
            text_rect = text.get_rect(center=(BLOCK_WIDTH//2, BLOCK_HEIGHT//2))
            surf.blit(text, text_rect)
            fallback[part] = surf
        
        return fallback
    
    def get_tower_part(self, tower_id, part_name, floor_num):
        """Получить часть башни в зависимости от этажа"""
        if tower_id not in self.tower_sprites:
            self.load_tower_parts(tower_id)
        
        parts = self.tower_sprites.get(tower_id)
        if not parts:
            parts = self.get_fallback_parts()
        
        # Логика выбора части
        if floor_num == 0:
            return parts.get('base', parts.get('middle'))
        elif part_name == 'top':
            return parts.get('top', parts.get('middle'))
        else:
            return parts.get('middle', parts.get('top'))
    
    def get_image(self, name):
        return self.images.get(name)
    
    def get_sound(self, name):
        return self.sounds.get(name)

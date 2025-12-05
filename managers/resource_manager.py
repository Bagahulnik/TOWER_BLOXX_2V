"""Менеджер ресурсов под Tower/Block"""
import pygame
import os
import itertools
from config import TOWER_MID_PARTS_COUNT

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.tower_sprites = {}
        self.sounds = {}
        self.next_block_cycle = {}

    def load_image(self, name, path):
        try:
            full_path = os.path.join("assets", path)
            img = pygame.image.load(full_path).convert_alpha()
            self.images[name] = img
            return img
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def get_image(self, name):
        return self.images.get(name)

    def load_sound(self, name, path):
        try:
            full_path = os.path.join("assets", path)
            snd = pygame.mixer.Sound(full_path)
            self.sounds[name] = snd
            return snd
        except Exception as e:
            print(f"Error loading sound {path}: {e}")
            return None

    def get_sound(self, name):
        return self.sounds.get(name)

    def load_tower_parts(self, skin_id):
        if skin_id in self.tower_sprites:
            return self.tower_sprites[skin_id]

        parts = {"base": None, "middle_list": []}
        tower_num = skin_id.split("_")[1]
        folder = f"towers/tower_{tower_num}"

        base_path = os.path.join(folder, f"tower_{tower_num}_bot.png")
        base_img = self.load_image(f"{skin_id}_base", base_path)
        if base_img:
            parts["base"] = base_img
            print(f"Loaded: {base_path}")

        for i in range(TOWER_MID_PARTS_COUNT):
            mid_path = os.path.join(folder, f"tower_{tower_num}_mid_{i}.png")
            mid_img = self.load_image(f"{skin_id}_mid_{i}", mid_path)
            if mid_img:
                parts["middle_list"].append(mid_img)
                print(f"Loaded: {mid_path}")

        self.tower_sprites[skin_id] = parts
        return parts

    def get_next_block_sprite(self, skin_id):
        if skin_id not in self.next_block_cycle:
            parts = self.load_tower_parts(skin_id)
            base = parts.get("base")
            mids = parts.get("middle_list", [])
            self.next_block_cycle[skin_id] = {
                'is_first': True,
                'base': base,
                'mids': mids,
                'cycle': itertools.cycle(mids) if mids else None
            }
        
        cycle_data = self.next_block_cycle[skin_id]
        
        if cycle_data['is_first']:
            cycle_data['is_first'] = False
            return cycle_data['base']
        
        if cycle_data['cycle']:
            return next(cycle_data['cycle'])
        
        return None

    def reset_block_cycle(self, skin_id):
        """Полный сброс очереди"""
        if skin_id in self.next_block_cycle:
            del self.next_block_cycle[skin_id]

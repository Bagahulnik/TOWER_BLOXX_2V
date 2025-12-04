"""Управление аудио"""
import pygame
import os
from config import ASSETS_PATH, AUDIO_PATH

class AudioManager:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        self.music_loaded = False
        
    def load_resources(self):
        """Загрузка всех звуков"""
        # Пробуем разные пути для музыки
        music_paths = [
            os.path.join(AUDIO_PATH, "bgm.wav"),
            os.path.join(ASSETS_PATH, "bgm.wav"),
            os.path.join(ASSETS_PATH, "audio", "bgm.wav"),
            "bgm.wav"
        ]
        
        for music_path in music_paths:
            if os.path.exists(music_path):
                try:
                    pygame.mixer.music.load(music_path)
                    self.music_loaded = True
                    print(f"✓ Background music loaded from: {music_path}")
                    break
                except Exception as e:
                    print(f"✗ Failed to load music from {music_path}: {e}")
        
        if not self.music_loaded:
            print("⚠ Background music not found, continuing without music")
        
        # Загружаем звуковые эффекты (БЕЗ 'over')
        sound_files = {
            'build': 'build.wav',
            'gold': 'gold.wav',
            'overmusic': 'overmusic.wav',
            'fall': 'fall.wav'
        }
        
        for sound_name, filename in sound_files.items():
            sound_paths = [
                os.path.join(AUDIO_PATH, filename),
                os.path.join(ASSETS_PATH, "audio", filename),
                os.path.join(ASSETS_PATH, filename),
                filename
            ]
            
            loaded = False
            for sound_path in sound_paths:
                if os.path.exists(sound_path):
                    try:
                        self.resource_manager.load_sound(sound_name, sound_path)
                        print(f"✓ Sound '{sound_name}' loaded from: {sound_path}")
                        loaded = True
                        break
                    except Exception as e:
                        print(f"✗ Failed to load sound '{sound_name}' from {sound_path}: {e}")
            
            if not loaded:
                print(f"⚠ Sound '{sound_name}' ({filename}) not found, continuing without it")
    
    def play_music(self, loop=-1):
        """Воспроизведение фоновой музыки"""
        if self.music_loaded:
            try:
                pygame.mixer.music.play(loop)
            except Exception as e:
                print(f"Failed to play music: {e}")
    
    def play_sound(self, name):
        """Воспроизведение звукового эффекта"""
        sound = self.resource_manager.get_sound(name)
        if sound:
            try:
                sound.play()
            except Exception as e:
                print(f"Failed to play sound '{name}': {e}")
    
    def set_music_volume(self, volume):
        """Установить громкость музыки (0.0 - 1.0)"""
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
    
    def set_sound_volume(self, volume):
        """Установить громкость звуков (0.0 - 1.0)"""
        volume = max(0.0, min(1.0, volume))
        for sound in self.resource_manager.sounds.values():
            if sound:
                sound.set_volume(volume)

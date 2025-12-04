"""Основной игровой класс с магазином и настройками"""
import pygame
from config import *
from entities.block import Block
from entities.tower import Tower
from ui.hud import HUD
from ui.gameover_screen import GameOverScreen
from ui.shop_menu import ShopMenu
from ui.settings_menu import SettingsMenu
from ui.button import Button
from managers.resource_manager import ResourceManager
from managers.audio_manager import AudioManager
from managers.save_manager import SaveManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Brocks")
        
        self.save_manager = SaveManager()
        self.resource_manager = ResourceManager()
        self.audio_manager = AudioManager(self.resource_manager)
        
        self.load_resources()
        
        self.hud = HUD(pygame.font.Font("freesansbold.ttf", 32))
        self.gameover_screen = GameOverScreen(
            pygame.font.Font("freesansbold.ttf", 64),
            pygame.font.Font("freesansbold.ttf", 32),
            pygame.font.Font("freesansbold.ttf", 16),
            self.create_fallback_background()
        )
        self.shop_menu = ShopMenu(self.save_manager, self.resource_manager)
        self.settings_menu = SettingsMenu(self.save_manager, self.audio_manager)
        
        self.shop_button = Button(650, 10, 130, 40, "Shop", 
                                  pygame.font.Font("freesansbold.ttf", 20),
                                  color=(100, 100, 200), hover_color=(150, 150, 255))
        
        self.settings_button = Button(500, 10, 130, 40, "Settings", 
                                      pygame.font.Font("freesansbold.ttf", 20),
                                      color=(120, 80, 200), hover_color=(180, 120, 255))
        
        self.shop_open = False
        self.settings_open = False
        self.force = INITIAL_FORCE
        self.camera_descending = False
        self.reset_game()
        
        self.audio_manager.set_music_volume(self.save_manager.get_music_volume())
        self.audio_manager.set_sound_volume(self.save_manager.get_sound_volume())
        
        self.clock = pygame.time.Clock()
    
    def create_fallback_background(self):
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((135, 206, 235))
        return bg
        
    def load_resources(self):
        icon = self.resource_manager.load_image('icon', 'ground_tileset.png')
        if icon:
            pygame.display.set_icon(icon)
        
        for i in range(1, BACKGROUND_COUNT + 1):
            bg = self.resource_manager.load_image(f'bg{i}', f'backgrounds/bg{i}.png')
            if not bg:
                bg = self.create_fallback_background()
                self.resource_manager.images[f'bg{i}'] = bg
        
        self.resource_manager.load_image('ground', 'ground_tileset.png')
        
        print("\n=== Loading tower skins ===")
        for tower_id in TOWER_SKINS.keys():
            self.resource_manager.load_tower_parts(tower_id)
        print("=== Tower skins loaded ===\n")
        
        self.audio_manager.load_resources()
        self.audio_manager.play_music()
    
    def reset_game(self):
        selected_skin = self.save_manager.get_selected_skin()
        block_sprite = self.resource_manager.get_tower_part(selected_skin, 'middle', 0)
        self.block = Block(block_sprite, self.force)
        self.tower = Tower(self.resource_manager, selected_skin)
        self.score = 0
        self.lives = MAX_LIVES
        self.screenY = 0
        self.force = INITIAL_FORCE
        self.gameover = False
        self.camera_descending = False
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.settings_open:
                result = self.settings_menu.handle_event(event, mouse_pos)
                if result == 'close':
                    self.settings_open = False
                elif result == 'background_changed':
                    pass
            
            elif self.shop_open:
                result = self.shop_menu.handle_event(event, mouse_pos)
                if result == 'close':
                    self.shop_open = False
                elif result == 'skin_selected' or result == 'skin_purchased':
                    selected_skin = self.save_manager.get_selected_skin()
                    self.tower.change_skin(selected_skin)
                    block_sprite = self.resource_manager.get_tower_part(selected_skin, 'middle', 0)
                    self.block.image = block_sprite
                    self.block.rotimg = block_sprite
            else:
                self.shop_button.update(mouse_pos)
                self.settings_button.update(mouse_pos)
                
                if self.shop_button.is_clicked(event):
                    self.shop_open = True
                if self.settings_button.is_clicked(event):
                    self.settings_open = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.block.get_state() == "ready" and not self.camera_descending:
                            self.block.drop(self.tower)
        
        return True
    
    def update(self):
        if self.shop_open or self.settings_open:
            return
        
        # Плавное опускание камеры после падения башни
        if self.camera_descending:
            if self.screenY > 0:
                self.screenY -= 10  # Скорость опускания
                if self.screenY < 0:
                    self.screenY = 0
            else:
                self.camera_descending = False
                # Восстанавливаем башню после опускания камеры
                selected_skin = self.save_manager.get_selected_skin()
                self.tower = Tower(self.resource_manager, selected_skin)
                self.tower.y = 600
                self.block.respawn(self.tower, self.force)
            return
        
        if self.block.get_state() == "ready":
            self.block.swing()
        elif self.block.get_state() == "dropped":
            self.block.drop(self.tower)
        elif self.block.get_state() == "landed":
            if self.block.to_build(self.tower):
                self.tower.build(self.block.xlast)
                if self.tower.is_golden():
                    self.audio_manager.play_sound('gold')
                    self.score += 2
                    self.save_manager.add_coins(2)
                else:
                    self.audio_manager.play_sound('build')
                    self.score += 1
                    self.save_manager.add_coins(1)
            
            if self.tower.size >= 2:
                self.block.collapse(self.tower)
        
        elif self.block.get_state() == "over":
            self.tower.unbuild(self.block)
            self.block.to_fall(self.tower)
            if not hasattr(self, '_fall_sound_played'):
                self._fall_sound_played = True
                self.audio_manager.play_sound('fall')
                self.audio_manager.play_sound('overmusic')
        
        elif self.block.get_state() == "scroll" and not self.tower.is_scrolling():
            self.force *= FORCE_MULTIPLIER
            self.block.respawn(self.tower, self.force)
            if self.tower.size >= 5:
                self.tower.reset()
            if hasattr(self, '_fall_sound_played'):
                del self._fall_sound_played
        
        if self.tower.height >= BLOCK_HEIGHT * 5 and self.tower.size >= 5:
            self.tower.scroll()
            self.screenY += SCROLL_SPEED
        
        self.tower.wobble()
        self.check_gameover()
    
    def check_gameover(self):
        if self.tower.get_width() < -140:
            self.tower.collapse("l")
            if not hasattr(self, '_collapse_sound_played'):
                self._collapse_sound_played = True
                self.audio_manager.play_sound('overmusic')
        elif self.tower.get_width() > 140:
            self.tower.collapse("r")
            if not hasattr(self, '_collapse_sound_played'):
                self._collapse_sound_played = True
                self.audio_manager.play_sound('overmusic')
        
        if self.tower.y > 600:
            self.block.x = 2000
            self.tower.size -= 1
            self.lives -= 1
            if self.lives <= 0:
                self.gameover = True
            else:
                # Запускаем опускание камеры
                self.camera_descending = True
            if hasattr(self, '_collapse_sound_played'):
                del self._collapse_sound_played
                
        elif self.block.get_state() == "over" and self.block.y > 600:
            self.tower.y = 2000
            self.tower.size -= 1
            self.lives -= 1
            if self.lives <= 0:
                self.gameover = True
            else:
                # Запускаем опускание камеры
                self.camera_descending = True
            if hasattr(self, '_fall_sound_played'):
                del self._fall_sound_played
                
        elif self.block.get_state() == "miss":
            if not hasattr(self, '_miss_sound_played'):
                self._miss_sound_played = True
                self.audio_manager.play_sound('overmusic')
            self.tower.y = 2000
            self.lives -= 1
            if self.lives <= 0:
                self.gameover = True
            else:
                # Запускаем опускание камеры
                self.camera_descending = True
            if hasattr(self, '_miss_sound_played'):
                del self._miss_sound_played
    
    def draw(self):
        selected_bg = self.save_manager.get_selected_background()
        bg_image = self.resource_manager.get_image(f'bg{selected_bg + 1}')
        
        if bg_image:
            bg_width = bg_image.get_width()
            bg_height = bg_image.get_height()
            
            # Верхние 8% фона - облака
            clouds_height = int(bg_height * 0.08)
            
            # Вырезаем облака
            clouds_part = pygame.Surface((bg_width, clouds_height), pygame.SRCALPHA)
            clouds_part.blit(bg_image, (0, 0), (0, 0, bg_width, clouds_height))
            
            # Основной фон (всё кроме облаков)
            main_part_height = bg_height - clouds_height
            main_part = pygame.Surface((bg_width, main_part_height), pygame.SRCALPHA)
            main_part.blit(bg_image, (0, 0), (0, clouds_height, bg_width, main_part_height))
            
            # Позиция основного фона (смещается вниз)
            main_bg_y = self.screenY
            
            # Рисуем основной фон (повторяем снизу если нужно заполнить экран)
            y_pos = main_bg_y
            while y_pos < SCREEN_HEIGHT:
                self.screen.blit(main_part, (0, y_pos))
                y_pos += main_part_height
            
            # Заполняем верх облаками
            if main_bg_y > 0:
                y_pos = main_bg_y - clouds_height
                while y_pos >= -clouds_height:
                    self.screen.blit(clouds_part, (0, y_pos))
                    y_pos -= clouds_height
        else:
            self.screen.fill((135, 206, 235))
        
        if self.tower.get_display() and not self.camera_descending:
            self.tower.display(self.screen)
        if not self.camera_descending:
            self.block.display(self.screen, self.tower)
        
        self.hud.show_score(self.screen, self.score)
        self.hud.show_coins(self.screen, self.save_manager.get_coins())
        self.hud.show_lives(self.screen, self.lives)
        
        if not self.shop_open and not self.settings_open:
            self.shop_button.draw(self.screen)
            self.settings_button.draw(self.screen)
        
        if self.shop_open:
            self.shop_menu.draw(self.screen)
        if self.settings_open:
            self.settings_menu.draw(self.screen)
        
        pygame.display.update()
    
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            if self.gameover and not self.shop_open and not self.settings_open:
                self.save_manager.update_high_score(self.score)
                self.gameover_screen.show(self.screen, self.score)
                self.reset_game()
            
            running = self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()

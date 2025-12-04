"""Меню настроек"""
import pygame
from config import *
from ui.button import Button

class SettingsMenu:
    def __init__(self, save_manager, audio_manager):
        self.save_manager = save_manager
        self.audio_manager = audio_manager
        
        # Шрифты
        self.title_font = pygame.font.Font("freesansbold.ttf", 48)
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.small_font = pygame.font.Font("freesansbold.ttf", 18)
        
        # Кнопка закрытия
        self.close_button = Button(650, 20, 130, 40, "Close", self.font,
                                   color=(200, 100, 100), hover_color=(255, 150, 150))
        
        # Фон меню
        self.background = pygame.Surface((700, 500))
        self.background.fill((40, 40, 60))
        pygame.draw.rect(self.background, (100, 100, 150), (0, 0, 700, 500), 3)
        
        # Позиции меню
        self.menu_x = (SCREEN_WIDTH - 700) // 2
        self.menu_y = (SCREEN_HEIGHT - 500) // 2
        
        # Абсолютные позиции слайдеров
        self.music_slider_x = self.menu_x + 250
        self.music_slider_y = self.menu_y + 150
        self.music_slider_width = 300
        
        self.sound_slider_x = self.menu_x + 250
        self.sound_slider_y = self.menu_y + 220
        self.sound_slider_width = 300
        
        self.dragging_music = False
        self.dragging_sound = False
        
        # Кнопки выбора фона
        self.bg_buttons = []
        bg_y = self.menu_y + 320
        for i in range(BACKGROUND_COUNT):
            btn = Button(self.menu_x + 50 + i * 110, bg_y, 100, 40, 
                        BACKGROUND_NAMES[i], self.small_font,
                        color=(80, 80, 120), hover_color=(120, 120, 180))
            self.bg_buttons.append(btn)
    
    def handle_event(self, event, mouse_pos):
        """Обработка событий"""
        # Обновляем позицию кнопки закрытия
        self.close_button.rect.x = self.menu_x + 550
        self.close_button.rect.y = self.menu_y + 20
        self.close_button.update(mouse_pos)
        
        # Кнопка закрытия
        if self.close_button.is_clicked(event):
            return 'close'
        
        # Слайдер музыки
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка клика на слайдер музыки
            music_rect = pygame.Rect(self.music_slider_x, self.music_slider_y, 
                                    self.music_slider_width, 20)
            if music_rect.collidepoint(mouse_pos):
                self.dragging_music = True
                # Сразу обновляем позицию
                x = mouse_pos[0] - self.music_slider_x
                volume = max(0.0, min(1.0, x / self.music_slider_width))
                self.save_manager.set_music_volume(volume)
                self.audio_manager.set_music_volume(volume)
            
            # Проверка клика на слайдер звуков
            sound_rect = pygame.Rect(self.sound_slider_x, self.sound_slider_y, 
                                    self.sound_slider_width, 20)
            if sound_rect.collidepoint(mouse_pos):
                self.dragging_sound = True
                # Сразу обновляем позицию
                x = mouse_pos[0] - self.sound_slider_x
                volume = max(0.0, min(1.0, x / self.sound_slider_width))
                self.save_manager.set_sound_volume(volume)
                self.audio_manager.set_sound_volume(volume)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_music = False
            self.dragging_sound = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_music:
                # Обновляем громкость музыки
                x = mouse_pos[0] - self.music_slider_x
                volume = max(0.0, min(1.0, x / self.music_slider_width))
                self.save_manager.set_music_volume(volume)
                self.audio_manager.set_music_volume(volume)
            
            if self.dragging_sound:
                # Обновляем громкость звуков
                x = mouse_pos[0] - self.sound_slider_x
                volume = max(0.0, min(1.0, x / self.sound_slider_width))
                self.save_manager.set_sound_volume(volume)
                self.audio_manager.set_sound_volume(volume)
        
        # Кнопки выбора фона
        for i, btn in enumerate(self.bg_buttons):
            btn.update(mouse_pos)
            if btn.is_clicked(event):
                self.save_manager.set_selected_background(i)
                return 'background_changed'
        
        return None
    
    def draw(self, screen):
        """Отрисовка меню настроек"""
        # Затемнение фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Фон меню
        screen.blit(self.background, (self.menu_x, self.menu_y))
        
        # Заголовок
        title = self.title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, (self.menu_x + 220, self.menu_y + 20))
        
        # === МУЗЫКА ===
        music_label = self.font.render("Music Volume:", True, (255, 255, 255))
        screen.blit(music_label, (self.menu_x + 50, self.menu_y + 145))
        
        # Слайдер музыки
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.music_slider_x, self.music_slider_y, 
                         self.music_slider_width, 20))
        
        music_volume = self.save_manager.get_music_volume()
        
        # Заполнение слайдера
        fill_width = int(music_volume * self.music_slider_width)
        if fill_width > 0:
            pygame.draw.rect(screen, (0, 200, 0), 
                           (self.music_slider_x, self.music_slider_y, 
                            fill_width, 20))
        
        # Ручка слайдера
        handle_x = self.music_slider_x + int(music_volume * self.music_slider_width)
        pygame.draw.circle(screen, (255, 255, 0), (handle_x, self.music_slider_y + 10), 12)
        pygame.draw.circle(screen, (200, 200, 0), (handle_x, self.music_slider_y + 10), 10)
        
        # Процент
        percent_text = self.font.render(f"{int(music_volume * 100)}%", True, (255, 255, 255))
        screen.blit(percent_text, (self.music_slider_x + self.music_slider_width + 20, 
                                   self.music_slider_y - 5))
        
        # === ЗВУКИ ===
        sound_label = self.font.render("Sound Volume:", True, (255, 255, 255))
        screen.blit(sound_label, (self.menu_x + 50, self.menu_y + 215))
        
        # Слайдер звуков
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.sound_slider_x, self.sound_slider_y, 
                         self.sound_slider_width, 20))
        
        sound_volume = self.save_manager.get_sound_volume()
        
        # Заполнение слайдера
        fill_width2 = int(sound_volume * self.sound_slider_width)
        if fill_width2 > 0:
            pygame.draw.rect(screen, (0, 200, 200), 
                           (self.sound_slider_x, self.sound_slider_y, 
                            fill_width2, 20))
        
        # Ручка слайдера
        handle_x2 = self.sound_slider_x + int(sound_volume * self.sound_slider_width)
        pygame.draw.circle(screen, (0, 255, 255), (handle_x2, self.sound_slider_y + 10), 12)
        pygame.draw.circle(screen, (0, 200, 200), (handle_x2, self.sound_slider_y + 10), 10)
        
        # Процент
        percent_text2 = self.font.render(f"{int(sound_volume * 100)}%", True, (255, 255, 255))
        screen.blit(percent_text2, (self.sound_slider_x + self.sound_slider_width + 20, 
                                    self.sound_slider_y - 5))
        
        # === ВЫБОР ФОНА ===
        bg_label = self.font.render("Background:", True, (255, 255, 255))
        screen.blit(bg_label, (self.menu_x + 50, self.menu_y + 285))
        
        selected_bg = self.save_manager.get_selected_background()
        
        for i, btn in enumerate(self.bg_buttons):
            # Подсвечиваем выбранный фон
            if i == selected_bg:
                btn.color = (0, 200, 0)
                btn.hover_color = (0, 255, 0)
            else:
                btn.color = (80, 80, 120)
                btn.hover_color = (120, 120, 180)
            
            btn.draw(screen)
        
        # Кнопка закрытия
        self.close_button.draw(screen)

"""Основной игровой класс с магазином"""
import pygame
from config import *
from entities.block import Block
from entities.tower import Tower
from ui.hud import HUD
from ui.gameover_screen import GameOverScreen
from ui.shop_menu import ShopMenu
from ui.button import Button
from managers.resource_manager import ResourceManager
from managers.audio_manager import AudioManager
from managers.save_manager import SaveManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Brocks")
        
        # Менеджеры
        self.save_manager = SaveManager()
        self.resource_manager = ResourceManager()
        self.audio_manager = AudioManager(self.resource_manager)
        
        # Загрузка ресурсов
        self.load_resources()
        
        # UI
        self.hud = HUD(pygame.font.Font("freesansbold.ttf", 32))
        self.gameover_screen = GameOverScreen(
            pygame.font.Font("freesansbold.ttf", 64),
            pygame.font.Font("freesansbold.ttf", 32),
            pygame.font.Font("freesansbold.ttf", 16),
            self.create_fallback_background()
        )
        self.shop_menu = ShopMenu(self.save_manager, self.resource_manager)
        
        # Кнопка магазина
        self.shop_button = Button(650, 10, 130, 40, "Shop", 
                                  pygame.font.Font("freesansbold.ttf", 20),
                                  color=(100, 100, 200), hover_color=(150, 150, 255))
        
        # Состояние игры
        self.shop_open = False
        self.force = INITIAL_FORCE
        self.reset_game()
        
        # FPS
        self.clock = pygame.time.Clock()
    
    def create_fallback_background(self):
        """Создать запасной фон если нет изображения"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((135, 206, 235))  # Голубой цвет
        return bg
        
    def load_resources(self):
        """Загрузка всех ресурсов"""
        # Иконка
        icon = self.resource_manager.load_image('icon', 'ground_tileset.png')
        if icon:
            pygame.display.set_icon(icon)
        
        # Фоны (5 штук)
        for i in range(1, BACKGROUND_COUNT + 1):
            bg = self.resource_manager.load_image(f'bg{i}', f'backgrounds/bg{i}.png')
            if not bg:
                # Создаем запасной фон
                bg = self.create_fallback_background()
                self.resource_manager.images[f'bg{i}'] = bg
        
        # Земля
        self.resource_manager.load_image('ground', 'ground_tileset.png')
        
        # Загрузка всех скинов башен
        print("\n=== Loading tower skins ===")
        for tower_id in TOWER_SKINS.keys():
            self.resource_manager.load_tower_parts(tower_id)
        print("=== Tower skins loaded ===\n")
        
        # Аудио
        self.audio_manager.load_resources()
        self.audio_manager.play_music()
    
    def reset_game(self):
        """Сброс игры"""
        selected_skin = self.save_manager.get_selected_skin()
        
        # Создаём блок (используем первый спрайт)
        block_sprite = self.resource_manager.get_tower_part(selected_skin, 'middle', 0)
        self.block = Block(block_sprite, self.force)
        
        self.tower = Tower(self.resource_manager, selected_skin)
        self.score = 0
        self.screenY = 0
        self.current_bg_index = 0
        self.force = INITIAL_FORCE
        self.gameover = False
    
    def handle_events(self):
        """Обработка событий"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Если магазин открыт
            if self.shop_open:
                result = self.shop_menu.handle_event(event, mouse_pos)
                if result == 'close':
                    self.shop_open = False
                elif result == 'skin_selected' or result == 'skin_purchased':
                    # Обновляем скин башни
                    selected_skin = self.save_manager.get_selected_skin()
                    self.tower.change_skin(selected_skin)
                    # Обновляем спрайт блока
                    block_sprite = self.resource_manager.get_tower_part(selected_skin, 'middle', 0)
                    self.block.image = block_sprite
                    self.block.rotimg = block_sprite
            else:
                # Обычная игра
                self.shop_button.update(mouse_pos)
                if self.shop_button.is_clicked(event):
                    self.shop_open = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.block.get_state() == "ready":
                            self.block.drop(self.tower)
        
        return True
    
    def update(self):
        """Обновление игровой логики"""
        if self.shop_open:
            return  # Не обновляем игру в магазине
        
        # Логика блока
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
            # Играем звуки только один раз
            if not hasattr(self, '_fall_sound_played'):
                self._fall_sound_played = True
                self.audio_manager.play_sound('fall')
                self.audio_manager.play_sound('overmusic')
        
        elif self.block.get_state() == "scroll" and not self.tower.is_scrolling():
            self.force *= FORCE_MULTIPLIER
            self.block.respawn(self.tower, self.force)
            if self.tower.size >= 5:
                self.tower.reset()
            # Сбрасываем флаг звука
            if hasattr(self, '_fall_sound_played'):
                del self._fall_sound_played
        
        # Скроллинг
        if self.tower.height >= BLOCK_HEIGHT * 5 and self.tower.size >= 5:
            self.tower.scroll()
            self.screenY += SCROLL_SPEED
            
            # Смена фона
            if self.screenY % BACKGROUND_SCROLL_HEIGHT == 0:
                self.current_bg_index = (self.current_bg_index + 1) % BACKGROUND_COUNT
        
        # Качание башни
        self.tower.wobble()
        
        # Проверка game over
        self.check_gameover()
    
    def check_gameover(self):
        """Проверка условий конца игры"""
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
            self.gameover = True
            if hasattr(self, '_collapse_sound_played'):
                del self._collapse_sound_played
        elif self.block.get_state() == "over" and self.block.y > 600:
            self.tower.y = 2000
            self.tower.size -= 1
            self.gameover = True
            if hasattr(self, '_fall_sound_played'):
                del self._fall_sound_played
        elif self.block.get_state() == "miss":
            if not hasattr(self, '_miss_sound_played'):
                self._miss_sound_played = True
                self.audio_manager.play_sound('overmusic')
            self.tower.y = 2000
            self.gameover = True
            if hasattr(self, '_miss_sound_played'):
                del self._miss_sound_played
    
    def draw(self):
        """Отрисовка"""
        self.screen.fill(WHITE)
        
        # Фон (с циклической прокруткой 5 фонов)
        bg_images = [self.resource_manager.get_image(f'bg{i+1}') for i in range(BACKGROUND_COUNT)]
        
        for i in range(-1, 4):
            bg_index = (self.current_bg_index + i) % BACKGROUND_COUNT
            bg_y = self.screenY - (i * BACKGROUND_SCROLL_HEIGHT)
            if bg_images[bg_index]:
                self.screen.blit(bg_images[bg_index], (0, bg_y))
        
        # Игровые объекты
        if self.tower.get_display():
            self.tower.display(self.screen)
        self.block.display(self.screen, self.tower)
        
        # HUD
        self.hud.show_score(self.screen, self.score)
        self.hud.show_coins(self.screen, self.save_manager.get_coins())
        
        # Кнопка магазина
        if not self.shop_open:
            self.shop_button.draw(self.screen)
        
        # Магазин
        if self.shop_open:
            self.shop_menu.draw(self.screen)
        
        pygame.display.update()
    
    def run(self):
        """Главный игровой цикл"""
        running = True
        while running:
            self.clock.tick(FPS)
            
            if self.gameover and not self.shop_open:
                self.save_manager.update_high_score(self.score)
                self.gameover_screen.show(self.screen, self.score)
                self.reset_game()
            
            running = self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()

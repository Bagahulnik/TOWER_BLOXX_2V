"""UI магазина"""
import pygame
from config import *
from ui.button import Button

class ShopMenu:
    def __init__(self, save_manager, resource_manager):
        self.save_manager = save_manager
        self.resource_manager = resource_manager
        self.font = pygame.font.Font("freesansbold.ttf", 24)
        self.title_font = pygame.font.Font("freesansbold.ttf", 48)
        self.small_font = pygame.font.Font("freesansbold.ttf", 16)
        
        # Кнопка закрытия
        self.close_button = Button(650, 20, 130, 50, "Close", self.font)
        
        # Кнопки скинов
        self.skin_buttons = {}
        self.create_skin_buttons()
    
    def create_skin_buttons(self):
        """Создание кнопок для каждого скина"""
        x_start = 50
        y_start = 120
        spacing = 10
        button_width = 150
        button_height = 180
        columns = 4
        
        for i, (skin_id, skin_data) in enumerate(TOWER_SKINS.items()):
            row = i // columns
            col = i % columns
            x = x_start + col * (button_width + spacing)
            y = y_start + row * (button_height + spacing)
            
            self.skin_buttons[skin_id] = {
                'rect': pygame.Rect(x, y, button_width, button_height),
                'data': skin_data
            }
    
    def draw(self, screen):
        """Отрисовка магазина"""
        # Полупрозрачный фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (0, 0))
        
        # Заголовок
        title = self.title_font.render("SHOP", True, GOLD)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
        
        # Монеты
        coins_text = self.font.render(f"Coins: {self.save_manager.get_coins()}", True, GOLD)
        screen.blit(coins_text, (50, 30))
        
        # Отрисовка скинов
        selected_skin = self.save_manager.get_selected_skin()
        
        for skin_id, button_data in self.skin_buttons.items():
            rect = button_data['rect']
            data = button_data['data']
            is_unlocked = self.save_manager.is_skin_unlocked(skin_id)
            is_selected = skin_id == selected_skin
            
            # Рамка кнопки
            if is_selected:
                color = GREEN
                thickness = 5
            elif is_unlocked:
                color = WHITE
                thickness = 3
            else:
                color = GRAY
                thickness = 2
            
            pygame.draw.rect(screen, color, rect, thickness, border_radius=10)
            
            # Предпросмотр башни
            if skin_id in self.resource_manager.tower_sprites:
                preview = self.resource_manager.get_tower_part(skin_id, 'middle', 1)
                if preview:
                    preview_scaled = pygame.transform.scale(preview, (60, 60))
                    screen.blit(preview_scaled, (rect.x + 45, rect.y + 10))
            
            # Название
            name_text = self.font.render(data['name'], True, WHITE)
            screen.blit(name_text, (rect.x + rect.width // 2 - name_text.get_width() // 2, rect.y + 80))
            
            # Цена или статус
            if is_unlocked:
                if is_selected:
                    status_text = self.small_font.render("SELECTED", True, GREEN)
                else:
                    status_text = self.small_font.render("Owned", True, WHITE)
            else:
                price_text = f"{data['price']} coins"
                status_text = self.small_font.render(price_text, True, GOLD)
            
            screen.blit(status_text, (rect.x + rect.width // 2 - status_text.get_width() // 2, rect.y + 110))
            
            # Кнопка действия
            button_y = rect.y + 140
            if is_unlocked and not is_selected:
                action_button = Button(rect.x + 20, button_y, 110, 30, "Select", self.small_font, 
                                      color=GREEN, hover_color=(0, 255, 0))
                action_button.draw(screen)
            elif not is_unlocked:
                can_afford = self.save_manager.get_coins() >= data['price']
                color = GREEN if can_afford else GRAY
                action_button = Button(rect.x + 20, button_y, 110, 30, "Buy", self.small_font,
                                      color=color, hover_color=(0, 255, 0) if can_afford else GRAY)
                action_button.draw(screen)
        
        # Кнопка закрытия
        self.close_button.draw(screen)
    
    def handle_event(self, event, mouse_pos):
        """Обработка событий магазина"""
        self.close_button.update(mouse_pos)
        
        if self.close_button.is_clicked(event):
            return 'close'
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for skin_id, button_data in self.skin_buttons.items():
                if button_data['rect'].collidepoint(mouse_pos):
                    return self.handle_skin_click(skin_id)
        
        return None
    
    def handle_skin_click(self, skin_id):
        """Обработка клика на скин"""
        data = TOWER_SKINS[skin_id]
        is_unlocked = self.save_manager.is_skin_unlocked(skin_id)
        
        if is_unlocked:
            # Выбрать скин
            self.save_manager.set_selected_skin(skin_id)
            return 'skin_selected'
        else:
            # Попытка купить
            if self.save_manager.spend_coins(data['price']):
                self.save_manager.unlock_skin(skin_id)
                self.save_manager.set_selected_skin(skin_id)
                return 'skin_purchased'
            else:
                return 'insufficient_funds'

"""Класс кнопки для UI"""
import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, 
                 color=(100, 100, 100), hover_color=(150, 150, 150),
                 text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, screen):
        """Отрисовка кнопки"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        """Обновление состояния кнопки"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, event):
        """Проверка клика по кнопке"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False

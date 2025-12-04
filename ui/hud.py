"""Интерфейс HUD с монетами и жизнями"""
import pygame
from config import GOLD, RED

class HUD:
    def __init__(self, font):
        self.font = font
        self.small_font = pygame.font.Font("freesansbold.ttf", 20)
        
    def show_score(self, screen, score, x=10, y=10):
        score_text = self.font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (x, y))
    
    def show_coins(self, screen, coins, x=10, y=50):
        coins_text = self.small_font.render(f"Coins: {coins}", True, GOLD)
        screen.blit(coins_text, (x, y))
    
    def show_lives(self, screen, lives, x=10, y=75):
        """Отображение жизней"""
        lives_text = self.small_font.render(f"Lives: {lives}", True, RED)
        screen.blit(lives_text, (x, y))
        
        # Рисуем сердечки
        heart_x = x + 70
        for i in range(lives):
            # Простое сердечко из кругов
            pygame.draw.circle(screen, RED, (heart_x + i*25, y + 5), 8)
            pygame.draw.circle(screen, RED, (heart_x + i*25 + 10, y + 5), 8)
            pygame.draw.polygon(screen, RED, [
                (heart_x + i*25 - 8, y + 5),
                (heart_x + i*25 + 18, y + 5),
                (heart_x + i*25 + 5, y + 18)
            ])

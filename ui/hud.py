"""Интерфейс HUD с монетами"""
import pygame
from config import GOLD

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

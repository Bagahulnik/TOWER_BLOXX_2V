"""Экран Game Over"""
import pygame

class GameOverScreen:
    def __init__(self, over_font, score_font, mini_font, background):
        self.over_font = over_font
        self.score_font = score_font
        self.mini_font = mini_font
        self.background = background
        self.blink_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.blink_event, 800)
        
    def show(self, screen, score):
        over_text = self.over_font.render("GAME OVER", True, (0, 0, 0))
        high_score = self.score_font.render(f"SCORE: {score}", True, (0, 0, 0))
        button = self.mini_font.render("PRESS ANY BUTTON TO RESTART", True, (0, 0, 0))
        
        blank_rect = button.get_rect()
        blank = pygame.Surface((blank_rect.size), pygame.SRCALPHA)
        blank.convert_alpha()
        
        instructions = [button, blank]
        index = 1
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
                if event.type == self.blink_event:
                    index = 1 - index
            
            screen.blit(self.background, (0, 0))
            screen.blit(over_text, (200, 150))
            screen.blit(high_score, (320, 250))
            screen.blit(instructions[index], (270, 450))
            pygame.display.update()

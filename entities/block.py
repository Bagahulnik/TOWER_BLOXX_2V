"""Класс блока"""
import pygame
from math import sin, cos
from config import GRAVITY, ROPE_LENGTH, ORIGIN

class Block(pygame.sprite.Sprite):
    def __init__(self, image, force):
        pygame.sprite.Sprite.__init__(self)
        self.image = image if image else self.create_default_block()
        self.rotimg = self.image
        self.x = 37
        self.y = 150
        self.xlast = 0
        self.xchange = 100
        self.speed = 0
        self.acceleration = 0
        self.speedmultiplier = 1
        self.rect = self.image.get_rect()
        self.state = "ready"
        self.angle = 45
        self.force = force

    def create_default_block(self):
        """Создать блок по умолчанию если нет текстуры"""
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        surf.fill((150, 150, 200, 255))
        pygame.draw.rect(surf, (255, 255, 255), (2, 2, 60, 60), 2)
        return surf

    def get_state(self):
        """Получить текущее состояние блока"""
        return self.state

    def swing(self):
        """Качание блока на веревке"""
        self.x = 370 + ROPE_LENGTH * sin(self.angle)
        self.y = 20 + ROPE_LENGTH * cos(self.angle)
        self.angle += self.speed
        self.acceleration = sin(self.angle) * self.force
        self.speed += self.acceleration

    def drop(self, tower):
        """Падение блока"""
        if self.state == "ready":
            self.state = "dropped"
            self.xlast = self.x

        if self.collided(tower):
            self.state = "landed"

        if tower.size == 0 and self.y >= 536:
            self.state = "landed"

        if tower.size >= 1 and self.y >= 536:
            self.state = "miss"

        if self.state == "dropped":
            self.speed += GRAVITY
            self.y += self.speed

    def collided(self, tower):
        """Проверка столкновения с башней"""
        if tower.size == 0:
            return False
        if (self.xlast < tower.xlist[-1] + 60) and (self.xlast > tower.xlist[-1] - 60) and (tower.y - self.y <= 70):
            if (self.xlast < tower.xlist[-1] + 5) and (self.xlast > tower.xlist[-1] - 5):
                tower.golden = True
            else:
                tower.golden = False
            return True
        return False

    def to_build(self, tower):
        """Проверка возможности постройки"""
        self.state = "scroll"
        if tower.size == 0 or self.collided(tower):
            return True
        return False

    def collapse(self, tower):
        """Обрушение блока"""
        if tower.size >= 2:
            if (self.xlast > tower.xlist[-2] + 40) or (self.xlast < tower.xlist[-2] - 40):
                if self.collided(tower):
                    self.state = "over"

    def rotate(self, direction):
        """Вращение блока"""
        if direction == "l":
            self.angle += 1
        if direction == "r":
            self.angle -= 1
        self.rotimg = pygame.transform.rotate(self.image, self.angle)

    def to_fall(self, tower):
        """Падение блока при обрушении"""
        self.y += 5

        if tower.size >= 2:
            if (self.xlast < tower.xlist[-2] + 30):
                self.x -= 2
                self.rotate("l")
            elif (self.xlast > tower.xlist[-2] - 30):
                self.x += 2
                self.rotate("r")

    def display(self, screen, tower):
        """Отображение блока"""
        if not tower.is_scrolling():
            pygame.draw.circle(screen, (200, 0, 0), ORIGIN, 5, 0)
            screen.blit(self.rotimg, (self.x, self.y))
            if self.state == "ready":
                self.draw_rope(screen)

    def draw_rope(self, screen):
        """Отрисовка веревки"""
        pygame.draw.aaline(screen, (0, 0, 0), ORIGIN, (self.x+32, self.y))
        pygame.draw.aaline(screen, (0, 0, 0), (401, 3), (self.x + 33, self.y))
        pygame.draw.aaline(screen, (0, 0, 0), (402, 3), (self.x + 34, self.y))
        pygame.draw.aaline(screen, (0, 0, 0), (399, 3), (self.x + 31, self.y))
        pygame.draw.aaline(screen, (0, 0, 0), (398, 3), (self.x + 30, self.y))
        pygame.draw.circle(screen, (200, 0, 0), (int(self.x+32), int(self.y+2.5)), 5, 0)

    def respawn(self, tower, force):
        """Возрождение блока"""
        if tower.size % 2 == 0:
            self.angle = -45
        else:
            self.angle = 45
        self.y = 150
        self.x = 370
        self.speed = 0
        self.state = "ready"
        self.force = force

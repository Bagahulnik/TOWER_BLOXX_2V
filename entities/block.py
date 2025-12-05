"""Класс блока (маятник + очередь спрайтов, падение при смещении >50%)"""
import pygame
from math import sin, cos
from config import (
    GRAVITY,
    ROPE_LENGTH,
    ORIGIN,
    BLOCK_HEIGHT,
    BLOCK_WIDTH,
)


class Block(pygame.sprite.Sprite):
    def __init__(self, image, force):
        pygame.sprite.Sprite.__init__(self)
        self.image = image if image is not None else self.create_default_block()
        self.rotimg = self.image
        self.x = 370
        self.y = 150
        self.xlast = 0           # центр блока при сбросе
        self.xchange = 100
        self.speed = 0
        self.acceleration = 0
        self.speedmultiplier = 1
        self.rect = self.image.get_rect()
        self.state = "ready"     # ready, dropped, landed, scroll, over, miss
        self.angle = 45
        self.force = force

    def create_default_block(self):
        surf = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
        surf.fill((150, 150, 200, 255))
        pygame.draw.rect(
            surf,
            (255, 255, 255),
            (2, 2, BLOCK_WIDTH - 4, BLOCK_HEIGHT - 4),
            2,
        )
        return surf

    def get_state(self):
        return self.state

    def swing(self):
        """Маятник (как в старом рабочем проекте)"""
        self.x = 370 + ROPE_LENGTH * sin(self.angle) - BLOCK_WIDTH // 2
        self.y = 20 + ROPE_LENGTH * cos(self.angle)
        self.angle += self.speed
        self.acceleration = sin(self.angle) * self.force
        self.speed += self.acceleration

    def drop(self, tower):
        """Падение блока"""
        if self.state == "ready":
            self.state = "dropped"
            # сохраняем ЦЕНТР блока, а не левый край
            self.xlast = self.x + BLOCK_WIDTH // 2

        if self.collided(tower):
            self.state = "landed"

        if tower.size == 0 and self.y >= 600 - BLOCK_HEIGHT:
            self.state = "landed"

        if tower.size >= 1 and self.y >= 600 - BLOCK_HEIGHT:
            self.state = "miss"

        if self.state == "dropped":
            self.speed += GRAVITY
            self.y += self.speed

    def collided(self, tower):
        """Столкновение с верхним этажом башни"""
        if tower.size == 0:
            return False

        top_x = tower.xlist[-1] + BLOCK_WIDTH // 2  # центр верхнего блока

        # допуск по X ~ ширина блока, по Y — высота + небольшой запас
        if (
            self.xlast < top_x + BLOCK_WIDTH - 4
            and self.xlast > top_x - (BLOCK_WIDTH - 4)
            and (tower.y - self.y) <= BLOCK_HEIGHT + 6
        ):
            # «золотой» попадание почти идеально по центру
            if self.xlast < top_x + 5 and self.xlast > top_x - 5:
                tower.golden = True
            else:
                tower.golden = False
            return True
        return False

    def to_build(self, tower):
        """После удачного приземления блок уходит в режим scroll"""
        self.state = "scroll"
        if tower.size == 0 or self.collided(tower):
            return True
        return False

    def collapse(self, tower):
        """
        Если блок ушёл по X больше чем на 50% ширины относительно ВЕРХНЕГО этажа,
        считаем, что он не удержался и падает.
        """
        if tower.size >= 1:
            top_center = tower.xlist[-1] + BLOCK_WIDTH // 2
            max_offset = BLOCK_WIDTH // 2  # 50% ширины: 48px при 96px блока

            if self.xlast > top_center + max_offset or self.xlast < top_center - max_offset:
                self.state = "over"

    def rotate(self, direction):
        if direction == "l":
            self.angle += 1
        if direction == "r":
            self.angle -= 1
        self.rotimg = pygame.transform.rotate(self.image, self.angle)

    def to_fall(self, tower):
        """Анимация падения после collapse/over"""
        self.y += 5

        if tower.size >= 1:
            top_center = tower.xlist[-1] + BLOCK_WIDTH // 2
            offset = BLOCK_WIDTH // 3  # небольшой «замах» при падении

            if self.xlast < top_center + offset:
                self.x -= 2
                self.rotate("l")
            elif self.xlast > top_center - offset:
                self.x += 2
                self.rotate("r")

    def display(self, screen, tower):
        if not tower.is_scrolling():
            pygame.draw.circle(screen, (200, 0, 0), ORIGIN, 5, 0)
            screen.blit(self.rotimg, (self.x, self.y))
            if self.state == "ready":
                self.draw_rope(screen)

    def draw_rope(self, screen):
        hook_x = self.x + BLOCK_WIDTH // 2
        hook_y = self.y
        pygame.draw.aaline(screen, (0, 0, 0), ORIGIN, (hook_x, hook_y))
        pygame.draw.circle(
            screen,
            (200, 0, 0),
            (int(hook_x), int(hook_y + 2.5)),
            5,
            0,
        )

    def respawn(self, tower, force):
        """Возврат блока на верёвку"""
        if tower.size % 2 == 0:
            self.angle = -45
        else:
            self.angle = 45
        self.speed = 0
        self.state = "ready"
        self.force = force
        self.rotimg = self.image

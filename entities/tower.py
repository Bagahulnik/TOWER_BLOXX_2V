"""Башня: первый этаж bot, остальные — тот же спрайт, что висел на верёвке"""
import pygame
from config import BLOCK_HEIGHT, BLOCK_WIDTH


class Tower(pygame.sprite.Sprite):
    def __init__(self, resource_manager, skin_id="tower_1"):
        pygame.sprite.Sprite.__init__(self)
        self.resource_manager = resource_manager
        self.skin_id = skin_id
        self.size = 0
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.xbase = 0
        self.y = 600
        self.x = 0
        self.height = 0
        self.xlist = []
        self.onscreen = 0
        self.change = 0
        self.speed = 0.4
        self.wobbling = False
        self.scrolling = False
        self.golden = False
        self.redraw = False
        self.display_status = True

        self.floors = []  # [{'x': ..., 'sprite': ...}]

        self.load_parts()

    def load_parts(self):
        self.parts = self.resource_manager.load_tower_parts(self.skin_id)

    def change_skin(self, skin_id):
        self.skin_id = skin_id
        self.load_parts()

    def build(self, block_x, block_sprite):
        """Строим этаж, используя спрайт упавшего блока"""
        self.size += 1
        self.onscreen += 1

        if self.size == 1:
            self.xbase = block_x
            sprite = self.parts.get("base", block_sprite)
        else:
            sprite = block_sprite

        self.xlist.append(block_x)
        self.floors.append({"x": block_x, "sprite": sprite})

        if self.size <= 5:
            self.height = self.size * BLOCK_HEIGHT
            self.y = 600 - self.height
        else:
            self.height += BLOCK_HEIGHT
            self.y -= BLOCK_HEIGHT

    def draw(self):
        if self.size >= 1:
            max_height = self.onscreen * BLOCK_HEIGHT
            surf = pygame.Surface((800, max_height), pygame.SRCALPHA)
            surf.convert_alpha()

            floors_to_draw = (
                self.floors[-self.onscreen :] if self.redraw else self.floors
            )

            for i, floor in enumerate(floors_to_draw):
                floor_sprite = floor["sprite"]
                if floor_sprite:
                    y_pos = max_height - BLOCK_HEIGHT * (i + 1)
                    surf.blit(floor_sprite, (floor["x"], y_pos))
        else:
            surf = pygame.Surface((0, 0))

        self.rect = surf.get_rect()
        return surf

    def get_display(self):
        return self.display_status

    def is_scrolling(self):
        return self.scrolling

    def is_golden(self):
        return self.golden

    def get_width(self):
        width = BLOCK_WIDTH
        if self.size == 0 or self.size == -1:
            return width
        if self.xlist[-1] > self.xbase:
            width = (self.xlist[-1] - self.xbase) + BLOCK_WIDTH
        if self.xlist[-1] < self.xbase:
            width = -((self.xbase - self.xlist[-1]) + BLOCK_WIDTH)
        return width

    def wobble(self):
        width = self.get_width()
        if ((width > 100 or width < -100) and self.size >= 5) or self.size >= 20:
            self.wobbling = True

        if self.wobbling:
            self.change += self.speed

        if self.change > 20:
            self.speed = -0.4
        elif self.change < -20:
            self.speed = 0.4

    def display(self, screen):
        surf = self.draw()
        screen.blit(surf, (self.x + self.change, self.y))

    def scroll(self):
        if self.y <= 440:
            self.y += 5
            self.scrolling = True
        else:
            self.height = 160
            self.scrolling = False
            self.onscreen = 3

    def reset(self):
        self.redraw = True
        if self.onscreen >= 7:
            self.onscreen = 3
            self.y = 440

    def unbuild(self, block):
        self.display_status = False
        if self.y > block.y:
            block.y = self.y
            self.size -= 1

    def collapse(self, direction):
        self.y += 5
        if direction == "l":
            self.x -= 5
        elif direction == "r":
            self.x += 5

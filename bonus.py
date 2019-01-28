import random

import pygame
from pygame.rect import Rect

from bonus_type import BonusType
from settings import MAX_FPS
from text_surface import TextSurface


class Bonus(pygame.Surface):
    """
    Falling bonus
    Returns: Bonus object
    Functions: update
    """

    text_surface = TextSurface()

    def __init__(self, block_rect):
        width = height = 30
        super().__init__((width, height))
        self.rect = Rect(0, 0, width, height)
        self.rect.center = block_rect.center
        self.speed = 100 / MAX_FPS
        self.active = True
        self.fill(pygame.Color('orange'))
        self.bonus_type = random.choice(list(BonusType))
        self.blit(Bonus.text_surface.get_text_surface('?'), (8, 0))

    def get_rect(self):
        return self.rect

    def update(self):
        if self.active:
            self.rect.move_ip(0, self.speed)

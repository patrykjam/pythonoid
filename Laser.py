import pygame

from load_utils import load_png
from settings import BALL_IMG
from surface_utils import SurfaceUtils


class Laser(pygame.sprite.Sprite):
    SHOW_TIME = 15

    def __init__(self, surface_height):
        super().__init__()
        self.image, self.rect = load_png(BALL_IMG)
        self.image = SurfaceUtils.color_surface(self.image, pygame.Color('Turquoise'))
        self._resize_height(surface_height)
        self.show = 0

    def _resize_height(self, height):
        self.image = pygame.transform.scale(self.image, (20, height))

    def update(self):
        if self.show:
            self.show -= 1

    def activate(self):
        self.show = Laser.SHOW_TIME

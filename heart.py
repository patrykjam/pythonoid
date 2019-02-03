import pygame

from load_utils import load_png
from settings import HEART_IMG
from surface_utils import SurfaceUtils


class Heart(pygame.sprite.Sprite):
    SIZE = 30

    def __init__(self):
        super().__init__()
        self.image, _ = load_png(HEART_IMG)
        self.image = pygame.transform.scale(self.image, (Heart.SIZE, Heart.SIZE))
        self.image = SurfaceUtils.color_surface(self.image, pygame.Color('Red'))
        self.rect = self.image.get_rect()

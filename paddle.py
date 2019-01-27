import numpy as np
import pygame

from load_utils import load_png
from settings import PADDLE_IMG, MAX_FPS


class Paddle(pygame.sprite.Sprite):
    """
    Movable paddle
    Returns: Paddle object
    Functions: reinit, update, move_left, move_right
    """

    MAX_RESIZE_TIMES = 2

    def __init__(self, area):
        super().__init__()
        self.image = self.rect = None
        self.area = area
        self.speed = 300 / MAX_FPS
        self.movepos = [0, 0]
        self.bounce_angle_range = (3.4, 6.)
        self.bounce_angle_array = None
        self.resize_state = 0
        self.reinit()

    def reinit(self):
        self.image, self.rect = load_png(PADDLE_IMG)
        self.movepos = [0, 0]
        self.rect.midbottom = self.area.midbottom
        self.resize_state = 0
        self.bounce_angle_array = np.linspace(*self.bounce_angle_range, self.rect.width)

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def move_left(self):
        self.movepos[0] = self.movepos[0] - self.speed

    def move_right(self):
        self.movepos[0] = self.movepos[0] + self.speed

    def stop(self):
        self.movepos = [0, 0]

    def get_bounce_angle(self, ball_x):
        idx = ball_x - self.rect.left
        if idx < 0:
            idx = 0
        if idx > self.rect.width:
            idx = self.rect.width - 1
        return self.bounce_angle_array[idx]

    def shrink(self):
        if self.resize_state != -self.MAX_RESIZE_TIMES:
            self._resize_width_by(0.8)
            self.resize_state -= 1

    def expand(self):
        if self.resize_state != self.MAX_RESIZE_TIMES:
            self._resize_width_by(1.2)
            self.resize_state += 1

    def _resize_width_by(self, by):
        self.image = pygame.transform.scale(self.image, (round(self.image.get_width() * by), self.image.get_height()))
        old_pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = old_pos
        self.bounce_angle_array = np.linspace(*self.bounce_angle_range, self.rect.width)
        if not self.area.contains(self.rect):
            self.rect.midbottom = self.area.midbottom

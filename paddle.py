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

    def __init__(self, area):
        super().__init__()
        self.image, self.rect = load_png(PADDLE_IMG)
        self.area = area
        self.speed = 600/MAX_FPS
        self.movepos = [0, 0]
        self.state = "still"
        self.bounce_angle_range = (3.4, 6.)
        self.bounce_angle_array = np.linspace(*self.bounce_angle_range, self.rect.width)
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0, 0]
        self.rect.midbottom = self.area.midbottom

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def move_left(self):
        self.movepos[0] = self.movepos[0] - self.speed
        self.state = "moveleft"

    def move_right(self):
        self.movepos[0] = self.movepos[0] + self.speed
        self.state = "moveright"

    def stop(self):
        self.movepos = [0, 0]
        self.state = "still"

    def get_bounce_angle(self, ball_x):
        idx = ball_x - self.rect.left
        if idx < 0:
            idx = 0
        if idx > self.rect.width:
            idx = self.rect.width - 1
        return self.bounce_angle_array[idx]

import math
import random

import pygame

from load_utils import load_png
from settings import BALL_IMG


class Ball(pygame.sprite.Sprite):
    """
    Moving ball
    Returns: Ball object
    Functions: reinit, update
    """

    def __init__(self, area, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(BALL_IMG)
        self.area = area
        if vector:
            self.vector = vector
        else:
            self.vector = random.uniform(0.25, 2 * math.pi - 0.25), 10
        self.collided = False

    def update(self, paddle_rect):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            angle *= -1
            if tr and br:
                angle -= math.pi
            elif tl and bl:
                angle += math.pi
        else:
            # Deflate the rectangles so you can't catch a ball behind the paddle
            paddle_rect.inflate(-3, -3)

            if self.rect.colliderect(paddle_rect) and not self.collided:
                angle *= -1
                self.collided = True
            elif self.collided:
                self.collided = False
        self.vector = (angle, z)

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)

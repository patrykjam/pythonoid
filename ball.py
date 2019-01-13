import math
import random
import soundmixer as soundmixer
import pygame
from settings import *

from load_utils import load_png
from settings import BALL_IMG


class Ball(pygame.sprite.Sprite):
    """
    Moving ball
    Returns: Ball object
    Functions: reinit, update
    """

    def __init__(self, area, vector):
        super().__init__()
        self.image, self.rect = load_png(BALL_IMG)
        self.area = area
        if vector:
            self.vector = vector
        else:
            self.vector = random.uniform(0.25, 2 * math.pi - 0.25), 10
        self.collided = self.hit = self.tl = self.tr = self.bl = self.br = False

    def update(self):
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
            soundmixer.solochanneleffect(PADDLE_HIT)
        else:
            if self.hit and not self.collided:
                angle *= -1
                if self.tr and self.br:
                    angle -= math.pi
                elif self.tl and self.bl:
                    angle += math.pi
                self.collided = True
            elif not self.hit and self.collided:
                self.collided = False
        self.vector = (angle, z)

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)

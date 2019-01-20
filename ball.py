import math
import random

import pygame

import soundmixer as soundmixer
from load_utils import load_png
from settings import BALL_IMG, BALL_LOSS, PADDLE_HIT, MAX_FPS


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
        self.active = True
        if vector:
            self.vector = vector
        else:
            self.vector = random.uniform(0.25, math.pi - 0.25), 1200/MAX_FPS
        self.custom_angle = self.collided = self.hit = self.tl = self.tr = self.bl = self.br = False

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if self.custom_angle:
            self.vector = (self.custom_angle, z)
            self.custom_angle = None
            return

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)

            if br and bl:
                self.active = False
                soundmixer.solochanneleffect(BALL_LOSS)
                return
            angle *= -1
            if tr and br:
                angle -= math.pi
            elif tl and bl:
                angle += math.pi
            soundmixer.solochanneleffect(PADDLE_HIT)
        else:
            if self.hit and not self.collided:
                angle *= -1
                soundmixer.solochanneleffect(PADDLE_HIT)
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

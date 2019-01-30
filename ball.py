import math
import random

import pygame

import soundmixer as soundmixer
from load_utils import load_png
from settings import BALL_IMG, BALL_LOSS, PADDLE_HIT, MAX_FPS, BASE_SPEED


class Ball(pygame.sprite.Sprite):
    """
    Moving ball
    Returns: Ball object
    Functions: reinit, update
    """

    MAX_RESIZE_TIMES = 1
    MAX_SPEED_CHANGE = 2
    SUPER_BALL_TIME = 160

    def __init__(self, area, vector):
        super().__init__()
        self.resize_state = self.speed_state = self.super_ball_time = 0
        self.image = self.rect = None
        self.area = area
        self.active = True
        if vector:
            self.vector = vector
        else:
            self.vector = random.uniform(1, math.pi - 1), BASE_SPEED / MAX_FPS
        self.custom_angle = self.collided = self.hit = self.tl = self.tr = self.bl = self.br = False
        self.reinit()

    def reinit(self):
        self.image, self.rect = load_png(BALL_IMG)
        self.rect.center = self.area.center
        self.resize_state = self.speed_state = 0

    def update(self):
        if self.super_ball_time:
            self.super_ball_time -= 1
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
        (dx, dy) = (round(z * math.cos(angle), 0), round(z * math.sin(angle), 0))
        return rect.move(dx, dy)

    def shrink(self):
        if self.resize_state != -self.MAX_RESIZE_TIMES:
            self._resize_by(0.8)
            self.resize_state -= 1

    def expand(self):
        if self.resize_state != self.MAX_RESIZE_TIMES:
            self._resize_by(1.2)
            self.resize_state += 1

    def _resize_by(self, by):
        self.image = pygame.transform.scale(self.image, (round(self.image.get_width() * by),
                                                         (round(self.image.get_height() * by))))
        old_pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = old_pos
        if not self.area.contains(self.rect):
            self.rect.center = self.area.center

    def slow_down(self):
        if self.speed_state != -self.MAX_SPEED_CHANGE:
            v, speed = self.vector
            speed *= 0.7
            self.vector = v, speed
            self.speed_state -= 1

    def speed_up(self):
        if self.speed_state != self.MAX_SPEED_CHANGE:
            v, speed = self.vector
            speed *= 1.3
            self.vector = v, speed
            self.speed_state += 1

    def is_super_ball(self):
        return self.super_ball_time

    def super_ball(self):
        self.super_ball_time = Ball.SUPER_BALL_TIME

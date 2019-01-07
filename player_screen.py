import math
import random

from ball import Ball
from paddle import Paddle
from text_surface import TextSurface


class PlayerScreen(object):
    """
    Object representing one player screen.
    Contains screen's subsurface, controls, score, paddle and ball(s).
    """
    text_surface = TextSurface()

    def __init__(self, subsurface, controls):
        self.subsurface = subsurface
        self.move_left_key, self.move_right_key = controls
        self.score = 0
        self.paddle = Paddle(subsurface.get_rect())
        self.balls = (Ball(subsurface.get_rect(), (random.uniform(0.25, 2 * math.pi - 0.25), 10)),)

    def update(self):
        for b in self.balls:
            b.update(self.paddle.rect)
        self.paddle.update()

    def blit(self):
        for b in self.balls:
            self.subsurface.blit(b.image, b.rect)
        self.subsurface.blit(self.paddle.image, self.paddle.rect)
        self.subsurface.blit(PlayerScreen.text_surface.get_text_surface('Score: {}'.format(self.score)), (0, 0))

import math
import random

from ball import Ball
from paddle import Paddle
from settings import WIDTH_RES, HEIGHT_RES
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
        self.balls = [Ball(subsurface.get_rect(), None)]
        self.balls[0].rect.move_ip([random.uniform(0, 0.5 * WIDTH_RES), random.uniform(0, 0.5 * HEIGHT_RES)])

    def update(self):
        for b in self.balls:
            b.update(self.paddle.rect)
        self.paddle.update()

    def blit(self):
        for b in self.balls:
            self.subsurface.blit(b.image, b.rect)
        self.subsurface.blit(self.paddle.image, self.paddle.rect)
        self.subsurface.blit(PlayerScreen.text_surface.get_text_surface('Score: {}'.format(self.score)), (0, 0))

    def multiply_balls(self):
        upd_balls = []
        for ball in self.balls:
            upd_balls.append(ball)
            temp_balls = [ball, Ball(self.subsurface.get_rect(), [ball.vector[0] + 0.25 * math.pi, ball.vector[1]]),
                          Ball(self.subsurface.get_rect(), [ball.vector[0] - 0.25 * math.pi, ball.vector[1]])]
            temp_balls[1].rect = ball.rect.copy()
            temp_balls[2].rect = ball.rect.copy()
            upd_balls.extend(temp_balls)
        self.balls = upd_balls

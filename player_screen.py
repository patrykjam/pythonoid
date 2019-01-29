import math

import soundmixer as soundmixer
from ball import Ball
from block import Block
from bonus import Bonus
from bonus_type import BonusType
from paddle import Paddle
from random_utils import RandomUtils
from settings import PADDLE_HIT, WIN, LIFE_LOSS, BONUS_CHANCE
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
        self.blocks = [
            Block(20, 50, 100, 30),
            Block(130, 50, 100, 30),
            Block(240, 50, 100, 30),
            Block(350, 50, 100, 30),
            Block(460, 50, 100, 30),
            Block(20, 130, 100, 30),
            Block(130, 130, 100, 30),
            Block(240, 130, 100, 30),
            Block(350, 130, 100, 30),
            Block(460, 130, 100, 30)
        ]
        self.bonuses = []

    def update(self):
        for ball in self.balls:
            if self._check_collision_corners(ball, self.paddle):
                ball.custom_angle = self.paddle.get_bounce_angle(ball.rect.centerx)
                ball.update()
                continue
            ball.hit = self._check_collision_corners(ball, *self.blocks)
            if ball.hit:
                for block in self.blocks:
                    if ball.rect.colliderect(block.rect) and not ball.collided:
                        self.score += 10
                        block.life -= 1
                        soundmixer.solochanneleffect(PADDLE_HIT)
                    block.update()
            self.check_blocks()
            self.check_bonuses()
            if not self.blocks:
                soundmixer.queueeffect(WIN)
            ball.update()
        self.paddle.update()
        self.balls = [ball for ball in self.balls if ball.active]
        if not self.balls:
            soundmixer.queueeffect(LIFE_LOSS)
        for b in self.bonuses:
            b.update()

    def blit(self):
        for b in self.balls:
            self.subsurface.blit(b.image, b.rect)
        for b in self.blocks:
            self.subsurface.blit(b, b.rect)
        for b in self.bonuses:
            self.subsurface.blit(b, b.rect)
        self.subsurface.blit(self.paddle.image, self.paddle.rect)
        self.subsurface.blit(PlayerScreen.text_surface.get_text_surface('Score: {}'.format(self.score)), (0, 0))

    def multiply_balls(self):
        upd_balls = []
        for ball in self.balls:
            temp_balls = [ball, Ball(self.subsurface.get_rect(), [ball.vector[0] + 0.25 * math.pi, ball.vector[1]]),
                          Ball(self.subsurface.get_rect(), [ball.vector[0] - 0.25 * math.pi, ball.vector[1]])]
            temp_balls[1].rect = ball.rect.copy()
            temp_balls[2].rect = ball.rect.copy()
            upd_balls.extend(temp_balls)
        self.balls = upd_balls

    def _check_collision_corners(self, ball, *areas):
        for a in areas:
            if ball.rect.colliderect(a.rect):
                ball.tl = a.rect.collidepoint(ball.rect.topleft)
                ball.tl = a.rect.collidepoint(ball.rect.topright)
                ball.tl = a.rect.collidepoint(ball.rect.bottomleft)
                ball.tl = a.rect.collidepoint(ball.rect.bottomright)
                return True
        return None

    def check_blocks(self):
        dead_blocks = [bl for bl in self.blocks if bl.life <= 0]
        if dead_blocks:
            self.bonuses.extend([Bonus(b.get_rect()) for b in dead_blocks if RandomUtils.decision(BONUS_CHANCE)])
        self.blocks = [bl for bl in self.blocks if bl.life > 0]

    def check_bonuses(self):
        for b in self.bonuses:
            if not self.subsurface.get_rect().contains(b.get_rect()):
                b.active = False
            elif self.paddle.rect.colliderect(b.get_rect()):
                self.apply_bonus(b.bonus_type)
                b.active = False
        self.bonuses = [b for b in self.bonuses if b.active]

    def apply_bonus(self, bonus_type):
        if bonus_type == BonusType.BALL_SHRINK:
            for b in self.balls:
                b.shrink()
        elif bonus_type == BonusType.BALL_EXPAND:
            for b in self.balls:
                b.expand()
        elif bonus_type == BonusType.PADDLE_SHRINK:
            self.paddle.shrink()
        elif bonus_type == BonusType.PADDLE_EXPAND:
            self.paddle.expand()
        elif bonus_type == BonusType.BALL_SPEED_UP:
            for b in self.balls:
                b.speed_up()
        elif bonus_type == BonusType.BALL_SLOW_DOWN:
            for b in self.balls:
                b.slow_down()
        elif bonus_type == BonusType.PADDLE_SPEED_UP:
            self.paddle.speed_up()
        elif bonus_type == BonusType.PADDLE_SLOW_DOWN:
            self.paddle.slow_down()
        elif bonus_type == BonusType.BALL_MULTIPLY:
            self.multiply_balls()
        elif bonus_type == BonusType.PADDLE_LASER:
            pass
        elif bonus_type == BonusType.BALL_SUPER:
            pass

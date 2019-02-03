import math

import soundmixer as soundmixer
from Laser import Laser
from ball import Ball
from bonus import Bonus
from bonus_type import BonusType
from heart import Heart
from map_loader import Map_Loader
from paddle import Paddle
from random_utils import RandomUtils
from settings import PADDLE_HIT, WIN, LIFE_LOSS, BONUS_CHANCE, MAP_TIME, MAX_FPS, START_LIVES, LASER_EFFECT
from text_surface import TextSurface


class PlayerScreen(object):
    """
    Object representing one player screen.
    Contains screen's subsurface, controls, score, paddle and ball(s).
    """
    text_surface = TextSurface()

    def __init__(self, subsurface, controls):
        self.subsurface = subsurface
        self.map_loader = Map_Loader()
        self.map_loader.next_map()
        self.active = True
        self.up_key, self.left_key, self.down_key, self.right_key = controls
        self.score = 0
        self.paddle = Paddle(subsurface.get_rect())
        self.balls = [Ball(subsurface.get_rect())]
        self.time_left = 0
        self.load_map(self.map_loader.get_blocks())
        self.bonuses = []
        self.blocks = []
        self.laser = Laser(self.subsurface.get_rect().height - 20)
        self.life = START_LIVES
        self.heart = Heart()

    def load_map(self, blocks):
        self.balls = [Ball(self.subsurface.get_rect())]
        self.blocks = blocks
        self.bonuses = []
        self.time_left = MAP_TIME * MAX_FPS
        self.paddle = Paddle(self.subsurface.get_rect())

    def update(self):
        self.time_left -= 1
        for ball in self.balls:
            if self._check_collision_corners(ball, self.paddle):
                ball.custom_angle = self.paddle.get_bounce_angle(ball.rect.centerx)
                ball.update()
                continue
            ball.hit = self._check_collision_corners(ball, *self.blocks)
            if ball.hit:
                for block in self.blocks:
                    if ball.rect.colliderect(block.rect) and not ball.collided:
                        if ball.is_super_ball():
                            self.score += 10 * block.life
                            block.life = 0
                            ball.hit = False
                        else:
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
            self.life -= 1
            if self.life:
                self.balls = [Ball(self.subsurface.get_rect())]
        for b in self.bonuses:
            b.update()
        self.laser.update()

        if not self.blocks:
            if self.map_loader.next_map():
                self.load_map(self.map_loader.get_blocks())
            else:
                self.active = False
        if not self.balls or not self.time_left:
            self.active = False

    def blit(self):
        for b in self.balls:
            self.subsurface.blit(b.image, b.rect)
        for b in self.blocks:
            self.subsurface.blit(b, b.rect)
        for b in self.bonuses:
            self.subsurface.blit(b, b.rect)
        self.subsurface.blit(self.paddle.image, self.paddle.rect)
        if self.laser.show:
            self.subsurface.blit(self.laser.image, (self.paddle.rect.centerx - 10, 0))
        self.subsurface.blit(PlayerScreen.text_surface.get_text_surface('Score: {}'.format(self.score)), (0, 0))
        self.subsurface.blit(
            PlayerScreen.text_surface.get_text_surface('Time left: {}'.format(round(self.time_left / MAX_FPS, 1))),
            (200, 0))
        self.subsurface.blit(self.heart.image, (self.subsurface.get_rect().width - 100, 5))
        self.subsurface.blit(PlayerScreen.text_surface.get_text_surface('x{}'.format(self.life)),
                             (self.subsurface.get_rect().width - 60, 10))

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
                ball.tr = a.rect.collidepoint(ball.rect.topright)
                ball.bl = a.rect.collidepoint(ball.rect.bottomleft)
                ball.br = a.rect.collidepoint(ball.rect.bottomright)
                return True
        return None

    def shoot_laser(self):
        if self.paddle.laser:
            soundmixer.solochanneleffect(LASER_EFFECT)
            self.laser.activate()
            self.paddle.laser -= 1
            for b in self.blocks:
                if b.get_rect().left < self.paddle.rect.centerx < b.get_rect().right:
                    b.life -= 1
                    self.score += 10
                    b.update()
            self.check_blocks()

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
        soundmixer.solochanneleffect(bonus_type.value)
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
            self.paddle.init_laser()
        elif bonus_type == BonusType.BALL_SUPER:
            for b in self.balls:
                b.super_ball()
        elif bonus_type == BonusType.EXTRA_LIFE:
            self.life += 1

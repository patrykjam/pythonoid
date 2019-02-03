from enum import Enum

import settings


class BonusType(Enum):
    BALL_SHRINK = settings.BALL_SHRINK
    BALL_EXPAND = settings.BALL_EXPAND
    PADDLE_SHRINK = settings.PADDLE_SHRINK
    PADDLE_EXPAND = settings.PADDLE_EXPAND
    BALL_SPEED_UP = settings.BALL_SPEED_UP
    BALL_SLOW_DOWN = settings.BALL_SLOW_DOWN
    PADDLE_SPEED_UP = settings.PADDLE_SPEED_UP
    PADDLE_SLOW_DOWN = settings.PADDLE_SLOW_DOWN
    BALL_MULTIPLY = settings.BALL_MULTIPLY
    PADDLE_LASER = settings.PADDLE_LASER
    BALL_SUPER = settings.BALL_SUPER
    EXTRA_LIFE = settings.EXTRA_LIFE

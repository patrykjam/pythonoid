from enum import Enum, auto


class BonusType(Enum):
    BALL_SHRINK = auto()
    BALL_EXPAND = auto()
    PADDLE_SHRINK = auto()
    PADDLE_EXPAND = auto()
    BALL_SPEED_UP = auto()
    BALL_SLOW_DOWN = auto()
    PADDLE_SPEED_UP = auto()
    PADDLE_SLOW_DOWN = auto()
    PADDLE_LASER = auto()
    BALL_SUPER = auto()

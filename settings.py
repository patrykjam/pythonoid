"""
Settings constants
"""
from pygame.constants import K_a, K_d, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_s, K_w

BASE_SPEED = 600
MAP_TIME = 180
PLAYERS = 1
MAX_FPS = 60
HEIGHT_RES = 700
WIDTH_RES = 600
INFO_BAR_HEIGHT = 30
FULLSCREEN = False
BONUS_CHANCE = 0.4
START_LIVES = 3
IMAGES_DIR = "images/"
SOUNDS_DIR = 'sounds/'
FONTS_DIR = 'fonts/'
MAPS_DIR = 'maps/'
MAP_PATH = MAPS_DIR + "mapy.json"
FONT_AZONIX = FONTS_DIR + "Azonix.otf"
PADDLE_IMG = IMAGES_DIR + "paddle.png"
BALL_IMG = IMAGES_DIR + "ball.png"
HEART_IMG = IMAGES_DIR + "heart.png"
BACKGROUND_COLOR = 'white'
BLOCK_COLORS = ('green', 'yellow', 'red', 'grey', 'black')
SOUNDTRACK = SOUNDS_DIR + "Soundtrack.wav"
PADDLE_HIT = SOUNDS_DIR + "paddle_hit.wav"
BALL_LOSS = SOUNDS_DIR + "ball_loss.wav"
LIFE_LOSS = SOUNDS_DIR + "life_loss.wav"
LASER_EFFECT = SOUNDS_DIR + "laser.wav"
BALL_SHRINK = SOUNDS_DIR + "ball_shrink.wav"
BALL_EXPAND = SOUNDS_DIR + "ball_expand.wav"
PADDLE_SHRINK = SOUNDS_DIR + "paddle_shrink.wav"
PADDLE_EXPAND = SOUNDS_DIR + "paddle_expand.wav"
BALL_SPEED_UP = SOUNDS_DIR + "ball_speed_up.wav"
BALL_SLOW_DOWN = SOUNDS_DIR + "ball_slow_down.wav"
PADDLE_SPEED_UP = SOUNDS_DIR + "paddle_speed_up.wav"
PADDLE_SLOW_DOWN = SOUNDS_DIR + "paddle_slow_down.wav"
BALL_MULTIPLY = SOUNDS_DIR + "ball_multiply.wav"
PADDLE_LASER = SOUNDS_DIR + "paddle_laser.wav"
BALL_SUPER = SOUNDS_DIR + "ball_super.wav"
EXTRA_LIFE = SOUNDS_DIR + "extra_life.wav"

WIN = SOUNDS_DIR + "win.wav"

PLAYER_CONTROLS = ((K_w, K_a, K_s, K_d), (K_UP, K_LEFT, K_DOWN, K_RIGHT))

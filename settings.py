"""
Settings constants
"""
from pygame.constants import K_a, K_d, K_LEFT, K_RIGHT

PLAYERS = 1
MAX_FPS = 60
HEIGHT_RES = 700
WIDTH_RES = 600
IMAGES_DIR = "images/"
SOUNDS_DIR = 'sounds/'
PADDLE_IMG = IMAGES_DIR + "paddle.png"
BALL_IMG = IMAGES_DIR + "ball.png"
BACKGROUND_COLOR = 'white'
BLOCK_COLORS = ('green', 'yellow', 'red', 'grey', 'black')
SOUNDTRACK = SOUNDS_DIR + "Soundtrack.wav"
PADDLE_HIT = SOUNDS_DIR + "paddle_hit.wav"

PLAYER_CONTROLS = ((K_a, K_d), (K_LEFT, K_RIGHT))

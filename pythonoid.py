import math
import random

import pygame
from pygame.locals import *

from ball import Ball
from paddle import Paddle
from settings import *

pygame.init()
screen = pygame.display.set_mode((HEIGHT_RES, WIDTH_RES))
pygame.display.set_caption('Pythonoid')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

paddle = Paddle()
screen.blit(background, (0, 0))
ball = Ball((random.uniform(0, 2 * math.pi), 10))

pygame.display.flip()

clock = pygame.time.Clock()

# Event loop
while 1:
    clock.tick(MAX_FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                paddle.move_left()
            if event.key == K_RIGHT or event.key == K_d:
                paddle.move_right()
                # set
        elif event.type == KEYUP and (
                event.key == K_LEFT or event.key == K_RIGHT or event.key == K_a or event.key == K_d):
            paddle.movepos = [0, 0]
            paddle.state = "still"
    paddle.update()
    ball.update(paddle.rect)

    screen.blit(background, (0, 0))
    screen.blit(paddle.image, paddle.rect)
    screen.blit(ball.image, ball.rect)
    pygame.display.flip()
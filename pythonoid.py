import pygame
from pygame.locals import *

import settings
import soundmixer as soundmixer
from player_screen import PlayerScreen
from settings import WIDTH_RES, HEIGHT_RES, MAX_FPS, PLAYER_CONTROLS, BACKGROUND_COLOR
from text_surface import TextSurface


def start_screen():
    width, height = (WIDTH_RES * 2, HEIGHT_RES)
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN if settings.FULLSCREEN else 0)
    surface = pygame.Surface((width, height))
    surface.fill(pygame.Color(BACKGROUND_COLOR))
    clock = pygame.time.Clock()
    text_surface_title = TextSurface(size=189)
    text_surface_text = TextSurface()
    intro = True

    while intro:
        surface.blit(text_surface_title.get_text_surface('PYTHONOID'), (0, 0))
        surface.blit(text_surface_text.get_text_surface('Controls:'), (0, height / 4))
        surface.blit(text_surface_text.get_text_surface('Player 1: W / D'), (0, height / 4 + 50))
        surface.blit(text_surface_text.get_text_surface('Player 2: Left / Right arrow'), (0, height / 4 + 100))
        surface.blit(text_surface_text.get_text_surface('Press \'1\' or \'2\' to choose number of players and play'),
                     (0, height / 4 + 400))
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                if event.key == K_1:
                    settings.PLAYERS = 1
                    intro = False
                elif event.key == K_2:
                    settings.PLAYERS = 2
                    intro = False


def pythonoid():
    PLAYERS = settings.PLAYERS
    clock = pygame.time.Clock()
    text_surface = TextSurface()
    soundmixer.init_mixer()
    width, height = WIDTH_RES * PLAYERS, HEIGHT_RES
    screen_res = (width, height)
    screen = pygame.display.set_mode(screen_res, pygame.FULLSCREEN if settings.FULLSCREEN else 0)

    canvas = pygame.Surface(screen_res)
    player_screens = \
        [PlayerScreen(canvas.subsurface(pygame.Rect(i * width / PLAYERS, 0, width / PLAYERS, height)), controls)
         for i, controls in zip(range(PLAYERS), PLAYER_CONTROLS)]

    time = 0
    soundmixer.setmusic()

    # Event loop
    while 1:
        clock.tick(MAX_FPS)
        time = time + 1
        canvas.blit(text_surface.get_text_surface('Time: {}'.format(round(time / MAX_FPS, 1), )), (200, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                for p in player_screens:
                    if event.key == p.up_key:
                        p.shoot_laser()
                    if event.key == p.left_key:
                        p.paddle.move_left()
                    if event.key == p.right_key:
                        p.paddle.move_right()

            elif event.type == KEYUP:
                for p in player_screens:
                    if event.key in (p.left_key, p.right_key):
                        p.paddle.stop()

        for i, p in enumerate(player_screens):
            screen.blit(p.subsurface, (i * width / PLAYERS, 0))
            p.subsurface.fill(pygame.Color(BACKGROUND_COLOR))
            if p.blocks and p.balls:
                p.update()
            p.blit()
            pygame.draw.line(p.subsurface, (0, 0, 0), (width / PLAYERS, 0), (width / PLAYERS, height), 5)

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pythonoid')
    start_screen()
    pythonoid()

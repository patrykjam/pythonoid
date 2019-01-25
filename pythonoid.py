import pygame
from pygame.locals import *

import soundmixer as soundmixer
from player_screen import PlayerScreen
from settings import WIDTH_RES, HEIGHT_RES, PLAYERS, MAX_FPS, PLAYER_CONTROLS, BACKGROUND_COLOR
from text_surface import TextSurface

def main():
    soundmixer.init_mixer()
    pygame.init()
    width, height = WIDTH_RES * PLAYERS, HEIGHT_RES
    screen_res = (width, height)
    screen = pygame.display.set_mode(screen_res)
    pygame.display.set_caption('Pythonoid')

    canvas = pygame.Surface(screen_res)
    textsurface = TextSurface()
    player_screens = \
        [PlayerScreen(canvas.subsurface(pygame.Rect(i * width / PLAYERS, 0, width / PLAYERS, height)), controls)
         for i, controls in zip(range(PLAYERS), PLAYER_CONTROLS)]

    clock = pygame.time.Clock()
    time = 0
    soundmixer.setmusic()

    # Event loop
    while 1:
        clock.tick(MAX_FPS)
        time = time + 1
        canvas.blit(textsurface.get_text_surface('Time: {}'.format(round(time/MAX_FPS, 1),)), (200, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    for p in player_screens:
                        p.multiply_balls()

                for p in player_screens:
                    if event.key == p.move_left_key:
                        p.paddle.move_left()
                    if event.key == p.move_right_key:
                        p.paddle.move_right()

            elif event.type == KEYUP:
                for p in player_screens:
                    if event.key in (p.move_left_key, p.move_right_key):
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
    main()


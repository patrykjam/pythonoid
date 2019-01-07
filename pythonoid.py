import pygame
from pygame.locals import *

from player_screen import PlayerScreen
from settings import WIDTH_RES, HEIGHT_RES, PLAYERS, MAX_FPS, PLAYER_CONTROLS


def main():
    pygame.init()
    width, height = WIDTH_RES * PLAYERS, HEIGHT_RES
    screen_res = (width, height)
    screen = pygame.display.set_mode(screen_res)
    pygame.display.set_caption('Pythonoid')

    canvas = pygame.Surface(screen_res)
    player_screens = \
        [PlayerScreen(canvas.subsurface(pygame.Rect(i * width / PLAYERS, 0, width / PLAYERS, height)), controls)
         for i, controls in zip(range(PLAYERS), PLAYER_CONTROLS)]

    background = pygame.Surface(player_screens[0].subsurface.get_size())
    background = background.convert(canvas)
    background.fill((255, 255, 255))

    clock = pygame.time.Clock()

    # Event loop
    while 1:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
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
            screen.blit(p.subsurface, (i * width / 2, 0))
            p.subsurface.blit(background, (0, 0))
            p.update()
            p.blit()

        if PLAYERS != 1:
            pygame.draw.line(player_screens[0].subsurface, (0, 0, 0), (width / 2, 0), (width / 2, height), 5)
        pygame.display.flip()


if __name__ == '__main__':
    main()

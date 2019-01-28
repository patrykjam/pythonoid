import pygame

from settings import FONT_AZONIX


class TextSurface(object):

    def __init__(self, font=FONT_AZONIX, size=30):
        pygame.font.init()
        self.font = pygame.font.Font(font, size)

    def get_text_surface(self, text):
        return self.font.render(text, True, (0, 0, 0))

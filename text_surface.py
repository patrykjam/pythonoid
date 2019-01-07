import pygame


class TextSurface(object):

    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Times New Roman', 30)

    def get_text_surface(self, text):
        return self.font.render(text, True, (0, 0, 0))

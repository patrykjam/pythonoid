import pygame


class SurfaceUtils(object):

    @staticmethod
    def color_surface(surface, color):
        """Returns colored surface without modifying transparency"""
        sur_copy = surface.copy()
        arr = pygame.surfarray.pixels3d(sur_copy)
        arr[:, :, 0] = color.r
        arr[:, :, 1] = color.g
        arr[:, :, 2] = color.b
        return sur_copy

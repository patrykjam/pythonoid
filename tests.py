import unittest

import pygame

from load_utils import load_png
from player_screen import PlayerScreen


class TestPythonoid(unittest.TestCase):

    def test_load_png_failure(self):
        self.assertRaises(SystemExit, load_png, 'nonexistent_image.ping')

    def test_initial_player_screen_balls(self):
        pygame.display.set_mode((0, 0))
        player_screen = PlayerScreen(pygame.Surface((0, 0)), (None, None))

        self.assertEqual(1, len(player_screen.balls))

    def test_player_screen_multiply_balls(self):
        pygame.display.set_mode((0, 0))
        player_screen = PlayerScreen(pygame.Surface((0, 0)), (None, None))
        expected_balls = 1
        expected_multiplication = 3

        for i in range(10):
            expected_balls *= expected_multiplication
            player_screen.multiply_balls()
            self.assertEqual(expected_balls, len(player_screen.balls))

import unittest

import pygame

import soundmixer
from ball import Ball
from block import Block
from load_utils import load_png
from player_screen import PlayerScreen
from settings import BLOCK_COLORS


class TestPythonoid(unittest.TestCase):

    def test_load_png_failure(self):
        self.assertRaises(SystemExit, load_png, 'nonexistent_image.ping')

    def test_initial_player_screen_balls(self):
        soundmixer.init_mixer()
        pygame.display.set_mode((0, 0))
        player_screen = PlayerScreen(pygame.Surface((100, 100)), (None, None, None, None), [])

        self.assertEqual(1, len(player_screen.balls))

    def test_player_screen_multiply_balls(self):
        soundmixer.init_mixer()
        pygame.display.set_mode((0, 0))
        player_screen = PlayerScreen(pygame.Surface((100, 100)), (None, None, None, None), [])
        expected_balls = 1
        expected_multiplication = 3
        tested_multiplication_count = 8

        for i in range(tested_multiplication_count):
            expected_balls *= expected_multiplication
            player_screen.multiply_balls()
            self.assertEqual(expected_balls, len(player_screen.balls))

    def test_player_screen_multiply_balls_random_initial(self):
        soundmixer.init_mixer()
        pygame.display.set_mode((0, 0))
        player_screen = PlayerScreen(pygame.Surface((100, 100)), (None, None, None, None), [])
        tested_initial_number_of_balls_count = 6

        for i in range(1, tested_initial_number_of_balls_count + 1):
            start_balls = i
            player_screen.balls = [Ball(pygame.Rect(0, 0, 0, 0), None) for _ in range(start_balls)]
            expected_balls = start_balls
            expected_multiplication = 3
            tested_multiplication_count = 6

            for i in range(tested_multiplication_count):
                expected_balls *= expected_multiplication
                player_screen.multiply_balls()
                self.assertEqual(expected_balls, len(player_screen.balls))

    def test_block_color_out_of_color_range(self):
        block = Block(0, 0, 0, 0, 0)
        max_colors = len(BLOCK_COLORS)

        expected = ((-1, BLOCK_COLORS[-1]),
                    (0, BLOCK_COLORS[-1]),
                    (max_colors, BLOCK_COLORS[-1]),
                    (max_colors + 1, BLOCK_COLORS[-1]))

        for life, expected_color in expected:
            block.life = life
            self.assertEqual(expected_color, block._get_color())

    def test_block_color_in_color_range(self):
        block = Block(0, 0, 0, 1, 1)

        for life, expected_color in enumerate(BLOCK_COLORS, start=1):
            block.life = life
            self.assertEqual(expected_color, block._get_color())

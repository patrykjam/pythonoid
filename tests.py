import unittest

from load_utils import load_png


class TestLoadMethods(unittest.TestCase):

    def test_load_png_failure(self):
        self.assertRaises(SystemExit, load_png, 'nonexistent_image.ping')

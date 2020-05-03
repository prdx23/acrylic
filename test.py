import unittest
from random import uniform, randint

from colorgen.colorgen import Color


class TestColor(unittest.TestCase):

    def test_basic(self):
        new_color = Color()
        self.assertEqual(new_color.hsl, (0, 0, 0))

    def test_validation(self):
        with self.assertRaises(TypeError):
            _ = Color(hsl='test')
            _ = Color(hsl=1)
            _ = Color(hsl=('test', 1, 0.5))
            _ = Color(hsl=(1, 'test', 0.5))
            _ = Color(hsl=(1, 0.5, 'test'))
            _ = Color(hsl=(0, 0.5))

        with self.assertRaises(ValueError):
            _ = Color(hsl=(0.5, 1, 5))
            _ = Color(hsl=(1, 5, 0.5))
            _ = Color(hsl=(5, 0.5, 1))
            _ = Color(hsl=(0, (1, 5), 5))
            _ = Color(hsl=(0, (5, 1), 5))

    def test_hsl(self):
        new_color = Color(hsl=(0, 1, 0.5))
        self.assertEqual(new_color.hsl, (0, 1, 0.5))

        for _ in range(20):
            new_color = Color(hsl=(-1, 0.4, 0.6))
            values = new_color.hsl
            self.assertEqual(values[1], 0.4)
            self.assertEqual(values[2], 0.6)
            self.assertTrue(isinstance(values[0], float))
            self.assertTrue(0 <= values[0] <= 1)

        for _ in range(20):
            a = round(uniform(0, 0.5), 3)
            b = round(uniform(0.5, 1), 3)
            new_color = Color(hsl=((a, b), 0.4, 0.6))
            values = new_color.hsl
            self.assertEqual(values[1], 0.4)
            self.assertEqual(values[2], 0.6)
            self.assertTrue(isinstance(values[0], float))
            self.assertTrue(a <= values[0] <= b)

    def test_rgb(self):
        new_color = Color(rgb=(24, 0, 255))
        self.assertEqual(new_color.rgb, (24, 0, 255))

        for _ in range(20):
            new_color = Color(rgb=(-1, 42, 62))
            values = new_color.rgb
            self.assertEqual(values[1], 42)
            self.assertEqual(values[2], 62)
            self.assertTrue(isinstance(values[0], int))
            self.assertTrue(0 <= values[0] <= 255)

        for _ in range(20):
            a, b = randint(0, 42), randint(42, 255)
            new_color = Color(rgb=((a, b), 42, 62))
            values = new_color.rgb
            self.assertEqual(values[1], 42)
            self.assertEqual(values[2], 62)
            self.assertTrue(isinstance(values[0], int))
            self.assertTrue(a <= values[0] <= b)

    def test_conversion(self):
        new_color = Color(hsl=(0.5, 0.9, 0.6))
        self.assertEqual(new_color.hsl, (0.5, 0.9, 0.6))
        self.assertEqual(new_color.rgb, (61, 245, 245))
        self.assertEqual(new_color.hsv, (0.5, 0.75, 0.96))

        new_color = Color(rgb=(61, 245, 245))
        self.assertEqual(new_color.hsl, (0.5, 0.9, 0.6))
        self.assertEqual(new_color.rgb, (61, 245, 245))
        self.assertEqual(new_color.hsv, (0.5, 0.75, 0.96))

        new_color = Color(hsv=(0.5, 0.75, 0.96))
        self.assertEqual(new_color.hsl, (0.5, 0.9, 0.6))
        self.assertEqual(new_color.rgb, (61, 245, 245))
        self.assertEqual(new_color.hsv, (0.5, 0.75, 0.96))

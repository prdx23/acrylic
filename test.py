import unittest
from random import uniform

from colorgen.colorgen import Color


class TestColor(unittest.TestCase):

    def test_basic(self):
        new_color = Color()
        self.assertEqual(new_color.hsl, (0, 0, 0))

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
            a = round(uniform(0, 0.2), 3)
            b = round(uniform(0.8, 1), 3)
            new_color = Color(hsl=((a, b), 0.4, 0.6))
            values = new_color.hsl
            self.assertEqual(values[1], 0.4)
            self.assertEqual(values[2], 0.6)
            self.assertTrue(isinstance(values[0], float))
            self.assertTrue(a <= values[0] <= b)

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

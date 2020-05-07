import unittest
from random import randint

from colorgen.colorgen import Color


class TestColor(unittest.TestCase):

    def test_basic(self):
        new_color = Color()
        self.assertEqual(new_color.hsl, (0, 0, 0))
        new_color.hsl = (180, 90, 60)
        self.assertEqual(new_color.hsl.h, 180)
        self.assertEqual(new_color.hsl.s, 90)
        self.assertEqual(new_color.hsl.l, 60)

    def test_validation(self):
        with self.assertRaises(TypeError):
            _ = Color(hsl=(5, 0.5, 1))
            _ = Color(hsl='test')
            _ = Color(hsl=1)
            _ = Color(hsl=('test', 1, 0.5))
            _ = Color(hsl=(1, 'test', 0.5))
            _ = Color(hsl=(1, 0.5, 'test'))
            _ = Color(hsl=(0, 0.5))

        with self.assertRaises(ValueError):
            _ = Color(hsl=(0, 1, 101))
            _ = Color(hsl=(1, 101, 0))
            _ = Color(hsl=(361, 0, 1))
            _ = Color(hsl=(0, (1, 101), 5))
            _ = Color(hsl=(0, (101, 1), 5))
            _ = Color(hsl=((1, 361), 1, 5))
            _ = Color(hsl=((361, 1), 1, 5))

        with self.assertRaises(TypeError):
            _ = Color(hex=1)
            _ = Color(hex=(5, 0.5, 1))

        with self.assertRaises(ValueError):
            _ = Color(hex='test')
            _ = Color(hex='#0000')
            _ = Color(hex='#0000xx')

    def test_hsl(self):
        new_color = Color(hsl=(180, 40, 60))
        self.assertEqual(new_color.hsl, (180, 40, 60))
        self.assertEqual(new_color.hsl.h, 180)
        self.assertEqual(new_color.hsl.s, 40)
        self.assertEqual(new_color.hsl.l, 60)

        for _ in range(20):
            new_color = Color(hsl=(-1, -1, 60))
            values = new_color.hsl
            self.assertEqual(values.l, 60)
            self.assertTrue(0 <= values.h <= 360)
            self.assertTrue(0 <= values.s <= 100)

        for _ in range(20):
            a, b = randint(0, 180), randint(180, 360)
            c, d = randint(0, 40), randint(60, 100)
            new_color = Color(hsl=((a, b), (c, d), 60))
            values = new_color.hsl
            self.assertEqual(values.l, 60)
            self.assertTrue(a <= values.h <= b)
            self.assertTrue(c <= values.s <= d)

    def test_rgb(self):
        new_color = Color(rgb=(24, 0, 255))
        self.assertEqual(new_color.rgb, (24, 0, 255))

        for _ in range(20):
            new_color = Color(rgb=(-1, 42, 62))
            values = new_color.rgb
            self.assertEqual(values[1], 42)
            self.assertEqual(values[2], 62)
            self.assertTrue(0 <= values[0] <= 255)

        for _ in range(20):
            a, b = randint(0, 42), randint(42, 255)
            new_color = Color(rgb=((a, b), 42, 62))
            values = new_color.rgb
            self.assertEqual(values[1], 42)
            self.assertEqual(values[2], 62)
            self.assertTrue(a <= values[0] <= b)

    def test_hex(self):
        tests = [
            '#3DF5F5', '3DF5F5', '#3df5f5', '3df5f5', '#3DF5F5FF',
            '3DF5F5FF', '#3df5f5ff', '3df5f5ff'
        ]
        for test in tests:
            new_color = Color(hex=test)
            self.assertEqual(new_color.hex, '#3DF5F5')

    def test_conversion(self):
        def test_all(color):
            self.assertEqual(color.hsl, (180, 90, 60))
            self.assertEqual(color.rgb, (61, 245, 245))
            self.assertEqual(color.hsv, (180, 75, 96))
            self.assertEqual(color.hex, '#3DF5F5')

        test_all(Color(hsl=(180, 90, 60)))
        test_all(Color(rgb=(61, 245, 245)))
        test_all(Color(hsv=(180, 75, 96)))
        test_all(Color(hex='#3DF5F5'))

import unittest
from random import randint

from colorgen.colorgen import Color, RANDOM


class TestColor(unittest.TestCase):

    def test_basic(self):
        color = Color()
        self.assertEqual(color.rgb, (0, 0, 0))

        color = Color(rgb=(83, 237, 229))
        self.assertEqual(color.rgb, (83, 237, 229))

    def test_str_repr(self):
        self.assertEqual(str(Color(rgb=(61, 245, 245))), 'r=61, g=245, b=245')
        self.assertEqual(str(Color(hex='#3DF5F5')), "hex='#3DF5F5'")

        new_color = Color(rgb=(61, 245, 245))
        self.assertEqual(eval(repr(new_color)), new_color)
        new_color = Color(hsl=(180, 90, 60))
        self.assertEqual(eval(repr(new_color)), new_color)
        new_color = Color(hex='#3DF5F5')
        self.assertEqual(eval(repr(new_color)), new_color)

    def test_eq(self):
        new_color = Color(rgb=(61, 245, 245))
        self.assertEqual(new_color, Color(hsl=(180, 90, 60)))
        self.assertEqual(new_color, Color(rgb=(61, 245, 245)))
        self.assertEqual(new_color, Color(hex='#3DF5F5'))
        self.assertNotEqual(new_color, Color(rgb=(62, 245, 245)))

    def test_hash(self):
        new_color = Color(rgb=(61, 245, 245))
        self.assertEqual(hash(new_color), hash(Color(hsl=(180, 90, 60))))
        self.assertEqual(hash(new_color), hash(Color(rgb=(61, 245, 245))))
        self.assertEqual(hash(new_color), hash(Color(hex='#3DF5F5')))
        self.assertNotEqual(hash(new_color), hash(Color(rgb=(62, 245, 245))))

        test_dict = {new_color: 'test!'}
        self.assertEqual(test_dict[Color(hsl=(180, 90, 60))], 'test!')
        self.assertEqual(test_dict[Color(hsl=(180, 90.1, 60))], 'test!')
        self.assertEqual(test_dict[Color(hsl=(180, 89.8, 60))], 'test!')

        test_set = set([
            Color(rgb=(61, 245, 245)), Color(hsl=(180, 90, 60)),
            Color(hsl=(180, 89.8, 60)), Color(hex='#3DF5F5')
        ])
        self.assertEqual(len(test_set), 1)

    def test_validation_inplist(self):
        with self.assertRaises(TypeError):
            _ = Color(rgb=1)
            _ = Color(rgb='123')
            _ = Color(rgb='test!')
            _ = Color(rgb=(0, 0.5))
            _ = Color(rgb=(1, 2, 3, 4))

    def test_validation_type(self):
        with self.assertRaises(TypeError):
            _ = Color(rgb=(25.123, 50, 200))
            _ = Color(rgb=('test!', 50, 200))
            _ = Color(rgb=((25.123, 24), 50, 200))
            _ = Color(rgb=((24, 25.123), 50, 200))
            _ = Color(rgb=(('test!', 24), 50, 200))
            _ = Color(rgb=((24, 'test!'), 50, 200))

    def test_validation_value(self):
        lower, upper = Color.LIMITS['rgb'].r
        with self.assertRaises(ValueError):
            _ = Color(rgb=(lower - 10, 50, 200))
            _ = Color(rgb=(upper + 10, 50, 200))
            _ = Color(rgb=((lower - 10, 24), 50, 200))
            _ = Color(rgb=((24, lower - 10), 50, 200))
            _ = Color(rgb=((upper + 10, 24), 50, 200))
            _ = Color(rgb=((23, upper + 10), 50, 200))
            _ = Color(rgb=((24, 42, 64), 50, 200))
            _ = Color(rgb=((24,), 50, 200))

    def test_single_values(self):
        limits = Color.LIMITS['rgb']
        for _ in range(50):
            values = [randint(limits[i][0], limits[i][1]) for i in range(3)]
            color = Color(rgb=values)
            self.assertEqual(color.rgb, tuple(values))
            [self.assertIsInstance(x, int) for x in color.rgb]

    def test_random(self):
        limits = Color.LIMITS['rgb']
        for _ in range(50):
            color = Color(rgb=RANDOM)
            check = lambda i, x: limits[i][0] <= x <= limits[i][1]
            self.assertTrue(all(check(i, x) for i, x in enumerate(color.rgb)))
            [self.assertIsInstance(x, int) for x in color.rgb]

    def test_range_values(self):
        for _ in range(50):
            lower, upper = Color.LIMITS['rgb'].r
            a, b = randint(lower, upper // 2), randint(upper // 2, upper)
            color = Color(rgb=([a, b], 42, 64))
            self.assertTrue(a <= color.rgb.r <= b)
            color = Color(rgb=([b, a], 42, 64))
            self.assertTrue(a <= color.rgb.r <= b)
            color = Color(rgb=([RANDOM, a], 42, 64))
            self.assertTrue(color.rgb.r <= a)
            color = Color(rgb=([b, RANDOM], 42, 64))
            self.assertTrue(b <= color.rgb.r)
            color = Color(rgb=([RANDOM, RANDOM], 42, 64))
            self.assertTrue(lower <= color.rgb.r <= upper)

    def test_validation_hex(self):
        with self.assertRaises(TypeError):
            _ = Color(hex=1)
            _ = Color(hex=(5, 0.5, 1))

        with self.assertRaises(ValueError):
            _ = Color(hex='test')
            _ = Color(hex='#0000')
            _ = Color(hex='#0000xx')

    def test_hex(self):
        tests = [
            '#3DF5F5', '3DF5F5', '#3df5f5', '3df5f5', '#3DF5F5FF',
            '3DF5F5FF', '#3df5f5ff', '3df5f5ff'
        ]
        for test in tests:
            self.assertEqual(Color(hex=test).hex, '#3DF5F5')

    def test_conversion(self):
        def test_all(color):
            self.assertEqual(color.hsl, (176.88, 81.05, 62.75))
            self.assertEqual(color.rgb, (83, 237, 229))
            self.assertEqual(color.hsv, (176.88, 64.98, 92.94))
            self.assertEqual(color.hex, '#53EDE5')
            self.assertEqual(color.ryb, (18, 97, 172))

        test_all(Color(hsl=(176.88, 81.05, 62.75)))
        test_all(Color(rgb=(83, 237, 229)))
        test_all(Color(hsv=(176.88, 64.98, 92.94)))
        test_all(Color(hex='#53EDE5'))
        test_all(Color(ryb=(18, 97, 172)))

    def test_immutability(self):
        with self.assertRaises(AttributeError):
            color = Color(rgb=(83, 237, 229))
            color.hsl = (176.88, 81.05, 62.75)
            color.rgb = (83, 237, 229)
            color.hsv = (176.88, 64.98, 92.94)
            color.hex = '#53EDE5'
            color.ryb = (18, 97, 172)

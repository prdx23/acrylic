from pytest import approx

from acrylic.Defaults import SCHEMAS
from acrylic.Converters import rgb_to, rgb_from


class Test_converters():

    rgbs = [(62, 244, 255), (255, 0, 0), (25, 24, 25), (127, 255, 212)]
    hsls = [(183, 100, 62), (0, 100, 50), (300, 2, 10), (160, 100, 75)]
    hsvs = [(183, 76, 100), (0, 100, 100), (300, 4, 10), (160, 50, 100)]
    hexes = ['#3EF4FF', '#FF0000', '#191819', '#7FFFD4']
    names = ['-', 'red', '-', 'aquamarine']
    rybs = [(0, 94, 193), (255, 0, 0), (231, 230, 230), (0, 77, 128)]

    def test_rgb_to_hsl(self):
        for rgb, hsl in zip(self.rgbs, self.hsls):
            result = rgb_to['hsl'](rgb)
            assert result == approx(hsl, abs=0.5)
            assert isinstance(result, SCHEMAS['hsl'].output_type)

    def test_rgb_to_hsv(self):
        for rgb, hsv in zip(self.rgbs, self.hsvs):
            result = rgb_to['hsv'](rgb)
            assert result == approx(hsv, abs=0.5)
            assert isinstance(result, SCHEMAS['hsv'].output_type)

    def test_rgb_to_hex(self):
        for rgb, hex_code in zip(self.rgbs, self.hexes):
            assert rgb_to['hex'](rgb) == hex_code

    def test_rgb_to_name(self):
        for rgb, name in zip(self.rgbs, self.names):
            assert rgb_to['name'](rgb) == name

    def test_rgb_to_ryb(self):
        for rgb, ryb in zip(self.rgbs, self.rybs):
            result = rgb_to['ryb'](rgb)
            assert result == approx(ryb, abs=1)
            assert isinstance(result, SCHEMAS['ryb'].output_type)

    # - - - - - - - - - -

    def test_hsl_to_rgb(self):
        for rgb, hsl in zip(self.rgbs, self.hsls):
            result = rgb_from['hsl'](hsl)
            assert result == approx(rgb, abs=1)
            assert isinstance(result, SCHEMAS['rgb'].output_type)

    def test_hsv_to_rgb(self):
        for rgb, hsv in zip(self.rgbs, self.hsvs):
            result = rgb_from['hsv'](hsv)
            assert result == approx(rgb, abs=1)
            assert isinstance(result, SCHEMAS['rgb'].output_type)

    def test_hex_to_rgb(self):
        for rgb, hex_code in zip(self.rgbs, self.hexes):
            assert rgb_from['hex'](hex_code) == rgb

    def test_name_to_rgb(self):
        for rgb, name in zip(self.rgbs, self.names):
            if name != '-':
                assert rgb_from['name'](name) == rgb

    def test_ryb_to_rgb(self):
        for rgb, ryb in zip(self.rgbs, self.rybs):
            result = rgb_from['ryb'](ryb)
            assert result == approx(rgb, abs=1)
            assert isinstance(result, SCHEMAS['rgb'].output_type)

from acrylic.Converters import rgb_to, rgb_from


class Test_converters():

    rgbs = [(62, 244, 255), (255, 0, 0), (25, 24, 25)]
    hsls = [(183.42, 100.0, 62.16), (0, 100, 50), (300.0, 2.04, 9.61)]
    hsvs = [(183.42, 75.69, 100.0), (0, 100, 100), (300.0, 4.0, 9.8)]
    hexes = ['#3EF4FF', '#FF0000', '#191819']
    names = ['-', 'red', '-']
    rybs = [(0, 94, 193), (255, 0, 0), (231, 230, 230)]

    def test_rgb_to_hsl(self):
        for rgb, hsl in zip(self.rgbs, self.hsls):
            for x, y in zip(rgb_to['hsl'](rgb), hsl):
                assert round(x) == round(y)

    def test_rgb_to_hsv(self):
        for rgb, hsv in zip(self.rgbs, self.hsvs):
            for x, y in zip(rgb_to['hsv'](rgb), hsv):
                assert round(x) == round(y)

    def test_rgb_to_hex(self):
        for rgb, hex_code in zip(self.rgbs, self.hexes):
            assert rgb_to['hex'](rgb) == hex_code

    def test_rgb_to_name(self):
        for rgb, name in zip(self.rgbs, self.names):
            assert rgb_to['name'](rgb) == name

    def test_rgb_to_ryb(self):
        for rgb, ryb in zip(self.rgbs, self.rybs):
            for x, y in zip(rgb_to['ryb'](rgb), ryb):
                assert x - y <= 1

    # - - - - - - - - - -

    def test_hsl_to_rgb(self):
        for rgb, hsl in zip(self.rgbs, self.hsls):
            assert rgb_from['hsl'](hsl) == rgb

    def test_hsv_to_rgb(self):
        for rgb, hsv in zip(self.rgbs, self.hsvs):
            assert rgb_from['hsv'](hsv) == rgb

    def test_hex_to_rgb(self):
        for rgb, hex_code in zip(self.rgbs, self.hexes):
            assert rgb_from['hex'](hex_code) == rgb

    def test_name_to_rgb(self):
        for rgb, name in zip(self.rgbs, self.names):
            if name != '-':
                assert rgb_from['name'](name) == rgb

    def test_ryb_to_rgb(self):
        for rgb, ryb in zip(self.rgbs, self.rybs):
            for x, y in zip(rgb_from['ryb'](ryb), rgb):
                assert x - y <= 1

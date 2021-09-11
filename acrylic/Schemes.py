from random import uniform, randint

from acrylic.Defaults import RANDOM, SCHEMAS
from acrylic.Validators import in_range, check_datatype


ANALOGOUS = 1
COMPLEMENTARY = 2
TRIADIC = TRIANGLE = 3
TETRADIC = SQUARE = 4
MONOCHROMATIC = 5
SHADES = 6
SPLIT_COMPLEMENTARY = 7
ACCENTED_ANALOGOUS = ANALOGOUS_COMPLEMENTARY = 8
RECTANGLE = 9
NEAR_COMPLEMENTARY = 10
COMPLEMENTARY_TRIADIC = 11
MODIFIED_TRIADIC = 12


def scheme(self, name, in_rgb=False, fuzzy=-1):
    '''
    Returns a list of `Color` according to the given color scheme

    Args:
        name(int):
            a variable from `acrylic.Schemes`
            example: Schemes.COMPLEMENTARY
        in_rgb(bool, optional):
            False: use the RYB color wheel for calculations
            True: use the RGB color wheel for calculations
            Default: False
        fuzzy(int, optional):
            adds a random value between -fuzzy and +fuzzy to
            the generated hue. Can be set to `RANDOM` to use
            the recommended value.
            Default: 0

    Returns:
        list of Color
    '''
    Color = type(self)

    colors, (a, b) = list(), SCHEMAS['hsl'].format.h
    if fuzzy == RANDOM:
        fuzzy = uniform(b / 20, b / 5) if randint(0, 5) else 0
    else:
        fuzzy = check_datatype(float, fuzzy, 'fuzzy')
        fuzzy = in_range(fuzzy, a, b, 'fuzzy')

    deltas = {
        ANALOGOUS: [b / 24, -(b / 24), b / 12, -(b / 12)],
        COMPLEMENTARY: [b / 2],
        TRIADIC: [b / 3, -(b / 3)],
        SQUARE: [b / 4, -(b / 4), b / 2],
        SPLIT_COMPLEMENTARY: [(b / 2) - (b / 12), (b / 2) + (b / 12)],
        ACCENTED_ANALOGOUS: [b / 12, -(b / 12), b / 2],
        RECTANGLE: [b / 2, (b / 2) - (b / 8), b / 8],
        NEAR_COMPLEMENTARY: [(b / 2) - (b / 12)],
        COMPLEMENTARY_TRIADIC: [b / 2, b / 4],
        MODIFIED_TRIADIC: [b / 12, b / 6],
    }

    if name == MONOCHROMATIC:
        m = (SCHEMAS['hsv'].format.s[1] / (SCHEMAS['hsv'].format.s[1] / 30))
        if self.hsv.s > m:
            s = [self.hsv.s, self.hsv.s - m, self.hsv.s, self.hsv.s - m]
        else:
            s = [self.hsv.s, self.hsv.s + m, self.hsv.s, self.hsv.s + m]
        v = [SCHEMAS['hsv'].format.v[1] / 5, SCHEMAS['hsv'].format.v[1]]
        for i in range(4):
            colors.append(Color(hsv=(self.hsl.h, s[i], v)))
        return colors

    elif name == SHADES:
        v = [SCHEMAS['hsv'].format.v[1] / 5, SCHEMAS['hsv'].format.v[1]]
        for i in range(4):
            colors.append(Color(hsv=(self.hsl.h, self.hsv.s, v)))
        return colors

    elif name not in deltas:
        raise ValueError(f'{name!r} is not a valid color scheme')

    for angle in deltas[name]:
        h = (self.hsl.h + angle + uniform(-fuzzy, +fuzzy)) % b
        if not in_rgb:
            colors.append(Color(hsv=(h, self.hsv.s, self.hsv.v))._in_ryb())
        else:
            colors.append(Color(hsv=(h, self.hsv.s, self.hsv.v)))
    return colors

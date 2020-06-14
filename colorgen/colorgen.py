import re
import colorsys
from functools import reduce
from collections import namedtuple
from random import randint, uniform
from collections.abc import Iterable

import colorgen.schemes as schemes


Hsl = namedtuple('Hsl', 'h s l')
Hsv = namedtuple('Hsv', 'h s v')
Rgb = namedtuple('Rgb', 'r g b')
Ryb = namedtuple('Ryb', 'r y b')

RANDOM = -1


def property_factory(attr):

    def getter(instance):
        return getattr(instance, f'_{attr}')

    def setter(instance, *args, **kwargs):
        raise AttributeError(f'{attr!r} is a readonly attribute')

    return property(getter, setter)


class Color:
    __slots__ = ('_hsl', '_hsv', '_rgb', '_hex', '_ryb', '_default_colorspace')

    hsl = property_factory('hsl')
    hsv = property_factory('hsv')
    rgb = property_factory('rgb')
    ryb = property_factory('ryb')
    hex = property_factory('hex')

    LIMITS = {
        'hsl': Hsl((0, 360.0), (0, 100.0), (0, 100.0)),
        'hsv': Hsv((0, 360.0), (0, 100.0), (0, 100.0)),
        'rgb': Rgb((0, 255), (0, 255), (0, 255)),
        'ryb': Ryb((0, 255), (0, 255), (0, 255)),
        'hex': re.compile(r'^[#]?([0-9a-fA-F]{6})(?:[0-9a-fA-F]{2})?$'),
    }
    PRECISION = 2

    def __init__(self, hsl=None, rgb=None, hsv=None, hex=None, ryb=None):
        validated_values = None

        #  find which color space was given and validate its input
        for color_spc in list(self.LIMITS.keys()):
            values = locals()[color_spc]
            if values is not None:
                if color_spc == 'hex':
                    validated_values = Color._validate_hex(values)
                else:
                    validated_values = Color._validate(values, color_spc)

                self.default_colorspace = color_spc
                break

        #  if no params given, assume rgb(0, 0, 0)
        if validated_values is None:
            validated_values = Color._validate((0, 0, 0), 'rgb')
            self.default_colorspace = 'rgb'

        #  if a color space other than rgb was given, convert to rgb
        if self.default_colorspace != 'rgb':
            to_rgb = getattr(Color, f'_{self.default_colorspace}_to_rgb')
            self._rgb = to_rgb(validated_values)
        else:
            self._rgb = validated_values

        #  convert from rgb to all others, including circling back rgb
        self._hsl = Color._rgb_to_hsl(self.rgb)
        self._rgb = Color._hsl_to_rgb(self.hsl)
        self._hsv = Color._rgb_to_hsv(self.rgb)
        self._hex = Color._rgb_to_hex(self.rgb)
        self._ryb = Color._rgb_to_ryb(self.rgb)

    def __repr__(self):
        cls_name = type(self).__name__
        if self.default_colorspace == 'hex':
            return f'{cls_name}(hex={repr(self.hex)})'
        else:
            values = tuple(getattr(self, self.default_colorspace))
            return f'{cls_name}({self.default_colorspace}={repr(values)})'

    def __str__(self):
        if self.default_colorspace == 'hex':
            return f'hex={self.hex!r}'
        else:
            values = getattr(self, self.default_colorspace)
            color_space = self.default_colorspace
            return ', '.join(f'{x}={y!r}' for x, y in zip(color_space, values))

    def __eq__(self, other):
        if isinstance(other, Color):
            return all([
                self.hsl == other.hsl,
                self.rgb == other.rgb,
                self.hsv == other.hsv,
                self.hex == other.hex,
                self.ryb == other.ryb
            ])
        return NotImplemented

    def __hash__(self):
        hashes = (hash(getattr(self, x)) for x in self.LIMITS.keys())
        return reduce(lambda a, b: a ^ b, hashes)

    @property
    def default_colorspace(self):
        return self._default_colorspace

    @default_colorspace.setter
    def default_colorspace(self, value):
        if value.lower() not in self.LIMITS.keys():
            raise ValueError('Not a valid Color Space')
        self._default_colorspace = value.lower()

    #  - - - - - - - -

    @classmethod
    def _hsl_to_rgb(cls, hsl):
        max_vals = [x[1] for x in cls.LIMITS['hsl']]
        (h, s, l) = [x / m for x, m in zip(hsl, max_vals)]
        return Rgb(*[round(x * 255) for x in colorsys.hls_to_rgb(h, l, s)])

    @classmethod
    def _rgb_to_hsl(cls, rgb):
        max_vals, prec = [x[1] for x in cls.LIMITS['hsl']], cls.PRECISION
        (h, l, s) = colorsys.rgb_to_hls(*[x / 255 for x in rgb])
        return Hsl(*[round(x * m, prec) for x, m in zip((h, s, l), max_vals)])

    @classmethod
    def _hsv_to_rgb(cls, hsv):
        max_vals = [x[1] for x in cls.LIMITS['hsv']]
        hsv_float = [x / m for x, m in zip(hsv, max_vals)]
        return Rgb(*[round(x * 255) for x in colorsys.hsv_to_rgb(*hsv_float)])

    @classmethod
    def _rgb_to_hsv(cls, rgb):
        max_vals, prec = [x[1] for x in cls.LIMITS['hsv']], cls.PRECISION
        hsv = colorsys.rgb_to_hsv(*[x / 255 for x in rgb])
        return Hsv(*[round(x * m, prec) for x, m in zip(hsv, max_vals)])

    @classmethod
    def _hex_to_rgb(cls, hex_str):
        return Rgb(*[int(hex_str[x:x + 2], 16) for x in range(1, 7, 2)])

    @classmethod
    def _rgb_to_hex(cls, rgb):
        return f'#{"".join(f"{x:02X}" for x in rgb)}'.upper()

    @classmethod
    def _rgb_to_ryb(cls, rgb):
        rgb_r, rgb_g, rgb_b = [x / 255 for x in rgb]

        white = min(rgb_r, rgb_g, rgb_b)
        black = min(1 - rgb_r, 1 - rgb_g, 1 - rgb_b)
        (rgb_r, rgb_g, rgb_b) = (x - white for x in (rgb_r, rgb_g, rgb_b))

        yellow = min(rgb_r, rgb_g)
        ryb_r = rgb_r - yellow
        ryb_y = (yellow + rgb_g) / 2
        ryb_b = (rgb_b + rgb_g - yellow) / 2

        norm = 0
        if max(rgb_r, rgb_g, rgb_b) != 0:
            norm = max(ryb_r, ryb_y, ryb_b) / max(rgb_r, rgb_g, rgb_b)
        ryb_r = ryb_r / norm if norm > 0 else ryb_r
        ryb_y = ryb_y / norm if norm > 0 else ryb_y
        ryb_b = ryb_b / norm if norm > 0 else ryb_b

        (ryb_r, ryb_y, ryb_b) = (x + black for x in (ryb_r, ryb_y, ryb_b))
        return Ryb(*[round(x * 255) for x in (ryb_r, ryb_y, ryb_b)])

    @classmethod
    def _ryb_to_rgb(cls, ryb):
        ryb_r, ryb_y, ryb_b = [x / 255 for x in ryb]

        black = min(ryb_r, ryb_y, ryb_b)
        white = min(1 - ryb_r, 1 - ryb_y, 1 - ryb_b)
        (ryb_r, ryb_y, ryb_b) = (x - black for x in (ryb_r, ryb_y, ryb_b))

        green = min(ryb_y, ryb_b)
        rgb_r = ryb_r + ryb_y - green
        rgb_g = ryb_y + green
        rgb_b = 2 * (ryb_b - green)

        norm = 0
        if max(ryb_r, ryb_y, ryb_b) != 0:
            norm = max(rgb_r, rgb_g, rgb_b) / max(ryb_r, ryb_y, ryb_b)
        rgb_r = rgb_r / norm if norm > 0 else rgb_r
        rgb_g = rgb_g / norm if norm > 0 else rgb_g
        rgb_b = rgb_b / norm if norm > 0 else rgb_b

        (rgb_r, rgb_g, rgb_b) = (x + white for x in (rgb_r, rgb_g, rgb_b))
        return Rgb(*[round(x * 255) for x in (rgb_r, rgb_g, rgb_b)])

    #  - - - - - - - -

    @staticmethod
    def _check(x, a, b, p, dt):
        '''
        checks if value matches the correct datatype
        and is within allowed limits
        '''
        msg = f'value {x!r} given for {p!r} is'
        if dt is int and not isinstance(x, int):
            raise TypeError(f'{msg} not an int')
        if dt is float and not (isinstance(x, int) or isinstance(x, dt)):
            raise TypeError(f'{msg} not as int or a float')
        if x < a or x > b:
            raise ValueError(f'{msg} not in range {a} <= {p!r} <= {b}')
        return x

    @classmethod
    def _validate(cls, inp_values, color_spc):
        '''
        common validation func for hsl, hsv, rgb, ryb
        '''
        inp_values = [RANDOM] * 3 if inp_values == RANDOM else inp_values

        #  validate input list
        num = len(cls.LIMITS[color_spc])
        is_iter = isinstance(inp_values, Iterable)
        is_str = isinstance(inp_values, str)
        is_valid_len = len(inp_values) == num
        if not ((is_iter and not is_str) and is_valid_len):
            raise TypeError(f'{inp_values!r} is not iterable with {num} items')

        values = list()
        for x, param in zip(inp_values, color_spc):
            #  lower and upper limits for param
            a, b = getattr(cls.LIMITS[color_spc], param)
            #  datatype for this param
            dt = type(b)
            #  random number generator to use according to datatype
            rng = {
                int: lambda a, b: randint(a, b),
                float: lambda a, b: round(uniform(a, b), cls.PRECISION)
            }[dt]

            #  value given for a param is -1 or RANDOM
            if x == RANDOM:
                values.append(rng(a, b))
                continue

            #  value given for a param is a range like [20, 40] or [-1, 60]
            if isinstance(x, Iterable) and not isinstance(x, str):
                if len(x) != 2:
                    raise ValueError(
                        f'range {x!r} given for {param!r} needs 2 values'
                    )

                if tuple(x) == (RANDOM, RANDOM):
                    values.append(rng(a, b))
                    continue

                x = [cls._check(y, a, b, param, dt)
                     if y != RANDOM else RANDOM for y in x]
                x[0] = rng(a, x[1]) if x[0] == RANDOM else x[0]
                x[1] = rng(x[0], b) if x[1] == RANDOM else x[1]
                x = list(reversed(x)) if x[0] > x[1] else x

                values.append(rng(x[0], x[1]))
                continue

            #  default case: single value given for a param
            value = round(cls._check(x, a, b, param, dt), cls.PRECISION)
            values.append(value)

        return type(cls.LIMITS[color_spc])(*values)

    @classmethod
    def _validate_hex(cls, value):
        if not isinstance(value, str):
            raise TypeError(f'{value!r} is not a string')

        inp_hex = cls.LIMITS['hex'].match(value)
        if inp_hex is None:
            raise ValueError(f'{value!r} is not a valid hex color')

        return f'#{inp_hex.groups()[0].upper()}'

    #  - - - - - - - -

    def _in_ryb(self):
        new_hue = Color(ryb=self.rgb).hsl.h
        return Color(hsl=(new_hue, self.hsl.s, self.hsl.l))

    def scheme(self, name, in_rgb=False, fuzzy=0):
        colors, (a, b) = list(), self.LIMITS['hsl'].h
        if fuzzy == RANDOM:
            fuzzy = uniform(b / 20, b / 5) if randint(0, 5) else 0
        else:
            fuzzy = self._check(fuzzy, a, b, 'fuzzy', float)

        deltas = {
            schemes.ANALOGOUS: [b / 24, -(b / 24), b / 12, -(b / 12)],
            schemes.COMPLEMENTARY: [b / 2],
            schemes.TRIADIC: [b / 3, -(b / 3)],
            schemes.SQUARE: [b / 4, -(b / 4), b / 2],
            schemes.SPLIT_COMPLEMENTARY: [
                (b / 2) - (b / 12), (b / 2) + (b / 12)
            ],
            schemes.ACCENTED_ANALOGOUS: [b / 12, -(b / 12), b / 2],
            schemes.RECTANGLE: [b / 2, (b / 2) - (b / 8), b / 8],
            schemes.NEAR_COMPLEMENTARY: [(b / 2) - (b / 12)],
            schemes.COMPLEMENTARY_TRIADIC: [b / 2, b / 4],
            schemes.MODIFIED_TRIADIC: [b / 12, b / 6],
        }

        if name == schemes.MONOCHROMATIC:
            m = (self.LIMITS['hsv'].s[1] / (self.LIMITS['hsv'].s[1] / 30))
            if self.hsv.s > m:
                s = [self.hsv.s, self.hsv.s - m, self.hsv.s, self.hsv.s - m]
            else:
                s = [self.hsv.s, self.hsv.s + m, self.hsv.s, self.hsv.s + m]
            v = [self.LIMITS['hsv'].v[1] / 5, self.LIMITS['hsv'].v[1]]
            for i in range(4):
                colors.append(Color(hsv=(self.hsl.h, s[i], v)))
            return colors

        elif name == schemes.SHADES:
            v = [self.LIMITS['hsv'].v[1] / 5, self.LIMITS['hsv'].v[1]]
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

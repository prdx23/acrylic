import colorsys
from collections.abc import Iterable
from random import random, uniform, randint


class Color:

    _RANGES = {
        'hsl': (0, 1, float),
        'hsv': (0, 1, float),
        'rgb': (0, 255, int),
    }
    _PRECISION = 2

    def __init__(self, hsl=None, rgb=None, hsv=None):
        for color_spc in ['hsl', 'rgb', 'hsv']:
            if locals()[color_spc] is not None:
                setattr(self, color_spc, locals()[color_spc])
                break
        else:
            self.hsl = (0, 0, 0)

    @property
    def hsl(self):
        return self._hsl

    @hsl.setter
    def hsl(self, values):
        self._hsl = Color._validate_basic(values, 'hsl')
        self._rgb = Color._hsl_to_rgb(self.hsl)
        self._hsv = Color._rgb_to_hsv(self.rgb)

    @property
    def hsv(self):
        return self._hsv

    @hsv.setter
    def hsv(self, values):
        self._hsv = Color._validate_basic(values, 'hsv')
        self._rgb = Color._hsv_to_rgb(self.hsv)
        self._hsl = Color._rgb_to_hsl(self.rgb)

    @property
    def rgb(self):
        return self._rgb

    @rgb.setter
    def rgb(self, values):
        self._rgb = Color._validate_basic(values, 'rgb')
        self._hsl = Color._rgb_to_hsl(self.rgb)
        self._hsv = Color._rgb_to_hsv(self.rgb)

    #  - - - - - - - -

    @classmethod
    def _hsl_to_rgb(cls, hsl):
        (h, s, l) = hsl
        return tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))

    @classmethod
    def _rgb_to_hsl(cls, rgb):
        (h, l, s) = colorsys.rgb_to_hls(*[x / 255 for x in rgb])
        hsl = (h, s, l)
        return tuple(round(x, cls._PRECISION) for x in hsl)

    @classmethod
    def _hsv_to_rgb(cls, hsv):
        return tuple(round(x * 255) for x in colorsys.hsv_to_rgb(*hsv))

    @classmethod
    def _rgb_to_hsv(cls, rgb):
        hsv = colorsys.rgb_to_hsv(*[x / 255 for x in rgb])
        return tuple(round(x, cls._PRECISION) for x in hsv)

    #  - - - - - - - -

    @classmethod
    def _validate_basic(cls, inp_values, color_spc):
        '''
        common validation func for hsl, hsv, rgb, ryb
        '''
        a, b = cls._RANGES[color_spc][0], cls._RANGES[color_spc][1]
        dtype = cls._RANGES[color_spc][2]

        if not (isinstance(inp_values, Iterable) and len(inp_values) == 3):
            raise TypeError(f'{color_spc} should be an Iterable with 3 items')

        def check_value(x, a, b, p):
            if not (isinstance(x, float) or isinstance(x, int)):
                raise TypeError(f'"{p}" should be a {dtype} in range {a}-{b}')
            if x < a or x > b:
                raise ValueError(f'"{p}" should be in range {a}-{b}')

        for x, param in zip(inp_values, color_spc):
            if x == -1:
                continue
            if isinstance(x, Iterable):
                if len(x) < 2:
                    raise ValueError(
                        f'setting "{param}" from a range needs 2 values'
                    )
                [check_value(y, a, b, f'"{param}" range') for y in x]
            else:
                check_value(x, a, b, param)

        #  - - - - - - - -
        values = list()
        for x in inp_values:
            if dtype == float:
                if x == -1:
                    values.append(round(random(), cls._PRECISION))
                elif isinstance(x, Iterable):
                    values.append(round(uniform(x[0], x[1]), cls._PRECISION))
                else:
                    values.append(float(x))
            else:
                if x == -1:
                    values.append(randint(a, b))
                elif isinstance(x, Iterable):
                    values.append(randint(x[0], x[1]))
                else:
                    values.append(int(x))

        return tuple(values)

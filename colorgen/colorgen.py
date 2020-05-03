import re
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
    _HEX_REGEX = re.compile(r'^[#]?([0-9a-fA-F]{6})(?:[0-9a-fA-F]{2})?$')

    def __init__(self, hsl=None, rgb=None, hsv=None, hex=None):
        for color_spc in ['hsl', 'rgb', 'hsv', 'hex']:
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
        self._hsl = Color._validate(values, 'hsl')
        self.rgb = Color._hsl_to_rgb(self.hsl)

    @property
    def hsv(self):
        return self._hsv

    @hsv.setter
    def hsv(self, values):
        self._hsv = Color._validate(values, 'hsv')
        self.rgb = Color._hsv_to_rgb(self.hsv)

    @property
    def rgb(self):
        return self._rgb

    @rgb.setter
    def rgb(self, values):
        self._rgb = Color._validate(values, 'rgb')
        self._hsl = Color._rgb_to_hsl(self.rgb)
        self._hsv = Color._rgb_to_hsv(self.rgb)
        self._hex = Color._rgb_to_hex(self.rgb)

    @property
    def hex(self):
        return self._hex

    @hex.setter
    def hex(self, value):
        self._hex = Color._validate_hex(value)
        self.rgb = Color._hex_to_rgb(self.hex)

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

    @classmethod
    def _hex_to_rgb(cls, hex_str):
        return tuple(int(hex_str[x:x + 2], 16) for x in range(1, 7, 2))

    @classmethod
    def _rgb_to_hex(cls, rgb):
        return f'#{"".join(f"{x:02X}" for x in rgb)}'.upper()

    #  - - - - - - - -

    @classmethod
    def _validate(cls, inp_values, color_spc):
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

    @classmethod
    def _validate_hex(cls, value):
        if not isinstance(value, str):
            raise TypeError('hex should be an string')

        inp_hex = cls._HEX_REGEX.match(value)
        if inp_hex is None:
            raise ValueError(f'{value} is not a valid hex color')

        return f'#{inp_hex.groups()[0].upper()}'

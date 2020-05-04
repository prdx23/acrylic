import re
import colorsys
from random import randint
from collections import namedtuple
from collections.abc import Iterable


Hsl = namedtuple('Hsl', 'h s l')
Hsv = namedtuple('Hsv', 'h s v')
Rgb = namedtuple('Rgb', 'r g b')


class Color:

    _RANGES = {
        'hsl': Hsl((0, 360), (0, 100), (0, 100)),
        'hsv': Hsv((0, 360), (0, 100), (0, 100)),
        'rgb': Rgb((0, 255), (0, 255), (0, 255)),
    }
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
        max_vals = [x[1] for x in cls._RANGES['hsl']]
        (h, s, l) = [x / m for x, m in zip(hsl, max_vals)]
        return Rgb(*[round(x * 255) for x in colorsys.hls_to_rgb(h, l, s)])

    @classmethod
    def _rgb_to_hsl(cls, rgb):
        max_vals = [x[1] for x in cls._RANGES['hsl']]
        (h, l, s) = colorsys.rgb_to_hls(*[x / 255 for x in rgb])
        return Hsl(*[round(x * m) for x, m in zip((h, s, l), max_vals)])

    @classmethod
    def _hsv_to_rgb(cls, hsv):
        max_vals = [x[1] for x in cls._RANGES['hsv']]
        hsv_float = [x / m for x, m in zip(hsv, max_vals)]
        return Rgb(*[round(x * 255) for x in colorsys.hsv_to_rgb(*hsv_float)])

    @classmethod
    def _rgb_to_hsv(cls, rgb):
        max_vals = [x[1] for x in cls._RANGES['hsv']]
        hsv = colorsys.rgb_to_hsv(*[x / 255 for x in rgb])
        return Hsv(*[round(x * m) for x, m in zip(hsv, max_vals)])

    @classmethod
    def _hex_to_rgb(cls, hex_str):
        return Rgb(*[int(hex_str[x:x + 2], 16) for x in range(1, 7, 2)])

    @classmethod
    def _rgb_to_hex(cls, rgb):
        return f'#{"".join(f"{x:02X}" for x in rgb)}'.upper()

    #  - - - - - - - -

    @classmethod
    def _validate(cls, inp_values, color_spc):
        '''
        common validation func for hsl, hsv, rgb, ryb
        '''

        def check_value(x, a, b, p, msg):
            '''
            helper func to test values in multiple places
            '''
            if not isinstance(x, int):
                raise TypeError(f'{msg} not Int')
            if x < a or x > b:
                raise ValueError(f'{msg} not in range {a} <= {p} <= {b}')

        values = list()

        if not (isinstance(inp_values, Iterable) and len(inp_values) == 3):
            raise TypeError(f'{color_spc} is not iterable with 3 items')

        for x, param in zip(inp_values, color_spc):
            a, b = getattr(cls._RANGES[color_spc], param)
            if x == -1:
                values.append(randint(a, b))
                continue
            if isinstance(x, Iterable) and not isinstance(x, str):
                if len(x) < 2:
                    raise ValueError(
                        f'setting "{param}" from a range needs 2 values'
                    )

                err_msg = f'values given in range for "{param}" are'
                [check_value(y, a, b, param, err_msg) for y in x]
                values.append(randint(x[0], x[1]))
            else:
                check_value(x, a, b, param, f'"{param}" is')
                values.append(x)

        return globals()[cls._RANGES[color_spc].__class__.__name__](*values)

    @classmethod
    def _validate_hex(cls, value):
        if not isinstance(value, str):
            raise TypeError('hex should be an string')

        inp_hex = cls._HEX_REGEX.match(value)
        if inp_hex is None:
            raise ValueError(f'{value} is not a valid hex color')

        return f'#{inp_hex.groups()[0].upper()}'

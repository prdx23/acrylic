import re
import colorsys
from random import randint, shuffle, choice
from collections import namedtuple
from collections.abc import Iterable


Hsl = namedtuple('Hsl', 'h s l')
Hsv = namedtuple('Hsv', 'h s v')
Rgb = namedtuple('Rgb', 'r g b')
Ryb = namedtuple('Ryb', 'r y b')


class Color:

    _RANGES = {
        'hsl': Hsl((0, 360), (0, 100), (0, 100)),
        'hsv': Hsv((0, 360), (0, 100), (0, 100)),
        'rgb': Rgb((0, 255), (0, 255), (0, 255)),
        'ryb': Ryb((0, 255), (0, 255), (0, 255)),
    }
    _HEX_REGEX = re.compile(r'^[#]?([0-9a-fA-F]{6})(?:[0-9a-fA-F]{2})?$')

    def __init__(self, hsl=None, rgb=None, hsv=None, hex=None, ryb=None):
        for color_spc in ['hsl', 'rgb', 'hsv', 'hex', 'ryb']:
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
        self._ryb = Color._rgb_to_ryb(self.rgb)

    @property
    def hex(self):
        return self._hex

    @hex.setter
    def hex(self, value):
        self._hex = Color._validate_hex(value)
        self.rgb = Color._hex_to_rgb(self.hex)

    @property
    def ryb(self):
        return self._ryb

    @ryb.setter
    def ryb(self, values):
        self._ryb = Color._validate(values, 'ryb')
        self.rgb = Color._ryb_to_rgb(self.ryb)

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

    def _ryb_mode(self):
        new_color = Color(ryb=self.rgb)
        new_color.hsv = (new_color.hsv.h, self.hsv.s, self.hsv.v)
        return new_color


def palette():
    ryb_mode = True
    #  ryb_mode = False
    #  fuzzy = randint(5, 25) if randint(0, 5) else 0
    fuzzy = None
    scheme = 1

    if scheme == 1:
        #  analogous
        rnd_v = [-0, -5, -10, -15]
        deltas = [
            Hsv(-30, randint(-10, 5), choice(rnd_v)),
            Hsv(-15, randint(-10, 5), choice(rnd_v)),
            Hsv(+15, randint(-10, 5), choice(rnd_v)),
            Hsv(+30, randint(-10, 5), choice(rnd_v))
        ]
        if fuzzy is None:
            fuzzy = randint(0, 20) if randint(0, 5) else 0

    elif scheme == 2:
        #  complementary
        rnd_s = [+10, +20, -10, -20]
        deltas = [
            Hsv(+0, choice(rnd_s), -30),
            Hsv(+0, -10, +0),
            Hsv(+180, +0, +0),
            Hsv(+180, choice(rnd_s), -30)
        ]
        if fuzzy is None:
            fuzzy = randint(5, 25) if randint(0, 5) else 0
    print(fuzzy)

    base = Color(hsv=(-1, (10, 75), 98))
    colors = list()

    for i, delta in enumerate(deltas):
        print('-->', delta)
        hue = (base.hsv.h + delta.h + randint(-fuzzy, fuzzy)) % 360

        sat = base.hsv.s + delta.s + randint(-fuzzy // 2, fuzzy // 3)
        sat = min(max(5, sat), 100)

        val = base.hsv.v + delta.v + randint(-fuzzy // 2, fuzzy // 3)
        val = min(max(5, val), 100)

        color = Color(hsv=(hue, sat, val))
        if ryb_mode:
            color = color._ryb_mode()

        colors.append(color)
        print(color.hsv)
        if i == (len(deltas) // 2) - 1:
            if ryb_mode:
                colors.append(base._ryb_mode())
                print(base._ryb_mode().hsv)
            else:
                colors.append(base)
                print(base.hsv)

    #  shuffle(colors)
    return colors

    #  new = [
    #      (+0, +10, -30), (-120, -10, +0),
    #      (+120, +0, +0), (+180, +20, -30)
    #  ]


#  def interpolate(OldMin, OldMax, NewMin, NewMax):
#      OldRange = (OldMax - OldMin)
#      NewRange = (NewMax - NewMin)
#      return lambda x: (((x - OldMin) * NewRange) / OldRange) + NewMin


def harmony():
    colors = [Color(hsv=(x, 58, 98)) for x in range(0, 360, 5)]
    #  print(len(colors))
    for color in list(colors):
        #  print(color.ryb, Color._ryb_to_rgb(color.rgb))
        #  c_ryb = Color(rgb=Color._ryb_to_rgb(color.rgb))
        c_ryb = Color(ryb=color.rgb)
        c_ryb.hsv = (c_ryb.hsv.h, c_ryb.hsv.v, c_ryb.hsv.s)
        #  print(c_ryb.hsv)
        colors.append(color._ryb_mode())

    return colors

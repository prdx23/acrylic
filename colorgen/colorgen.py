import re
import colorsys
from random import randint
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
        colors.append(c_ryb)

    return colors
    #  fuzzy = 0
    #  fuzzy = 20
    fuzzy = 30

    colors = []
    h = randint(0, 360)
    #  for _ in range(1):
    for a in range(15, 75, 5):
        #  a = (15, 75)
        h2 = randint(h - (fuzzy // 2), h + (fuzzy // 2)) % 360
        base = Color(hsv=(h2, a, 100))
        #
        new = [
            (+0, +10, -30), (+0, -10, +0),
            (+180, +0, +0), (+180, +20, -30)
        ]

        new = [
            (+0, +10, -30), (-120, -10, +0),
            (+120, +0, +0), (+180, +20, -30)
        ]



        #  new = [
        #      (+180, -0.25, +0.10), (+180, -0.35, -0.10),
        #      (+0, -0.15, -0.15), (+0, -0.20, -0.40)
        #  ]
        #  hue, s, l = base.hsl[0] * 360, base.hsl[1], base.hsl[2]
        for i, vals in enumerate(new):
            #  new_vals = [base.hsv[x] + vals[x] for x in range(3)]
            #  new_vals = [x % 360 if i == 0 else x % 101
            #              for i, x in enumerate(new_vals)]
            new_vals = []
            for j, (x, y) in enumerate(zip(vals, [360, 100, 100])):
                new = base.hsv[j] + x + randint(-fuzzy // 2, fuzzy // 2)
                if j == 0:
                    h3 = new
                    new = new % y
                else:
                    new = min(new, y)
                    new = max(0, new)
                #  print(new)
                #  if j == 2:
                #      new = (base.hsv[j] + x) % 101
                new_vals.append(new)

            print(new_vals, base.hsv[0] + vals[0], h3, (base.hsv[0] + vals[0])- h3)

            #  new_vals[0] = (base.hsv.h + vals[0]) % 360
            #  new_vals[0] = randint(new_vals[0] - fuzzy, new_vals[0] + fuzzy)
            #
            #  new_vals[1] = (base.hsv.s + vals[1]) % 100
            #  new_vals[1] = randint(new_vals[1] - fuzzy, new_vals[1] + fuzzy)
            #
            #  new_vals[2] = (base.hsv.s + vals[2]) % 100
            #  new_vals[2] = randint(new_vals[2] - fuzzy, new_vals[2] + fuzzy)
            #  print(new_vals)

            colors.append(Color(hsv=new_vals))
            if i == 0:
                colors.append(base)
        #  print(len(colors))
        print('-=-=-=-=-=-=-')



    return colors

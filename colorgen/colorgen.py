from collections.abc import Iterable
from random import random, uniform, randint


class Color:

    _RANGES = {
        'hsl': (0, 1, float),
    }

    def __init__(self, hsl=None):
        if hsl is None:
            self.hsl = (0, 0, 0)
        else:
            self.hsl = hsl

    @property
    def hsl(self):
        return self._hsl

    @hsl.setter
    def hsl(self, values):
        self._hsl = self._validate_basic(values, 'hsl')

    #  - - - - - - - -

    def _validate_basic(self, values, color_spc):
        '''
        common validation func for hsl, hsv, rgb, ryb
        '''
        a, b = self._RANGES[color_spc][0], self._RANGES[color_spc][1]
        dtype = self._RANGES[color_spc][2]

        if not (isinstance(values, Iterable) and len(values) == 3):
            raise TypeError(f'{color_spc} should be an Iterable with 3 items')

        def check_value(x, a, b, p):
            if not (isinstance(x, float) or isinstance(x, int)):
                raise TypeError(f'"{p}" should be a {dtype} in range {a}-{b}')
            if x < a or x > b:
                raise ValueError(f'"{p}" should be in range {a}-{b}')

        for x, param in zip(values, color_spc):
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
        gen_values = list()
        for x in values:
            if dtype == float:
                if x == -1:
                    gen_values.append(round(random(), 3))
                elif isinstance(x, Iterable):
                    gen_values.append(round(uniform(x[0], x[1]), 3))
                else:
                    gen_values.append(float(x))
            else:
                if x == -1:
                    gen_values.append(randint(a, b))
                elif isinstance(x, Iterable):
                    gen_values.append(randint(a, b))
                else:
                    gen_values.append(int(x))

        return tuple(gen_values)

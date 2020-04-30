from collections.abc import Iterable


class Color:

    _RANGES = {
        'hsl': (0, 1),
        'hsv': (0, 1),
        'rgb': (0, 255),
    }

    def __init__(self, hsl=None, hsv=None, rgb=None):
        for col_space in ['hsl', 'hsv', 'rgb']:
            if locals()[col_space] is not None:
                setattr(self, f'{col_space}', locals()[col_space])
                break
            else:
                self.hsl = (0, 0, 0)

    @property
    def hsl(self):
        return self._hsl

    @hsl.setter
    def hsl(self, values):
        self._hsl = self._validate('hsl', values)

    def _validate(self, color_space, values):
        a, b = self._RANGES[color_space][0], self._RANGES[color_space][1]
        for x, param in zip(values, color_space):
            if x == -1:
                continue
            elif isinstance(x, int):
                if x < a or x > b:
                    raise ValueError(f'"{param}" is not in range {a} - {b}')
            elif isinstance(x, Iterable):
                if len(x) < 2:
                    raise ValueError(
                        f'setting "{param}" from a range needs 2 values'
                    )
                elif not all(isinstance(x[y], int) for y in [0, 1]):
                    raise ValueError(
                        f'values while setting "{param}" from a range '
                        f'are not of type "int"'
                    )
                elif any(x[y] < a or x[y] > b for y in [0, 1]):
                    raise ValueError(
                        f'values while setting "{param}" from a range '
                        f'are not in range {a} - {b}'
                    )

        return values

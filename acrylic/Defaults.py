import re
from collections import namedtuple
from random import randint, uniform, choice

from acrylic.color_names import color_names


Rgb = namedtuple('Rgb', 'r g b')
Hsl = namedtuple('Hsl', 'h s l')
Hsv = namedtuple('Hsv', 'h s v')
Ryb = namedtuple('Ryb', 'r y b')


Schema = namedtuple(
    'Schema',
    'format names length rng input_type output_type validation_type'
)


RANDOM = -1
PRECISION = 2


SCHEMAS = {
    'rgb': Schema(
        format=Rgb((0, 255), (0, 255), (0, 255)),
        names=Rgb('red', 'green', 'blue'),
        length=3,
        rng=lambda a, b: randint(a, b),
        input_type=int,
        output_type=Rgb,
        validation_type='values',
    ),
    'hsl': Schema(
        format=Hsl((0, 360.0), (0, 100.0), (0, 100.0)),
        names=Hsl('hue', 'saturation', 'lightness'),
        length=3,
        rng=lambda a, b: round(uniform(a, b), PRECISION),
        input_type=float,
        output_type=Hsl,
        validation_type='values',
    ),
    'hsv': Schema(
        format=Hsv((0, 360.0), (0, 100.0), (0, 100.0)),
        names=Hsv('hue', 'saturation', 'value'),
        length=3,
        rng=lambda a, b: round(uniform(a, b), PRECISION),
        input_type=float,
        output_type=Hsv,
        validation_type='values',
    ),
    'ryb': Schema(
        format=Ryb((0, 255), (0, 255), (0, 255)),
        names=Rgb('red', 'yellow', 'blue'),
        length=3,
        rng=lambda a, b: randint(a, b),
        input_type=int,
        output_type=Ryb,
        validation_type='values',
    ),
    'hex': Schema(
        format=re.compile(r''.join([
            '^#?(?:0x)?(?:',  # optional '#' or '0x'
            '(?P<hex>[0-9a-fA-F]{6})|',  # -> #12bc56
            '(?P<hex_short>[0-9a-fA-F]{3})|',  # -> #1b5
            '(?:(?P<hex_alpha>[0-9a-fA-F]{6})[0-9a-fA-F]{2})',  # -> #12bc56FF
            ')$'
        ])),
        names=tuple(),
        length=0,
        rng='#' + ''.join(choice('0123456789ABCDEF') for _ in range(6)),
        input_type=str,
        output_type=lambda x: f'#{x.upper()}',
        validation_type='string',
    ),
    'name': Schema(
        format=color_names,
        names=tuple(),
        length=0,
        rng=choice(list(color_names.keys())),
        input_type=str,
        output_type=str,
        validation_type='string',
    ),
}

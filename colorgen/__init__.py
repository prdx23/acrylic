from colorsys import hls_to_rgb
from collections import namedtuple
from random import random, uniform, choice


PRESETS = {}
Color = namedtuple('Color', 'h s l rgb', defaults=(0, 0, 0, '#000000'))
Param = namedtuple('Param', 'mode value', defaults=('random', None))


def gen_color(color):
    options = {
        'value': lambda x: color[x].value,
        'range': lambda x: uniform(color[x].value[0], color[x].value[1]),
        'random': lambda x: random(),
        'preset': lambda x: PRESETS[x][color[x].value]
    }
    h, s, l = [options[color[x].mode](x) for x in 'hsl']  # noqa: E741
    rgb = '#' + ''.join(f'{int(256*i):02X}' for i in hls_to_rgb(h, l, s))
    return Color(h, s, l, rgb)


def gen_colors(inp, num=1, **kwargs):
    inp = [{y: Param(*x[y]) for y in 'hsl'} for x in inp]
    colors = [gen_color(choice(inp)) for _ in range(num)]
    return random.shuffle(colors) if 'shuffle' in kwargs else colors


if __name__ == '__main__':
    color = [{
        'h': ('value', 0.4),
        's': ('random', None),
        'l': ('range', (0.5, 0.8)),
    }]
    print(gen_colors(color, 10))

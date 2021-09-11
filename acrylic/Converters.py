import colorsys

from acrylic.Defaults import SCHEMAS, PRECISION
from acrylic.color_names import color_names, color_names_reverse


def rgb_to_hsl(rgb):
    rgb_format, hsl_format = SCHEMAS['rgb'].format, SCHEMAS['hsl'].format

    norm = [x / m[1] for x, m in zip(rgb, rgb_format)]
    h, l, s = colorsys.rgb_to_hls(*norm)

    hsl = [round(x * m[1], PRECISION) for x, m in zip([h, s, l], hsl_format)]
    return SCHEMAS['hsl'].output_type(*hsl)


def rgb_to_hsv(rgb):
    rgb_format, hsv_format = SCHEMAS['rgb'].format, SCHEMAS['hsv'].format

    norm = [x / m[1] for x, m in zip(rgb, rgb_format)]
    h, s, v = colorsys.rgb_to_hsv(*norm)

    hsv = [round(x * m[1], PRECISION) for x, m in zip([h, s, v], hsv_format)]
    return SCHEMAS['hsv'].output_type(*hsv)


def rgb_to_hex(rgb):
    return SCHEMAS['hex'].output_type(''.join(f'{x:02X}' for x in rgb))


def rgb_to_name(rgb):
    return color_names_reverse[rgb] if rgb in color_names_reverse else '-'


def rgb_to_ryb(rgb):
    # Source:
    # https://www.jstage.jst.go.jp/article/tievciieej/5/2/5_110/_pdf/-char/en

    rgb_format, ryb_format = SCHEMAS['rgb'].format, SCHEMAS['ryb'].format
    rgb_r, rgb_g, rgb_b = [x / m[1] for x, m in zip(rgb, rgb_format)]

    white = min(rgb_r, rgb_g, rgb_b)
    black = min(1 - rgb_r, 1 - rgb_g, 1 - rgb_b)
    rgb_r, rgb_g, rgb_b = [x - white for x in (rgb_r, rgb_g, rgb_b)]

    yellow = min(rgb_r, rgb_g)
    ryb_r = rgb_r - yellow
    ryb_y = (yellow + rgb_g) / 2
    ryb_b = (rgb_b + rgb_g - yellow) / 2

    norm = 0
    if max(rgb_r, rgb_g, rgb_b) != 0:
        norm = max(ryb_r, ryb_y, ryb_b) / max(rgb_r, rgb_g, rgb_b)

    ryb = [x / norm if norm > 0 else x for x in (ryb_r, ryb_y, ryb_b)]
    ryb = [x + black for x in ryb]

    result = [round(x * m[1]) for x, m in zip(ryb, ryb_format)]
    return SCHEMAS['ryb'].output_type(*result)


# - - - - - - - - - - - - - -


def hsl_to_rgb(hsl):
    rgb_format, hsl_format = SCHEMAS['rgb'].format, SCHEMAS['hsl'].format

    (h, s, l) = [x / m[1] for x, m in zip(hsl, hsl_format)]
    rgb = colorsys.hls_to_rgb(h, l, s)

    rgb = [round(x * m[1]) for x, m in zip(rgb, rgb_format)]
    return SCHEMAS['rgb'].output_type(*rgb)


def hsv_to_rgb(hsv):
    rgb_format, hsv_format = SCHEMAS['rgb'].format, SCHEMAS['hsv'].format

    (h, s, v) = [x / m[1] for x, m in zip(hsv, hsv_format)]
    rgb = colorsys.hsv_to_rgb(h, s, v)

    rgb = [round(x * m[1]) for x, m in zip(rgb, rgb_format)]
    return SCHEMAS['rgb'].output_type(*rgb)


def hex_to_rgb(hex_str):
    rgb = [int(hex_str[x:x + 2], 16) for x in range(1, 7, 2)]
    return SCHEMAS['rgb'].output_type(*rgb)


def name_to_rgb(name):
    if name == '-':
        return SCHEMAS['rgb'].output_type(0, 0, 0)
    return SCHEMAS['rgb'].output_type(*color_names[name])


def ryb_to_rgb(ryb):
    # Source:
    # https://www.jstage.jst.go.jp/article/tievciieej/5/2/5_110/_pdf/-char/en

    rgb_format, ryb_format = SCHEMAS['rgb'].format, SCHEMAS['ryb'].format
    ryb_r, ryb_y, ryb_b = [x / m[1] for x, m in zip(ryb, ryb_format)]

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

    rgb = [x / norm if norm > 0 else x for x in (rgb_r, rgb_g, rgb_b)]
    rgb = [x + white for x in rgb]

    result = [round(x * m[1]) for x, m in zip(rgb, rgb_format)]
    return SCHEMAS['rgb'].output_type(*result)


# - - - - - - - - - - - - - -


rgb_to = {
    'hsl': rgb_to_hsl,
    'hsv': rgb_to_hsv,
    'hex': rgb_to_hex,
    'name': rgb_to_name,
    'ryb': rgb_to_ryb,
}


rgb_from = {
    'hsl': hsl_to_rgb,
    'hsv': hsv_to_rgb,
    'hex': hex_to_rgb,
    'name': name_to_rgb,
    'ryb': ryb_to_rgb,
}

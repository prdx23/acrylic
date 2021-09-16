from acrylic.Schemes import scheme
from acrylic.Defaults import SCHEMAS
from acrylic.Validators import validate
from acrylic.Converters import rgb_to, rgb_from


class ColorMeta(type):
    def __new__(cls, clsname, bases, attrs):

        # generates readonly, lazy evaluation properties
        def property_factory(attr):

            def getter(instance):
                value = getattr(instance, f'_{attr}')

                if value:
                    # value for `attr` is already present, send cached value
                    return value

                if value is None and attr == 'rgb':
                    # rgb for this color has not been calculated yet
                    # convert color's default to rgb and cache
                    default = getattr(instance, instance._default)
                    converted = rgb_from[instance._default](default)
                    instance._rgb = converted
                    return converted

                # `attr` for this color has not been calculated yet
                # convert to `attr` from rgb and cache
                converted = rgb_to[attr](instance.rgb)
                setattr(instance, f'_{attr}', converted)
                return converted

            def setter(instance, *args, **kwargs):
                raise AttributeError(f'{attr!r} is a readonly attribute')

            doc = f'(readonly) return {attr} component of the color'
            return property(getter, setter, doc=doc)

        for colorspace in SCHEMAS:
            # add properties for each colorspace using factory (Color.rgb)
            attrs[colorspace] = property_factory(colorspace)

            # add private attributes for each colorspace property (Color._rgb)
            attrs[f'_{colorspace}'] = None

        return super(ColorMeta, cls).__new__(cls, clsname, bases, attrs)


class Color(metaclass=ColorMeta):
    '''
    class to represent colors

    Supported color formats: rgb, hsl, hsv, hex, name, ryb
    check `help(acrylic.Color)` for creating a new Color instance

    '''

    def __init__(self, **kwargs):
        '''
        Create an instance of `Color`

        Supported formats:
        rgb, hsl, hsv, ryb, hex, name

        Examples:
            >>> from acrylic import Color, RANDOM

            Create a color using rgb
            >>> Color(rgb=[83, 237, 229])
            Color(rgb=(83, 237, 229))

            Create a color using hsl with a range of saturation values
            >>> Color(hsl=[176.5, (20, 70), 62])
            Color(hsl=(176.5, 51.58, 62))

            Note: Since saturation is picked from the range (20, 70),
            it can differ from 51.58

            Create a color with random hue
            >>> Color(hsv=[RANDOM, 75, 98])
            Color(hsv=(167.23, 75, 98))

            Note: Since hue is random it can differ from 167.23

            Create a color using hex
            >>> Color(hex='#80ffd4')
            Color(hex='#80ffd4')

            Create a color using a valid CSS3 name
            >>> Color(name='aquamarine')
            Color(name='aquamarine')

        Args:
            rgb (optional):
                Iterable with 3 values
                0 <= {r, g, b} <= 255
            ryb (optional):
                Iterable with 3 values
                0 <= {r, y, b} <= 255
            hsv (optional):
                Iterable with 3 values
                0.0 <= {h} <= 360.0
                0.0 <= {s, v} <= 100.0
            hsl (optional):
                Iterable with 3 values
                0.0 <= {h} <= 360.0
                0.0 <= {s, l} <= 100.0
            hex (optional):
                String representing 6-digit hex number
            name (optional):
                String representing a valid CSS3 color name

        Note:
            Each value of the Iterable can be:
                - a single value
                - a list of 2 values, a random value will be picked from
                  between these 2 values
                - `Color.RANDOM` or -1, a random value from that component's
                  range will be picked

        Raises:
            TypeError: if datatypes dont match
            ValueError: values are not within valid ranges
        '''

        if len(kwargs) > 1:
            raise TypeError('Color() got multiple keyword arguments')

        if kwargs:
            colorspace, value = list(kwargs.items())[0]
        else:
            colorspace, value = 'rgb', (0, 0, 0)

        if colorspace not in SCHEMAS.keys():
            msg = f'Color() got an unexpected keyword argument {colorspace!r}'
            raise TypeError(msg)

        # set the private attribute for this colorspace's property
        # ex: set _rgb for Color().rgb
        setattr(self, f'_{colorspace}', validate(value, colorspace))

        # set default format to use for repr() and str() and lazy evaluation
        self._default = colorspace

    def __repr__(self):
        template = f'{type(self).__name__}({self._default}={{}})'

        if SCHEMAS[self._default].validation_type == 'values':
            values = tuple(getattr(self, self._default))
            return template.format(repr(values))

        if SCHEMAS[self._default].validation_type == 'string':
            return template.format(repr(getattr(self, self._default)))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.rgb == other.rgb
        return NotImplemented

    def __hash__(self):
        return hash(self.rgb)

    # - - - - - - - - - -

    def _in_ryb(self):
        new_hue = Color(ryb=self.rgb).hsl.h
        return Color(hsl=(new_hue, self.hsl.s, self.hsl.l))

    scheme = scheme

'''
acrylic is a simple and intutive library to work with color in python. 
It can be used to handle color data, easily convert between different 
color spaces and work with colorschemes. acrylic currently supports the 
following color formats:
rgb, hsl, hsv, hex, name, ryb

Try this for more details on how to use acrylic:
>>> from acrylic import Color
>>> help(Color)
'''


__version__ = '0.3.0'


from .Color import Color
from .Defaults import RANDOM
from . import Schemes

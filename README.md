# <img src="https://user-images.githubusercontent.com/15089721/85012237-5cdae100-b180-11ea-8fc2-9946de05653b.png" alt="logo" width=70% />

![PyPI](https://img.shields.io/pypi/v/acrylic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/acrylic)
![PyPI - License](https://img.shields.io/pypi/l/acrylic)

Have you ever wanted a simple and intuitive way to work with colors in python? Then this library is for you! `acrylic` is a python package that you can use to manage colors, convert between different color formats, and work with color schemes and palettes.

Currently supported color formats are:  
`rgb`, `hsl`, `hsv`, `ryb`, `hex`, `name`

Small example:  
```python
from acrylic import Color, RANDOM

#  Define a color using rgb values
orange = Color(rgb=[247, 177, 79])

#  Use saturation from that color to create a new random color with hsv
random_color = Color(hsv=[RANDOM, orange.hsv.s, 98])

#  Print the random color's value in hex
print(random_color.hex)  # Output: '#50FAF0'
```
check out [more examples](https://github.com/prdx23/acrylic#example-usecases)
below.

`acrylic` also has support for [color
schemes](https://github.com/prdx23/acrylic/wiki/Color-Schemes), support for more
color schemes and functions to generate color palettes will be added in the
future.
```python
complementary = cyan.scheme(Schemes.COMPLEMENTARY)
shades = cyan.scheme(Schemes.SHADES)
color_palette = [cyan, *complementary, *shades]
```
More about color schemes [here](https://github.com/prdx23/acrylic/wiki/Color-Schemes)

## How to Install
`acrylic` can be installed using pip:
```shell
pip install acrylic
```
It has no dependencies and works with Python >=3.6

## Documentation

### Defining Colors

You can create a new color like this:
```python
from acrylic import Color
cyan = Color(rgb=[83, 237, 229])
```

The same syntax can be used to give input in any of the supported color formats. Currently supported formats are `rgb`, `hsv`, `hsl`, `hex` and `ryb`. Example:
```python
color = Color(rgb=[127, 255, 212])
color = Color(hsl=[160, 100, 75])
color = Color(hsv=[160, 50, 100])
color = Color(hex='#7fffd4')
color = Color(name='aquamarine')
color = Color(ryb=[0, 77, 128])
```
- All values for `rgb` and `ryb` should be between `0` - `255`  
- The value of hue for `hsv` and `hsl` should be between `0.0` - `360.0` and the other two components should be between `0.0` - `100.0`.  
- Values for `hex` should be a string representing 6-digit hex number  
- Values for `name` should be a string representing a valid CSS3 color name  

### Converting between color formats

Any instance of `Color()` is automatically converted to every supported color format when its created, so there is no need to manually convert from one format to another. For any color, no matter how it was created, you can get its value in any format like this:

```python
cyan = Color(rgb=[83, 237, 229])
print(cyan.rgb)
print(cyan.hsv)
print(cyan.hsl)
print(cyan.hex)
print(cyan.name)
print(cyan.ryb)
```

This makes converting from say `rgb` to `hsl` as easy as doing:
```python
hsl_values = Color(rgb=[83, 237, 229]).hsl
```

### Accessing values of colors

When accessing these attributes for a color, it returns the values back as a `namedtuple` instance. This behaves exactly as a normal `tuple` would, but has an added benefit that its values can be accessed directly via the dot notation. Example:
```python
>>> cyan = Color(rgb=[83, 237, 229])
>>> cyan.rgb  # returns a namedtuple containing the values
Rgb(r=83, g=237, b=229)
>>> [x for x in cyan.rgb]  # can be iterated over like a normal tuple
[83, 237, 229]
>>> cyan.rgb[1]  # items can be accessed via index
237
>>> r, g, b = cyan.rgb  # items can be unpacked
>>> cyan.rgb.r, cyan.rgb.g  # items can also be accessed via their name
(83, 237)
```


### Additional ways to define a color

In addition to the default way to create a color, `Color()` offers additional methods that would enhance your ability to create colors. 

For example, to create a random color:
```python
from acrylic import Color, RANDOM
random_color = Color(rgb=RANDOM)
```

Creating a color with a random hue, but fixed saturation and value:
```python
random_hue = Color(hsv=[RANDOM, 65, 95])
```
(for aesthetically pleasing random colors, check [example 2](https://github.com/prdx23/acrylic#example-usecases) below)

Any of the components can be given as a list of 2 values like `[a, b]` instead of a single value. When given a range, a value `a <= value <= b` will randomly be picked for that component. For example to create a cyan color where saturation is randomly picked between 30 to 70:
```python
random_cyan = Color(hsv=[176, (30, 70), 95])
```

Giving both values for a range isn't required, you can use this to just set the upper or lower limit by setting the other half to `RANDOM`:
```python
random_cyan = Color(hsv=[176, (RANDOM, 70), 95])
random_cyan = Color(hsv=[176, (30, RANDOM), 95])
```

### Note: Immutability and Hashibility

- All instances of colors are immutable, meaning their values can't be changed once they are defined. This means that each instance of `Color()` represents a specific color and will always represent that color. If you feel the need to modify a color, this can easily be done as:
  ```python
  old_color = Color(rgb=[83, 237, 229])
  #  change hue, but not saturation or value
  new_color = Color(hsv=[230, old_color.hsv.s, old_color.hsv.v])
  ```
- All instances of colors are also hashable. They can be safely used as keys for `dict()`s and can be added to `set()` to efficiently find unique colors or to test membership.
  ```python
  >>> colors = {Color(hex='#7fffd4'): 'Can be used in dict() keys!'}
  >>> Color(name='aquamarine') in colors
  True
  >>> colors[Color(rgb=[127, 255, 212])]
  'Can be used in dict() keys!'
  ```
- As a result of colors being immutable and hashable, colors that represent the same `RGB` values will always be unambiguously equal to each other. This prevents a lot of bugs that can randomly appear when working with float `hsv`/`hsl` values and removes the inconsistencies in the conversion algorithm that converts between `rgb` and `hsv`/`hsl`. An example that demonstrates this:
  ```python
  >>> Color(hsl=[236.94, 9.29, 84.54]) == Color(hsl=[240.0, 8.86, 84.51])
  True
  ```
  This results in `True` because both of these `hsl` values map to the same `rgb` value `(212, 212, 219)` and thus represent the same color.

### Color schemes

The `Color()` class also provides some convenience functions to work with color schemes. In the future, these would also be used to build color palettes. For now, the corresponding colors from a color scheme for a specific color can be generated like this:
```python
from acrylic import Color, Schemes
cyan = Color(rgb=[83, 237, 229])

complementary_color = cyan.scheme(Schemes.COMPLEMENTARY)
cyan_triads = cyan.scheme(Schemes.TRIADIC)
cyan_shades = cyan.scheme(Schemes.SHADES)
```

Taking inspiration from traditional art where most of these color schemes originated from, these are calculated using the `ryb`(red-yellow-blue) color wheel by default. To use the `rgb`(red-green-blue) color wheel instead you can pass `in_rgb=True` to the `.scheme()` function. 

For a list of all the available color schemes and their explanations, check **[this page](https://github.com/prdx23/acrylic/wiki/Color-Schemes)**.

## Example Usecases

1. Create a color using `RGB`, use its saturation to create a new color, and print its value as a hex string:
    ```python
    orange = Color(rgb=[247, 177, 79])
    cyan = Color(hsv=[176.5, orange.hsv.s, 98])
    print(cyan.hex)  # Output: '#50FAF0'
    ```

2. Generating random aesthetically pleasing colors, which for example can be used to color the default profile pictures for users of an app
    ```python
    def aesthetic_color():
        return Color(hsl=[RANDOM, (65, RANDOM), (60, 75)])
    ```
    (If you have ever tried generating random colors by randomizing `rgb` values, you would know how badly that works)

3. Finding unique colors:
    ```python
    test_set = set([
        Color(rgb=[61, 245, 245]), Color(hex='#3DF5F5'),
        Color(hsl=[180, 89.8, 60]), Color(hsl=[179.8, 90.2, 60.1]) 
    ])
    print(test_set)  # Output: {Color(rgb=(61, 245, 245))}
    ```
    The set contains only one color as all those colors map to the same `rgb` values.

4. Sorting all the pixels in an image horizontally by hue: 
    ```python
    from acrylic import Color
    from PIL import Image

    orignal_image = Image.open('test.jpg')
    sorted_img = orignal_image.copy()
    pixels = orignal_image.load()

    for y in range(sorted_image.height):
          row = [Color(rgb=pixels[n, y]) for n in range(sorted_image.width)]
          sorted_row = sorted(row, key=lambda c: c.hsl.h)
          for x, c in enumerate(sorted_row):
              sorted_image.putpixel((x, y), c.rgb)
    ```
    This example also illustrates how easy it is to integrate `acrylic` with other libraries and seamlessly switch between `rgb` and `hsl`

## Contributions
All contributions to `acrylic` are welcome and appreciated! Ways in which you can contribute are:
- Report an issue ([here](https://github.com/prdx23/acrylic/issues))
- Raise a pull request ([here](https://github.com/prdx23/acrylic/pulls))
- Request new features
- Spread the word about `acrylic`!

## License
**MIT License**: Copyright (c) 2020 Arsh  
[License.txt](https://github.com/prdx23/acrylic/blob/master/LICENSE.txt)

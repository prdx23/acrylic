import pytest
from pytest import approx

from acrylic import Color, RANDOM
from acrylic.Defaults import SCHEMAS, Rgb


class Test_Color():

    def test_basic(self):
        color = Color()
        assert color.rgb.r == 0
        assert color.rgb.g == 0
        assert color.rgb.b == 0

        rgb = [62, 244, 255]
        color = Color(rgb=rgb)
        assert color.rgb.r == rgb[0]
        assert color.rgb.g == rgb[1]
        assert color.rgb.b == rgb[2]

        hex_code = '#3EF4FF'
        color = Color(hex=hex_code)
        assert color.hex == hex_code

    def test_init_errors(self):
        with pytest.raises(TypeError):
            _ = Color(rgb=[62, 244, 255], hex='#3ef4ff')

        with pytest.raises(TypeError):
            _ = Color(abc=[62, 244, 255])

    def test_repr(self):
        color = Color(rgb=(62, 244, 255))
        assert eval(repr(color)) == color

        color = Color(hsl=(183, 76, 100))
        assert eval(repr(color)) == color

        color = Color(hex='#3EF4FF')
        assert eval(repr(color)) == color

    def test_hash(self):
        color1 = Color(rgb=[128, 255, 212])
        color2 = Color(hsl=[160, 100, 75])
        color3 = Color(hex='#80ffd4')

        assert hash(color1) == hash(color2)
        assert hash(color1) == hash(color3)
        assert hash(color2) == hash(color3)

        color1 = Color(rgb=[128, 255, 212])
        color2 = Color(hsl=[160, 100, 75])
        color3 = Color(hex='#80ffd4')
        test_dict = {color1: 'test!'}
        assert test_dict[color2] == 'test!'
        assert test_dict[color3] == 'test!'

        color1 = Color(rgb=[128, 255, 212])
        color2 = Color(hsl=[160, 100, 75])
        color3 = Color(hex='#80ffd4')
        test_set = set([color1, color2, color3])
        assert len(test_set) == 1

    def test_lazy_eval(self):
        color = Color(hsl=[160, 100, 75])
        assert color._hsl == (160, 100, 75)
        assert color._rgb is None
        assert color._hex is None

        _ = color.hex
        assert color._hsl == (160, 100, 75)
        assert color._rgb == (128, 255, 212)
        assert color._hex == '#80FFD4'

    def test_immutability(self):
        color = Color(rgb=[128, 255, 212])

        with pytest.raises(AttributeError):
            color.rgb = 'test'

        with pytest.raises(AttributeError):
            color.hsl = 'test'

        with pytest.raises(AttributeError):
            color.hsv = 'test'

        with pytest.raises(AttributeError):
            color.ryb = 'test'

        with pytest.raises(AttributeError):
            color.hex = 'test'

        with pytest.raises(AttributeError):
            color.name = 'test'

    def test_basic_conversion(self):
        def check_all(color):
            assert color.rgb.r == approx(127, abs=1)
            assert color.rgb.g == approx(255, abs=1)
            assert color.rgb.b == approx(212, abs=1)

            assert color.hsl.h == approx(160, abs=0.5)
            assert color.hsl.s == approx(100, abs=0.5)
            assert color.hsl.l == approx(75, abs=0.5)

            assert color.hsv.h == approx(160, abs=0.5)
            assert color.hsv.s == approx(50, abs=0.5)
            assert color.hsv.v == approx(100, abs=0.5)

            assert color.ryb.r == approx(0, abs=1)
            assert color.ryb.y == approx(77, abs=1)
            assert color.ryb.b == approx(128, abs=1)

            # could deviate slightly in some cases as rgb might not line up
            # due to rounding off
            assert color.hex == '#7FFFD4' or color.hex == '#80FFD4'
            assert color.name == 'aquamarine' or '-'

        check_all(Color(rgb=[127, 255, 212]))
        check_all(Color(hsl=[160, 100, 75]))
        check_all(Color(hsv=[160, 50, 100]))
        check_all(Color(ryb=[0, 77, 128]))
        check_all(Color(hex='#7FFFD4'))
        check_all(Color(name='aquamarine'))

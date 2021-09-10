import pytest
from decimal import Decimal
from collections.abc import Iterable

from acrylic.Validators import (
    in_range, check_datatype, check_iter, validate_values, validate_string
)
from acrylic.Defaults import SCHEMAS, Rgb
from acrylic import RANDOM


class Test_in_range():

    def test_basic(self):
        for x in range(11):
            assert x == in_range(x, 0, 10, 'test')

    def test_limits(self):
        with pytest.raises(ValueError):
            in_range(-1, 0, 10, 'test')
        with pytest.raises(ValueError):
            in_range(11, 0, 10, 'test')


class Test_check_datatype():

    def test_basic(self):
        assert isinstance(check_datatype(int, 1, 'test'), int)
        assert isinstance(check_datatype(float, 1.0, 'test'), float)
        assert isinstance(check_datatype(str, 'abc', 'test'), str)

    def test_int(self):
        options = [123, 123.456, '123', Decimal('123.456'), FakeInt(123)]
        for option in options:
            value = check_datatype(int, option, 'test')
            assert isinstance(value, int) and value == 123

        with pytest.raises(ValueError):
            check_datatype(int, 'abcd', 'test')

        options = [[12, 23], {}, FakeStr(123), FakeFloat(123.234), fake_rgb()]
        for option in options:
            with pytest.raises(TypeError):
                check_datatype(int, option, 'test')

    def test_float(self):
        options = [123.456, '123.456', Decimal('123.456'), FakeFloat(123.456)]
        for option in options:
            value = check_datatype(float, option, 'test')
            assert isinstance(value, float) and value == 123.456

        options = [123, '123', Decimal('123')]
        for option in options:
            value = check_datatype(float, option, 'test')
            assert isinstance(value, float) and value == 123.0

        with pytest.raises(ValueError):
            check_datatype(float, 'abcd', 'test')

        options = [[12, 23], {}, FakeStr(123), FakeInt(123), fake_rgb()]
        for option in options:
            with pytest.raises(TypeError):
                check_datatype(float, option, 'test')


class Test_check_iter():

    def test_basic(self):
        values = check_iter([12, 23, 34], 3, 'test')
        assert isinstance(values, Iterable) and values == (12, 23, 34)

    def test_limits(self):
        with pytest.raises(ValueError):
            check_iter([12, 23], 3, 'test')
        with pytest.raises(ValueError):
            check_iter([12, 23, 34, 45], 3, 'test')

    def test_iterables(self):
        options = [
            [12, 23], (12, 23), {12: 'a', 23: 'b'},
            {'1': 12, '2': 23}.values(),
            FakeList([12, 23]), FakeIter([12, 23])
        ]
        for option in options:
            values = check_iter(option, 2, 'test')
            assert isinstance(values, Iterable) and values == (12, 23)

    def test_non_iterables(self):
        options = [123, 12.23, FakeInt(123), FakeFloat(12.23)]
        for option in options:
            with pytest.raises(TypeError):
                check_iter(option, 2, 'test')

    def test_generators(self):
        values = check_iter(fake_rgb(), 3, 'test')
        assert isinstance(values, Iterable) and values == (12, 23, 34)

        with pytest.raises(ValueError):
            check_iter(fake_rgb(), 4, 'test')
        with pytest.raises(ValueError):
            check_iter(fake_rgb(), 2, 'test')
        with pytest.raises(ValueError):
            check_iter(infinite_generator(), 3, 'test')


class Test_validate_values():

    def test_rgb_basic(self):
        assert validate_values([12, 23, 34], 'rgb') == Rgb(12, 23, 34)

    def test_rgb_range(self):
        schema = SCHEMAS['rgb'].format.r
        for _ in range(100):
            r, _, _ = validate_values([(10, 100), 0, 0], 'rgb')
            assert r >= 10 and r <= 100

            r, _, _ = validate_values([(100, 10), 0, 0], 'rgb')
            assert r >= 10 and r <= 100

            r, _, _ = validate_values([(schema[0], schema[1]), 0, 0], 'rgb')
            assert r >= schema[0] and r <= schema[1]

            input_values = [FakeList([FakeInt(10), 100.123]), 0, 0]
            r, _, _ = validate_values(input_values, 'rgb')
            assert r >= 10 and r <= 100

            input_values = [FakeIter(['12', FakeInt(100)]), 0, 0]
            r, _, _ = validate_values(input_values, 'rgb')
            assert r >= 12 and r <= 100

    def test_rgb_range_error(self):
        with pytest.raises(ValueError):
            validate_values([[10], 0, 0], 'rgb')
        with pytest.raises(ValueError):
            validate_values([[12, 23, 34], 0, 0], 'rgb')

    def test_rgb_random(self):
        schema = SCHEMAS['rgb'].format.r
        for _ in range(100):
            r, _, _ = validate_values(RANDOM, 'rgb')
            assert r >= schema[0] and r <= schema[1]

            r, _, _ = validate_values([RANDOM, 0, 0], 'rgb')
            assert r >= schema[0] and r <= schema[1]

            r, _, _ = validate_values([(RANDOM, 100), 0, 0], 'rgb')
            assert r >= schema[0] and r <= 100

            r, _, _ = validate_values([(100, RANDOM), 0, 0], 'rgb')
            assert r >= 100 and r <= schema[1]

            r, _, _ = validate_values([(RANDOM, RANDOM), 0, 0], 'rgb')
            assert r >= schema[0] and r <= schema[1]


class Test_validate_string():

    def test_hex_basic(self):
        assert validate_string('#63B2A4', 'hex') == '#63B2A4'
        assert validate_string('#63b2a4', 'hex') == '#63B2A4'
        assert validate_string('63B2A4', 'hex') == '#63B2A4'
        assert validate_string('0x63b2a4', 'hex') == '#63B2A4'

    def test_hex_short(self):
        assert validate_string('#6ba', 'hex') == '#66BBAA'
        assert validate_string('6ba', 'hex') == '#66BBAA'

    def test_hex_alpha(self):
        assert validate_string('#63b2a4ff', 'hex') == '#63B2A4'
        assert validate_string('63b2a4ff', 'hex') == '#63B2A4'

    def test_hex_extra(self):
        assert validate_string(123456, 'hex') == '#123456'
        assert validate_string(FakeStr('#63B2A4'), 'hex') == '#63B2A4'

    def test_hex_errors(self):
        with pytest.raises(ValueError):
            validate_string('#63B2AX', 'hex')

        with pytest.raises(ValueError):
            validate_string('#63B2A4C', 'hex')

        with pytest.raises(ValueError):
            validate_string('63B2C', 'hex')

        with pytest.raises(ValueError):
            validate_string(FakeInt('#63B2A4'), 'hex')

        with pytest.raises(ValueError):
            # raw hex number evals to int before we can detect
            validate_string(0x63b2a4, 'hex')

    def test_hex_random(self):
        r = validate_string(RANDOM, 'hex')
        assert validate_string(r, 'hex') == r

    # - - - - - - - - - - -

    def test_name_basic(self):
        assert validate_string('cyan', 'name') == 'cyan'

    def test_name_other(self):
        assert validate_string('\n Alice  Blue   \n', 'name') == 'aliceblue'
        assert validate_string(FakeStr('Alice  Blue '), 'name') == 'aliceblue'

    def test_name_random(self):
        r = validate_string(RANDOM, 'name')
        assert validate_string(r, 'name') == r

    def test_name_error(self):
        with pytest.raises(ValueError):
            validate_string('abcd', 'name')

        with pytest.raises(ValueError):
            validate_string(123, 'name')


#  - - -  Helper Classes  - - -


class FakeStr():

    def __init__(self, x):
        self.x = x

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return str(self.x)


class FakeInt():

    def __init__(self, x):
        self.x = x

    def __int__(self):
        return self.x


class FakeFloat():

    def __init__(self, x):
        self.x = x

    def __float__(self):
        return self.x


class FakeIter():
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for x in self.data:
            yield x


class FakeList():
    def __init__(self, data):
        self.data = data

    def __getitem__(self, i):
        return self.data[i]


def fake_rgb():
    yield 12
    yield 23
    yield 34


def infinite_generator():
    while True:
        yield 0

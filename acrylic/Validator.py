from random import randint, uniform


RANDOM = -1
PRECISION = 3
SCHEMAS = {
    'rgb': [(0, 255, 'red'), (0, 255, 'green'), (0, 255, 'blue')],
    'hsl': [(0, 360.0, 'hue'), (0, 100.0, 'saturation'), (0, 100.0, 'lightness')],
    'hsv': [(0, 360.0, 'hue'), (0, 100.0, 'saturation'), (0, 100.0, 'value')],
    'ryb': [(0, 255, 'red'), (0, 255, 'yellow'), (0, 255, 'blue')],
}

RNGS = {
    int: lambda a, b: randint(a, b),
    float: lambda a, b: round(uniform(a, b), PRECISION),
}


def in_range(x, a, b, p):
    if x < a or x > b:
        raise ValueError(f'{p!r} should be in range {a} - {b}')
    return x


def check_datatype(datatype, value, param):
    msg = f'cannot convert {{}} given for {param!r} to {datatype.__name__}'
    try:
        return datatype(value)
    except ValueError:
        raise ValueError(msg.format(f'value {value!r}')) from None
    except TypeError:
        cls = type(value).__name__
        raise TypeError(msg.format(f'object of type {cls!r}')) from None


def check_iter(iterable, length, param):
    try:
        generator = (x for x in iterable)
    except TypeError:
        cls = type(iterable).__name__
        msg = f'{cls!r} object given for {param!r} is not iterable'
        raise TypeError(msg) from None

    try:
        values = [next(generator) for _ in range(length)]
    except StopIteration:
        msg = f'{param!r} should have {length} values'
        raise ValueError(msg) from None

    try:
        next(generator)
    except StopIteration:
        return values
    else:
        msg = f'{param!r} should have {length} values'
        raise ValueError(msg) from None


def validate_values(values, colorspace):
    schema = SCHEMAS[colorspace]
    datatype = type(schema[0][1])
    rng = RNGS[datatype]

    if values == RANDOM:
        return [rng(a, b) for a, b, _ in schema]

    values = check_iter(values, len(schema), colorspace)

    result = list()
    for x, (a, b, p) in zip(values, schema):
        value = None

        if x == RANDOM:
            result.append(rng(a, b))
            continue

        try:
            value = check_datatype(datatype, x, p)
        except TypeError as err:
            try:
                limits = check_iter(x, 2, p)
            except TypeError:
                raise err
            except ValueError:
                msg = f'{p!r} when given as a range needs 2 values'
                raise ValueError(msg) from None
        else:
            if datatype != float:
                result.append(in_range(value, a, b, p))
            else:
                result.append(round(in_range(value, a, b, p), PRECISION))
            continue

        limits = [check_datatype(datatype, x, 'r') for x in limits]

        if limits == [-1, -1]:
            result.append(rng(a, b))
            continue

        limits = [in_range(x, a, b, p) if x != RANDOM else x for x in limits]

        if limits[0] == RANDOM:
            limits[0] = rng(a, limits[1])
        if limits[1] == RANDOM:
            limits[1] = rng(limits[0], b)

        result.append(rng(min(limits), max(limits)))

    return result

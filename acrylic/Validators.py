import itertools

from acrylic.Defaults import RANDOM, PRECISION, SCHEMAS


def validate(value, colorspace):
    if SCHEMAS[colorspace].validation_type == 'values':
        return validate_values(value, colorspace)
    if SCHEMAS[colorspace].validation_type == 'string':
        return validate_string(value, colorspace)


def in_range(x, a, b, p):
    if x < a or x > b:
        raise ValueError(f'{p!r} should be in range {a} - {b}')
    return x


def check_datatype(datatype, value, param):
    try:
        return datatype(value)
    except ValueError:
        msg = f'cannot convert value {value!r} given for {param!r} '
        msg += f'to {datatype.__name__}'
        raise ValueError(msg) from None
    except TypeError:
        msg = f'cannot convert object of type {type(value).__name__!r} '
        msg += f'given for {param!r} to {datatype.__name__}'
        raise TypeError(msg) from None


def check_iter(iterable, length, param):
    try:
        values = tuple(itertools.islice(iterable, length + 1))
    except TypeError:
        cls = type(iterable).__name__
        msg = f'{cls!r} object given for {param!r} is not iterable'
        raise TypeError(msg) from None

    try:
        values[length - 1]
    except IndexError:
        msg = f'{param!r} should have {length} values'
        raise ValueError(msg) from None

    try:
        values[length]
    except IndexError:
        return values
    else:
        msg = f'{param!r} should have {length} values'
        raise ValueError(msg) from None


def validate_values(values, colorspace):
    schema = SCHEMAS[colorspace]
    datatype = schema.input_type

    if values == RANDOM:
        return [schema.rng(a, b) for a, b in schema.format]

    values = check_iter(values, schema.length, colorspace)

    validated = list()
    for x, (a, b), p in zip(values, schema.format, schema.names):
        value = None

        if x == RANDOM:
            validated.append(schema.rng(a, b))
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
                validated.append(in_range(value, a, b, p))
            else:
                validated.append(round(in_range(value, a, b, p), PRECISION))
            continue

        limits = [check_datatype(datatype, x, 'r') for x in limits]

        if limits == [-1, -1]:
            validated.append(schema.rng(a, b))
            continue

        limits = [in_range(x, a, b, p) if x != RANDOM else x for x in limits]

        if limits[0] == RANDOM:
            limits[0] = schema.rng(a, limits[1])
        if limits[1] == RANDOM:
            limits[1] = schema.rng(limits[0], b)

        validated.append(schema.rng(min(limits), max(limits)))

    return schema.output_type(*validated)


def validate_string(value, colorspace):
    schema = SCHEMAS[colorspace]

    if value == RANDOM:
        return schema.rng

    value = check_datatype(schema.input_type, value, colorspace)

    if colorspace == 'hex':
        match = schema.format.match(value, 0, 10)
        if match and match.lastgroup == 'hex':
            return schema.output_type(match.group('hex'))
        elif match and match.lastgroup == 'hex_alpha':
            return schema.output_type(match.group('hex_alpha'))
        elif match and match.lastgroup == 'hex_short':
            extended = ''.join(f'{x}{x}' for x in match.group('hex_short'))
            return schema.output_type(extended)

    if colorspace == 'name':
        value = ''.join(value.strip().lower().split())
        if value in schema.format:
            return schema.output_type(value)

    raise ValueError(f'{value!r} is not a valid value for {colorspace!r}')

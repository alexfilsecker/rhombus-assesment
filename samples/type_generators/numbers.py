from random import choice, randint, random, uniform

import numpy as np


def generate_number(bits: int, signed: bool, float: bool) -> int:
    if not signed and not float:
        # Cannot support 64 bit unsigned in db
        if bits == 64:
            bits = 63
        boundaries = (0, (2**bits) - 1)
    else:
        boundaries = (-(2 ** (bits - 1)), 2 ** (bits - 1) - 1)

    def inner():
        if not float:
            return str(randint(*boundaries))

        if bits == 32:
            return str(np.float32(random() * randint(-1000, 1000)))

        # Generate a large exponent and a precise mantissa
        exponent = randint(100, 200)
        mantissa = uniform(1.0, 2.0)

        # Combine the exponent and mantissa to form the float64 number
        large_float64 = mantissa * 2**exponent
        return str(large_float64)

    return inner


NUMBER_TYPES = {
    "uint8": generate_number(8, False, False),
    "uint16": generate_number(16, False, False),
    "uint32": generate_number(32, False, False),
    "uint64": generate_number(64, False, False),
    "int8": generate_number(8, True, False),
    "int16": generate_number(16, True, False),
    "int32": generate_number(32, True, False),
    "float32": generate_number(32, True, True),
    "float64": generate_number(64, True, True),
}


def number_generator():
    return choice(list(NUMBER_TYPES.items()))

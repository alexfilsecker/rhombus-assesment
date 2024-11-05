import argparse
import string
from random import choice, randint, random, uniform
from typing import Tuple

import numpy as np

PATH = "sample.csv"


parser = argparse.ArgumentParser("hola!")

parser.add_argument(
    "-r", "--rows", type=int, default=10, help="number of rows for the csv"
)
parser.add_argument(
    "-c", "--cols", type=int, default=3, help="number of cols for the csv"
)


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


def generate_giberish(length: int):
    def inner():
        letters = string.ascii_letters
        return "".join(choice(letters) for _ in range(length))

    return inner


number_types = {
    # "uint8": generate_number(8, False, False),
    # "uint16": generate_number(16, False, False),
    # "uint32": generate_number(32, False, False),
    # "uint64": generate_number(64, False, False),
    # "int8": generate_number(8, True, False),
    # "int16": generate_number(16, True, False),
    # "int32": generate_number(32, True, False),
    "float32": generate_number(32, True, True),
    "float64": generate_number(64, True, True),
}


def number_generator():
    return choice(list(number_types.items()))


def string_generator():
    return ("string", generate_giberish(randint(1, 20)))


types = {
    # "string": string_generator,
    "number": number_generator
}


if __name__ == "__main__":
    args = parser.parse_args()
    cols: int = args.cols
    rows: int = args.rows

    with open(PATH, "w+", encoding="utf-8") as f:
        header = "".join(f"field_{i}," for i in range(cols))
        f.write(f"{header[:-1]}\n")
        choices = [choice(list(types.items()))[1]() for _ in range(cols)]
        print([chosen[0] for chosen in choices])
        generators = [chosen[1] for chosen in choices]

        for _ in range(rows):
            row_string = ""
            for col in range(cols):
                generator = generators[col]
                row_string += generator() + ","

            row_string = row_string[:-1] + "\n"
            f.write(row_string)

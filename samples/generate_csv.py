import argparse
import datetime
import string
from random import choice, randint, random, randrange, uniform
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


def random_datetime():
    start = datetime.datetime(1970, 1, 1)
    end = datetime.datetime.now()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


DATE_TIME_FORMATS = [
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y/%m/%d",
    "%B %d %Y",
    "%b %d %Y",
    "%I:%M:%S %p",
    "%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %I:%M:%S",
]


def random_datetime_str(format: str):
    def inner():
        # rand_datetime = random_datetime()
        rand_datetime = datetime.datetime.now()
        return rand_datetime.strftime(format)

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


def datetime_generator():
    format = choice(DATE_TIME_FORMATS)
    return (f"datetime({format})", random_datetime_str(format))


def number_generator():
    return choice(list(number_types.items()))


def string_generator():
    return ("string", generate_giberish(randint(1, 20)))


types = {
    # "string": string_generator,
    # "number": number_generator
    "datetime": datetime_generator
}


if __name__ == "__main__":
    args = parser.parse_args()
    cols: int = args.cols
    rows: int = args.rows

    with open(PATH, "w+", encoding="utf-8") as f:
        header = "".join(f"field_{i}," for i in range(len(DATE_TIME_FORMATS)))
        f.write(f"{header[:-1]}\n")
        # choices = [choice(list(types.items()))[1]() for _ in range(cols)]
        choices = [
            (format, random_datetime_str(format)) for format in DATE_TIME_FORMATS
        ]
        print([chosen[0] for chosen in choices])
        generators = [chosen[1] for chosen in choices]

        for _ in range(rows):
            row_string = ""
            for col in range(len(DATE_TIME_FORMATS)):
                generator = generators[col]
                row_string += generator() + ","

            row_string = row_string[:-1] + "\n"
            f.write(row_string)

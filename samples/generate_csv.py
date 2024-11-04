import argparse
import string
from random import choice, randint
from typing import Tuple

PATH = "sample.csv"

parser = argparse.ArgumentParser("hola!")

parser.add_argument(
    "-r", "--rows", type=int, default=20, help="number of rows for the csv"
)
parser.add_argument(
    "-c", "--cols", type=int, default=3, help="number of cols for the csv"
)


def generate_number(bits: int, signed: bool) -> int:
    if not signed:
        # Cannot support 64 bit unsigned in db
        if bits == 64:
            bits = 63
        boundaries = (0, (2**bits) - 1)
    else:
        boundaries = (-(2 ** (bits - 1)), 2 ** (bits - 1) - 1)

    def inner():
        return str(randint(*boundaries))

    return inner


def generate_giberish(length: int):
    def inner():
        letters = string.ascii_letters
        return "".join(choice(letters) for _ in range(length))

    return inner


number_types = {
    "uint8": generate_number(8, False),
    "uint16": generate_number(16, False),
    "uint32": generate_number(32, False),
    "uint64": generate_number(64, False),
    "int8": generate_number(8, True),
    "int16": generate_number(16, True),
    "int32": generate_number(32, True),
    "int64": generate_number(64, True),
}


def number_generator():
    return choice(list(number_types.values()))


def string_generator():
    return generate_giberish(randint(1, 20))


types = {"string": string_generator, "number": number_generator}


if __name__ == "__main__":
    args = parser.parse_args()
    cols: int = args.cols
    rows: int = args.rows

    with open(PATH, "w+", encoding="utf-8") as f:
        header = "".join(f"field_{i}," for i in range(cols))
        f.write(f"{header[:-1]}\n")
        generators = [choice(list(types.values()))() for _ in range(cols)]

        for _ in range(rows):
            row_string = ""
            for col in range(cols):
                generator = generators[col]
                row_string += generator() + ","

            row_string = row_string[:-1] + "\n"
            f.write(row_string)

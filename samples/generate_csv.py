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
        boundaries = (0, 2**bits - 1)
    else:
        boundaries = (-(2 ** (bits - 1)), 2**bits - 1)

    def inner():
        return str(randint(*boundaries))

    return inner


def generate_giberish(length: int) -> str:
    letters = string.ascii_letters
    return "".join(choice(letters) for _ in range(length))


types = {
    "uint8": generate_number(8, False),
    "uint16": generate_number(16, False),
    "uint32": generate_number(32, False),
    "uint64": generate_number(64, False),
    "int8": generate_number(8, True),
    "int16": generate_number(16, True),
    "int32": generate_number(32, True),
    "int64": generate_number(64, True),
    "string": generate_giberish,
}


if __name__ == "__main__":
    args = parser.parse_args()
    cols: int = args.cols
    rows: int = args.rows

    with open(PATH, "w+", encoding="utf-8") as f:
        header = "".join(f"field_{i}," for i in range(cols))
        f.write(f"{header[:-1]}\n")
        col_types = [choice(list(types.keys())) for _ in range(cols)]
        for _ in range(rows):
            row_string = ""
            for col in range(cols):
                selected_type = col_types[col]
                args = []
                if selected_type == "string":
                    args.append(randint(1, 20))
                row_string += types[selected_type](*args) + ","

            row_string = row_string[:-1] + "\n"
            f.write(row_string)

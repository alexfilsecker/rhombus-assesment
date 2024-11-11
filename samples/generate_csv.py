import argparse
from random import choice

from type_generators.categories import category_generator
from type_generators.complex import complex_generator
from type_generators.datetimes import datetime_generator
from type_generators.numbers import number_generator
from type_generators.strings import string_generator
from type_generators.time_delta import time_delta_generator

# Parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-r", "--rows", type=int, default=10, help="number of rows for the csv"
)
parser.add_argument(
    "-c", "--cols", type=int, default=3, help="number of cols for the csv"
)
parser.add_argument(
    "-f", "--file", type=str, default="sample.csv", help="name of the file output"
)


types = {
    "string": string_generator,
    "number": number_generator,
    "datetime": datetime_generator,
    "categories": category_generator,
    "complex": complex_generator,
    "timedelta": time_delta_generator,
}


if __name__ == "__main__":
    args = parser.parse_args()
    cols: int = args.cols
    rows: int = args.rows
    file: str = args.file

    with open(file, "w+", encoding="utf-8") as f:
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

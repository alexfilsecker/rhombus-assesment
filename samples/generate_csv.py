"""hola"""

from random import randint

PATH = "generated.csv"


def generate_giberish(length: int):
    """hola"""
    string = ""
    for _ in range(length):
        string += chr(randint(65, 65 + 26))

    return string


if __name__ == "__main__":
    with open(PATH, "w+", encoding="utf-8") as f:
        f.write("field_1,field_2,field_3\n")
        for _ in range(10000):
            first = str(randint(0, 99))
            f.write(f"{first},{generate_giberish(randint(3, 20))},{randint(0, 99)}")
            f.write("\n")

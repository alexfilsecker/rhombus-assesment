import string
from random import choice, randint


def generate_giberish(length: int):
    def inner():
        letters = string.ascii_letters
        return "".join(choice(letters) for _ in range(length))

    return inner


def string_generator():
    return ("string", generate_giberish(randint(1, 20)))

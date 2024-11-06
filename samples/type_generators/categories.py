from random import choice, choices, randint
from typing import List


def generate_categories(categories: List[str]):
    def inner():
        return choice(categories)

    return inner


def category_generator():
    with open("type_generators/english_words.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        words = [line[:-1] for line in lines]
        k = randint(3, 7)
        categories = choices(words, k=k)

    return (f"categories({k})", generate_categories(categories))

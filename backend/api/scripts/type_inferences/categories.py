from typing import Set

import pandas as pd

MAX_NUMBER_OF_CATEGORIES = 10


def category_conversion(df: pd.DataFrame, col: str) -> bool:
    data = df[col]
    string_set: Set[str] = set()
    for value in data:
        string_set.add(value)
        if len(string_set) > MAX_NUMBER_OF_CATEGORIES:
            return False

    converted = pd.Categorical(data)
    df[col] = converted

    return True

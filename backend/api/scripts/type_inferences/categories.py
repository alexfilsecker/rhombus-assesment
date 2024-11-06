from typing import Set

import pandas as pd

PERCENTAGE_TO_BE_CATEGORY = 0.05


def category_conversion(df: pd.DataFrame, col: str) -> bool:
    data = df[col]
    string_set: Set[str] = set()
    for value in data:
        string_set.add(value)
        if len(string_set) / len(data) > PERCENTAGE_TO_BE_CATEGORY:
            return False

    converted = pd.Categorical(data)
    df[col] = converted

    return True

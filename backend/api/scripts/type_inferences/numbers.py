import pandas as pd


class NotNumbers(Exception):
    """Just a custom Exception to identify a failure in number conversion"""


# Accept a maximum of MAX_NAN exceptions for number conversion
MAX_NAN = 2


def number_downcast(data: pd.Series) -> pd.Series:
    """Gets a data and converts it to the smallest posible number"""
    converted = pd.to_numeric(data, errors="coerce", downcast="unsigned")
    num_of_exceptions = len(converted) - converted.count()
    if num_of_exceptions > MAX_NAN:
        raise NotNumbers
    elif num_of_exceptions > 0:
        # As there will be NaN, we will be converting to float (32) ideally
        return pd.to_numeric(data, errors="coerce", downcast="float")

    # Check it it could be the smallest posible unsigned
    if converted.dtype in [f"uint{base}" for base in [8, 16, 32, 64]]:
        return converted

    # Check if it could be the smallest posible signed integer
    converted = pd.to_numeric(data, errors="coerce", downcast="integer")

    if converted.dtype in [f"int{base}" for base in [8, 16, 32, 64]]:
        return converted

    # Only case posible is float so try to downcast it to the smallest (32)
    return pd.to_numeric(data, errors="coerce", downcast="float")


def number_conversion(df: pd.DataFrame, col: str) -> bool:
    data = df[col]
    try:
        new_col = number_downcast(data)
        df[col] = new_col
        return True
    except NotNumbers:
        pass

    return False

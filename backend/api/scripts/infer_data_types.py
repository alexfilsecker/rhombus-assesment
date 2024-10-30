import pandas as pd


class NotNumbers(Exception):
    """Just a custom Exception to identify a failure in number conversion"""


# Accept a maximum of MAX_NAN exceptions for number conversion
MAX_NAN = 0


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
    except Exception as e:
        print("SEMEEEEN", e)

    return False


def date_time_conversion(df: pd.DataFrame, col: str) -> bool:
    data = df[col]
    converted = pd.to_datetime(data, errors="coerce")
    if not converted.notna().all():
        return False

    df[col] = converted
    return True


def infer_and_convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        data = df[col]

        if data.dtype == "int64" or data.dtype == "float64":
            # downcast the data
            df[col] = number_downcast(data)
            continue

        if data.dtype == "bool":
            # Nothing to do here
            continue

        # Try to do better than object
        if data.dtype == "object":
            # Attempt to convert to numeric first
            if number_conversion(df, col):
                continue

            if date_time_conversion(df, col):
                continue

    return df


# Test the function with your DataFrame
df = pd.read_csv("sample_data.csv")
hola = infer_and_convert_data_types(df)

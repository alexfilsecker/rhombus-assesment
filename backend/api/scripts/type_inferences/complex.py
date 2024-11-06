import pandas as pd


def complex_conversion(df: pd.DataFrame, col: str) -> bool:
    data = df[col]
    try:
        converted = data.astype("complex", errors="raise")
    except ValueError:
        return False

    df[col] = converted

    return True

import pandas as pd


def complex_conversion(df: pd.DataFrame, col: str) -> bool:
    """
    Convert the column to a complex number if possible.

    Args:
        df (pd.DataFrame): The whole dataframe
        col (str): The column to convert

    Returns:
        bool: Whether the column was converted to a complex number or not.
    """

    data = df[col]
    try:
        converted = data.astype("complex", errors="raise")
    except ValueError:
        return False

    df[col] = converted

    return True

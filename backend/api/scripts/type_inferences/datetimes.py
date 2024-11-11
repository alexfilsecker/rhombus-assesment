import pandas as pd


def date_time_conversion(df: pd.DataFrame, col: str) -> bool:
    """
    Convert the column to a datetime if possible.

    Args:
        df (pd.DataFrame): The whole dataframe
        col (str): The column to convert

    Returns:
        bool: Whether the column was converted to a datetime or not.
    """
    data = df[col]
    converted = pd.to_datetime(data, errors="coerce")
    if not converted.notna().all():
        return False

    df[col] = converted
    return True

import pandas as pd


def time_delta_conversion(df: pd.DataFrame, col: str) -> bool:
    """
    Convert the column to a timedelta if possible.

    Args:
        df (pd.DataFrame): The whole dataframe
        col (str): The column to convert

    Returns:
        bool: Whether the column was converted to a timedelta or not.
    """
    data = df[col]
    converted = pd.to_timedelta(data, errors="coerce")
    if not converted.notna().all():
        return False

    df[col] = converted
    return True

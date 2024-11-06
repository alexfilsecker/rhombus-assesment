import pandas as pd


def date_time_conversion(df: pd.DataFrame, col: str) -> bool:
    data = df[col]
    converted = pd.to_datetime(data, errors="coerce")
    if not converted.notna().all():
        return False

    df[col] = converted
    return True

import pandas as pd


def time_delta_conversion(df: pd.DataFrame, col: str):
    data = df[col]
    converted = pd.to_timedelta(data, errors="coerce")
    if not converted.notna().all():
        return False

    df[col] = converted
    return True

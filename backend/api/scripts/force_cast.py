from typing import Optional, Tuple

import pandas as pd

from ..models.table_col_model import TableCol

CASTING_NAMES = TableCol.TYPES
CASTING_NAMES["uint"] = "Unsigned Integer"
CASTING_NAMES["int"] = "Signed Integer"
CASTING_NAMES["float"] = "Floating Point Number"


def force_cast(
    data: pd.Series, casting: str, col: str
) -> Tuple[pd.Series, Optional[str]]:
    # print(f"\n--- FORCE CASTING: {col} -> {casting} ---\n")

    try:
        human_casting = CASTING_NAMES[casting]
    except KeyError:
        human_casting = casting

    try:
        if casting.startswith("uint"):
            if casting == "uint":  # default
                casting = "uint32"
            return data.astype(casting), None

        elif casting.startswith("int"):
            if casting == "int":
                casting = "int64"
            return data.astype(casting), None

        elif casting.startswith("float"):
            if casting == "float":
                casting = "float64"
            return data.astype(casting), None

        elif casting.startswith("complex"):
            return data.astype("complex128"), None

        elif casting == "category":
            return data.astype("category"), None

        elif casting == "object":
            return data.astype("object"), None

        elif casting.startswith("datetime"):
            if casting == "datetime":  # no format
                return pd.to_datetime(data, errors="raise"), None
            datetime_format = casting.split("(")[1][:-1]
            return pd.to_datetime(data, errors="raise", format=datetime_format), None

        elif casting == "timedelta":
            return pd.to_timedelta(data, errors="raise"), None

        return data, f"force casting to {human_casting} not supported"

    except Exception as e:
        return data, f"could not cast to {human_casting}, defaulting to inference"

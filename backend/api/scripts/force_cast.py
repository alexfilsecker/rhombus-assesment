from typing import Optional, Tuple

import pandas as pd


def force_cast(
    data: pd.Series, casting: str, col: str
) -> Tuple[pd.Series, Optional[str]]:
    print(f"\n--- FORCE CASTING: {col} -> {casting} ---\n")

    try:

        # Numbers
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

        return data, f"force casting to {casting} not supported"

    except Exception as e:
        print(e)
        return data, f"could not cast to {casting}"

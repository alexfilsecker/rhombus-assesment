from typing import Dict, Tuple

import pandas as pd

from .force_cast import force_cast
from .type_inferences.categories import category_conversion
from .type_inferences.complex import complex_conversion
from .type_inferences.datetimes import date_time_conversion
from .type_inferences.numbers import number_conversion, number_downcast
from .type_inferences.time_delta import time_delta_conversion


def infer_and_convert_data_types(
    df: pd.DataFrame, force_casting: Dict[str, str]
) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    The function to infer and convert data types.
    It will first attempt to force cast the data if the column
    is in the force_casting dictionary. Then it will attempt to
    infer the data type of the column and convert it to a more
    appropriate data type.

    Args:
        df (pd.DataFrame): The dataframe to infer and convert
        force_casting (Dict[str, str]): The dictionary of force casting options.

    Returns:
        Tuple: A tuple containing the dataframe and a dictionary of errors.
            - **df** (pd.DataFrame): The dataframe with the inferred and converted data types.
            - **errors** (Dict[str, str]): A dictionary of errors that occurred during the process.
    """

    errors: Dict[str, str] = {}

    for col in df.columns:
        data = df[col]

        if col in force_casting:
            df[col], error = force_cast(data, force_casting[col])
            if error is not None:
                errors[col] = error
            else:
                continue

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

            if complex_conversion(df, col):
                continue

            if category_conversion(df, col):
                continue

            if time_delta_conversion(df, col):
                continue

            if date_time_conversion(df, col):
                continue

    return df, errors

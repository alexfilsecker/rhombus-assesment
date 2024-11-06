import pandas as pd

from .type_inferences.categories import category_conversion
from .type_inferences.datetimes import date_time_conversion
from .type_inferences.numbers import number_conversion, number_downcast


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

            # if date_time_conversion(df, col):
            #     continue

            if category_conversion(df, col):
                continue

    return df


# if __name__ == "__main__":
#     print("\n--- SCRIPT TESTING ---")
#     PATH = "samples/sample.csv"
#     df = pd.read_csv(PATH)
#     df = infer_and_convert_data_types(df)
#     print(df.dtypes)
